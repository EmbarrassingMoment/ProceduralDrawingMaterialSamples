"""時間で動くマテリアル (Materials/Animation) を集めた Showcase_Animation レベルを生成する。

エディタ内から: メニュー Tools > Execute Python Script で本ファイルを選ぶ、
または Output Log で  py "<repo>/Tools/BuildShowcaseAnimation.py"

コマンドラインから (Python プラグインを一時的に有効化して実行):
  UnrealEditor-Cmd.exe <repo>/ProceduralDrawingMaterialSamples.uproject
      -EnablePlugins=PythonScriptPlugin -ExecCmds="py <repo>/Tools/BuildShowcaseAnimation.py"
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

LEVEL_PATH = "/Game/Levels/Showcase_Animation"
OUTLINER_FOLDER = "Showcase_Animation"
ANIM = "/Game/Materials/Animation"

# 行ごとの (グループ名, 既定フォルダ, [マテリアル名...])
# どれも時間でループする。元のマテリアルを既定値のまま並べる。
#   採用ルールは Showcase_Shape と同じで、V2 があればそちらを採用する。除外: M_Tunnel
#   インスタンスは入れない。MI_ECG, MI_SpeedLine, MI_Spiral, MI_Triangle_Animation,
#   MI_Rect_Transtition, MI_Swirl_Transition(_V2) はどれも親と同じ値で、見た目が変わらない
ROWS = [
    [
        # 線や波形が動くもの
        ("Wave", ANIM, [
            "M_ECG", "M_Pulse", "M_Simple_Wave", "M_Sine_Wave", "M_Rainbow_Wave",
        ]),
        # 中心から放射状・渦状に動くもの
        ("Radial", ANIM, ["M_SpeedLine", "M_Spiral", "M_Star_Trail", "M_TunnelV2"]),
    ],
    [
        # タイル状の模様が動くもの
        ("Pattern", ANIM, [
            "M_Pulse_Animation", "M_Rainbow_Sample", "M_Rect_Animation",
            "M_Triangle_Animation", "M_Triangle_Animation_2", "M_Triangle_Animation_3",
        ]),
    ],
    [
        # 四角・渦・三角の形でテクスチャが現れては消える切り替え
        ("Transition", ANIM, [
            "M_Rect_Transtition", "M_Swirl_Transition", "M_Triangle", "M_Triangle1",
        ]),
        ("Glitch", ANIM, ["M_Glitch"]),
    ],
]

# 名前の長いもの (M_Triangle_Animation_2 など) のラベルが重ならないよう、Shape より間隔を広げる
LAYOUT = sb.Layout(col_step=300.0, label_size=24.0)

sb.run(LEVEL_PATH, ROWS, OUTLINER_FOLDER, "Showcase_Animation.png", LAYOUT)
