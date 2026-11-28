"""六角形のマス目のマテリアル (Materials/Hex) を集めた Showcase_Hex レベルを生成する。

エディタ内から: メニュー Tools > Execute Python Script で本ファイルを選ぶ、
または Output Log で  py "<repo>/Tools/BuildShowcaseHex.py"

コマンドラインから (Python プラグインを一時的に有効化して実行):
  UnrealEditor-Cmd.exe <repo>/ProceduralDrawingMaterialSamples.uproject
      -EnablePlugins=PythonScriptPlugin -ExecCmds="py <repo>/Tools/BuildShowcaseHex.py"
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

LEVEL_PATH = "/Game/Levels/Showcase_Hex"
OUTLINER_FOLDER = "Showcase_Hex"
HEX = "/Game/Materials/Hex"

# 行ごとの (グループ名, 既定フォルダ, [マテリアル名...])
# M_HexTiling 以外は時間でループする。元のマテリアルを既定値のまま並べる。
#   _V2 / V3 などの版は Showcase_Dissolve と同じく、見た目がはっきり違うものはすべて並べる
#   (M_Hex_Animation の 1〜V4 は色も動きもそれぞれ違う)
#   M_HexTiling は動かない六角形の格子。線が 1 px ほどと細く、この距離では点に潰れて見える
#   (近づけば格子になる)
#   入れないもの: MI_HexTiling, MI_HexTiling_V3, MI_Hex_V2 ... 値を上書きしておらず、親と同じ見た目
ROWS = [
    [
        # 六角形の格子と、マス目ごとに明滅・フェードするもの
        ("Tiling", HEX, ["M_HexTiling", "M_HexTiling_V3", "M_Hex_V2"]),
        # マス目の境目が動いてテクスチャが現れるもの
        ("Dissolve", HEX, ["M_Hex_Dissolve"]),
    ],
    [
        # 色や光が六角形のマス目を流れるもの (M_Hex_Animatoin_V2 は綴りが元のまま)
        ("Animation", HEX, [
            "M_Hex_Animation", "M_Hex_Animatoin_V2", "M_Hex_Animation_V3", "M_Hex_Animation_V4",
        ]),
    ],
]

LAYOUT = sb.Layout(col_step=300.0, label_size=24.0)

sb.run(LEVEL_PATH, ROWS, OUTLINER_FOLDER, "Showcase_Hex.png", LAYOUT)
