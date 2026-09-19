"""季節もののマテリアルを集めた Showcase_Seasons レベルを生成する。

エディタ内から: メニュー Tools > Execute Python Script で本ファイルを選ぶ、
または Output Log で  py "<repo>/Tools/BuildShowcaseSeasons.py"

コマンドラインから (Python プラグインを一時的に有効化して実行):
  UnrealEditor-Cmd.exe <repo>/ProceduralDrawingMaterialSamples.uproject
      -EnablePlugins=PythonScriptPlugin -ExecCmds="py <repo>/Tools/BuildShowcaseSeasons.py"
      -unattended -nosplash

環境変数 SHOWCASE_SCREENSHOT=1 を付けると、生成後にスクリーンショットを撮って
エディタを終了する (検証用)。
"""
import os
import sys

# 同じフォルダの showcase_builder を import できるようにする
_HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import showcase_builder as sb

LEVEL_PATH = "/Game/Levels/Showcase_Seasons"
OUTLINER_FOLDER = "Showcase_Seasons"

# 季節ごとのグループ。点数が少ないので V1 / V2 は両方並べて見比べられるようにする。
# 夏に当たるマテリアルはまだ無いので、春・秋・冬の 3 グループ。
ROWS = [
    [
        ("Spring", "/Game/Materials/Icon", [
            "M_CherryBloosom", "M_CherryBlossom_V2",
        ]),
        ("Autumn", None, [
            "/Game/Materials/Leaf/MapleLeaf/M_JapaneseMapleLeaf",
            "/Game/Materials/Leaf/Ginkgo/M_Ginkgo",
        ]),
        ("Winter", "/Game/Materials/SnowFlake", [
            "M_SnowFlake", "M_SnowFlake_V2", "M_CinematicSnow",
        ]),
    ],
]

# 1 行だけなので Shape より大きめに見せ、季節の区切りが分かるよう間隔を広げる
LAYOUT = sb.Layout(
    plane_scale=2.6,
    col_step=340.0,
    group_gap=200.0,
    base_z=400.0,
    camera_distance=2100.0,
    label_size=34.0,
    group_label_size=80.0,
)

sb.run(LEVEL_PATH, ROWS, OUTLINER_FOLDER, "Showcase_Seasons.png", LAYOUT)
