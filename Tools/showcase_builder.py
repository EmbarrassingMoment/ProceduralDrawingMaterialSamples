"""ジャンル別 Showcase レベルを組み立てる共通モジュール (UE エディタ用)。

各ジャンルのスクリプト (BuildShowcase*.py) から import して使う。
マテリアルを Plane に貼って壁面に並べ、名前ラベルとグループ見出し、
正面カメラを置いて保存するところまでを担当する。

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
    """並べ方の設定。単位は cm。"""

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


def build(level_path, rows, outliner_folder, layout=None, tag="Showcase"):
    """rows の内容でレベルを組み立てて保存し、(カメラ, 見つからなかったパス) を返す。

    rows は行のリスト。各行はグループのリストで、グループは
    (グループ名, 既定フォルダ, [マテリアル名...])。
    マテリアル名が /Game/ で始まる場合は既定フォルダを無視して絶対パス扱い。
    """
    layout = layout or Layout()

    def log(msg):
        unreal.log("[%s] %s" % (tag, msg))

    if eal.does_asset_exist(level_path):
        # 既存レベルは削除せず開き直し、前回このスクリプトが置いたアクターだけ消す
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

    plane = unreal.load_asset(PLANE_MESH)
    prot = _plane_rotation(layout)
    trot = _text_rotation(layout)
    half = layout.plane_scale * 50.0   # Plane の半分の実寸

    def spawn_text(text, location, size, color, folder):
        actor = eas.spawn_actor_from_class(unreal.TextRenderActor, location, trot)
        comp = actor.text_render
        comp.set_text(text)
        comp.set_world_size(size)
        comp.set_horizontal_alignment(unreal.HorizTextAligment.EHTA_CENTER)
        comp.set_vertical_alignment(unreal.VerticalTextAligment.EVRTA_TEXT_CENTER)
        comp.set_text_render_color(_color(color))
        comp.set_cast_shadow(False)
        actor.set_actor_label("Label_" + text)
        actor.set_folder_path(folder)
        return actor

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
            for name in names:
                path = name if name.startswith("/Game/") else gfolder + "/" + name
                short = path.rsplit("/", 1)[-1]
                mat = unreal.load_asset(path)
                loc = unreal.Vector(x, layout.wall_y, z)
                if mat is None:
                    missing.append(path)
                    log("MISSING " + path)
                else:
                    actor = eas.spawn_actor_from_class(unreal.StaticMeshActor, loc, prot)
                    smc = actor.static_mesh_component
                    smc.set_static_mesh(plane)
                    smc.set_material(0, mat)
                    smc.set_cast_shadow(False)
                    actor.set_actor_scale3d(unreal.Vector(layout.plane_scale,
                                                          layout.plane_scale,
                                                          layout.plane_scale))
                    actor.set_actor_label("SM_" + short)
                    actor.set_folder_path(outliner_folder + "/" + gname)
                    placed += 1
                spawn_text(short, loc + unreal.Vector(0, 0, -(half + 35.0)),
                           layout.label_size, layout.label_color,
                           outliner_folder + "/" + gname)
                x += layout.col_step
            gx = (group_start_x + (x - layout.col_step)) / 2.0
            spawn_text(gname, unreal.Vector(gx, layout.wall_y, z + half + 55.0),
                       layout.group_label_size, layout.group_label_color,
                       outliner_folder + "/" + gname)
            x += layout.group_gap

    # カメラと PlayerStart を壁の正面へ
    center_z = layout.base_z + (n_rows - 1) * layout.row_step / 2.0
    target = unreal.Vector(0.0, layout.wall_y, center_z)
    cam_loc = target + layout.face_dir * layout.camera_distance
    cam_rot = unreal.MathLibrary.find_look_at_rotation(cam_loc, target)
    cam = eas.spawn_actor_from_class(unreal.CameraActor, cam_loc, cam_rot)
    cam.set_actor_label("Cam_" + outliner_folder)
    cam.set_folder_path(outliner_folder)
    cam.camera_component.set_field_of_view(layout.camera_fov)
    for a in eas.get_all_level_actors():
        if isinstance(a, unreal.PlayerStart):
            start_rot = unreal.Rotator()
            start_rot.yaw = cam_rot.yaw
            a.set_actor_location(unreal.Vector(cam_loc.x, cam_loc.y, 100.0), False, False)
            a.set_actor_rotation(start_rot, False)

    ues.set_level_viewport_camera_info(cam_loc, cam_rot)
    if not les.save_current_level():
        raise RuntimeError("save failed")
    log("saved %s: placed=%d missing=%d" % (level_path, placed, len(missing)))
    return cam, missing


def run(level_path, rows, outliner_folder, screenshot_name, layout=None, tag=None):
    """build() を呼び、SHOWCASE_SCREENSHOT=1 ならスクリーンショットを撮って終了する。"""
    tag = tag or outliner_folder

    def log(msg):
        unreal.log("[%s] %s" % (tag, msg))

    screenshot_mode = os.environ.get("SHOWCASE_SCREENSHOT") == "1"
    try:
        cam, missing = build(level_path, rows, outliner_folder, layout, tag)
    except Exception:
        if screenshot_mode:
            # 検証実行では失敗してもエディタを残さない
            unreal.log_error("[%s] build failed, quitting editor" % tag)
            unreal.SystemLibrary.quit_editor()
        raise

    if not screenshot_mode:
        return cam, missing

    shot_path = os.path.join(unreal.Paths.project_saved_dir(), "Screenshots",
                             "WindowsEditor", screenshot_name)
    if os.path.exists(shot_path):
        os.remove(shot_path)   # 既存ファイルがあると上書きされないことがある
    state = {"t0": time.time(), "step": 0, "handle": None}

    def tick(delta):
        elapsed = time.time() - state["t0"]
        if state["step"] == 0 and elapsed > 40.0:
            # シェーダーのコンパイル待ち。早すぎると黒いまま写る
            state["step"] = 1
            les.editor_set_game_view(True)
            ues.set_level_viewport_camera_info(cam.get_actor_location(), cam.get_actor_rotation())
            log("screenshot requested: %s" % unreal.AutomationLibrary.take_high_res_screenshot(
                1920, 1080, screenshot_name, camera=cam))
        elif state["step"] == 1 and elapsed > 52.0:
            state["step"] = 2
            if os.path.exists(shot_path):
                log("screenshot written: " + shot_path)
            else:
                # AutomationLibrary で書き出されなかった場合はコンソールコマンドで撮る
                log("fallback: HighResShot")
                unreal.SystemLibrary.execute_console_command(
                    None, "HighResShot 1920x1080 filename=" + screenshot_name)
        elif state["step"] == 2 and elapsed > 66.0:
            state["step"] = 3
            log("screenshot exists: %s -> quitting editor" % os.path.exists(shot_path))
            unreal.unregister_slate_post_tick_callback(state["handle"])
            unreal.SystemLibrary.quit_editor()

    state["handle"] = unreal.register_slate_post_tick_callback(tick)
    log("screenshot mode: waiting for shaders")
    return cam, missing
