"""ジャンル別 Showcase レベルを組み立てる共通モジュール (UE エディタ用)。

各ジャンルのスクリプト (BuildShowcase*.py) から import して使う。

- build / run: マテリアルを Plane に貼って壁面に並べる (Shape, Seasons)
- build_booths / run_booths: PostProcess マテリアル用。範囲を区切った PostProcessVolume と
  同じ小道具を 1 マテリアルずつ「ブース」として一列に並べ、中に入るとその効果がかかる

使う側の例:
    import showcase_builder as sb
    sb.run("/Game/Levels/Showcase_Xxx", ROWS, "Showcase_Xxx", "Showcase_Xxx.png")
"""
import os
import time

import unreal

TEMPLATE = "/Engine/Maps/Templates/Template_Default"
PLANE_MESH = "/Engine/BasicShapes/Plane"

les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
eal = unreal.EditorAssetLibrary


class Layout(object):
    """壁面に並べるときの設定。単位は cm。"""

    def __init__(self, plane_scale=2.0, col_step=250.0, row_step=350.0,
                 group_gap=60.0, base_z=200.0, wall_y=0.0,
                 camera_distance=2200.0, camera_fov=70.0,
                 label_size=30.0, group_label_size=60.0,
                 label_color=(20, 20, 20), group_label_color=(255, 140, 0),
                 plane_spin=0.0, face_dir=(0.0, 1.0, 0.0)):
        self.plane_scale = plane_scale        # Plane は 100x100 なので倍率で実寸が決まる
        self.col_step = col_step              # 横の間隔
        self.row_step = row_step              # 縦の間隔
        self.group_gap = group_gap            # グループ間の追加間隔
        self.base_z = base_z                  # 最下段の中心高さ
        self.wall_y = wall_y                  # 壁面の位置
        self.camera_distance = camera_distance
        self.camera_fov = camera_fov
        self.label_size = label_size          # マテリアル名の文字サイズ
        self.group_label_size = group_label_size
        self.label_color = label_color
        self.group_label_color = group_label_color
        self.plane_spin = plane_spin          # Plane の法線まわりの追加回転 (UV 調整用)
        self.face_dir = unreal.Vector(*face_dir)   # 壁が向く方向


class BoothLayout(object):
    """PostProcess ブースの設定。単位は cm。ブースは +X 方向に並び、見る位置は +Y 側。

    props は全ブース共通の小道具で、各要素は次のどちらか:
      ("panel", マテリアルのパス, x, z, 倍率)       ... 見る位置を向いた Plane
      ("mesh",  メッシュのパス,   x, y, z, 倍率, yaw) ... 既定マテリアルのままの形状
    """

    def __init__(self, props=(), spacing=1500.0, group_gap=1500.0,
                 camera_distance=900.0, camera_z=200.0, camera_fov=70.0,
                 volume_y=(-600.0, 1200.0), volume_z=(-200.0, 800.0), volume_gap=200.0,
                 blend_radius=50.0, label_z=360.0, label_size=50.0, label_color=(20, 20, 20),
                 heading_z=260.0, heading_size=150.0, heading_color=(255, 140, 0),
                 floor_margin=3000.0):
        self.props = list(props)
        self.spacing = spacing                # ブース中心の間隔。隣のブースが画角に入らない幅にする
        self.group_gap = group_gap            # グループの切れ目に足す間隔 (見出しを置く)
        self.camera_distance = camera_distance
        self.camera_z = camera_z
        self.camera_fov = camera_fov
        self.volume_y = volume_y              # ボリュームが覆う Y の範囲。見る位置と小道具の両方を含める
        self.volume_z = volume_z
        self.volume_gap = volume_gap          # 隣り合うボリュームの隙間。ここでは効果がかからない
        self.blend_radius = blend_radius
        self.label_z = label_z
        self.label_size = label_size
        self.label_color = label_color
        self.heading_z = heading_z
        self.heading_size = heading_size
        self.heading_color = heading_color
        self.floor_margin = floor_margin      # 端のブースの先にも床を残す長さ
        self.face_dir = unreal.Vector(0.0, 1.0, 0.0)
        self.plane_spin = 0.0


def _logger(tag):
    def log(msg):
        unreal.log("[%s] %s" % (tag, msg))
    return log


def _color(rgb):
    return unreal.Color(r=rgb[0], g=rgb[1], b=rgb[2], a=255)


