"""Showcase_Shape レベルを自動生成する UE エディタ用 Python スクリプト。

エディタ内から: メニュー Tools > Execute Python Script で本ファイルを選ぶ、
または Output Log で  py "<repo>/Tools/BuildShowcaseShape.py"

コマンドラインから (Python プラグインを一時的に有効化して実行):
  UnrealEditor-Cmd.exe <repo>/ProceduralDrawingMaterialSamples.uproject
      -EnablePlugins=PythonScriptPlugin -ExecCmds="py <repo>/Tools/BuildShowcaseShape.py"
      -unattended -nosplash

環境変数 SHOWCASE_SCREENSHOT=1 を付けると、生成後にスクリーンショットを撮って
エディタを終了する (検証用)。
"""
import os
import time
import unreal

LEVEL_PATH = "/Game/Levels/Showcase_Shape"
TEMPLATE = "/Engine/Maps/Templates/Template_Default"
PLANE_MESH = "/Engine/BasicShapes/Plane"

# 行ごとの (グループ名, フォルダ, [マテリアル名...])
# ルール: _AA があれば _AA、_V2 / 2 があればそちらを採用
ROWS = [
    [
        ("Shape", "/Game/Materials/Shape", [
            "M_Circle_AA", "M_CrossMark_V2", "M_Heart", "M_Hex", "M_Polygon_AA",
            "M_Rectangle", "M_Rhombus2", "M_Ring_V2", "M_RoundedRectangle", "M_Square",
        ]),
    ],
    [
        ("SDF", "/Game/Materials/SDF", [
            "M_4PointStar2", "M_ExclamationMark", "M_Grid", "M_Heart_SDF", "M_Star_V2",
        ]),
        ("YinYang", "/Game/Materials/YinYang", ["M_YinYang2"]),
        ("Leaf", None, [
            "/Game/Materials/Leaf/Ginkgo/M_Ginkgo",
            "/Game/Materials/Leaf/MapleLeaf/M_JapaneseMapleLeaf",
        ]),
    ],
    [
        ("Icon", "/Game/Materials/Icon", [
            "M_5PointStar_V2", "M_CherryBlossom_V2", "M_Gear", "M_HazardMark",
            "M_JA3_Loading_Icon", "M_Loading_Icon", "M_Radar_Icon",
        ]),
        ("SnowFlake", "/Game/Materials/SnowFlake", ["M_SnowFlake_V2", "M_CinematicSnow"]),
    ],
]

# レイアウト (単位: cm)
PLANE_SCALE = 2.0          # Plane は 100x100 なので 200x200 に
COL_STEP = 250.0           # 横の間隔
ROW_STEP = 350.0           # 縦の間隔
GROUP_GAP = 60.0           # グループ間の追加間隔
BASE_Z = 200.0             # 最下段の中心高さ
WALL_Y = 0.0
FACE_DIR = unreal.Vector(0.0, 1.0, 0.0)   # 壁が向く方向 (+Y 側から見る)
PLANE_SPIN = 0.0           # Plane の法線まわりの追加回転 (UV の向き調整用)
CAMERA_DISTANCE = 2200.0
OUTLINER_FOLDER = "Showcase_Shape"

les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
eal = unreal.EditorAssetLibrary


def log(msg):
    unreal.log("[ShowcaseShape] " + str(msg))


def plane_rotation():
    """Plane(法線 +Z) の法線を FACE_DIR に向ける Rotator を求める。"""
    for roll in (-90.0, 90.0):
        r = unreal.Rotator()
        r.roll = roll
        up = unreal.MathLibrary.get_up_vector(r)
        if up.dot(FACE_DIR) > 0.99:
            spin = unreal.Rotator()
            spin.yaw = PLANE_SPIN
            return unreal.MathLibrary.compose_rotators(spin, r)
    raise RuntimeError("could not orient plane")


def text_rotation():
    """TextRender(既定で +X を向く) を FACE_DIR に向ける。"""
    for yaw in (90.0, -90.0, 0.0, 180.0):
        r = unreal.Rotator()
        r.yaw = yaw
        if unreal.MathLibrary.get_forward_vector(r).dot(FACE_DIR) > 0.99:
            return r
    raise RuntimeError("could not orient text")


def spawn_text(text, location, size, color, folder):
    actor = eas.spawn_actor_from_class(unreal.TextRenderActor, location, text_rotation())
    comp = actor.text_render
    comp.set_text(text)
    comp.set_world_size(size)
    comp.set_horizontal_alignment(unreal.HorizTextAligment.EHTA_CENTER)
    comp.set_vertical_alignment(unreal.VerticalTextAligment.EVRTA_TEXT_CENTER)
    comp.set_text_render_color(color)
    comp.set_cast_shadow(False)
    actor.set_actor_label("Label_" + text)
    actor.set_folder_path(folder)
    return actor


