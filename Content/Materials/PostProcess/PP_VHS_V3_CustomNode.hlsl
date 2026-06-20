// =============================================================================
//  PP_VHS_V3 : all-in-one Post Process Custom node (reference implementation)
// =============================================================================
//  仕様書 PP_VHS_V3「§3 main 背骨 / §5 MF / §6 インライン変調 / §9 パラメータ」を
//  1 つの Custom ノードに統合した、そのまま動く版。
//  → エディタでこれを Custom ノード 1 個に貼り、出力を Emissive Color へ。
//    （MF 分解版を組む前に「まず動かす」ための骨格。各ブロックは §2.1 の MF へ
//     そのまま切り出せるよう、関数 vhs_* に分離してある）
//
//  --- マテリアル設定 -------------------------------------------------------
//    Material Domain      : Post Process
//    Output Type (Custom) : CMOT Float3
//    接続先               : Custom 出力 → Emissive Color
//
//  --- Custom ノードの入力ピン ----------------------------------------------
//    UV   (float2) : ViewportUV(ScreenPosition の ViewportUV) または TexCoord[0]
//    Time (float) : Time ノード
//    ※ §9 のパラメータは下の #define 既定値。MI から触る場合は
//      ScalarParameter / StaticSwitchParameter に置き換えて入力ピン化する。
//
//  --- 入力サンプリング -----------------------------------------------------
//    PostProcessInput0 は SceneTextureLookup(uv, 14, false) で直接読む
//    （14 = PPI_PostProcessInput0）。別途 SceneTexture ノードは不要。
//
//  --- 既存アセットとの差分メモ --------------------------------------------
//    * 仕様書 §2.1 は本編 MF を MF_Spike と表記。リポジトリ既存は MF_SpikeNoise。
//      → V3 で MF 化する際は名称を MF_Spike に統一するか、既存名を流用するか要決定。
//    * Grain/Scanline/Blink/Vignette/Dirty/Bezel は V3 では「インライン」(§2.2)。
//      VHS フォルダに同名 MF が既にあるが、V3 本編では main 直書きが仕様。
// =============================================================================

// ---- §9 パラメータ（既定値。MI 化する場合は入力ピンへ昇格）----------------
#define TimeQuantFreq    11.0
#define CurveBend        1.2
#define CurveShrink      1.15
#define CurveAspectX     5.0
#define CurveAspectY     4.0
#define GrainCut         0.7
#define GrainAmount      0.05
#define RollGain         14.0
#define RollMax          2.0
#define RollSpeed        2.0
#define StripCut         0.5
#define StripBandFloor   0.9
#define StripAmount      0.03
#define ChromaCut        0.85
#define ChromaOffset     0.05
#define DecolorAmount    0.95
#define ColorGamma       1.5
#define ColorGammaGBias  0.1
#define ScanDensityDiv   2.7
#define ScanDepth        0.25
#define BlinkSpeed       100.0
#define BlinkDepth       0.04
#define VigGain          44.0
#define VigMix           0.4
#define VigFlicker       0.7
#define DirtyAmount      0.2
#define BezelColorV      float3(0.4, 0.4, 0.4)

// ---- ヘルパー（① 基盤）----------------------------------------------------
float vhs_hash1d(float n)   { return frac(sin(n) * 43758.5453123); }
float vhs_hash2d(float2 co) { return frac(sin(dot(co, float2(12.9898, 78.233))) * 43758.5453); }
float vhs_vnoise1d(float p) { float fl = floor(p); return lerp(vhs_hash1d(fl), vhs_hash1d(fl + 1.0), frac(p)); }
float vhs_snoise1d(float p) { return vhs_vnoise1d(p) * 2.0 - 1.0; }

// MF_Spike : 符号付き間欠スパイク（cut を上げるほど発火が疎）
float vhs_spike(float v, float cut)
{
    float s = clamp(abs(v) - cut, 0.0, 1.0);
    s = sign(v) * s;
    return s * (1.0 / (1.0 - cut));
}

// MF_ColorGrade : 平均値脱色 + チャンネル別ガンマ（G だけ弱め＝暖色寄り）
float3 vhs_grade(float3 c)
{
    float bw = (c.r + c.g + c.b) / 3.0;        // 既定=平均。Rec.709版は dot(c, float3(0.2126,0.7152,0.0722))
    c = lerp(c, bw.xxx, DecolorAmount);
    c.r = pow(c.r, ColorGamma);
    c.g = pow(c.g, ColorGamma - ColorGammaGBias);
    c.b = pow(c.b, ColorGamma);
    return c;
}