def _plane_rotation(layout):
    """Plane(法線 +Z) の法線を face_dir に向ける Rotator を求める。"""
    for roll in (-90.0, 90.0):
        r = unreal.Rotator()
        r.roll = roll
        if unreal.MathLibrary.get_up_vector(r).dot(layout.face_dir) > 0.99:
            spin = unreal.Rotator()
            spin.yaw = layout.plane_spin
            return unreal.MathLibrary.compose_rotators(spin, r)
    raise RuntimeError("could not orient plane")


def _text_rotation(layout):
    """TextRender(既定で +X を向く) を face_dir に向ける。"""
    for yaw in (90.0, -90.0, 0.0, 180.0):
        r = unreal.Rotator()
        r.yaw = yaw
        if unreal.MathLibrary.get_forward_vector(r).dot(layout.face_dir) > 0.99:
            return r
    raise RuntimeError("could not orient text")


def _spawn_text(text, location, rotation, size, rgb, folder):
    actor = eas.spawn_actor_from_class(unreal.TextRenderActor, location, rotation)
    comp = actor.text_render
    comp.set_text(text)
    comp.set_world_size(size)
    comp.set_horizontal_alignment(unreal.HorizTextAligment.EHTA_CENTER)
    comp.set_vertical_alignment(unreal.VerticalTextAligment.EVRTA_TEXT_CENTER)
    comp.set_text_render_color(_color(rgb))
    comp.set_cast_shadow(False)
    actor.set_actor_label("Label_" + text)
    actor.set_folder_path(folder)
    return actor


def _spawn_mesh(mesh, location, rotation, scale, folder, label, material=None):
    actor = eas.spawn_actor_from_class(unreal.StaticMeshActor, location, rotation)
    smc = actor.static_mesh_component
    smc.set_static_mesh(mesh)
    if material is not None:
        smc.set_material(0, material)
    actor.set_actor_scale3d(unreal.Vector(scale, scale, scale))
    actor.set_actor_label(label)
    actor.set_folder_path(folder)
    return actor


def _open_level(level_path, outliner_folder, log):
    """レベルを開く。既存なら削除せず開き直し、前回このスクリプトが置いたアクターだけ消す。"""
    if eal.does_asset_exist(level_path):
        if not les.load_level(level_path):
            raise RuntimeError("load_level failed: " + level_path)
        removed = 0
        for a in eas.get_all_level_actors():
            fp = str(a.get_folder_path())
            if fp == outliner_folder or fp.startswith(outliner_folder + "/"):
                eas.destroy_actor(a)
                removed += 1
        log("reusing existing level, removed %d actors" % removed)
    else:
        if not les.new_level_from_template(level_path, TEMPLATE):
            raise RuntimeError("new_level_from_template failed")
        log("created level from template")


def _place_player_start(cam_loc, cam_rot):
    for a in eas.get_all_level_actors():
        if isinstance(a, unreal.PlayerStart):
            start_rot = unreal.Rotator()
            start_rot.yaw = cam_rot.yaw
            a.set_actor_location(unreal.Vector(cam_loc.x, cam_loc.y, 100.0), False, False)
            a.set_actor_rotation(start_rot, False)


def _spawn_camera(location, target, fov, label, folder):
    rot = unreal.MathLibrary.find_look_at_rotation(location, target)
    cam = eas.spawn_actor_from_class(unreal.CameraActor, location, rot)
    cam.set_actor_label(label)
    cam.set_folder_path(folder)
    cam.camera_component.set_field_of_view(fov)
    return cam


def _save(level_path, log, summary):
    if not les.save_current_level():
        raise RuntimeError("save failed")
    log("saved %s: %s" % (level_path, summary))


