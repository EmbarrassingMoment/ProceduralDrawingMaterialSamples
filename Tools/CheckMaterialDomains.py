"""全マテリアルのドメインを調べて CSV に書き出す (UE エディタ用、読み取り専用)。

マテリアルドメイン (Surface / PostProcess / UI / DeferredDecal ...) と、
置かれているフォルダ・名前のプレフィックスが食い違っていないかを確認するために使う。

コマンドラインから:
  UnrealEditor-Cmd.exe <repo>/ProceduralDrawingMaterialSamples.uproject
      -EnablePlugins=PythonScriptPlugin -ExecCmds="py <repo>/Tools/CheckMaterialDomains.py"
      -unattended -nosplash

出力先は環境変数 DOMAIN_CSV で指定する (既定: <project>/Saved/material_domains.csv)。
DOMAIN_QUIT=1 を付けると書き出し後にエディタを終了する。
"""
import csv
import os

import unreal

OUT = os.environ.get("DOMAIN_CSV") or os.path.join(
    unreal.Paths.project_saved_dir(), "material_domains.csv")

DOMAIN_NAMES = {
    unreal.MaterialDomain.MD_SURFACE: "Surface",
    unreal.MaterialDomain.MD_DEFERRED_DECAL: "DeferredDecal",
    unreal.MaterialDomain.MD_LIGHT_FUNCTION: "LightFunction",
    unreal.MaterialDomain.MD_VOLUME: "Volume",
    unreal.MaterialDomain.MD_POST_PROCESS: "PostProcess",
    unreal.MaterialDomain.MD_UI: "UI",
}


def log(msg):
    unreal.log("[CheckDomains] " + str(msg))


def parent_of(mi):
    try:
        return mi.get_editor_property("parent")
    except Exception:
        return None


def domain_of(mat):
    """Material / MaterialInstance からドメイン名を取る。MI は親のドメインを継承する。"""
    base = mat
    guard = 0
    while isinstance(base, unreal.MaterialInstance) and guard < 16:
        base = parent_of(base)
        guard += 1
    if base is None:
        return "?", ""
    try:
        d = base.get_editor_property("material_domain")
    except Exception:
        return "?", base.get_path_name()
    return DOMAIN_NAMES.get(d, str(d)), base.get_path_name()


ar = unreal.AssetRegistryHelpers.get_asset_registry()
rows = []
for data in ar.get_assets_by_path("/Game", recursive=True):
    cls = str(data.asset_class_path.asset_name)
    if cls not in ("Material", "MaterialInstanceConstant"):
        continue
    path = str(data.package_name)
    asset = unreal.load_asset(path)
    if asset is None:
        log("could not load " + path)
        continue
    dom, base_path = domain_of(asset)
    name = path.rsplit("/", 1)[-1]
    folder = path.rsplit("/", 1)[0]
    prefix = "PP_" if name.startswith("PP_") or name.startswith("M_PP") else \
             "MI_" if name.startswith("MI_") else "M_"
    in_pp_folder = "/PostProcess" in folder
    rows.append(dict(
        name=name, folder=folder, kind=cls, domain=dom, prefix=prefix,
        in_pp_folder="Y" if in_pp_folder else "",
        # ドメインと置き場所・名前が食い違っているもの
        misplaced="Y" if (dom == "PostProcess") != bool(in_pp_folder) else "",
        misnamed="Y" if (dom == "PostProcess") != (prefix == "PP_") else "",
        parent=base_path if cls != "Material" else "",
    ))

rows.sort(key=lambda r: (r["domain"], r["folder"], r["name"]))
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

# ListMaterials.py がエディタ無しで参照する控え (name, domain の 2 列)
DIGEST = os.path.join(unreal.Paths.project_dir(), "Tools", "material_domains.csv")
with open(DIGEST, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["name", "domain"])
    for r in sorted(rows, key=lambda r: r["name"]):
        w.writerow([r["name"], r["domain"]])
log("wrote digest " + DIGEST)

counts = {}
for r in rows:
    counts[r["domain"]] = counts.get(r["domain"], 0) + 1
log("wrote %s (%d assets)" % (OUT, len(rows)))
log("domains: " + ", ".join("%s=%d" % kv for kv in sorted(counts.items())))
log("PostProcess domain but not in a PostProcess folder:")
for r in rows:
    if r["domain"] == "PostProcess" and not r["in_pp_folder"]:
        log("   %s/%s" % (r["folder"], r["name"]))
log("in a PostProcess folder but not PostProcess domain:")
for r in rows:
    if r["domain"] != "PostProcess" and r["in_pp_folder"]:
        log("   %s/%s  (%s)" % (r["folder"], r["name"], r["domain"]))

if os.environ.get("DOMAIN_QUIT") == "1":
    unreal.SystemLibrary.quit_editor()