def build():
    if eal.does_asset_exist(LEVEL_PATH):
        # 既存レベルは削除せず開き直し、前回このスクリプトが置いたアクターだけ消す
        if not les.load_level(LEVEL_PATH):
            raise RuntimeError("load_level failed: " + LEVEL_PATH)
        removed = 0
        for a in eas.get_all_level_actors():
            fp = str(a.get_folder_path())
            if fp == OUTLINER_FOLDER or fp.startswith(OUTLINER_FOLDER + "/"):
                eas.destroy_actor(a)
                removed += 1
        log("reusing existing level, removed %d actors" % removed)
    else:
        if not les.new_level_from_template(LEVEL_PATH, TEMPLATE):
            raise RuntimeError("new_level_from_template failed")
        log("created level from template")

    plane = unreal.load_asset(PLANE_MESH)
    prot = plane_rotation()
    log("plane rotation: %s  up=%s" % (prot, unreal.MathLibrary.get_up_vector(prot)))
    log("text rotation: %s" % text_rotation())

    missing = []
    placed = 0
    n_rows = len(ROWS)
    for row_idx, groups in enumerate(ROWS):
        z = BASE_Z + (n_rows - 1 - row_idx) * ROW_STEP
        # 行全体の幅を求めて中央寄せ
        n_items = sum(len(g[2]) for g in groups)
        width = (n_items - 1) * COL_STEP + (len(groups) - 1) * GROUP_GAP
        x = -width / 2.0
        for g_idx, (gname, gfolder, names) in enumerate(groups):
            group_start_x = x
            for name in names:
                path = name if name.startswith("/Game/") else gfolder + "/" + name
                short = path.rsplit("/", 1)[-1]
                mat = unreal.load_asset(path)
                loc = unreal.Vector(x, WALL_Y, z)
                if mat is None:
                    missing.append(path)
                    log("MISSING " + path)
                else:
                    actor = eas.spawn_actor_from_class(unreal.StaticMeshActor, loc, prot)
                    smc = actor.static_mesh_component
                    smc.set_static_mesh(plane)
                    smc.set_material(0, mat)
                    smc.set_cast_shadow(False)
                    actor.set_actor_scale3d(unreal.Vector(PLANE_SCALE, PLANE_SCALE, PLANE_SCALE))
                    actor.set_actor_label("SM_" + short)
                    actor.set_folder_path(OUTLINER_FOLDER + "/" + gname)
                    placed += 1
                spawn_text(short, loc + unreal.Vector(0, 0, -(PLANE_SCALE * 50 + 35)), 30.0,
                           unreal.Color(r=20, g=20, b=20, a=255), OUTLINER_FOLDER + "/" + gname)
                x += COL_STEP
            gx = (group_start_x + (x - COL_STEP)) / 2.0
            spawn_text(gname, unreal.Vector(gx, WALL_Y, z + PLANE_SCALE * 50 + 55), 60.0,
                       unreal.Color(r=255, g=140, b=0, a=255), OUTLINER_FOLDER + "/" + gname)
            x += GROUP_GAP

    # カメラと PlayerStart を壁の正面へ
    center_z = BASE_Z + (n_rows - 1) * ROW_STEP / 2.0
    target = unreal.Vector(0.0, WALL_Y, center_z)
    cam_loc = target + FACE_DIR * CAMERA_DISTANCE
    cam_rot = unreal.MathLibrary.find_look_at_rotation(cam_loc, target)
    cam = eas.spawn_actor_from_class(unreal.CameraActor, cam_loc, cam_rot)
    cam.set_actor_label("Cam_Showcase_Shape")
    cam.set_folder_path(OUTLINER_FOLDER)
    cam.camera_component.set_field_of_view(70.0)
    for a in eas.get_all_level_actors():
        if isinstance(a, unreal.PlayerStart):
            start_rot = unreal.Rotator()
            start_rot.yaw = cam_rot.yaw
            a.set_actor_location(unreal.Vector(cam_loc.x, cam_loc.y, 100.0), False, False)
            a.set_actor_rotation(start_rot, False)

    ues.set_level_viewport_camera_info(cam_loc, cam_rot)
    if not les.save_current_level():
        raise RuntimeError("save failed")
    log("saved %s: placed=%d missing=%d" % (LEVEL_PATH, placed, len(missing)))
    return cam, missing


SCREENSHOT_MODE = os.environ.get("SHOWCASE_SCREENSHOT") == "1"

try:
    cam, missing = build()
except Exception:
    if SCREENSHOT_MODE:
        # 検証実行では失敗してもエディタを残さない
        unreal.log_error("[ShowcaseShape] build failed, quitting editor")
        unreal.SystemLibrary.quit_editor()
    raise

if SCREENSHOT_MODE:
    shot_name = "Showcase_Shape.png"
    shot_path = os.path.join(unreal.Paths.project_saved_dir(), "Screenshots", "WindowsEditor", shot_name)
    if os.path.exists(shot_path):
        os.remove(shot_path)  # 既存ファイルがあると上書きされないことがある
    state = {"t0": time.time(), "step": 0, "handle": None}

    def tick(delta):
        elapsed = time.time() - state["t0"]
        if state["step"] == 0 and elapsed > 40.0:
            state["step"] = 1
            les.editor_set_game_view(True)
            ues.set_level_viewport_camera_info(cam.get_actor_location(), cam.get_actor_rotation())
            ok = unreal.AutomationLibrary.take_high_res_screenshot(1920, 1080, shot_name, camera=cam)
            log("screenshot requested: %s" % ok)
        elif state["step"] == 1 and elapsed > 52.0:
            state["step"] = 2
            if os.path.exists(shot_path):
                log("screenshot written: " + shot_path)
            else:
                # AutomationLibrary で書き出されなかった場合はコンソールコマンドで撮る
                log("fallback: HighResShot")
                unreal.SystemLibrary.execute_console_command(None, "HighResShot 1920x1080 filename=" + shot_name)
        elif state["step"] == 2 and elapsed > 66.0:
            state["step"] = 3
            log("screenshot exists: %s -> quitting editor" % os.path.exists(shot_path))
            unreal.unregister_slate_post_tick_callback(state["handle"])
            unreal.SystemLibrary.quit_editor()

    state["handle"] = unreal.register_slate_post_tick_callback(tick)
    log("screenshot mode: waiting for shaders")
