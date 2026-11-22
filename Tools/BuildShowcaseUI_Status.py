"""値を表示する UI マテリアル (レーダーチャートとゲージ) を集めた Showcase_UI_Status レベルを生成する。

UI マテリアルはメッシュに貼れないので、3D の壁面ではなくウィジェット WBP_Showcase_UI_Status に
並べ、画面に重ねて表示する。レベルは空で、BeginPlay でウィジェットを画面に出すアクター
BP_WidgetShowcase を 1 つ置くだけ。

見かた:
  - PIE: レベルを開いて再生すると、全マテリアルが同時に並んで動く
  - エディタ: Widgets/WBP_Showcase_UI_Status をデザイナーで開いても同じ並びが見える

エディタ内から: メニュー Tools > Execute Python Script で本ファイルを選ぶ、
または Output Log で  py "<repo>/Tools/BuildShowcaseUI_Status.py"

コマンドラインから (Python プラグインを一時的に有効化して実行):
  UnrealEditor-Cmd.exe <repo>/ProceduralDrawingMaterialSamples.uproject
      -EnablePlugins=PythonScriptPlugin -ExecCmds="py <repo>/Tools/BuildShowcaseUI_Status.py"
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

LEVEL_PATH = "/Game/Levels/Showcase_UI_Status"
WIDGET_PATH = sb.WIDGET_FOLDER + "/WBP_Showcase_UI_Status"
OUTLINER_FOLDER = "Showcase_UI_Status"
UI = "/Game/Materials/Ui"

# マテリアルドメインが UI のものだけを並べる。ゲージでもドメインが Surface のもの
# (M_CircleGauge, M_UI_ZZZ_HP_Gauge, M_2D_Liquid, M_Potion) はウィジェットに描けないので入れない。
#   Radar Chart: M_Rader_Chart は目盛り (_BG) と値の多角形 (_Core) を重ねたもの。部品も並べて
#                見比べられるようにする。既定値は全項目 0.5 で正六角形になるので、値を変えた
#                MI_Rader_Chart も並べる
#   Radar Chart (Minimal): 上を作り直した M_RadarChart (Custom ノードなし、各軸の値は Value1〜6 の 0〜1、
#                背景は透過)。既定値は全項目 0.5、MI_RadarChart は見本の値
#   Gauge: M_UI_Battery1 は時間で残量が減っていく
GROUPS = [
    ("Radar Chart", UI, [
        "M_Rader_Chart", "M_Rader_Chart_BG", "M_Rader_Chart_Core", "MI_Rader_Chart",
    ]),
    ("Radar Chart (Minimal)", UI + "/RadarChart", [
        "M_RadarChart", "MI_RadarChart",
    ]),
    ("Gauge", UI, [
        "M_UI_Battery1",
    ]),
]

sb.run_widget(LEVEL_PATH, WIDGET_PATH, GROUPS, OUTLINER_FOLDER)
