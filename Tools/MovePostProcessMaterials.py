"""ドメインが PostProcess のマテリアルを PostProcess フォルダへ移動する (UE エディタ用)。

ドメインを見て判定するので、名前が M_ で始まっていても PostProcess なら対象になる。
参照は UE 側で張り替えられる。移動できないものはスキップして最後に一覧を出す。

  - 作業中フォルダ (EXCLUDE_FOLDERS) のものは対象外
  - 移動先に同名アセットがある場合は中身が別物の可能性があるのでスキップ

まず何が動くのかを見るドライラン:
  UnrealEditor-Cmd.exe <uproject> -EnablePlugins=PythonScriptPlugin
      -ExecCmds="py <repo>/Tools/MovePostProcessMaterials.py" -unattended -nosplash

実際に移動するときは環境変数 MOVE_APPLY=1 を付ける。MOVE_QUIT=1 で終了。
"""
import os

import unreal

DEST = "/Game/Materials/PostProcess"
EXCLUDE_FOLDERS = ("/Game/WIP",)   # 作業中。完成品の整理対象に含めない

APPLY = os.environ.get("MOVE_APPLY") == "1"

eal = unreal.EditorAssetLibrary


def log(msg):
    unreal.log("[MovePP] " + str(msg))


def parent_of(mi):
    try:
        return mi.get_editor_property("parent")
    except Exception:
        return None


def is_post_process(asset):
    base = asset
    guard = 0
    while isinstance(base, unreal.MaterialInstance) and guard < 16:
        base = parent_of(base)
        guard += 1
    if base is None:
        return False
    try:
        return base.get_editor_property("material_domain") == unreal.MaterialDomain.MD_POST_PROCESS
    except Exception:
        return False


ar = unreal.AssetRegistryHelpers.get_asset_registry()
moves, skipped = [], []
for data in ar.get_assets_by_path("/Game", recursive=True):
    if str(data.asset_class_path.asset_name) not in ("Material", "MaterialInstanceConstant"):
        continue
    path = str(data.package_name)
    folder, name = path.rsplit("/", 1)
    if "/PostProcess" in folder:
        continue
    asset = unreal.load_asset(path)
    if asset is None or not is_post_process(asset):
        continue
    if any(folder == e or folder.startswith(e + "/") for e in EXCLUDE_FOLDERS):
        skipped.append((path, "作業中フォルダのため対象外"))
        continue
    dest = DEST + "/" + name
    if eal.does_asset_exist(dest):
        skipped.append((path, "移動先に同名あり: " + dest))
        continue
    moves.append((path, dest))

moves.sort()
log("%s: %d 件を移動, %d 件をスキップ" % ("実行" if APPLY else "ドライラン", len(moves), len(skipped)))
for src, dest in moves:
    log("   %s  ->  %s" % (src, dest))
for path, why in sorted(skipped):
    log("   SKIP %s  (%s)" % (path, why))

def dependency_options():
    try:
        return unreal.AssetRegistryDependencyOptions(
            include_soft_package_references=True,
            include_hard_package_references=True)
    except Exception:
        return unreal.AssetRegistryDependencyOptions()


def fix_redirectors():
    """移動で残った ObjectRedirector を、参照元を保存し直してから削除する。"""
    ar.scan_paths_synchronous(["/Game"], force_rescan=True)
    redirs = [str(d.package_name) for d in ar.get_assets_by_path("/Game", recursive=True)
              if str(d.asset_class_path.asset_name) == "ObjectRedirector"]
    if not redirs:
        log("no redirectors left behind")
        return
    log("resolving %d redirectors" % len(redirs))
    opts = dependency_options()
    for pkg in redirs:
        refs = [str(r) for r in (ar.get_referencers(pkg, opts) or [])]
        log("   %s  <- %d referencers" % (pkg, len(refs)))
        for r in refs:
            # ロードするとリダイレクタが解決され、保存で新しいパスが書かれる
            if unreal.load_asset(r) is not None:
                eal.save_asset(r, only_if_is_dirty=False)
        log("   %s redirector %s" % ("deleted" if eal.delete_asset(pkg) else "FAILED to delete", pkg))


if APPLY:
    done = 0
    for src, dest in moves:
        if eal.rename_asset(src, dest):
            done += 1
        else:
            log("   FAILED " + src)
    log("moved %d/%d" % (done, len(moves)))

    fix_redirectors()
    eal.save_directory("/Game", only_if_is_dirty=True, recursive=True)
    log("saved dirty packages")

if os.environ.get("MOVE_QUIT") == "1":
    unreal.SystemLibrary.quit_editor()
