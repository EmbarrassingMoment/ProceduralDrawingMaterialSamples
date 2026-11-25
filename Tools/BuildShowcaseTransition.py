"""画面の切り替え用マテリアル (Materials/Transition) を集めた Showcase_Transition レベルを生成する。

エディタ内から: メニュー Tools > Execute Python Script で本ファイルを選ぶ、
または Output Log で  py "<repo>/Tools/BuildShowcaseTransition.py"

コマンドラインから (Python プラグインを一時的に有効化して実行):
  UnrealEditor-Cmd.exe <repo>/ProceduralDrawingMaterialSamples.uproject
      -EnablePlugins=PythonScriptPlugin -ExecCmds="py <repo>/Tools/BuildShowcaseTransition.py"
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

LEVEL_PATH = "/Game/Levels/Showcase_Transition"
OUTLINER_FOLDER = "Showcase_Transition"
TRANS = "/Game/Materials/Transition"
# M_Flip_Transition の不具合を直した版。フォルダが Transition ではないので /Game/ からのパスで渡す
FLIP_FIXED = "/Game/Materials/Transitions/FlipTransition/M_FlipTransition"

# 行ごとの (グループ名, 既定フォルダ, [マテリアル名...])
# どれも時間でループし、2 枚のテクスチャ (または色) を行き来する。元のマテリアルを既定値のまま並べる。
#   M_Flip_Transition の隣には、パラメータと既定値をそのままに不具合を直した M_FlipTransition を置く
#   (元はタイルがめくれず帯で切り抜かれ、線幅が段の境目で跳び、タイルの縦の大きさが 1/TilingX で、
#   めくり中の隙間が常に黒だった)
#   入れないもの:
#     M_HalfTone_V2          ... 時間で動かず、既定値 (Control=3) では全面が黒のまま。
#                                見せるには Control を変えたインスタンスが要る
#     MI_Halftone_Transition ... 値を上書きしておらず、親の M_Halftone_Transition_V2 と同じ見た目
#   M_Transition_V6 と M_Transition_Warp はパラメータが同じだが、歪み方が違うので両方並べる
ROWS = [
    [
        # 燃える・めくれる・網点・四角など、形で境目が動いて切り替わるもの
        ("Wipe", TRANS, [
            "M_Burn_Transition", "M_Flip_Transition", FLIP_FIXED, "M_Halftone_Transition_V2",
            "M_Page_Curl", "M_Rectangle_Transition",
        ]),
    ],
    [
        # 画像を波打たせたり、ぼかしたりしながら切り替わるもの
        ("Distortion", TRANS, [
            "M_Transition_Ripple", "M_Transition_Wave", "M_Transition_Warp", "M_Transition_V6",
            "M_Zoom_Blur_Transition", "Transition_Export/M_Transition_Distortion",
        ]),
    ],
]

# 名前の長いもの (M_Halftone_Transition_V2 など) のラベルが重ならないよう、Shape より間隔を広げる
LAYOUT = sb.Layout(col_step=300.0, label_size=24.0)

sb.run(LEVEL_PATH, ROWS, OUTLINER_FOLDER, "Showcase_Transition.png", LAYOUT)
