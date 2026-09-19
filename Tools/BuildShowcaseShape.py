"""図形系のマテリアルを集めた Showcase_Shape レベルを生成する。

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
import sys

# 同じフォルダの showcase_builder を import できるようにする
_HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import showcase_builder as sb

LEVEL_PATH = "/Game/Levels/Showcase_Shape"
OUTLINER_FOLDER = "Showcase_Shape"

# 行ごとの (グループ名, 既定フォルダ, [マテリアル名...])
# 採用ルール: _AA があれば _AA、_V2 / 2 があればそちらを採用
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

sb.run(LEVEL_PATH, ROWS, OUTLINER_FOLDER, "Showcase_Shape.png", sb.Layout())
