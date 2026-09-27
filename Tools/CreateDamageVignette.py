"""FPS のダメージ演出 (画面隅の赤黒いビネット) を PostProcess マテリアルとして生成する (UE エディタ用)。

生成するもの:
  /Game/Materials/PostProcess/PP_DamageVignette   マテリアル本体 (Domain: PostProcess)
  /Game/Materials/PostProcess/PPI_DamageVignette  パラメータ調整用のインスタンス

テクスチャは使わず、ScreenPosition から求めた距離と正弦波だけで描く。
Blendable Location は After Tonemapping なので、シーンのライティングや露出の影響を
受けずに常に同じ色で画面隅が染まる。

グラフの流れ:
  UV -> 中心からの距離 (楕円と矩形をブレンド) -> 角度ベースの正弦波で縁を崩す
     -> SmoothStep でマスク化 -> Intensity と脈動を掛ける
     -> シーン色に血の色を乗算し、角を EdgeColor へ沈める -> EmissiveColor

エディタ内から: Output Log で  py "<repo>/Tools/CreateDamageVignette.py"

コマンドラインから:
  UnrealEditor-Cmd.exe <repo>/ProceduralDrawingMaterialSamples.uproject
      -EnablePlugins=PythonScriptPlugin -ExecCmds="py <repo>/Tools/CreateDamageVignette.py"
      -unattended -nosplash

同名アセットがある場合は作り直す (手で編集した内容は消えるので注意)。
環境変数 PPDV_SCREENSHOT=1 を付けると、Showcase_Shape レベルに PostProcessVolume を
置いて効果を写したスクリーンショットを撮り、レベルは保存せずにエディタを終了する (検証用)。
さらに PPDV_DEBUG=1 を付けると、単色の赤 / 赤とシーンの Lerp / マスクのみ / シーンそのまま を出力する
派生マテリアル (保存しない) も続けて撮影する。
PPDV_QUIT=1 は生成後にそのまま終了する。

型の不一致などのシェーダーコンパイルエラーは Python 側には上がってこないので、実行後に
ログの "Failed to compile Material" を確認すること (失敗すると DefaultMaterial で描かれる)。
"""
import os
import time

import unreal

FOLDER = "/Game/Materials/PostProcess"
MAT_NAME = "PP_DamageVignette"
MI_NAME = "PPI_DamageVignette"
MAT_PATH = FOLDER + "/" + MAT_NAME
MI_PATH = FOLDER + "/" + MI_NAME

VERIFY_LEVEL = "/Game/Levels/Showcase_Shape"
SCREENSHOT_NAME = "PP_DamageVignette.png"

mel = unreal.MaterialEditingLibrary
eal = unreal.EditorAssetLibrary
tools = unreal.AssetToolsHelpers.get_asset_tools()


def log(msg):
    unreal.log("[PPDV] " + str(msg))


def enum_value(enum_cls, *candidates):
    """エンジンのバージョンで名前が違う列挙値を、候補の中から見つける。"""
    for name in candidates:
        if hasattr(enum_cls, name):
            return getattr(enum_cls, name)
    raise RuntimeError("%s has none of %s" % (enum_cls, candidates))


# ---------------------------------------------------------------- graph helpers
class Graph(object):
    """ノードの生成と接続をまとめた薄いラッパー。座標は左が入力、右が出力。"""

    def __init__(self, material):
        self.material = material

    def node(self, cls, x, y, **props):
        expr = mel.create_material_expression(self.material, cls, x, y)
        for key, value in props.items():
            expr.set_editor_property(key, value)
        return expr

    def link(self, src, dst, dst_input, src_output=""):
        if not mel.connect_material_expressions(src, src_output, dst, dst_input):
            raise RuntimeError("connect failed: %s -> %s.%s (inputs: %s)" % (
                src.get_name(), dst.get_name(), dst_input,
                list(mel.get_material_expression_input_names(dst))))

    def scalar(self, name, default, x, y, group, prio, smin=0.0, smax=1.0, desc=""):
        return self.node(unreal.MaterialExpressionScalarParameter, x, y,
                         parameter_name=name, default_value=default, group=group,
                         sort_priority=prio, slider_min=smin, slider_max=smax, desc=desc)

    def vector(self, name, rgb, x, y, group, prio, desc=""):
        color = unreal.LinearColor(rgb[0], rgb[1], rgb[2], 1.0)
        return self.node(unreal.MaterialExpressionVectorParameter, x, y,
                         parameter_name=name, default_value=color, group=group,
                         sort_priority=prio, desc=desc)