# ------------------------------------------------------------------ 壁面に並べる
def build(level_path, rows, outliner_folder, layout=None, tag="Showcase"):
    """rows の内容でレベルを組み立てて保存し、(カメラ, 見つからなかったパス) を返す。

    rows は行のリスト。各行はグループのリストで、グループは
    (グループ名, 既定フォルダ, [マテリアル名...])。
    マテリアル名が /Game/ で始まる場合は既定フォルダを無視して絶対パス扱い。
    """
    layout = layout or Layout()
    log = _logger(tag)
    _open_level(level_path, outliner_folder, log)

    plane = unreal.load_asset(PLANE_MESH)
    prot = _plane_rotation(layout)
    trot = _text_rotation(layout)
    half = layout.plane_scale * 50.0   # Plane の半分の実寸

    missing = []
    placed = 0
    n_rows = len(rows)
    for row_idx, groups in enumerate(rows):
        z = layout.base_z + (n_rows - 1 - row_idx) * layout.row_step
        # 行全体の幅を求めて中央寄せ
        n_items = sum(len(g[2]) for g in groups)
        width = (n_items - 1) * layout.col_step + (len(groups) - 1) * layout.group_gap
        x = -width / 2.0
        for gname, gfolder, names in groups:
            group_start_x = x
            folder = outliner_folder + "/" + gname
            for name in names:
                path = name if name.startswith("/Game/") else gfolder + "/" + name
                short = path.rsplit("/", 1)[-1]
                mat = unreal.load_asset(path)
                loc = unreal.Vector(x, layout.wall_y, z)
                if mat is None:
                    missing.append(path)
                    log("MISSING " + path)
                else:
                    actor = _spawn_mesh(plane, loc, prot, layout.plane_scale, folder,
                                        "SM_" + short, mat)
                    actor.static_mesh_component.set_cast_shadow(False)
                    placed += 1
                _spawn_text(short, loc + unreal.Vector(0, 0, -(half + 35.0)), trot,
                            layout.label_size, layout.label_color, folder)
                x += layout.col_step
            gx = (group_start_x + (x - layout.col_step)) / 2.0
            _spawn_text(gname, unreal.Vector(gx, layout.wall_y, z + half + 55.0), trot,
                        layout.group_label_size, layout.group_label_color, folder)
            x += layout.group_gap

    # カメラと PlayerStart を壁の正面へ
    center_z = layout.base_z + (n_rows - 1) * layout.row_step / 2.0
    target = unreal.Vector(0.0, layout.wall_y, center_z)
    cam_loc = target + layout.face_dir * layout.camera_distance
    cam = _spawn_camera(cam_loc, target, layout.camera_fov, "Cam_" + outliner_folder,
                        outliner_folder)
    _place_player_start(cam_loc, cam.get_actor_rotation())

    ues.set_level_viewport_camera_info(cam_loc, cam.get_actor_rotation())
    _save(level_path, log, "placed=%d missing=%d" % (placed, len(missing)))
    return cam, missing


# ------------------------------------------------------------------ PostProcess ブース
def _box_volume(center, half_extent, folder, label, log):
    """範囲を区切った PostProcessVolume を置く。ブラシの寸法から倍率を決めて half_extent に合わせる。"""
    vol = eas.spawn_actor_from_class(unreal.PostProcessVolume, center)
    _, ext = vol.get_actor_bounds(False)
    if min(ext.x, ext.y, ext.z) < 1.0:
        # スポーン経路によってはブラシが空になるので、立方体のブラシを作る
        log("volume spawned without a brush; building a cube brush")
        builder = unreal.CubeBuilder()
        for axis in ("x", "y", "z"):
            builder.set_editor_property(axis, 200.0)
        builder.build(ues.get_editor_world(), vol)
        _, ext = vol.get_actor_bounds(False)
    vol.set_actor_scale3d(unreal.Vector(half_extent.x / ext.x, half_extent.y / ext.y,
                                        half_extent.z / ext.z))
    vol.set_actor_label(label)
    vol.set_folder_path(folder)
    vol.set_editor_property("unbound", False)
    return vol


def _set_blendable(vol, material, blend_radius):
    settings = vol.get_editor_property("settings")
    settings.set_editor_property("weighted_blendables", unreal.WeightedBlendables(
        array=[unreal.WeightedBlendable(weight=1.0, object=material)]))
    vol.set_editor_property("settings", settings)
    vol.set_editor_property("blend_radius", blend_radius)
    vol.set_editor_property("blend_weight", 1.0)


def _extend_floor(x_min, x_max, folder, log):
    """テンプレートの床が並びの端まで届かなければ、床を X 方向に複製して継ぎ足す。"""
    floor = None
    for a in eas.get_all_level_actors():
        fp = str(a.get_folder_path())   # フォルダ無しは "None" になる
        if isinstance(a, unreal.StaticMeshActor) and not fp.startswith(folder.split("/")[0]):
            sm = a.static_mesh_component.get_editor_property("static_mesh")
            if sm is not None and "Floor" in sm.get_name():
                floor = a
                break
    if floor is None:
        log("no template floor found; leaving the floor as is")
        return 0
    origin, ext = floor.get_actor_bounds(False)
    size = ext.x * 2.0
    log("template floor: center=(%.0f, %.0f) half=(%.0f, %.0f)" % (origin.x, origin.y, ext.x, ext.y))
    added = 0
    k = 1
    while origin.x + k * size - ext.x < x_max or origin.x - k * size + ext.x > x_min:
        for sign in (1, -1):
            cx = origin.x + sign * k * size
            if cx - ext.x < x_max and cx + ext.x > x_min:
                dup = eas.duplicate_actor(floor, None, unreal.Vector(sign * k * size, 0.0, 0.0))
                dup.set_actor_label("Floor_Extension_%+d" % (sign * k))
                dup.set_folder_path(folder + "/_Floor")
                added += 1
        k += 1
        if k > 200:
            break
    log("floor tiles added: %d" % added)
    return added


