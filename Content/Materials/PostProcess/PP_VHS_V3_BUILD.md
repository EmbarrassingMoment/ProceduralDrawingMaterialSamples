# PP_VHS_V3 構築ガイド（エディタ作業手順）

このリポジトリの `.uasset` はすべて Unreal Editor 上で作成・コミットされたバイナリ
パッケージ（UE 5.7）です。マテリアル本体 `PP_VHS_V3.uasset` のバイナリは
エディタのシリアライザでしか正しく生成できないため、ここでは**エディタで組むための
手順**と、即動かすための統合 HLSL（`PP_VHS_V3_CustomNode.hlsl`）を提供します。

---

## A. まず動かす（最速・推奨の初手）

1. `Content/Materials/PostProcess/` に Material を新規作成 → `PP_VHS_V3`。
2. Details で **Material Domain = Post Process**。
3. **Custom** ノードを 1 個置く → Output Type = **CMOT Float3**。
4. `PP_VHS_V3_CustomNode.hlsl` の中身を Custom ノードの Code に貼る。
5. Custom ノードに入力ピンを追加：
   - `UV`   ← ScreenPosition ノードの **ViewportUV**（または TexCoord[0]）
   - `Time` ← **Time** ノード
6. Custom 出力 → **Emissive Color**。
7. PostProcessVolume に割り当て（Blendables / Post Process Materials）or
   Global Post Process で確認。

これで §3〜§12 の全パイプラインが動きます（パラメータは HLSL 内 `#define` 既定）。

---

## B. MF 分解版（仕様書 §1〜§5 の到達点）に組み替える

`PP_VHS_V3_CustomNode.hlsl` の各 `vhs_*` 関数ブロックが、そのまま §2.1 の
本編 MF に対応します。既存の `Content/Materials/PostProcess/MaterialFunctions/VHS/`
の MF を呼ぶ形へ置換していく。

### 本編で呼ぶ MF（6本・§2.1）
| MF | 呼出 | 既存アセット | 備考 |
|---|---|---|---|
| `MF_Spike` | 5 | `MF_SpikeNoise` | ★名称差。V3 命名(§14)に合わせるなら MF_Spike にリネーム |
| `MF_ColorGrade` | 3 (CA内) | `MF_ColorGrade` | per-sample 適用 |
| `MF_CRTCurve` | 1 | `MF_CRTCurve` | |
| `MF_YRoll` | 1 | `MF_YRoll` | |
| `MF_HStrip` | 1 | `MF_HStrip` | |
| `MF_ChromaAberr` | 1 | `MF_ChromaAberr` | 内部で MF_ColorGrade×3 |

### インライン化する効果（§2.2・main 直書き、MF にしない）
GrainOffset / Scanline / Blink / Vignette / DirtyNoise / BezelMask
※ VHS フォルダに同名 MF が既存だが、V3 仕様では main インラインが正。
　既存 MF を流用してもよい（その場合 §2.1 と本数が変わる点だけ注意）。

### Named Reroute（§4・バス）
`RawUV` / `PP_UV` / `StableUV` / `SampleUV` / `QuantT` / `Chroma`
- **StableUV は Vignette / BezelMask のみが消費**（湾曲には追従・横揺れには非追従）。
- `QuantT = floor(Time × TimeQuantFreq)` を段1で1度計算し reroute 配布。

### main 背骨（§3）
```
ViewportUV → RawUV
  → MF_CRTCurve              → PP_UV
  → (reroute)                → StableUV
  → GrainOffset(inline)      → UV_g
  → MF_YRoll → MF_HStrip     → SampleUV
  → MF_ChromaAberr           → Chroma   (内部 MF_ColorGrade×3)
  → × Scanline(inline, SampleUV)
  → × Blink(inline, Time)
  → × Vignette(inline, StableUV)
  → × DirtyNoise(inline, SampleUV, QuantT)
  → MF_BezelMask(StableUV)   → Emissive Color
```

### 時間1Dノイズ（§7・唯一残す Custom）
空間ノイズは built-in（Noise/VectorNoise）へ委譲。`SNoise1D` だけ 1 行 Custom で残す。
roll/strip/CA の発火タイミングを駆動するため空間ノイズで代替不可。

---

## C. パラメータ集約（§9）と StaticSwitch

- `#define` を ScalarParameter に昇格し、グループ（Time/Curve/Grain/…）で整理。
- 各効果に `Use_Curve` / `Use_Scanline` … の StaticSwitchParameter を付け、
  GLSL の `#ifdef` を再現（講義の積み上げ実演＝材料機能）。
- `DecolorMode`（Average / Rec.709）の StaticSwitch を ColorGrade に用意（§8 対比教材）。

---

## D. 地雷回避（§13・流用時のチェック）
- V1: SliderMin=1.0 誤設定 / ColorNoiseSpeed 共有結合 / orphan ノード / `Alhpa` typo を持ち込まない。Frame 角丸box は本編不使用。
- V2: typo 全修正（`Distorded_*`→`Distorted_*` 等）。
- GLSL: BLUR 死枝・FLICKS 従属（色を CA から独立段に）・未使用変数は捨てる。

---

## 注記
`PP_VHS_V3.uasset`（マテリアル本体バイナリ）は本 CI 環境に Unreal Engine が無いため
自動生成できません。上記 A の手順で Custom ノードに HLSL を貼れば、エディタ保存時に
正規の `.uasset` が生成されます。
