"""UI ドメインのローディングアイコンを集めた Showcase_UI_LoadingIcon レベルを生成する。

UI マテリアルはメッシュに貼れないので、3D の壁面ではなくウィジェット WBP_Showcase_UI_LoadingIcon に
横一列に並べ、画面に重ねて表示する。レベルは空で、BeginPlay でウィジェットを画面に出すアクター
BP_WidgetShowcase を 1 つ置くだけ。

見かた:
  - PIE: レベルを開いて再生すると、全アイコンが同時に並んで動く
  - エディタ: Widgets/WBP_Showcase_UI_LoadingIcon をデザイナーで開いても同じ並びが見える

エディタ内から: メニュー Tools > Execute Python Script で本ファイルを選ぶ、
または Output Log で  py "<repo>/Tools/BuildShowcaseUI_LoadingIcon.py"

コマンドラインから (Python プラグインを一時的に有効化して実行):
  UnrealEditor-Cmd.exe <repo>/ProceduralDrawingMaterialSamples.uproject
      -EnablePlugins=PythonScriptPlugin -ExecCmds="py <repo>/Tools/BuildShowcaseUI_LoadingIcon.py"
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

LEVEL_PATH = "/Game/Levels/Showcase_UI_LoadingIcon"
WIDGET_PATH = sb.WIDGET_FOLDER + "/WBP_Showcase_UI_LoadingIcon"
OUTLINER_FOLDER = "Showcase_UI_LoadingIcon"
UI = "/Game/Materials/Ui"

# マテリアルドメインが UI のローディング表示だけを、元のマテリアルの既定値のまま並べる。
#   ドメインが Surface なので入れない: Ui/M_Loading_Icon_V2, Icon/M_Loading_Icon,
#                                     Icon/M_JA3_Loading_Icon
#   MI_Loading_Icon_V3 は親の M_Loading_Icon_V3 と見た目が同じなので入れない
GROUPS = [
    ("Loading Icon", UI, [
        "M_Loading_Icon_UI", "M_Loading_Icon_V3", "M_Loading_Icon_V4",
        "LoadingIcon/M_LoadingIcon", "LoadingBoxes/M_LoadingBoxes",
    ]),
]

sb.run_widget(LEVEL_PATH, WIDGET_PATH, GROUPS, OUTLINER_FOLDER)