# ---------------------------------------------------------------- build
def build_material(name=MAT_NAME, debug=None, save=True):
    """マテリアルを組み立てる。debug は検証用の出力切り替え (None / "const3" / "red" / "mask" / "scene")。"""
    mat_path = FOLDER + "/" + name
    for path in ((MI_PATH, mat_path) if name == MAT_NAME else (mat_path,)):
        if eal.does_asset_exist(path):
            log("deleting existing " + path)
            eal.delete_asset(path)

    mat = tools.create_asset(name, FOLDER, unreal.Material, unreal.MaterialFactoryNew())
    if mat is None:
        raise RuntimeError("create_asset failed: " + mat_path)

    mat.set_editor_property("material_domain", unreal.MaterialDomain.MD_POST_PROCESS)
    mat.set_editor_property("blendable_location", enum_value(
        unreal.BlendableLocation,
        "BL_SCENE_COLOR_AFTER_TONEMAPPING", "BL_AFTER_TONEMAPPING"))
    mat.set_editor_property("blendable_priority", 0)

    g = Graph(mat)
    G_DAMAGE, G_SHAPE, G_WOBBLE, G_PULSE = "Damage", "Shape", "Wobble", "Pulse"

    # ---- 1. UV を中心原点 (-1..1) に直す
    screen = g.node(unreal.MaterialExpressionScreenPosition, -2450, -220)
    sub = g.node(unreal.MaterialExpressionSubtract, -2250, -220, const_b=0.5)
    mul2 = g.node(unreal.MaterialExpressionMultiply, -2080, -220, const_b=2.0,
                  desc="1. p = (ViewportUV - 0.5) * 2")
    g.link(screen, sub, "A")
    g.link(sub, mul2, "A")
    vstretch = g.scalar("VerticalStretch", 0.8, -2250, -60, G_SHAPE, 40, 0.3, 1.5,
                        desc="< 1 pulls the tint away from the top/bottom edges")
    one = g.node(unreal.MaterialExpressionConstant, -2250, 60, r=1.0)
    stretch2 = g.node(unreal.MaterialExpressionAppendVector, -2080, 0)
    g.link(one, stretch2, "A")
    g.link(vstretch, stretch2, "B")
    p = g.node(unreal.MaterialExpressionMultiply, -1930, -220,
               desc="p *= (1, VerticalStretch)")
    g.link(mul2, p, "A")
    g.link(stretch2, p, "B")

    # ---- 2. 中心からの距離。楕円 (dot) と矩形 (max) を RectMix で混ぜる
    dot = g.node(unreal.MaterialExpressionDotProduct, -1700, -420,
                 desc="2a. radial = dot(p, p)  (0 center, 2 corners)")
    g.link(p, dot, "A")
    g.link(p, dot, "B")

    absn = g.node(unreal.MaterialExpressionAbs, -1800, -140)
    g.link(p, absn, "")
    mask_r = g.node(unreal.MaterialExpressionComponentMask, -1650, -200, r=True, g=False, b=False, a=False)
    mask_g = g.node(unreal.MaterialExpressionComponentMask, -1650, -80, r=False, g=True, b=False, a=False)
    g.link(absn, mask_r, "")
    g.link(absn, mask_g, "")
    mx = g.node(unreal.MaterialExpressionMax, -1480, -140)
    g.link(mask_r, mx, "A")
    g.link(mask_g, mx, "B")
    rect_sq = g.node(unreal.MaterialExpressionMultiply, -1330, -140,
                     desc="2b. rect = max(|p.x|, |p.y|)^2  (1 along the border)")
    g.link(mx, rect_sq, "A")
    g.link(mx, rect_sq, "B")

    rect_mix = g.scalar("RectMix", 0.5, -1330, 40, G_SHAPE, 30,
                        desc="0 = elliptical vignette, 1 = rectangular frame")
    shape = g.node(unreal.MaterialExpressionLinearInterpolate, -1120, -300,
                   desc="2c. v = lerp(radial, rect, RectMix)")
    g.link(dot, shape, "A")
    g.link(rect_sq, shape, "B")
    g.link(rect_mix, shape, "Alpha")

    # ---- 3. 縁を崩す。角度ごとに周期の違う正弦波を重ねて血だまりのような凹凸を作る
    #         (Noise ノードは格子状のアーティファクトが出たので使わない)
    #         中心 (v=0) には影響しないよう v に比例させる
    wob_amount = g.scalar("WobbleAmount", 0.25, -1200, 700, G_WOBBLE, 10, 0.0, 1.0,
                          desc="How uneven the inner edge is (0 = clean ellipse)")
    wob_detail = g.scalar("WobbleDetail", 4.0, -1800, 380, G_WOBBLE, 20, 1.0, 12.0,
                          desc="Number of lobes around the border. Integers keep the seam invisible")
    wob_speed = g.scalar("WobbleSpeed", 0.4, -1800, 560, G_WOBBLE, 30, 0.0, 3.0,
                         desc="How fast the lobes drift (0 = static)")
    px = g.node(unreal.MaterialExpressionComponentMask, -1800, 250, r=True, g=False, b=False, a=False)
    py = g.node(unreal.MaterialExpressionComponentMask, -1800, 310, r=False, g=True, b=False, a=False)
    g.link(p, px, "")
    g.link(p, py, "")
    angle = g.node(unreal.MaterialExpressionArctangent2, -1650, 280,
                   desc="angle = atan2(p.y, p.x)")
    g.link(py, angle, "Y")
    g.link(px, angle, "X")
    time_n = g.node(unreal.MaterialExpressionTime, -1800, 470)
    t = g.node(unreal.MaterialExpressionMultiply, -1600, 520)
    g.link(time_n, t, "A")
    g.link(wob_speed, t, "B")
    base = g.node(unreal.MaterialExpressionMultiply, -1480, 300,
                  desc="angle * WobbleDetail")
    g.link(angle, base, "A")
    g.link(wob_detail, base, "B")

    two_pi = 6.2831853
    harmonics = []   # (周波数倍率, 時間の倍率, 重み)
    for i, (freq, tmul, weight) in enumerate([(1.0, 1.0, 0.5), (2.0, -1.7, 0.3), (3.0, 0.9, 0.2)]):
        y = 300 + i * 140
        f = g.node(unreal.MaterialExpressionMultiply, -1320, y, const_b=freq)
        g.link(base, f, "A")
        tm = g.node(unreal.MaterialExpressionMultiply, -1320, y + 60, const_b=tmul)
        g.link(t, tm, "A")
        ph = g.node(unreal.MaterialExpressionAdd, -1180, y)
        g.link(f, ph, "A")
        g.link(tm, ph, "B")
        sn = g.node(unreal.MaterialExpressionSine, -1050, y, period=two_pi)
        g.link(ph, sn, "")
        w = g.node(unreal.MaterialExpressionMultiply, -920, y, const_b=weight)
        g.link(sn, w, "A")
        harmonics.append(w)
    sum1 = g.node(unreal.MaterialExpressionAdd, -780, 360)
    g.link(harmonics[0], sum1, "A")
    g.link(harmonics[1], sum1, "B")
    wobble = g.node(unreal.MaterialExpressionAdd, -650, 420,
                    desc="wobble = 0.5 sin(a) + 0.3 sin(2a) + 0.2 sin(3a)   (-1..1)")
    g.link(sum1, wobble, "A")
    g.link(harmonics[2], wobble, "B")

    wob_amt = g.node(unreal.MaterialExpressionMultiply, -1000, 620)
    g.link(wobble, wob_amt, "A")
    g.link(wob_amount, wob_amt, "B")
    one_plus = g.node(unreal.MaterialExpressionAdd, -850, 620, const_a=1.0)
    g.link(wob_amt, one_plus, "B")
    v_noisy = g.node(unreal.MaterialExpressionMultiply, -700, -300,
                     desc="3. v' = v * (1 + wobble * WobbleAmount)  center stays clean")
    g.link(shape, v_noisy, "A")
    g.link(one_plus, v_noisy, "B")

    # ---- 4. マスク化して強さと脈動を掛ける
    inner = g.scalar("InnerRadius", 0.4, -560, -480, G_SHAPE, 10, 0.0, 2.0,
                     desc="Distance where the tint starts (0 = center, 1 = border)")
    outer = g.scalar("OuterRadius", 1.15, -560, -330, G_SHAPE, 20, 0.0, 3.0,
                     desc="Distance where the tint is fully opaque")
    smooth = g.node(unreal.MaterialExpressionSmoothStep, -350, -400,
                    desc="4. mask = smoothstep(InnerRadius, OuterRadius, v')")
    g.link(inner, smooth, "Min")
    g.link(outer, smooth, "Max")
    g.link(v_noisy, smooth, "Value")

    intensity = g.scalar("Intensity", 1.0, -560, -180, G_DAMAGE, 10,
                         desc="Overall strength. Drive this from gameplay (0 = off)")
    pulse_amount = g.scalar("PulseAmount", 0.15, -560, -30, G_PULSE, 10,
                            desc="Heartbeat throb depth (0 = none)")
    pulse_speed = g.scalar("PulseSpeed", 1.5, -560, 120, G_PULSE, 20, 0.0, 5.0,
                           desc="Heartbeat frequency in Hz")
    time_p = g.node(unreal.MaterialExpressionTime, -560, 200)
    pulse_t = g.node(unreal.MaterialExpressionMultiply, -380, 120)
    g.link(time_p, pulse_t, "A")
    g.link(pulse_speed, pulse_t, "B")
    sine = g.node(unreal.MaterialExpressionSine, -240, 120, period=1.0)
    g.link(pulse_t, sine, "")
    pulse_mul = g.node(unreal.MaterialExpressionMultiply, -100, 20)
    g.link(sine, pulse_mul, "A")
    g.link(pulse_amount, pulse_mul, "B")
    pulse = g.node(unreal.MaterialExpressionAdd, 40, 20, const_a=1.0,
                   desc="1 + PulseAmount * sin(Time * PulseSpeed)")
    g.link(pulse_mul, pulse, "B")

    strength = g.node(unreal.MaterialExpressionMultiply, -100, -200)
    g.link(intensity, strength, "A")
    g.link(pulse, strength, "B")
    mask = g.node(unreal.MaterialExpressionMultiply, 60, -400)
    g.link(smooth, mask, "A")
    g.link(strength, mask, "B")
    mask_sat = g.node(unreal.MaterialExpressionSaturate, 200, -400)
    g.link(mask, mask_sat, "")

    # ---- 5. 色。血の赤から角に向かって黒へ落とし、シーン色と合成
    blood = g.vector("BloodColor", (0.9, 0.04, 0.02), 400, -120, G_DAMAGE, 20,
                     desc="Scene color is multiplied by this inside the mask")
    edge = g.vector("EdgeColor", (0.02, 0.0, 0.0), 400, 60, G_DAMAGE, 30,
                    desc="Color the very corners sink to (near black)")
    darken = g.scalar("Darken", 1.0, 400, 250, G_DAMAGE, 40,
                      desc="How much the corners sink toward EdgeColor")
    white = g.node(unreal.MaterialExpressionConstant, 400, -300, r=1.0)
    blood_rgb = g.node(unreal.MaterialExpressionComponentMask, 560, -120, r=True, g=True, b=True, a=False)
    g.link(blood, blood_rgb, "")
    edge_rgb = g.node(unreal.MaterialExpressionComponentMask, 560, 60, r=True, g=True, b=True, a=False)
    g.link(edge, edge_rgb, "")
    tint = g.node(unreal.MaterialExpressionLinearInterpolate, 700, -200,
                  desc="5a. tint = lerp(1, BloodColor, mask)")
    g.link(white, tint, "A")
    g.link(blood_rgb, tint, "B")
    g.link(mask_sat, tint, "Alpha")

    scene_tex = g.node(unreal.MaterialExpressionSceneTexture, 500, -480,
                       scene_texture_id=unreal.SceneTextureId.PPI_POST_PROCESS_INPUT0)
    scene = g.node(unreal.MaterialExpressionComponentMask, 700, -480, r=True, g=True, b=True, a=False,
                   desc="SceneColor.rgb  (float4 -> float3 so the math below type-checks)")
    g.link(scene_tex, scene, "", "Color")
    tinted = g.node(unreal.MaterialExpressionMultiply, 900, -400,
                    desc="5b. tinted = SceneColor * tint  (keeps detail, goes red)")
    g.link(scene, tinted, "A")
    g.link(tint, tinted, "B")

    mask_sq = g.node(unreal.MaterialExpressionMultiply, 650, 200)
    g.link(mask_sat, mask_sq, "A")
    g.link(mask_sat, mask_sq, "B")
    dark_t = g.node(unreal.MaterialExpressionMultiply, 800, 230)
    g.link(mask_sq, dark_t, "A")
    g.link(darken, dark_t, "B")
    final = g.node(unreal.MaterialExpressionLinearInterpolate, 1150, -300,
                   desc="5c. out = lerp(tinted, EdgeColor, mask^2 * Darken)")
    g.link(tinted, final, "A")
    g.link(edge_rgb, final, "B")
    g.link(dark_t, final, "Alpha")

    out = final
    if debug == "mask":
        out = mask_sat
    elif debug == "scene":
        out = scene
    elif debug == "red":
        red = g.node(unreal.MaterialExpressionConstant3Vector, 900, 100,
                     constant=unreal.LinearColor(1.0, 0.0, 0.0, 1.0))
        out = g.node(unreal.MaterialExpressionLinearInterpolate, 1150, 100)
        g.link(scene, out, "A")
        g.link(red, out, "B")
        g.link(mask_sat, out, "Alpha")
    elif debug == "const3":
        out = g.node(unreal.MaterialExpressionConstant3Vector, 900, 100,
                     constant=unreal.LinearColor(1.0, 0.0, 0.0, 1.0))
    if not mel.connect_material_property(out, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR):
        raise RuntimeError("connect_material_property failed")

    mel.recompile_material(mat)
    if save:
        if not eal.save_asset(mat_path, only_if_is_dirty=False):
            raise RuntimeError("save failed: " + mat_path)
        log("saved " + mat_path)
    else:
        log("built (unsaved) " + mat_path)
    return mat


