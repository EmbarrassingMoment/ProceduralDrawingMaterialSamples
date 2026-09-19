"""Content 以下のマテリアル一覧を CSV と Markdown チェックリストに出力する。

使い方 (リポジトリルートで):
    python Tools/ListMaterials.py                       # CSV と ShowcaseCandidates.md
    python Tools/ListMaterials.py --csv out.csv         # 出力先を変える
    python Tools/ListMaterials.py --domains d.csv       # ドメイン情報を取り込む

- M_ / PP_ / PPI_ / MI_ / MF_ を列挙し、git 履歴の追加日・更新日、
  ジャンル別 Showcase レベルへの採用状況、MI の親、使用 MF を付ける。
- .uasset のバイナリから /Game/ パス文字列を拾うだけの簡易実装で、
  UE エディタを起動せずに動く。
- ドメイン列は Tools/material_domains.csv (CheckMaterialDomains.py の出力を控えたもの)
  から取る。マテリアルを増やしたらエディタで CheckMaterialDomains.py を流して更新する。
"""
import csv
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

CONTENT = Path("Content")

# 一覧の見出しに使うフォルダの並び。ここに無いものは後ろに五十音順で続く
FOLDER_ORDER = [
    "Materials/Shape", "Materials/SDF", "Materials/Icon",
    "Materials/Leaf/Ginkgo", "Materials/Leaf/MapleLeaf", "Materials/YinYang",
    "Materials/SnowFlake", "Materials/Animation", "Materials/Hex",
    "Materials/Bonus", "Materials/Bonus/Other", "Materials/Bonus/Dissolve",
    "Materials/Bonus/Fade/Dot", "Materials/Bonus/Fade/Hex",
    "Materials/Transition", "Materials/Transition/Transition_Export",
    "Materials/PostProcess", "Materials/PostProcess/MaterialFunctions/VHS",
    "Materials", "Materials/SF", "Materials/Warp", "Materials/Flare",
    "Materials/Caustics", "Materials/SumiE", "Materials/Ui",
    "Export", "Materials/Export", "WIP",
]

# ジャンル別 Showcase レベル。参照を読んで採用状況を判定する
SHOWCASE_LEVELS = [
    ("Shape", CONTENT / "Levels/Showcase_Shape.umap"),
    ("Seasons", CONTENT / "Levels/Showcase_Seasons.umap"),
]
LEGACY_LEVEL = CONTENT / "Levels/Showcase.umap"


def refs(path):
    """.uasset / .umap のバイナリから /Game/... の参照を拾う。"""
    data = Path(path).read_bytes()
    return {m.group().decode() for m in re.finditer(rb"/Game/[A-Za-z0-9_/\-\.]{4,}", data)}


def base_name(ref):
    return ref.split("/")[-1].split(".")[0]


def git_dates():
    """Content 以下の各ファイルの (追加日, 最終更新日) を git 履歴から拾う。

    -M でリネームを検出し、フォルダ移動があっても元の追加日を引き継ぐ。
    """
    log = subprocess.check_output(
        # -M10%: UE はフォルダ移動時に中身も書き換えるので、既定の閾値ではリネームを取り逃す
        ["git", "log", "--name-status", "-M10%", "--format=@@%ad", "--date=short", "--", "Content"],
        text=True, encoding="utf-8", errors="replace")
    added, updated, renamed_from, date = {}, {}, {}, None
    for line in log.splitlines():
        if line.startswith("@@"):
            date = line[2:]
            continue
        parts = line.split("\t")
        if len(parts) < 2 or not re.match(r"^[AMDRC]\d*$", parts[0]):
            continue
        path = parts[-1]
        if parts[0].startswith(("R", "C")) and len(parts) >= 3:
            # 閾値を緩めてあるので、ファイル名が同じ移動だけを履歴の続きとみなす
            if parts[1].rsplit("/", 1)[-1] == path.rsplit("/", 1)[-1]:
                renamed_from.setdefault(path, parts[1])
        updated.setdefault(path, date)   # 最初に出た = 最新
        added[path] = date               # 最後に出た = 最古

    def origin(path):
        seen = set()
        while path in renamed_from and path not in seen:
            seen.add(path)
            path = renamed_from[path]
        return path

    return {p: added.get(origin(p), d) for p, d in added.items()}, updated


def dates_for(rel, added, updated):
    """新パスの履歴が無い場合 (移動直後など) は同名の旧パスから日付を引き継ぐ。"""
    key = "Content/" + rel
    if key in added:
        return added[key], updated.get(key, "")
    name = key.rsplit("/", 1)[-1]
    cands = [k for k in added if k.rsplit("/", 1)[-1] == name]
    if len(cands) == 1:
        return added[cands[0]], updated.get(cands[0], "")
    return "", ""


def kind_of(name):
    if name.startswith("MI_") or name.startswith("PPI_"):
        return "MI"
    if name.startswith("MF_"):
        return "MF"
    if name.startswith("PP_") or name.startswith("M_PP"):
        return "PP"
    if name.startswith("M_"):
        return "M"
    return None


