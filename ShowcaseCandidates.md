# Showcase 候補リスト

Content 以下の Material / PostProcess マテリアルの全一覧。ジャンル別 Showcase レベルに載せるものを選ぶための作業用チェックリスト。

- 対象: 174 件(M_ 134 / PP 40)
- `採用` 列はジャンル別 Showcase レベルへの採用状況。空欄はどのレベルにも未掲載
  - Shape: 27 件(`Tools/BuildShowcaseShape.py`)
  - Seasons: 7 件(`Tools/BuildShowcaseSeasons.py`)
- `旧` 列は初代 Showcase.umap に配置済みのもの
- `MI` 列はそのマテリアルを親にする Material Instance の数。バリエーション展示の目安
- `追加` / `更新` は git 履歴上の日付。`⚠重複` は同名アセットが別フォルダにもあるもの
- `ドメイン` 列はマテリアルドメイン。PostProcess のものは `Materials/PostProcess` にまとめてある

このファイルは生成物。編集せず `python Tools/ListMaterials.py` で作り直す(採用状況は各 Showcase レベルの参照から自動判定される)。

## Materials/Shape

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
|  | M_Circle | M | Surface | ✓ | 2023-06-20 | 2023-06-20 | 1 | MI: MI_Circle |
| Shape | M_Circle_AA | M | Surface | ✓ | 2023-06-20 | 2023-06-20 | 1 | MI: MI_Circle_AA |
|  | M_CrossMark | M | Surface | ✓ | 2023-10-09 | 2023-10-09 | 1 | MI: MI_CrossMark |
| Shape | M_CrossMark_V2 | M | Surface | ✓ | 2023-10-09 | 2023-10-09 | 1 | MI: MI_CrossMark_V2 |
| Shape | M_Heart | M | Surface | ✓ | 2023-10-09 | 2023-10-09 | 1 | MI: MI_Heart |
| Shape | M_Hex | M | Surface |  | 2023-06-20 | 2023-06-20 | 1 | MI: MI_Hex |
|  | M_Polygon | M | Surface | ✓ | 2023-06-20 | 2023-06-20 | 1 | MI: MI_Polygon |
| Shape | M_Polygon_AA | M | Surface |  | 2023-06-20 | 2023-06-20 | 1 | MI: MI_Polygon_AA |
| Shape | M_Rectangle | M | Surface | ✓ | 2023-06-20 | 2023-06-20 | 1 | MI: MI_Rectangle |
|  | M_Rhombus | M | Surface | ✓ | 2023-06-20 | 2023-06-20 | 1 | MI: MI_Rhombus |
| Shape | M_Rhombus2 | M | Surface | ✓ | 2023-06-20 | 2023-06-20 | 1 | MI: MI_Rhombus2 |
|  | M_Ring | M | Surface | ✓ | 2023-06-20 | 2023-06-20 | 1 | MI: MI_Ring |
| Shape | M_Ring_V2 | M | Surface | ✓ | 2023-10-09 | 2023-10-09 | 0 |  |
| Shape | M_RoundedRectangle | M | Surface | ✓ | 2023-06-20 | 2023-06-20 | 1 | MI: MI_RoundedRectangle |
| Shape | M_Square | M | Surface | ✓ | 2023-06-20 | 2023-06-20 | 1 | MI: MI_Square |

## Materials/SDF

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
|  | M_4PointStar | M | Surface | ✓ | 2023-08-20 | 2023-08-20 | 1 | MI: MI_4PointStar |
| Shape | M_4PointStar2 | M | Surface | ✓ | 2023-08-20 | 2023-08-20 | 1 | MI: MI_4PointStar_2 |
| Shape | M_ExclamationMark | M | Surface | ✓ | 2023-08-20 | 2023-08-20 | 1 | MI: MI_ExclamationMark |
| Shape | M_Grid | M | Surface |  | 2022-06-07 | 2026-01-05 | 1 | MI: MI_Grid |
| Shape | M_Heart_SDF | M | Surface |  | 2023-07-03 | 2023-07-03 | 0 |  |
|  | M_Star | M | Surface | ✓ | 2023-08-20 | 2023-08-20 | 1 | MI: MI_Star |
| Shape | M_Star_V2 | M | Surface | ✓ | 2023-08-20 | 2023-08-20 | 0 |  |

