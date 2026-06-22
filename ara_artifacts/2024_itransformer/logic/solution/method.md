# Method Summary

- **Paper ID**: `2024_itransformer`
- **Title**: iTransformer: Inverted Transformers Are Effective for Time Series Forecasting
- **Method family**: `variate_attention`
- **Venue/status**: ICLR 2024 Spotlight
- **Source URL**: https://arxiv.org/abs/2310.06625
- **Lingxi transfer target**: Cross-sectional variate-attention ranking proxy
- **Local priority**: 1

## Proposed Local Proxy

The first local implementation should translate the method into a CPU-first score generator over existing OHLCV panels. The proxy must be evaluated as an auxiliary or replacement score for Lingxi10/Lingxi5, not as a generic forecasting benchmark only.

## Official Implementation Status

Not imported in the current repository. Any future official-code reproduction must be added as a separate experiment with explicit environment and config evidence.
