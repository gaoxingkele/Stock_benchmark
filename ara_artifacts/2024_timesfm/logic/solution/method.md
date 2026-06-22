# Method Summary

- **Paper ID**: `2024_timesfm`
- **Title**: A Decoder-Only Foundation Model for Time-Series Forecasting
- **Method family**: `foundation_forecaster`
- **Venue/status**: ICML 2024 / Google Research
- **Source URL**: https://research.google/blog/a-decoder-only-foundation-model-for-time-series-forecasting/
- **Lingxi transfer target**: Later-stage foundation-model feature source
- **Local priority**: 6

## Proposed Local Proxy

The first local implementation should translate the method into a CPU-first score generator over existing OHLCV panels. The proxy must be evaluated as an auxiliary or replacement score for Lingxi10/Lingxi5, not as a generic forecasting benchmark only.

## Official Implementation Status

Not imported in the current repository. Any future official-code reproduction must be added as a separate experiment with explicit environment and config evidence.
