# VHS PostProcess Material Functions - 実装準備調査

## 対象パス

`/Game/Materials/PostProcess/MaterialFunctions/VHS/`

## 参照シェーダー

ShaderToy ベースの VHS エフェクト GLSL コード（下記クレジット）

- https://www.shadertoy.com/view/ldXGW4 by ehj1
- https://www.shadertoy.com/view/XtK3W3 by dyvoid
- https://www.shadertoy.com/view/Xdl3D8 by jmpep
- https://www.shadertoy.com/view/ldjGzV by ryk

---

## MF 一覧と GLSL 対応

### エフェクト系 MF

| MF 名 | 対応 GLSL 要素 | `#define` フラグ |
|---|---|---|
| MF_CRTCurve | `uv_curve()` — バレル歪み | `CURVE` |
| MF_Scanline | `scanA` / `scanB` による輝度変調 | `SCANS` |
| MF_ChromaAberr | `ghost()` — RGB チャンネル個別 UV シフト | `FLICKS` |
| MF_GrainOffset | `rand2d` によるランダム UV オフセット | `GRAINS` |
| MF_YRoll | `uv_ybug()` — Y 方向ロールノイズ | `YBUG` |
| MF_DirtyNoise | `rand2d * 0.2` による輝度ノイズ乗算 | `DIRTY` |
| MF_HStrip | `uv_hstrip()` — 水平ストリップ歪み | `STRIP` |
| MF_Decolor | `mix(color, vec3(bw), 0.95)` — 脱色 | `COLOR` |
| MF_ColorGrade | `pow(r/g/b, p)` — ガンマ補正 | `COLOR` |
| MF_Blink | `sin(iTime*100.)` による輝度フリッカー | `BLINK` |
| MF_Vignette | `44.0 * uv.x*(1-uv.x)*uv.y*(1-uv.y)` | `VIG` |
| MF_BezelMask | UV 範囲外 (`< 0` or `> 1`) のバックカラー処理 | — |

### ユーティリティ系 MF

| MF 名 | 対応 GLSL 関数 | 説明 |
|---|---|---|
| MF_Hash2D | `rand2d(vec2)` | 2D → [0,1] ハッシュ |
| MF_Hash1D | `rand(float)` | 1D → [0,1] ハッシュ |
| MF_ValueNoise | `noise(float)` | 1D Value Noise（`rand` 補間） |
| MF_SNoise1D | `snoise(float)` | `noise` を [-1, 1] にリマップ（`map()` を内包） |
| MF_SpikeNoise | `threshold(float, float)` | カットオフ以下を 0 にクランプしスパイク化 |
| MF_TimeQuant | `float(int(iTime * FREQUENCY))` | 時間を整数ステップに量子化（FREQUENCY=11） |

---

## 未対応・省略可能な GLSL 要素

| 要素 | 判定 | 理由 |
|---|---|---|
| `map(val, amin, amax, bmin, bmax)` | **MF 不要** | `snoise` 内部でのみ使用する単純リマップ。MF_SNoise1D にインライン実装で対応 |
| `#define BLUR`（コード内に記述あり） | **MF 不要** | 元コードで `#define` されていないデッドコード |
| `iMouse` バイパス処理 | **省略** | ShaderToy 固有機能。PostProcess ドメインに相当物なし |

---

## ShaderToy → UE PostProcess 読み替え

| ShaderToy | UE PostProcess マテリアル |
|---|---|
| `iChannel0` | SceneTexture: PostProcessInput0 |
| `iTime` | Time ノード |
| `iResolution.xy` | ViewSize または `1 / SceneTexture Texel Size` |
| `fragCoord / iResolution` | SceneTexture UV（自動取得） |
| `texture(iChannel0, uv)` | SceneTexture ノード（UV 入力付き） |

---

## 結論

**実装準備完了。** 18 個の MF が全 `#define` エフェクトおよびすべてのヘルパー関数を網羅している。

唯一確認すべき点は `map()` 関数が **MF_SNoise1D 内部にインライン実装されているか**どうか。これが確認できれば、メインの PostProcess マテリアル（`PP_VHS_V2` 等）でこれら 18 MF を結線するだけで GLSL コードをほぼ忠実に再現できる。

### 関連アセット

- `PP_VHS_V1.uasset` / `PP_VHS_V2.uasset` — メイン PostProcess マテリアル
- `PPI_VHS.uasset` / `PPI_VHS_V2.uasset` — PostProcess マテリアルインスタンス
