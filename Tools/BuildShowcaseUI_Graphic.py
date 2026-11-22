"""イラストや背景に使う UI マテリアルを集めた Showcase_UI_Graphic レベルを生成する。

UI マテリアルはメッシュに貼れないので、3D の壁面ではなくウィジェット WBP_Showcase_UI_Graphic に
並べ、画面に重ねて表示する。レベルは空で、BeginPlay でウィジェットを画面に出すアクター
BP_WidgetShowcase を 1 つ置くだけ。

見かた:
  - PIE: レベルを開いて再生すると、全マテリアルが同時に並んで動く
  - エディタ: Widgets/WBP_Showcase_UI_Graphic をデザイナーで開いても同じ並びが見える

エディタ内から: メニュー Tools > Execute Python Script で本ファイルを選ぶ、
または Output Log で  py "<repo>/Tools/BuildShowcaseUI_Graphic.py"

コマンドラインから (Python プラグインを一時的に有効化して実行):
  UnrealEditor-Cmd.exe <repo>/ProceduralDrawingMaterialSamples.uproject
      -EnablePlugins=PythonScriptPlugin -ExecCmds="py <repo>/Tools/BuildShowcaseUI_Graphic.py"
      -unattended -nosplash

ウィジェットは UE 5.8 の UMGToolSet で組むので、AllToolsets プラグイン (.uproject で有効) が要る。

環境変数 SHOWCASE_SCREENSHOT=1 を付けると、生成後に PIE で再生してウィジェットごと撮り、
エディタを終了する (検証用)。
"""
import os
import sys

# 同じフォルダの showcase_builder を import できるようにする
_HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import showcase_builder as sb

LEVEL_PATH = "/Game/Levels/Showcase_UI_Graphic"
WIDGET_PATH = sb.WIDGET_FOLDER + "/WBP_Showcase_UI_Graphic"
OUTLINER_FOLDER = "Showcase_UI_Graphic"
MATERIALS = "/Game/Materials"

# マテリアルドメインが UI のものだけを並べる。
#   Illustration: M_2DLemon はレモンの輪切り (静止、半透明)
#   Background: M_Warp_Effect_UI は SF/M_Warp_Effect の UI 版で、時間でループする。
#               Surface 版の M_Warp_Effect はウィジェットに描けないので入れない
GROUPS = [
    ("Illustration", MATERIALS, [
        "Ui/M_2DLemon",
    ]),
    ("Background", MATERIALS, [
        "SF/M_Warp_Effect_UI",
    ]),
]

sb.run_widget(LEVEL_PATH, WIDGET_PATH, GROUPS, OUTLINER_FOLDER)
