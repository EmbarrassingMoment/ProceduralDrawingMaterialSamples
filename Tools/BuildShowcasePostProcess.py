"""PostProcess マテリアルを集めた Showcase_PostProcess レベルを生成する。

PostProcess は Plane に貼れないので、1 マテリアルずつ「ブース」に分けて +X 方向へ一列に並べる。
各ブースには同じ小道具と、範囲を区切った PostProcessVolume がある。ブースに入るとその効果がかかり、
ブースの間の隙間とグループ見出しの位置では何もかからない。

見かた:
  - エディタ: レベルを開くと最初のブースの正面にいる。+X 方向へ移動するか、
    アウトライナーの Cam_<マテリアル名> を Pilot する
  - PIE: PlayerStart は最初のブース。+X 方向へ飛んで順に見る

エディタ内から: メニュー Tools > Execute Python Script で本ファイルを選ぶ、
または Output Log で  py "<repo>/Tools/BuildShowcasePostProcess.py"

コマンドラインから (Python プラグインを一時的に有効化して実行):
  UnrealEditor-Cmd.exe <repo>/ProceduralDrawingMaterialSamples.uproject
      -EnablePlugins=PythonScriptPlugin -ExecCmds="py <repo>/Tools/BuildShowcasePostProcess.py"
      -unattended -nosplash

環境変数 SHOWCASE_SCREENSHOT=1 を付けると、生成後に全ブースを撮ってエディタを終了する (検証用)。
"""
import os
import sys

# 同じフォルダの showcase_builder を import できるようにする
_HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import showcase_builder as sb

LEVEL_PATH = "/Game/Levels/Showcase_PostProcess"
OUTLINER_FOLDER = "Showcase_PostProcess"
PP = "/Game/Materials/PostProcess"

# 採用ルールは Showcase_Shape と同じで、_V2 / V3 があればそちらを採用する。
#   除外: PP_Burn_Transition, PP_Flip_Transition, PP_Hex_Transition, PP_NVG,
#         PP_Transition_Warp, PP_Triangle_Transition, PP_VHS_V1, PP_VHS_V2
# 同名の別アセット (Export/PP_Halftone_Color, SF/PP_Hex_Transition) と WIP は入れない。
# インスタンス (PPI_) ではなく元のマテリアルを既定値のまま見せる。
#
# 既定値のままでは効果が見えないので外したもの (時間をずらして 6 回撮って確認した):
#   PP_Scanning_System  ... 常に画面全体が黒になる
#   M_SwordSlash        ... ほとんどの時間で画面全体が黒になる
#   PP_Rect_Dissolve    ... 時間で動かず、既定値では何も起きない。見せるには
#                           DirectionAmount などを変えたインスタンスが要る
GROUPS = [
    # 画面全体の見た目を変えるもの
    ("Filter", PP, [
        "PP_Glitch", "PP_HalfTone", "PP_Halftone_Color", "PP_NVG_V2",
        "PP_Old_TV", "PP_SumiE_Param", "MaterialFunctions/VHS/PP_VHSV3",
    ]),
    # ゲーム中の演出として画面に重ねるもの
    ("Effect", PP, [
        "PP_DamageVignette", "PP_ScanLine", "PP_SpeedLine",
    ]),
    # 画面の切り替え。どれも時間でループするか、進行度の既定値が途中の 0.5 になっている
    ("Transition", PP, [
        "PP_Burn_Transition_V2", "M_Half_Tone_Transition", "PP_Half_Tone", "PP_Hex_Fade",
        "PP_Hex_Transition_V2",
        "PP_Hypnosis_Transition", "PP_PageCurl", "PP_Rect_Transition",
        "PP_SliceTransition", "PP_Slice_Transition", "M_PP_SpiralWipe", "PP_Transition",
        "PP_Transition_Ripple", "PP_Transition_Warp_V2", "PP_Transtion_Flip_V2",
        "PP_Triangle_Transition_V2", "PP_VortexDrainTransition",
    ]),
]

# 全ブース共通の小道具。効果の違いが分かるよう、色相の違う図形と陰影の付く立体を置く。
#   ("panel", マテリアル, x, z, 倍率) / ("mesh", メッシュ, x, y, z, 倍率, yaw)
PROPS = [
    ("panel", "/Game/Materials/Leaf/MapleLeaf/M_JapaneseMapleLeaf", -460.0, 200.0, 1.8),
    ("panel", "/Game/Materials/Leaf/Ginkgo/M_Ginkgo", -230.0, 200.0, 1.8),
    ("panel", "/Game/Materials/YinYang/M_YinYang2", 0.0, 200.0, 1.8),
    ("panel", "/Game/Materials/Shape/M_Heart", 230.0, 200.0, 1.8),
    ("panel", "/Game/Materials/SnowFlake/M_SnowFlake_V2", 460.0, 200.0, 1.8),
    ("mesh", "/Engine/BasicShapes/Sphere", -300.0, 150.0, 40.0, 0.8, 0.0),
    ("mesh", "/Engine/BasicShapes/Cube", 0.0, 150.0, 40.0, 0.8, 30.0),
    ("mesh", "/Engine/BasicShapes/Cone", 300.0, 150.0, 40.0, 0.8, 0.0),
]

LAYOUT = sb.BoothLayout(props=PROPS)

sb.run_booths(LEVEL_PATH, GROUPS, OUTLINER_FOLDER, LAYOUT)
