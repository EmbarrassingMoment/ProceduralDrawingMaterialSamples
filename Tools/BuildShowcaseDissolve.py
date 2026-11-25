"""ディゾルブとフェード (Materials/Bonus) を集めた Showcase_Dissolve レベルを生成する。

エディタ内から: メニュー Tools > Execute Python Script で本ファイルを選ぶ、
または Output Log で  py "<repo>/Tools/BuildShowcaseDissolve.py"

コマンドラインから (Python プラグインを一時的に有効化して実行):
  UnrealEditor-Cmd.exe <repo>/ProceduralDrawingMaterialSamples.uproject
      -EnablePlugins=PythonScriptPlugin -ExecCmds="py <repo>/Tools/BuildShowcaseDissolve.py"
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

LEVEL_PATH = "/Game/Levels/Showcase_Dissolve"
OUTLINER_FOLDER = "Showcase_Dissolve"
BONUS = "/Game/Materials/Bonus"
DISSOLVE = BONUS + "/Dissolve"
HEX_FADE = BONUS + "/Fade/Hex"

# 行ごとの (グループ名, 既定フォルダ, [マテリアル名...])
# どれも時間でループする。元のマテリアルを既定値のまま並べる。
#   _V2 / V3 などの版は、見た目がはっきり違うものはすべて並べる (Rect_Dissolve の V1〜V6 は
#   流れる向き・形・色がそれぞれ違う)。見た目が同じものだけ新しい版に寄せる。
#   入れないもの:
#     M_Rect_Dissolve_V4 ... V6 と同じ動きで、違いは Tiling (8 と 10) だけ
#     M_TriangleTiling   ... 時間で動かず、既定値では白い面に点が散るだけで三角の模様に見えない
#     インスタンス (MI_Hex_Tiling_Dissolve, MI_Transition_Square, MI_Triangle_Tilling_Dissolve,
#       MI_Dot_Fade, MI_Hex_Fade, Mi_Hex_Fade2, MI_Hex_Random_Fade, MI_Hex_Random_Noise,
#       MI_TriangleTiling) ... どれも値を上書きしておらず、親と同じ見た目
ROWS = [
    [
        # 四角いマス目で消えていくもの
        ("Rectangle", DISSOLVE, [
            "M_Rect_Dissolve", "M_Rect_Dissolve_V2", "M_Rect_Dissolve_V3", "M_Rect_Dissolve_V5",
            "M_Rect_Dissolve_V6", "M_Soft_Rectangle_Dissolve", "M_Transition_Square",
        ]),
    ],
    [
        # 三角のマス目。M_Triangle_Motion (Bonus/Other) は消えずに模様が流れ続ける
        ("Triangle", DISSOLVE, [
            "M_Triangle_Dissolve_V2", "M_Triangle_Dissolve_V3", "M_Triangle_Tilling_Dissolve",
            BONUS + "/Other/M_Triangle_Motion",
        ]),
        ("Dot", BONUS + "/Fade/Dot", ["M_Dot_Fade"]),
    ],
    [
        # 六角形のマス目。M_Hex_Learning (Bonus/Other) は M_Hex_Fade_V3 に近いが色が違う
        ("Hex", HEX_FADE, [
            DISSOLVE + "/M_Hex_Tiling_Dissolve", "M_Hex_Fade1", "M_Hex_Fade2", "M_Hex_Fade_V3",
            BONUS + "/Other/M_Hex_Learning", "M_Hex_Random_Fade", "M_Hex_Random_Noise",
            "M_Hex_Tiling_Fade_V2",
        ]),
    ],
]

# 名前の長いもの (M_Soft_Rectangle_Dissolve など) のラベルが重ならないよう、Shape より間隔を広げる
LAYOUT = sb.Layout(col_step=300.0, label_size=24.0)

sb.run(LEVEL_PATH, ROWS, OUTLINER_FOLDER, "Showcase_Dissolve.png", LAYOUT)