// 入力サンプル（PostProcessInput0）
float3 vhs_sample(float2 uv) { return SceneTextureLookup(uv, 14, false).rgb; }

// =============================================================================
//  main 背骨（§3）
// =============================================================================

// 段1: コマ送り時刻 QuantT = floor(Time * Freq)
float QuantT = floor(Time * TimeQuantFreq);

// 段2: MF_CRTCurve（中心化 → 多項式バレル → 戻し）
float2 cu = (UV - 0.5) * 2.0;                  // [-1,1]
cu *= CurveBend;
cu.x *= 1.0 + pow(abs(cu.y) / CurveAspectX, 2.0);
cu.y *= 1.0 + pow(abs(cu.x) / CurveAspectY, 2.0);
cu /= CurveShrink;
float2 PP_UV = cu * 0.5 + 0.5;                 // [0,1]

// 段3: StableUV 退避（vig/bezel 専用。横揺れ・ロールに追従させない）
float2 StableUV = PP_UV;

// 段4: GrainOffset（inline・PP_UV を微小に揺らす）
float xn = vhs_spike(vhs_snoise1d(Time * 10.0),          GrainCut) * GrainAmount;
float yn = vhs_spike(vhs_snoise1d((500.0 + Time) * 10.0), GrainCut) * GrainAmount;
float gr = vhs_hash2d(PP_UV + (QuantT + 100.0) * 0.01);
float2 UV_g = PP_UV + float2(xn, yn) * gr;

// 段5: MF_YRoll（clamp下限0＝間欠故障 → frac でラップ）
float rn = clamp(vhs_vnoise1d(200.0 + Time * RollSpeed) * RollGain, 0.0, RollMax);
float2 UV_y = UV_g;
UV_y.y = frac(UV_y.y + rn);

// 段6: MF_HStrip（sin 上位帯抽出 → frac ラップ）
float vn = vhs_snoise1d(Time * 6.0);
float hn = vhs_spike(vhs_snoise1d(Time * 10.0), StripCut);
float lineV = (sin(UV_y.y * 10.0 + vn) + 1.0) * 0.5;
lineV = (clamp(lineV, StripBandFloor, 1.0) - StripBandFloor) * (1.0 / (1.0 - StripBandFloor));
float2 SampleUV = UV_y;
SampleUV.x = frac(SampleUV.x + lineV * StripAmount * hn);

// 段7: MF_ChromaAberr（R/G 横・B 縦の3点 + per-ch スパイク、各サンプルに ColorGrade）
float nR = vhs_spike(vhs_snoise1d(Time * 10.0),           ChromaCut);
float nG = vhs_spike(vhs_snoise1d(2000.0 + Time * 10.0),  ChromaCut);
float nB = vhs_spike(vhs_snoise1d(3000.0 + Time * 10.0),  ChromaCut);
float r = vhs_grade(vhs_sample(SampleUV + float2(nR * ChromaOffset, 0))).r;
float g = vhs_grade(vhs_sample(SampleUV + float2(nG * ChromaOffset, 0))).g;
float b = vhs_grade(vhs_sample(SampleUV + float2(0, nB * ChromaOffset))).b;   // ★ B だけ縦
float3 color = float3(r, g, b);

// 段8: Scanline（解像度ロック走査線）
float resY = View.ViewSizeAndInvSize.y;
float scan = (sin(SampleUV.y * 3.1415 * resY / ScanDensityDiv) + 1.0) * 0.5;
color *= (1.0 - ScanDepth) + scan * ScanDepth;

// 段9: Blink（高速ブリンク）
color *= (1.0 - BlinkDepth) + BlinkDepth * (sin(Time * BlinkSpeed) + 1.0) * 0.5;

// 段10: Vignette（放物線・StableUV を使う）
float vig = VigGain * (StableUV.x * (1.0 - StableUV.x) * StableUV.y * (1.0 - StableUV.y));
vig *= lerp(VigFlicker, 1.0, vhs_hash1d(QuantT + 0.5));
color *= (1.0 - VigMix) + VigMix * vig;

// 段11: DirtyNoise（全画面ダート）
color *= 1.0 + vhs_hash2d(SampleUV + QuantT * 0.01) * DirtyAmount;

// 段12: MF_BezelMask（[0,1] 外＝画面外を背景色に）
if (StableUV.x < 0.0 || StableUV.x > 1.0 || StableUV.y < 0.0 || StableUV.y > 1.0)
    color = BezelColorV;

return color;
