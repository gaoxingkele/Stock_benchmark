# Lingxi10 / Lingxi5 SOTA Upgrade Survey

Date: 2026-06-23

This report extends the current 31-paper ARA finance benchmark with 2020+ cross-domain time-series methods. The goal is not to replace the Lingxi backbone blindly, but to identify method modules that can be engineered into continuous Lingxi10/Lingxi5 upgrade validation.

## Current Anchor

Current production/research stance:

1. **Lingxi10** remains the default practical strategy.
2. **Lingxi5** remains the high-conviction/aggressive research strategy.
3. Prior runner-up fusion with Qlib Alpha158 and FinTSB did not justify replacing Lingxi10. It only created conditional candidates in US Top5 and small neutral robustness experiments.
4. The 31-paper ARA pool is already complete at Level 1 and should remain the finance-method reference base.

## External SOTA Sources Reviewed

| Method | Venue/status | Core idea | Source |
|---|---|---|---|
| PatchTST | ICLR 2023 | Patch tokens plus channel independence for efficient long-context forecasting | https://arxiv.org/abs/2211.14730 |
| TimesNet | ICLR 2023 | Convert 1D series into 2D temporal variation patterns for general TS tasks | https://arxiv.org/abs/2210.02186 |
| iTransformer | ICLR 2024 Spotlight | Invert dimensions: attention over variate tokens, FFN over time representation | https://arxiv.org/abs/2310.06625 |
| TimeMixer | ICLR 2024 | Decomposable multiscale mixing with efficient MLP blocks | https://arxiv.org/abs/2405.14616 |
| TimeMixer++ | ICLR 2025 | Universal time-series pattern machine with multi-resolution time imaging | https://arxiv.org/abs/2410.16032 |
| Non-stationary Transformer | NeurIPS 2022 | Series stationarization plus de-stationary attention for shifted distributions | https://proceedings.neurips.cc/paper_files/paper/2022/hash/4054556fcaa934b0bf76da52cf4f92cb-Abstract-Conference.html |
| FEDformer | ICML 2022 | Seasonal-trend decomposition plus Fourier/Wavelet frequency blocks | https://proceedings.mlr.press/v162/zhou22g.html |
| N-HiTS | AAAI 2023 | Hierarchical interpolation and multi-rate sampling for efficient long horizon | https://ojs.aaai.org/index.php/AAAI/article/view/25854 |
| DLinear / LTSF-Linear | AAAI 2023 | Simple decomposition-linear baseline that challenges heavy Transformers | https://ojs.aaai.org/index.php/AAAI/article/view/26317 |
| TimesFM | ICML 2024 | Decoder-only time-series foundation model | https://research.google/blog/a-decoder-only-foundation-model-for-time-series-forecasting/ |
| Chronos | arXiv 2024 | Quantized time-series value tokens trained as language modeling | https://arxiv.org/abs/2403.07815 |
| Moirai | ICML 2024 Oral | Universal forecasting transformer with any-variate handling and probabilistic heads | https://arxiv.org/abs/2402.02592 |
| MOMENT | ICML 2024 | Open general-purpose TS foundation model for forecasting/classification/anomaly/imputation | https://arxiv.org/abs/2402.03885 |
| Tiny Time Mixer / TTM | NeurIPS 2024 | Compact pre-trained multivariate TS model with adaptive patching and exogenous support | https://openreview.net/forum?id=3O5YCEWETq |

## Claude CLI Review

Claude Code CLI was asked to rank the most useful method ideas for a stock Top10/Top5 cross-sectional strategy under practical constraints: no heavy GPU first, proxyable with OHLCV panels, point-in-time safe, and validated across China A-share, US, HK, and crypto.

Claude's returned ranking:

1. **iTransformer**: best structural match because cross-variate attention maps naturally to cross-stock/cross-factor ranking.
2. **Non-stationary Transformer**: most relevant robustness module for regime drift and return distribution shifts.
3. **PatchTST**: strong low-overfit per-stock forecasting backbone; useful as a dependable IC anchor.
4. **TimeMixer**: useful for short/long horizon momentum-reversal decomposition, but more as a complement.
5. **TTM**: attractive lightweight foundation baseline, but generic pretraining priors should not become the core ranker without evidence.
6. **DLinear**: indispensable sanity baseline; every neural upgrade must beat it after cost.

The practical synthesis is: lead with iTransformer-style cross-sectional/variate attention, harden it with Non-stationary-style normalization, validate against DLinear, and only then add patch/multiscale/foundation modules.