def build_booths(level_path, groups, outliner_folder, layout, tag="Showcase"):
    """PostProcess マテリアルを 1 つずつブースに入れてレベルを組み立てて保存する。

    groups は (グループ名, 既定フォルダ, [マテリアル名...]) のリスト。名前の扱いは build() と同じ。
    返り値は [(カメラ, マテリアル名), ...] と見つからなかったパスのリスト。
    """
    log = _logger(tag)
    _open_level(level_path, outliner_folder, log)

    plane = unreal.load_asset(PLANE_MESH)
    prot = _plane_rotation(layout)
    trot = _text_rotation(layout)

    # 小道具は先に読み込んで、見つからないものを早めに知らせる
    props = []
    for p in layout.props:
        asset = unreal.load_asset(p[1])
        if asset is None:
            log("MISSING prop " + p[1])
            continue
        props.append((p, asset))

    booths, missing = [], []
    vol_half = unreal.Vector(layout.spacing / 2.0 - layout.volume_gap / 2.0,
                             (layout.volume_y[1] - layout.volume_y[0]) / 2.0,
                             (layout.volume_z[1] - layout.volume_z[0]) / 2.0)
    vol_cy = (layout.volume_y[0] + layout.volume_y[1]) / 2.0
    vol_cz = (layout.volume_z[0] + layout.volume_z[1]) / 2.0

    x = 0.0
    first_x = None
    # 見出しはグループの切れ目の真ん中に置く。どの効果もかからず、どのブースの画角にも入らない
    heading_offset = (layout.spacing + layout.group_gap) / 2.0
    for g_idx, (gname, gfolder, names) in enumerate(groups):
        if g_idx > 0:
            x += layout.group_gap
        _spawn_text(gname, unreal.Vector(x - heading_offset, 0.0, layout.heading_z), trot,
                    layout.heading_size, layout.heading_color, outliner_folder + "/" + gname)
        for name in names:
            path = name if name.startswith("/Game/") else gfolder + "/" + name
            short = path.rsplit("/", 1)[-1]
            mat = unreal.load_asset(path)
            if mat is None:
                missing.append(path)
                log("MISSING " + path)
                continue
            if first_x is None:
                first_x = x
            folder = "%s/%s/%s" % (outliner_folder, gname, short)
            for i, (p, asset) in enumerate(props):
                if p[0] == "panel":
                    _, _, dx, z, scale = p
                    a = _spawn_mesh(plane, unreal.Vector(x + dx, 0.0, z), prot, scale, folder,
                                    "Prop_%s_%d" % (short, i), asset)
                else:
                    _, _, dx, dy, z, scale, yaw = p
                    rot = unreal.Rotator()
                    rot.yaw = yaw
                    a = _spawn_mesh(asset, unreal.Vector(x + dx, dy, z), rot, scale, folder,
                                    "Prop_%s_%d" % (short, i))
            _spawn_text(short, unreal.Vector(x, 0.0, layout.label_z), trot,
                        layout.label_size, layout.label_color, folder)
            vol = _box_volume(unreal.Vector(x, vol_cy, vol_cz), vol_half, folder,
                              "PPV_" + short, log)
            _set_blendable(vol, mat, layout.blend_radius)
            cam = _spawn_camera(unreal.Vector(x, layout.camera_distance, layout.camera_z),
                                unreal.Vector(x, 0.0, layout.camera_z), layout.camera_fov,
                                "Cam_" + short, folder)
            booths.append((cam, short))
            x += layout.spacing

    if not booths:
        raise RuntimeError("no booths were built")
    last_x = x - layout.spacing
    _extend_floor(first_x - layout.floor_margin, last_x + layout.floor_margin,
                  outliner_folder, log)

    first_cam = booths[0][0]
    _place_player_start(first_cam.get_actor_location(), first_cam.get_actor_rotation())
    ues.set_level_viewport_camera_info(first_cam.get_actor_location(),
                                       first_cam.get_actor_rotation())
    _save(level_path, log, "booths=%d missing=%d" % (len(booths), len(missing)))
    return booths, missing