## Materials/Icon

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
| Shape | M_5PointStar_V2 | M | Surface | ✓ | 2025-07-11 | 2025-07-11 | 1 | MI: MI_5PointStar_V2 |
|  | M_5pointStar | M | Surface | ✓ | 2025-07-11 | 2025-07-11 | 1 | MI: MI_5pointStar |
| Seasons | M_CherryBloosom | M | Surface | ✓ | 2025-07-11 | 2025-07-11 | 1 | MI: MI_CherryBloosom |
| Seasons+Shape | M_CherryBlossom_V2 | M | Surface | ✓ | 2025-07-11 | 2025-07-11 | 1 | MI: MI_CherryBlossom_V2 |
| Shape | M_Gear | M | Surface | ✓ | 2025-07-11 | 2025-07-11 | 1 | MI: MI_Gear |
| Shape | M_HazardMark | M | Surface | ✓ | 2025-07-11 | 2025-07-11 | 0 |  |
| Shape | M_JA3_Loading_Icon | M | Surface | ✓ | 2024-03-16 | 2024-03-16 | 0 |  |
| Shape | M_Loading_Icon | M | Surface | ✓ | 2025-07-11 | 2026-03-16 | 1 | MI: MI_Loading_Icon |
| Shape | M_Radar_Icon | M | Surface |  | 2023-12-31 | 2025-07-11 | 0 |  |

## Materials/Leaf/Ginkgo

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
| Seasons+Shape | M_Ginkgo | M | Surface | ✓ | 2022-08-12 | 2026-01-08 | 1 | MI: MI_Ginkgo |

## Materials/Leaf/MapleLeaf

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
| Seasons+Shape | M_JapaneseMapleLeaf | M | Surface |  | 2022-06-15 | 2022-12-25 | 1 | MI: MI_JapaneseMapleLeaf |

## Materials/YinYang

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
|  | M_YinYang1 | M | Surface | ✓ | 2023-08-20 | 2023-08-20 | 1 | MI: MI_YinYang |
| Shape | M_YinYang2 | M | Surface |  | 2023-08-20 | 2023-08-20 | 0 |  |

## Materials/SnowFlake

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
| Seasons+Shape | M_CinematicSnow | M | Surface |  | 2026-03-04 | 2026-03-16 | 0 |  |
| Seasons | M_SnowFlake | M | Surface | ✓ | 2023-06-20 | 2023-06-20 | 1 | MI: MI_SnowFlake |
| Seasons+Shape | M_SnowFlake_V2 | M | Surface | ✓ | 2023-06-20 | 2023-06-20 | 1 | MI: MI_SnowFlake_V2 |

## Materials/Animation

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
|  | M_ECG | M | Surface | ✓ | 2026-01-05 | 2026-01-05 | 1 | MI: MI_ECG |
|  | M_Glitch | M | Surface | ✓ | 2026-01-05 | 2026-01-05 | 0 |  |
|  | M_Pulse | M | Surface | ✓ | 2026-01-05 | 2026-01-05 | 0 |  |
|  | M_Pulse_Animation | M | Surface | ✓ | 2024-03-24 | 2024-03-24 | 0 |  |
|  | M_Rainbow_Sample | M | Surface | ✓ | 2024-03-24 | 2024-03-24 | 0 |  |
|  | M_Rainbow_Wave | M | Surface | ✓ | 2026-01-05 | 2026-01-05 | 0 |  |
|  | M_Rect_Animation | M | Surface | ✓ | 2024-03-24 | 2024-03-24 | 0 |  |
|  | M_Rect_Transtition | M | Surface |  | 2025-08-16 | 2026-01-05 | 1 | MI: MI_Rect_Transtition |
|  | M_Simple_Wave | M | Surface |  | 2024-07-12 | 2026-01-05 | 0 |  |
|  | M_Sine_Wave | M | Surface | ✓ | 2026-01-05 | 2026-01-05 | 0 |  |
|  | M_SpeedLine | M | Surface | ✓ | 2026-01-05 | 2026-01-05 | 1 | MI: MI_SpeedLine |
|  | M_Spiral | M | Surface | ✓ | 2026-01-05 | 2026-01-05 | 1 | MI: MI_Spiral |
|  | M_Star_Trail | M | Surface | ✓ | 2026-01-05 | 2026-01-08 | 0 |  |
|  | M_Swirl_Transition | M | Surface |  | 2025-11-09 | 2026-01-05 | 2 | MI: MI_Swirl_Transition, MI_Swirl_Transition_V2 |
|  | M_Triangle | M | Surface |  | 2025-12-20 | 2026-08-23 | 0 |  |
|  | M_Triangle1 | M | Surface |  | 2025-12-20 | 2026-01-05 | 0 |  |
|  | M_Triangle_Animation | M | Surface | ✓ | 2024-03-24 | 2024-03-24 | 1 | MI: MI_Triangle_Animation |
|  | M_Triangle_Animation_2 | M | Surface |  | 2024-03-24 | 2024-03-24 | 0 |  |
|  | M_Triangle_Animation_3 | M | Surface |  | 2024-03-24 | 2024-03-24 | 0 |  |
|  | M_Tunnel | M | Surface | ✓ | 2026-01-05 | 2026-01-05 | 0 |  |
|  | M_TunnelV2 | M | Surface |  | 2026-07-20 | 2026-08-03 | 0 |  |