## Engineering Priority For Lingxi

| Priority | Upgrade name | Source methods | Why it fits Lingxi10/5 | First proxy implementation |
|---:|---|---|---|---|
| 1 | `Lingxi-VarAttn` | iTransformer | Lingxi10/5 are TopK ranking strategies, so cross-sectional interactions matter more than pure univariate forecasting | Per-date variate-token attention proxy over factor/stock embeddings; output residual alpha score |
| 2 | `Lingxi-PITNorm` | Non-stationary Transformer, RevIN-style logic | Prior Fusion failed when auxiliary signals were not regime-robust; stock alpha is non-stationary | Point-in-time rolling stationarization and de-stationary restoration features before ranking |
| 3 | `Lingxi-Patch` | PatchTST, TTM | Patch tokens reduce noise and overfit; fits OHLCV windows without heavy external data | Patch-level return/volume/range embeddings with shared ridge/light MLP scorer |
| 4 | `Lingxi-MScale` | TimeMixer, N-HiTS, FEDformer | Captures simultaneous reversal, medium-term momentum, and long-term trend/frequency components | Multi-scale decomposition features: 5/10/20/60/120 day trend, residual, Fourier energy, volatility |
| 5 | `Lingxi-TinyFM` | TTM, TimesFM, Chronos, Moirai, MOMENT | Useful only after lightweight local proxies prove value; direct foundation inference may be expensive or leakage-prone | Optional zero/few-shot feature source, never default until it beats Lingxi10/5 under PIT audit |
| 6 | `Lingxi-LinearGuard` | DLinear / LTSF-Linear | Prevents over-engineering; catches cases where simple decomposition is enough | Always-on benchmark: decomposition-linear score must be included in every upgrade comparison |

## What Not To Do

1. Do not make a fixed weighted average of external SOTA scores with Lingxi. The Qlib/FinTSB experiment already showed that fixed fusion can reduce A-share performance.
2. Do not start with large foundation models as the main strategy. They are useful for representation tests, but point-in-time contamination and domain mismatch risk are high.
3. Do not optimize only raw annual return. Lingxi5 already has high return; the upgrade must improve drawdown, neutral robustness, or capacity without destroying Sharpe.
4. Do not treat generic forecasting loss as equivalent to stock ranking. The real target is cost-adjusted Top10/Top5 spread and rank-IC stability.

## Next Validation Matrix

The next upgrade experiment should compare:

| Family | Methods |
|---|---|
| Current mainline | `lingxi`, Top10/Top5 |
| Linear guard | `lingxi_linear_guard`, `dlinear_proxy` |
| Normalization | `lingxi_pitnorm` |
| Cross-sectional attention proxy | `lingxi_varattn` |
| Patch proxy | `lingxi_patch` |
| Multiscale proxy | `lingxi_mscale` |
| Combined candidates | `lingxi_varattn_pitnorm`, `lingxi_patch_mscale`, `lingxi_sota_stack_gated` |

Required markets:

- China A-share CSI300
- US large cap
- HK large cap
- Crypto major, with Top30 skipped when universe size is only 20

Required portfolio settings:

- H5 label
- Top10 and Top5
- equal-weight long-only
- daily rebalance
- single-side 10 bps cost
- raw and industry/size neutral variants where industry/size metadata is meaningful

Required decision gates:

1. A candidate can replace Lingxi10 only if it improves average Sharpe or drawdown in at least 3 of 4 markets without hurting China A-share.
2. A candidate can replace Lingxi5 only if it improves drawdown or neutral Sharpe while keeping most of the return edge.
3. A candidate can become an experimental sleeve if it improves exactly one market/TopK cleanly, like the prior US Top5 Fusion-Regime case.
4. Every candidate must beat `Lingxi-LinearGuard`; otherwise the complexity is not justified.

## Recommended Next Step

Implement the next validation in this order:

1. `Lingxi-LinearGuard`: DLinear-style decomposition baseline.
2. `Lingxi-PITNorm`: point-in-time rolling normalization/de-stationarization.
3. `Lingxi-MScale`: multiscale decomposition features.
4. `Lingxi-VarAttn`: cross-sectional variate-attention proxy.
5. `Lingxi-Patch`: patch-token feature proxy.
6. `Lingxi-SOTA-Stack-Gated`: online gate over only the modules that individually pass.

This order is deliberately conservative. It tests cheap, interpretable modules first and reserves heavier model ideas for cases where the proxy signal already proves value.