def collect(domains_csv=None):
    added, updated = git_dates()
    legacy = {r.split(".")[0] for r in refs(LEGACY_LEVEL)} if LEGACY_LEVEL.exists() else set()
    adopted = defaultdict(list)
    for label, path in SHOWCASE_LEVELS:
        if not path.exists():
            continue
        for r in refs(path):
            adopted[base_name(r)].append(label)

    domains = {}
    if domains_csv and Path(domains_csv).exists():
        for row in csv.DictReader(open(domains_csv, encoding="utf-8")):
            domains[row["name"]] = row["domain"]

    rows = []
    for p in sorted(CONTENT.rglob("*.uasset")):
        name = p.stem
        kind = kind_of(name)
        if kind is None:
            continue
        rel = p.relative_to(CONTENT).as_posix()
        r = refs(p)
        parent = ";".join(sorted({base_name(x) for x in r
                                  if kind == "MI" and ("/M_" in x or "/PP_" in x)}))
        mfs = sorted({base_name(x) for x in r if "/MF_" in x and base_name(x) != name})
        rows.append(dict(
            kind=kind, folder=Path(rel).parent.as_posix(), name=name,
            domain=domains.get(name, ""),
            size_kb=p.stat().st_size // 1024,
            added=dates_for(rel, added, updated)[0], updated=dates_for(rel, added, updated)[1],
            in_legacy_showcase="Y" if "/Game/" + rel[:-7] in legacy else "",
            adopted="+".join(sorted(set(adopted.get(name, [])))),
            parent=parent, uses_mf=";".join(mfs)))
    return rows


def write_csv(rows, out):
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def write_markdown(rows, out, has_domains):
    mats = [r for r in rows if r["kind"] in ("M", "PP")]
    kids = defaultdict(list)
    for r in rows:
        if r["kind"] == "MI":
            for parent in r["parent"].split(";"):
                if parent:
                    kids[parent].append(r["name"])
    dup = {n for n, c in Counter(r["name"] for r in mats).items() if c > 1}
    by_folder = defaultdict(list)
    for r in mats:
        by_folder[r["folder"]].append(r)
    order = [f for f in FOLDER_ORDER if f in by_folder]
    order += [f for f in sorted(by_folder) if f not in FOLDER_ORDER]

    counts = Counter(r["adopted"] for r in mats if r["adopted"])
    out_lines = [
        "# Showcase 候補リスト", "",
        "Content 以下の Material / PostProcess マテリアルの全一覧。"
        "ジャンル別 Showcase レベルに載せるものを選ぶための作業用チェックリスト。", "",
        "- 対象: %d 件(M_ %d / PP %d)" % (
            len(mats), sum(1 for r in mats if r["kind"] == "M"),
            sum(1 for r in mats if r["kind"] == "PP")),
        "- `採用` 列はジャンル別 Showcase レベルへの採用状況。空欄はどのレベルにも未掲載",
    ]
    for label, _ in SHOWCASE_LEVELS:
        n = sum(1 for r in mats if label in r["adopted"].split("+"))
        out_lines.append("  - %s: %d 件(`Tools/BuildShowcase%s.py`)" % (label, n, label))
    out_lines += [
        "- `旧` 列は初代 Showcase.umap に配置済みのもの",
        "- `MI` 列はそのマテリアルを親にする Material Instance の数。バリエーション展示の目安",
        "- `追加` / `更新` は git 履歴上の日付。`⚠重複` は同名アセットが別フォルダにもあるもの",
    ]
    if has_domains:
        out_lines.append("- `ドメイン` 列はマテリアルドメイン。"
                         "PostProcess のものは `Materials/PostProcess` にまとめてある")
    out_lines += [
        "",
        "このファイルは生成物。編集せず `python Tools/ListMaterials.py` で作り直す"
        "(採用状況は各 Showcase レベルの参照から自動判定される)。",
    ]

    dom_head = " ドメイン |" if has_domains else ""
    dom_sep = ":--:|" if has_domains else ""
    for folder in order:
        out_lines += ["", "## %s" % folder, "",
                      "| 採用 | 名前 | 種別 |%s 旧 | 追加 | 更新 | MI | 備考 |" % dom_head,
                      "|:--:|---|:--:|%s:--:|---|---|:--:|---|" % dom_sep]
        for r in sorted(by_folder[folder], key=lambda r: r["name"]):
            note = []
            if r["name"] in dup:
                note.append("⚠重複")
            if kids.get(r["name"]):
                note.append("MI: " + ", ".join(sorted(kids[r["name"]])))
            dom = (" %s |" % (r["domain"] or "?")) if has_domains else ""
            out_lines.append("| %s | %s | %s |%s %s | %s | %s | %d | %s |" % (
                r["adopted"] or "", r["name"], r["kind"], dom,
                "✓" if r["in_legacy_showcase"] else "",
                r["added"], r["updated"], len(kids.get(r["name"], [])), " / ".join(note)))

    Path(out).write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    return counts


def main(argv):
    csv_out, md_out, domains = "materials.csv", "ShowcaseCandidates.md", None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--csv" and i + 1 < len(argv):
            csv_out = argv[i + 1]; i += 2
        elif a == "--md" and i + 1 < len(argv):
            md_out = argv[i + 1]; i += 2
        elif a == "--domains" and i + 1 < len(argv):
            domains = argv[i + 1]; i += 2
        elif not a.startswith("--"):
            csv_out = a; i += 1          # 旧来の位置引数
        else:
            i += 1
    if domains is None and Path("Tools/material_domains.csv").exists():
        # CheckMaterialDomains.py の出力を控えたもの。エディタ無しでも列を出せるようにする
        domains = "Tools/material_domains.csv"

    rows = collect(domains)
    write_csv(rows, csv_out)
    write_markdown(rows, md_out, bool(domains))
    print("total", len(rows), dict(Counter(r["kind"] for r in rows)))
    print("wrote", csv_out, "and", md_out)
    for label, _ in SHOWCASE_LEVELS:
        n = sum(1 for r in rows if r["kind"] in ("M", "PP") and label in r["adopted"].split("+"))
        print("  adopted in %s: %d" % (label, n))


if __name__ == "__main__":
    main(sys.argv[1:])