def build_instance(mat):
    mi = tools.create_asset(MI_NAME, FOLDER, unreal.MaterialInstanceConstant,
                            unreal.MaterialInstanceConstantFactoryNew())
    if mi is None:
        raise RuntimeError("create_asset failed: " + MI_PATH)
    mel.set_material_instance_parent(mi, mat)
    # 代表的な項目をインスタンス側に出しておく (値は親と同じ)
    mel.set_material_instance_scalar_parameter_value(mi, "Intensity", 1.0)
    mel.set_material_instance_vector_parameter_value(
        mi, "BloodColor", unreal.LinearColor(0.9, 0.04, 0.02, 1.0))
    mel.update_material_instance(mi)
    if not eal.save_asset(MI_PATH, only_if_is_dirty=False):
        raise RuntimeError("save failed: " + MI_PATH)
    log("saved " + MI_PATH)
    return mi


# ---------------------------------------------------------------- verify
def verify_screenshot(shots):
    """Showcase_Shape に無限範囲の PostProcessVolume を置き、shots の各 (マテリアル, PNG 名) を
    順に撮影してからレベルは保存せずにエディタを終了する。"""
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)

    if not les.load_level(VERIFY_LEVEL):
        raise RuntimeError("load_level failed: " + VERIFY_LEVEL)

    cam = None
    for a in eas.get_all_level_actors():
        if isinstance(a, unreal.CameraActor):
            cam = a
            break
    if cam is None:
        raise RuntimeError("no CameraActor in " + VERIFY_LEVEL)

    vol = eas.spawn_actor_from_class(unreal.PostProcessVolume, unreal.Vector(0, 0, 0))
    vol.set_editor_property("unbound", True)
    vol.set_editor_property("priority", 100.0)
    vol.set_actor_label("PPV_DamageVignette_Verify")

    def set_blendable(mat):
        settings = vol.get_editor_property("settings")
        settings.set_editor_property("weighted_blendables", unreal.WeightedBlendables(
            array=[unreal.WeightedBlendable(weight=1.0, object=mat)]))
        vol.set_editor_property("settings", settings)

    shot_dir = os.path.join(unreal.Paths.project_saved_dir(), "Screenshots", "WindowsEditor")
    for _, png in shots:
        path = os.path.join(shot_dir, png)
        if os.path.exists(path):
            os.remove(path)   # 既存ファイルがあると上書きされないことがある

    state = {"t0": time.time(), "i": 0, "step": 0, "since": 0.0, "handle": None}
    set_blendable(shots[0][0])
    les.editor_set_game_view(True)
    ues.set_level_viewport_camera_info(cam.get_actor_location(), cam.get_actor_rotation())

    def tick(delta):
        elapsed = time.time() - state["t0"]
        mat, png = shots[state["i"]]
        path = os.path.join(shot_dir, png)
        exists = os.path.exists(path)
        # 最初はシェーダーのコンパイル待ち。早すぎると黒いまま写る
        warmup = 60.0 if state["i"] == 0 else 20.0
        if state["step"] == 0 and elapsed - state["since"] > warmup:
            state["step"], state["since"] = 1, elapsed
            log("screenshot requested: %s -> %s" % (mat.get_name(), unreal.AutomationLibrary.take_high_res_screenshot(
                1920, 1080, png, camera=cam)))
        elif state["step"] == 1 and (exists or elapsed - state["since"] > 30.0):
            state["step"], state["since"] = 2, elapsed
            if not exists:
                # たまに書き出されないことがあるのでもう一度頼む
                log("retry: take_high_res_screenshot")
                unreal.AutomationLibrary.take_high_res_screenshot(1920, 1080, png, camera=cam)
        elif state["step"] == 2 and (exists or elapsed - state["since"] > 30.0):
            state["step"], state["since"] = 3, elapsed
            if not exists:
                # AutomationLibrary で書き出されなかった場合はコンソールコマンドで撮る
                log("fallback: HighResShot")
                unreal.SystemLibrary.execute_console_command(
                    None, "HighResShot 1920x1080 filename=" + png)
        elif state["step"] == 3 and (exists or elapsed - state["since"] > 30.0):
            log("screenshot %s exists: %s" % (png, exists))
            state["i"] += 1
            if state["i"] < len(shots):
                state["step"], state["since"] = 0, elapsed
                set_blendable(shots[state["i"]][0])
            else:
                state["step"] = 4
                log("quitting editor")
                unreal.unregister_slate_post_tick_callback(state["handle"])
                unreal.SystemLibrary.quit_editor()

    state["handle"] = unreal.register_slate_post_tick_callback(tick)
    log("verify mode: waiting for shaders")


def main():
    screenshot_mode = os.environ.get("PPDV_SCREENSHOT") == "1"
    quit_mode = os.environ.get("PPDV_QUIT") == "1"
    try:
        mat = build_material()
        build_instance(mat)
    except Exception:
        if screenshot_mode or quit_mode:
            unreal.log_error("[PPDV] build failed, quitting editor")
            unreal.SystemLibrary.quit_editor()
        raise
    if screenshot_mode:
        shots = [(mat, SCREENSHOT_NAME)]
        if os.environ.get("PPDV_DEBUG") == "1":
            # 検証用の派生マテリアル (保存しない)
            for mode in ("const3", "red", "mask", "scene"):
                shots.append((build_material(MAT_NAME + "_Dbg" + mode.capitalize(), mode, save=False),
                              "PP_DamageVignette_dbg_%s.png" % mode))
        verify_screenshot(shots)
    elif quit_mode:
        unreal.SystemLibrary.quit_editor()


main()