# ------------------------------------------------------------------ 撮影
def _shoot(shots, log, first_warmup=60.0, warmup=20.0):
    """shots の各 (カメラ, PNG 名) を順に撮影し、終わったらエディタを終了する。

    take_high_res_screenshot はたまに書き出されないので、待ってから再依頼し、
    それでもだめならコンソールコマンドで撮る。
    """
    shot_dir = os.path.join(unreal.Paths.project_saved_dir(), "Screenshots", "WindowsEditor")
    for _, png in shots:
        path = os.path.join(shot_dir, png)
        if os.path.exists(path):
            os.remove(path)   # 既存ファイルがあると上書きされないことがある
    state = {"t0": time.time(), "i": 0, "step": 0, "since": 0.0, "handle": None, "ok": 0}
    les.editor_set_game_view(True)

    def aim(cam):
        ues.set_level_viewport_camera_info(cam.get_actor_location(), cam.get_actor_rotation())

    aim(shots[0][0])

    def tick(delta):
        elapsed = time.time() - state["t0"]
        cam, png = shots[state["i"]]
        exists = os.path.exists(os.path.join(shot_dir, png))
        # 最初はシェーダーのコンパイル待ち。早すぎると黒いまま写る
        wait = first_warmup if state["i"] == 0 else warmup
        if state["step"] == 0 and elapsed - state["since"] > wait:
            state["step"], state["since"] = 1, elapsed
            unreal.AutomationLibrary.take_high_res_screenshot(1920, 1080, png, camera=cam)
        elif state["step"] == 1 and (exists or elapsed - state["since"] > 30.0):
            state["step"], state["since"] = 2, elapsed
            if not exists:
                log("retry: take_high_res_screenshot " + png)
                unreal.AutomationLibrary.take_high_res_screenshot(1920, 1080, png, camera=cam)
        elif state["step"] == 2 and (exists or elapsed - state["since"] > 30.0):
            state["step"], state["since"] = 3, elapsed
            if not exists:
                log("fallback: HighResShot " + png)
                unreal.SystemLibrary.execute_console_command(
                    None, "HighResShot 1920x1080 filename=" + png)
        elif state["step"] == 3 and (exists or elapsed - state["since"] > 30.0):
            state["ok"] += 1 if exists else 0
            log("screenshot %d/%d %s: %s" % (state["i"] + 1, len(shots), png,
                                             "ok" if exists else "MISSING"))
            state["i"] += 1
            if state["i"] < len(shots):
                state["step"], state["since"] = 0, elapsed
                aim(shots[state["i"]][0])
            else:
                state["step"] = 4
                log("screenshots written: %d/%d -> quitting editor" % (state["ok"], len(shots)))
                unreal.unregister_slate_post_tick_callback(state["handle"])
                unreal.SystemLibrary.quit_editor()

    state["handle"] = unreal.register_slate_post_tick_callback(tick)
    log("screenshot mode: waiting for shaders")


def _run(builder, tag):
    """builder() を呼び、失敗時は検証実行ならエディタを閉じる。"""
    screenshot_mode = os.environ.get("SHOWCASE_SCREENSHOT") == "1"
    try:
        result = builder()
    except Exception:
        if screenshot_mode:
            # 検証実行では失敗してもエディタを残さない
            unreal.log_error("[%s] build failed, quitting editor" % tag)
            unreal.SystemLibrary.quit_editor()
        raise
    return screenshot_mode, result


def run(level_path, rows, outliner_folder, screenshot_name, layout=None, tag=None):
    """build() を呼び、SHOWCASE_SCREENSHOT=1 ならスクリーンショットを撮って終了する。"""
    tag = tag or outliner_folder
    screenshot_mode, (cam, missing) = _run(
        lambda: build(level_path, rows, outliner_folder, layout, tag), tag)
    if screenshot_mode:
        _shoot([(cam, screenshot_name)], _logger(tag))
    return cam, missing


def run_booths(level_path, groups, outliner_folder, layout, tag=None):
    """build_booths() を呼び、SHOWCASE_SCREENSHOT=1 なら全ブースを撮って終了する。

    画像は Saved/Screenshots/WindowsEditor/<outliner_folder>_<連番>_<マテリアル名>.png。
    """
    tag = tag or outliner_folder
    screenshot_mode, (booths, missing) = _run(
        lambda: build_booths(level_path, groups, outliner_folder, layout, tag), tag)
    if screenshot_mode:
        shots = [(cam, "%s_%02d_%s.png" % (outliner_folder, i + 1, name))
                 for i, (cam, name) in enumerate(booths)]
        _shoot(shots, _logger(tag), first_warmup=90.0, warmup=8.0)
    return booths, missing
