[English](README.md)

# ProceduralDrawingMaterialSamples

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Repo Size](https://img.shields.io/github/repo-size/EmbarrassingMoment/ProceduralDrawingMaterialSamples)
[![Sponsor](https://img.shields.io/badge/Sponsor-EmbarrassingMoment-ff69b4?logo=github-sponsors&logoColor=white)](https://github.com/sponsors/EmbarrassingMoment)

## 概要

このリポジトリは、Unreal Engine 5 (UE5)で作成した、テクスチャを使用せずに図形を描画するマテリアルおよびマテリアル関数のコレクションです。
このプロジェクトは、Unreal Engineコミュニティにおける個人開発者を支援することも目的としています
[LICENSE](LICENSE)ファイルの内容に反しない限り、ご自由にご利用いただけます。

## 特徴

* **図形にテクスチャ不要:** 図形や模様はすべてマテリアル内の計算で描画しています。テクスチャを使うのは、サンプルの入力(トランジションで切り替えるデバッグ画像、アウトライン効果に使う星の画像)と、7セグ・14セグ表示用の小さなルックアップテーブルだけです。
* **カスタマイズ可能:** パラメータを変更することで、色、形状、アニメーションを簡単に調整できます。多くのマテリアルには、バリエーションを示すマテリアルインスタンスが付いています。
* **3通りの使い方:** Surface のマテリアルはメッシュに、User Interface のマテリアルは UMG のウィジェットに、Post Process のマテリアルは画面全体に使えます。
* **豊富なサンプル:**
    * 図形・アイコン: 円、多角形、星、ハート、歯車、ハザードマーク、太極図
    * 季節のモチーフ: 桜、紅葉、イチョウ、雪の結晶、降雪
    * アニメーション: レーダー、心電図、波、トンネル、SF風のリング、ワープ
    * トランジション・ディゾルブ: 六角形・三角形・矩形のタイル、燃焼、ページめくり、波紋、渦
    * ポストプロセス: VHS、古いテレビ、グリッチ、暗視、ハーフトーン、墨絵、集中線、被ダメージのビネット
    * UI: ローディングアイコン、ゲージ、レーダーチャート、7セグ・14セグ表示、ポーション・液体

## Showcase

| Radar | Animation |
| :---: | :---: |
| ![Radar](gif/Rader.gif) | ![Animation](gif/Animation.gif) |
| **SnowFlake** | **Transition** |
| ![SnowFlake](gif/Snow.gif) | ![Transition](gif/Transition.gif) |
| **OldTV** | **Others** |
| ![OldTV](gif/OldTV.gif) | ![Others](gif/Samples.gif) |
| **PageCurl** | |
| ![PageCurl](gif/PageCurl.gif) | |

## Showcase レベル

`Content/Levels` にある次のレベルを開くと、マテリアルを並べて見比べられます。

| レベル | 内容 |
| --- | --- |
| `Showcase_Shape` | 図形、SDF の図形、アイコン、季節のモチーフ 27 件 |
| `Showcase_Seasons` | 春・秋・冬に分けた季節のモチーフ 7 件 |
| `Showcase_PostProcess` | ポストプロセス効果 27 件(1 件ずつブースに分けて展示) |
| `Showcase_UI_LoadingIcon` | UI 用のローディングアイコン 5 件 |
| `Showcase` | 初代のレベル。全マテリアルの約半数を配置 |

### Showcase_Shape

![Showcase_Shape](docs/images/Showcase_Shape.jpg)

### Showcase_Seasons

![Showcase_Seasons](docs/images/Showcase_Seasons.jpg)

### Showcase_PostProcess

ブースごとに範囲を区切った Post Process Volume があり、カメラがそのブースの中にいる間だけ効果がかかります。レベルを開くと最初のブースの正面にいるので、+X 方向へ移動するか、アウトライナーの `Cam_<マテリアル名>` カメラを Pilot してください。下の画像は 27 ブースのうち 9 件です。

![Showcase_PostProcess](docs/images/Showcase_PostProcess.jpg)

### Showcase_UI_LoadingIcon

アイコンはウィジェット(`Content/Widgets/WBP_Showcase_UI_LoadingIcon`)に並べてあり、実行時に画面へ追加されます。表示するには Play(PIE)を押してください。

![Showcase_UI_LoadingIcon](docs/images/Showcase_UI_LoadingIcon.png)

## マテリアル一覧

マテリアル 177 件、マテリアル関数 91 件、マテリアルインスタンス 85 件を収録しています。全件の一覧は [Material Catalog](docs/MaterialCatalog.md)(英語)にあり、各マテリアルのドメインと、展示している Showcase レベルも載せています。

| カテゴリ | 例 | 件数 |
| --- | --- | ---: |
| Shapes | 円、多角形、リング、角丸矩形、星、ハート、グリッド、太極図 | 24 |
| Icons | 星、桜、歯車、ハザードマーク、レーダー、ローディングアイコン | 9 |
| Seasons | 紅葉、イチョウ、雪の結晶、降雪 | 5 |
| Animation & Effects | 心電図、波、トンネル、渦巻き、六角形の模様、SF風のリング、ワープ、レンズフレア、コースティクス | 40 |
| Dissolve & Fade | 矩形・三角形・六角形のディゾルブ、ドット・六角形のフェード | 22 |
| Transitions | 燃焼、フリップ、ページめくり、波紋、ワープ、ズームブラー | 12 |
| Post Process | VHS、古いテレビ、グリッチ、暗視、ハーフトーン、墨絵、集中線、被ダメージのビネット、画面トランジション | 43 |
| UI | ローディングアイコン、ゲージ、レーダーチャート、7セグ・14セグ表示、ポーション、アウトライン | 21 |
| Work in Progress | 制作途中のもの | 1 |

## 再利用できるマテリアル関数

マテリアル関数は、ご自身のマテリアルから呼び出せる部品です。ほとんどは `Content/Materials/Function` にあります。主なもの:

| 関数 | 内容 |
| --- | --- |
| `MF_DrawCircle` / `MF_DrawCircle_AA` | 円(`_AA` は縁をアンチエイリアス) |
| `MF_DrawPolygon` / `MF_DrawPolygon_AA` | 辺の数を指定できる正多角形 |
| `MF_DrawRoundedRectangle` | 角丸矩形 |
| `MF_DrawRing` | リング |
| `MF_DrawStar` / `MF_DrawPentagram` | 星 |
| `MF_DrawHeart` | ハート |
| `MF_SDBox` / `MF_Capsule` | 符号付き距離関数による箱とカプセル |
| `MF_DrawHexTiling` / `MF_DrawTriangleTiling` | 六角形・三角形のタイル模様 |
| `MF_HalftoneDot` | ハーフトーンのドット模様 |
| `MF_N21` | 2 次元の入力から擬似乱数を返す |
| `MF_GLSLMod` | GLSL の `mod`(`x - y * floor(x / y)`)。負の値で HLSL の `fmod` と結果が異なる |
| `MF_SmoothMin` / `MF_SmoothMax` | 距離場をなめらかにつなぐ最小値・最大値 |
| `MF_EaseOutExpo` / `MF_SmootherStep` | アニメーション用のイージングカーブ |
| `MF_PingPong` | 往復する値 |
| `MF_Posterize` | 値を指定した段数に丸める |

`Content/Materials/PostProcess/MaterialFunctions/VHS` には、ブラウン管の歪み、色収差、走査線、ビネット、ノイズなど、レトロな画面効果用の関数がさらに 18 件あります。

## 動作環境

* Unreal Engine 5.8 以降
    * アセットは 5.8 で保存しているため、それより前のバージョンでは開けません。

## 導入方法

1.  このリポジトリをクローンまたはダウンロードします。
2.  ご自身のプロジェクトの`Content`フォルダに、このリポジトリの`Content`フォルダの中身をコピーします。

## ライセンス

このプロジェクトは[MIT License](LICENSE)の下で公開されています。

## 謝辞 (順不同)

このプロジェクトの制作にあたり、以下のWebサイトやリソースを参考にさせていただきました。心より感謝申し上げます。

* [シェーダーだけで円を描く - テラシュールブログ](https://karanokan.info/2019/03/31/post-2465/)
* [Rounded Rectangle Node - Unity Documentation](https://docs.unity3d.com/Packages/com.unity.shadergraph@6.9/manual/Rounded-Rectangle-Node.html)
* [Unityシェーダーお絵描き入門 - Scrapbox](https://scrapbox.io/Porin-Room/Unity%E3%82%B7%E3%82%A7%E3%83%BC%E3%83%80%E3%83%BC%E3%81%8A%E7%B5%B5%E6%8F%8F%E3%81%8D%E5%85%A5%E9%96%80)
* [shadertoy](https://www.shadertoy.com/)
    * [MlySzw](https://www.shadertoy.com/view/MlySzw)
    * [MlBBWt](https://www.shadertoy.com/view/MlBBWt)
    * [WdVfzt](https://www.shadertoy.com/view/WdVfzt)
    * [4tGfWy](https://shadertoy.com/view/4tGfWy)
* [Eiliram's ArtStation](https://eiliram.artstation.com/projects/KaDLKR)
* [【ShaderGraph】グリッド状に分割して、中央から広がる三角形エフェクト - Zenn](https://zenn.dev/r_ngtm/books/shadergraph-cookbook/viewer/recipe-triangle-effect)
* [UE4マテリアルだけで作る図形 - Qiita](https://qiita.com/edo_m18/items/37d8773a5295bc6aba3d)
* [cmzw_ on Twitter](https://twitter.com/cmzw_)
* [【UE5】マテリアルで矢印を作る - Renard's Blog](https://renard-blog.netlify.app/2023/05/25/_25/)
* [2D Distance Functions - Iñigo Quilez](https://iquilezles.org/articles/distfunctions2d/)

### 使用テクスチャ

* [Debug Textures for VFX - Real Time VFX](https://realtimevfx.com/t/debug-textures-for-vfx/7510)