## Materials/Hex

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
|  | M_HexTiling | M | Surface | ✓ | 2025-07-11 | 2025-07-11 | 1 | MI: MI_HexTiling |
|  | M_HexTiling_V3 | M | Surface | ✓ | 2023-08-13 | 2023-08-13 | 1 | MI: MI_HexTiling_V3 |
|  | M_Hex_Animation | M | Surface | ✓ | 2023-08-13 | 2023-08-13 | 0 |  |
|  | M_Hex_Animation_V3 | M | Surface | ✓ | 2023-08-13 | 2023-08-13 | 0 |  |
|  | M_Hex_Animation_V4 | M | Surface | ✓ | 2023-08-13 | 2026-05-18 | 0 |  |
|  | M_Hex_Animatoin_V2 | M | Surface | ✓ | 2023-08-13 | 2023-08-13 | 0 |  |
|  | M_Hex_Dissolve | M | Surface | ✓ | 2025-07-11 | 2026-05-18 | 0 |  |
|  | M_Hex_V2 | M | Surface | ✓ | 2023-08-13 | 2023-08-13 | 1 | MI: MI_Hex_V2 |

## Materials/Bonus

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
|  | M_TriangleTiling | M | Surface |  | 2022-04-29 | 2026-01-05 | 1 | MI: MI_TriangleTiling |

## Materials/Bonus/Other

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
|  | M_Hex_Learning | M | Surface | ✓ | 2022-11-07 | 2022-12-25 | 0 |  |
|  | M_Triangle_Motion | M | Surface | ✓ | 2022-12-11 | 2022-12-25 | 0 |  |

## Materials/Bonus/Dissolve

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
|  | M_Hex_Tiling_Dissolve | M | Surface | ✓ | 2022-09-16 | 2022-12-25 | 1 | MI: MI_Hex_Tiling_Dissolve |
|  | M_Rect_Dissolve | M | Surface | ✓ | 2022-10-24 | 2023-08-13 | 0 |  |
|  | M_Rect_Dissolve_V2 | M | Surface | ✓ | 2022-10-31 | 2026-06-11 | 0 |  |
|  | M_Rect_Dissolve_V3 | M | Surface | ✓ | 2022-11-26 | 2022-12-25 | 0 |  |
|  | M_Rect_Dissolve_V4 | M | Surface |  | 2026-06-11 | 2026-06-13 | 0 |  |
|  | M_Rect_Dissolve_V5 | M | Surface |  | 2026-06-12 | 2026-06-13 | 0 |  |
|  | M_Rect_Dissolve_V6 | M | Surface |  | 2026-06-13 | 2026-06-13 | 0 |  |
|  | M_Soft_Rectangle_Dissolve | M | Surface | ✓ | 2022-11-13 | 2022-12-25 | 0 |  |
|  | M_Transition_Square | M | Surface | ✓ | 2022-09-24 | 2025-03-15 | 1 | MI: MI_Transition_Square |
|  | M_Triangle_Dissolve_V2 | M | Surface | ✓ | 2022-11-20 | 2025-03-15 | 0 |  |
|  | M_Triangle_Dissolve_V3 | M | Surface | ✓ | 2022-12-03 | 2023-09-10 | 0 |  |
|  | M_Triangle_Tilling_Dissolve | M | Surface | ✓ | 2022-09-10 | 2022-12-25 | 1 | MI: MI_Triangle_Tilling_Dissolve |

## Materials/Bonus/Fade/Dot

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
|  | M_Dot_Fade | M | Surface | ✓ | 2022-08-04 | 2022-12-25 | 1 | MI: MI_Dot_Fade |

