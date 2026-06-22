# Method Summary

- **Paper ID**: `2024_ttm`
- **Title**: Tiny Time Mixers for Long-term Multivariate Time Series Forecasting
- **Method family**: `tiny_pretrained_ts_model`
- **Venue/status**: NeurIPS 2024
- **Source URL**: https://openreview.net/forum?id=3O5YCEWETq
- **Lingxi transfer target**: Lightweight pretrained baseline/feature candidate
- **Local priority**: 5

## Proposed Local Proxy

The first local implementation should translate the method into a CPU-first score generator over existing OHLCV panels. The proxy must be evaluated as an auxiliary or replacement score for Lingxi10/Lingxi5, not as a generic forecasting benchmark only.

## Official Implementation Status

Not imported in the current repository. Any future official-code reproduction must be added as a separate experiment with explicit environment and config evidence.
