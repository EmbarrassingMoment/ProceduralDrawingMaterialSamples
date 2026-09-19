"""Content 以下のマテリアル一覧を CSV に出力する。

使い方 (リポジトリルートで):
    python Tools/ListMaterials.py materials.csv

- M_ / PP_ / MI_ / MF_ を列挙し、git 履歴の追加日・更新日、
  Showcase.umap から参照されているか、MI の親、使用 MF を付ける。
- .uasset のバイナリから /Game/ パス文字列を拾うだけの簡易実装で、
  UE エディタを起動せずに動く。
"""
import csv, re, subprocess, sys
from collections import Counter
from pathlib import Path

content = Path("Content")

log = subprocess.check_output(
    ["git", "log", "--name-status", "--format=@@%ad", "--date=short", "--", "Content"],
    text=True, encoding="utf-8", errors="replace")
added, updated, date = {}, {}, None
for line in log.splitlines():
    if line.startswith("@@"):
        date = line[2:]
        continue
    m = re.match(r"^([AMDR]\d*)\t(.+)$", line)
    if not m:
        continue
    path = m.group(2).split("\t")[-1]
    updated.setdefault(path, date)  # 最初に出た = 最新
    added[path] = date              # 最後に出た = 最古


def refs(p: Path):
    return {m.group().decode() for m in re.finditer(rb"/Game/[A-Za-z0-9_/\-\.]{4,}", p.read_bytes())}


def base(r):
    return r.split("/")[-1].split(".")[0]


show = {s.split(".")[0] for s in refs(content / "Levels/Showcase.umap")}
rows = []
for p in sorted(content.rglob("*.uasset")):
    n = p.stem
    if n.startswith("MI_"): kind = "MI"
    elif n.startswith("MF_"): kind = "MF"
    elif n.startswith("PP_") or n.startswith("M_PP"): kind = "PP"
    elif n.startswith("M_"): kind = "M"
    else: continue
    rel = p.relative_to(content).as_posix()
    r = refs(p)
    parent = ";".join(sorted({base(x) for x in r if kind == "MI" and ("/M_" in x or "/PP_" in x)}))
    mfs = sorted({base(x) for x in r if "/MF_" in x and base(x) != n})
    rows.append(dict(
        kind=kind, folder=Path(rel).parent.as_posix(), name=n, size_kb=p.stat().st_size // 1024,
        added=added.get("Content/" + rel, ""), updated=updated.get("Content/" + rel, ""),
        in_showcase="Y" if "/Game/" + rel[:-7] in show else "",
        parent=parent, uses_mf=";".join(mfs)))

out = sys.argv[1] if len(sys.argv) > 1 else "materials.csv"
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print("total", len(rows), dict(Counter(r["kind"] for r in rows)))
print("in showcase:", sum(1 for r in rows if r["in_showcase"]))