## Materials/Bonus/Fade/Hex

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
|  | M_Hex_Fade1 | M | Surface | ✓ | 2022-08-04 | 2022-12-25 | 1 | MI: MI_Hex_Fade |
|  | M_Hex_Fade2 | M | Surface | ✓ | 2022-08-04 | 2022-12-25 | 0 |  |
|  | M_Hex_Fade_V3 | M | Surface | ✓ | 2022-12-31 | 2023-08-13 | 0 |  |
|  | M_Hex_Random_Fade | M | Surface |  | 2022-08-19 | 2022-12-25 | 1 | MI: MI_Hex_Random_Fade |
|  | M_Hex_Random_Noise | M | Surface | ✓ | 2022-10-02 | 2023-08-13 | 1 | MI: MI_Hex_Random_Noise |
|  | M_Hex_Tiling_Fade_V2 | M | Surface |  | 2022-10-19 | 2022-12-25 | 0 |  |

## Materials/Transition

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
|  | M_Burn_Transition | M | Surface |  | 2025-04-19 | 2025-07-11 | 0 |  |
|  | M_Flip_Transition | M | Surface | ✓ | 2024-06-29 | 2024-06-29 | 0 |  |
|  | M_HalfTone_V2 | M | Surface |  | 2025-03-15 | 2026-01-05 | 0 |  |
|  | M_Halftone_Transition_V2 | M | Surface |  | 2023-01-15 | 2026-01-05 | 1 | MI: MI_Halftone_Transition |
|  | M_Page_Curl | M | Surface | ✓ | 2026-01-05 | 2026-01-05 | 0 |  |
|  | M_Rectangle_Transition | M | Surface |  | 2024-03-24 | 2024-03-24 | 0 |  |
|  | M_Transition_Ripple | M | Surface | ✓ | 2024-02-25 | 2024-02-25 | 0 |  |
|  | M_Transition_V6 | M | Surface | ✓ | 2024-02-25 | 2026-01-20 | 0 |  |
|  | M_Transition_Warp | M | Surface | ✓ | 2024-02-25 | 2024-02-25 | 0 |  |
|  | M_Transition_Wave | M | Surface | ✓ | 2024-02-25 | 2024-02-25 | 0 |  |
|  | M_Zoom_Blur_Transition | M | Surface | ✓ | 2025-07-11 | 2025-07-11 | 0 |  |

## Materials/Transition/Transition_Export

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
|  | M_Transition_Distortion | M | Surface |  | 2024-02-25 | 2024-02-25 | 0 |  |

## Materials/PostProcess

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
|  | M_Half_Tone_Transition | M | PostProcess |  | 2025-03-15 | 2026-09-19 | 0 |  |
|  | M_PP_SpiralWipe | PP | PostProcess |  | 2026-08-03 | 2026-09-19 | 1 | MI: MI_PP_SpiralWipe |
|  | M_SwordSlash | M | PostProcess |  | 2026-08-23 | 2026-08-23 | 0 |  |
|  | PP_Burn_Transition | PP | PostProcess | ✓ | 2025-07-11 | 2025-07-11 | 1 | MI: PPI_Burn_Transition |
|  | PP_Burn_Transition_V2 | PP | PostProcess |  | 2026-04-06 | 2026-09-19 | 1 | MI: PPI_Burn_Transition_V2 |
|  | PP_Flip_Transition | PP | PostProcess | ✓ | 2026-01-20 | 2026-06-13 | 3 | ⚠重複 / MI: PPI_Flip_Transition, PPI_Flip_Transition, PPI_Flip_Transition_V2 |
|  | PP_Glitch | PP | PostProcess |  | 2024-01-27 | 2024-01-27 | 0 |  |
|  | PP_HalfTone | PP | PostProcess |  | 2025-08-30 | 2026-01-05 | 1 | MI: PPI_HalfTone |
|  | PP_Half_Tone | PP | PostProcess | ✓ | 2025-06-28 | 2026-01-05 | 0 |  |
|  | PP_Halftone_Color | PP | PostProcess |  | 2026-04-06 | 2026-04-06 | 0 | ⚠重複 |
|  | PP_Hex_Fade | PP | PostProcess |  | 2026-01-15 | 2026-09-19 | 0 |  |
|  | PP_Hex_Transition | PP | PostProcess |  | 2026-02-02 | 2026-05-18 | 1 | ⚠重複 / MI: PPI_Hex_Transition |
|  | PP_Hex_Transition_V2 | PP | PostProcess |  | 2026-05-18 | 2026-09-19 | 0 |  |
|  | PP_Hypnosis_Transition | PP | PostProcess |  | 2025-06-28 | 2026-09-19 | 0 |  |
|  | PP_NVG | PP | PostProcess | ✓ | 2026-01-05 | 2026-01-05 | 1 | MI: PPI_NVG |
|  | PP_NVG_V2 | PP | PostProcess |  | 2026-06-16 | 2026-07-05 | 1 | MI: PPI_NVG_V2 |
|  | PP_Old_TV | PP | PostProcess | ✓ | 2025-07-11 | 2026-01-05 | 1 | MI: PPI_Old_TV |
|  | PP_PageCurl | PP | PostProcess | ✓ | 2026-01-05 | 2026-05-18 | 1 | MI: PPI_PageCurl |
|  | PP_Rect_Dissolve | PP | PostProcess |  | 2026-01-05 | 2026-01-05 | 0 |  |
|  | PP_Rect_Transition | PP | PostProcess |  | 2025-12-30 | 2026-05-29 | 0 |  |
|  | PP_ScanLine | PP | PostProcess | ✓ | 2026-03-16 | 2026-03-16 | 0 | ⚠重複 |
|  | PP_Scanning_System | PP | PostProcess |  | 2026-01-05 | 2026-01-05 | 0 |  |
|  | PP_SliceTransition | PP | PostProcess |  | 2026-08-03 | 2026-09-19 | 1 | MI: MI_PP_SliceTransition |
|  | PP_Slice_Transition | PP | PostProcess | ✓ | 2024-11-24 | 2026-05-18 | 0 |  |
|  | PP_SpeedLine | PP | PostProcess |  | 2026-03-16 | 2026-03-16 | 0 |  |
|  | PP_SumiE_Param | PP | PostProcess |  | 2026-07-20 | 2026-09-19 | 0 |  |
|  | PP_Transition | PP | PostProcess |  | 2026-02-02 | 2026-02-02 | 0 |  |
|  | PP_Transition_Ripple | PP | PostProcess | ✓ | 2025-05-24 | 2026-09-19 | 1 | MI: PPI_Transition_Ripple |
|  | PP_Transition_Warp | PP | PostProcess |  | 2026-02-02 | 2026-03-16 | 1 | MI: PPI_Transition_Warp |
|  | PP_Transition_Warp_V2 | PP | PostProcess |  | 2026-02-02 | 2026-09-19 | 0 |  |
|  | PP_Transtion_Flip_V2 | PP | PostProcess | ✓ | 2026-03-16 | 2026-03-16 | 1 | ⚠重複 / MI: PPI_Transtion_Flip_V2 |
|  | PP_Triangle_Transition | PP | PostProcess |  | 2026-02-02 | 2026-02-02 | 1 | MI: PPI_Triangle_Transition |
|  | PP_Triangle_Transition_V2 | PP | PostProcess |  | 2026-05-29 | 2026-05-29 | 0 |  |
|  | PP_VHS_V1 | PP | PostProcess |  | 2024-12-28 | 2026-01-09 | 1 | MI: PPI_VHS |
|  | PP_VHS_V2 | PP | PostProcess |  | 2026-01-09 | 2026-01-09 | 1 | MI: PPI_VHS_V2 |
|  | PP_VortexDrainTransition | PP | PostProcess |  | 2026-07-14 | 2026-09-19 | 1 | MI: MI_PP_VortexDrainTransition |

## Materials/PostProcess/MaterialFunctions/VHS

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
|  | PP_VHSV3 | PP | PostProcess |  | 2026-06-21 | 2026-07-05 | 0 |  |

## Materials

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
|  | M_Warp_Effect | M | Surface |  | 2023-05-21 | 2026-01-22 | 1 | ⚠重複 / MI: MI_Warp_Effect |
|  | PP_Flip_Transition | PP | PostProcess |  | 2026-02-02 | 2026-02-02 | 3 | ⚠重複 / MI: PPI_Flip_Transition, PPI_Flip_Transition, PPI_Flip_Transition_V2 |
|  | PP_ScanLine | PP | PostProcess |  | 2026-03-16 | 2026-03-16 | 0 | ⚠重複 |
|  | PP_Transtion_Flip_V2 | PP | PostProcess |  | 2026-02-02 | 2026-03-16 | 1 | ⚠重複 / MI: PPI_Transtion_Flip_V2 |

## Materials/SF

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
|  | M_Sci-fi_Circle | M | Surface |  | 2023-08-20 | 2023-08-20 | 1 | MI: MI_Sci-fi_Circle |
|  | M_Sci-fi_Ring | M | Surface | ✓ | 2023-08-20 | 2023-08-20 | 1 | MI: MI_Sci-fi_Ring |
|  | M_Sci-fi_Tunnel | M | Surface |  | 2023-08-20 | 2023-08-20 | 1 | MI: MI_Sci-fi_Tunnel |
|  | M_Warp_Effect | M | Surface | ✓ | 2023-08-20 | 2023-08-20 | 1 | ⚠重複 / MI: MI_Warp_Effect |
|  | M_Warp_Effect_UI | M | UI |  | 2026-05-18 | 2026-05-18 | 0 |  |
|  | PP_Hex_Transition | PP | PostProcess |  | 2026-01-15 | 2026-05-18 | 1 | ⚠重複 / MI: PPI_Hex_Transition |

## Materials/Warp

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
|  | M_Warp_Effect2 | M | Surface |  | 2023-09-10 | 2025-07-11 | 0 |  |
|  | M_Warp_Effect3 | M | Surface |  | 2025-01-04 | 2025-07-11 | 0 |  |

## Materials/Flare

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
|  | M_Flare | M | Surface | ✓ | 2023-08-20 | 2023-08-20 | 0 |  |
|  | M_Flare_V2 | M | Surface | ✓ | 2023-08-20 | 2023-08-20 | 0 |  |

## Materials/Caustics

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
|  | M_Caustic | M | Surface |  | 2025-07-26 | 2025-07-26 | 1 | MI: MI_Caustic |

## Materials/Ui

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
|  | M_2DLemon | M | UI |  | 2026-08-06 | 2026-08-23 | 0 |  |
|  | M_2D_Liquid | M | Surface | ✓ | 2024-07-13 | 2024-07-13 | 0 |  |
|  | M_7Seg | M | Surface | ✓ | 2026-01-05 | 2026-08-23 | 1 | MI: MI_7Seg |
|  | M_Checker | M | Surface | ✓ | 2026-01-05 | 2026-01-05 | 1 | MI: MI_Checker |
|  | M_Checker2 | M | Surface | ✓ | 2026-01-05 | 2026-01-05 | 1 | MI: MI_Checker2 |
|  | M_CircleGauge | M | Surface | ✓ | 2024-07-13 | 2024-07-13 | 1 | MI: MI_CircleGauge |
|  | M_Loading_Icon_UI | M | UI |  | 2026-03-16 | 2026-03-16 | 0 |  |
|  | M_Loading_Icon_V2 | M | Surface |  | 2026-03-16 | 2026-03-16 | 0 |  |
|  | M_Loading_Icon_V3 | M | UI |  | 2026-02-27 | 2026-05-18 | 1 | MI: MI_Loading_Icon_V3 |
|  | M_Loading_Icon_V4 | M | UI |  | 2026-03-16 | 2026-03-16 | 0 |  |
|  | M_OutLine_V2 | M | Surface |  | 2025-12-20 | 2026-01-05 | 0 |  |
|  | M_Outline | M | Surface |  | 2025-12-13 | 2026-01-05 | 1 | MI: MI_Outline |
|  | M_Potion | M | Surface |  | 2025-12-30 | 2026-01-05 | 1 | MI: MI_Posion |
|  | M_Rader_Chart | M | UI |  | 2024-12-21 | 2024-12-21 | 1 | MI: MI_Rader_Chart |
|  | M_Rader_Chart_BG | M | UI |  | 2024-12-21 | 2024-12-21 | 0 |  |
|  | M_Rader_Chart_Core | M | UI |  | 2024-12-21 | 2024-12-21 | 0 |  |
|  | M_UI_Battery1 | M | UI |  | 2026-04-13 | 2026-04-16 | 0 |  |
|  | M_UI_ZZZ_HP_Gauge | M | Surface |  | 2024-07-13 | 2026-07-05 | 1 | MI: MI_UI_ZZZ_HP_Gauge |

## Export

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
|  | M_14Seg | M | Surface |  | 2026-08-26 | 2026-08-26 | 0 |  |

## Materials/Export

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
|  | PP_Halftone_Color | PP | PostProcess |  | 2026-04-06 | 2026-04-06 | 0 | ⚠重複 |

## WIP

| 採用 | 名前 | 種別 | ドメイン | 旧 | 追加 | 更新 | MI | 備考 |
|:--:|---|:--:|:--:|:--:|---|---|:--:|---|
|  | M_BreakGlassTransition | M | PostProcess |  | 2026-07-05 | 2026-07-05 | 1 | MI: MI_BreakGlassTransition |
