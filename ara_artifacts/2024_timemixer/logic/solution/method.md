# Method Summary

- **Paper ID**: `2024_timemixer`
- **Title**: TimeMixer: Decomposable Multiscale Mixing for Time Series Forecasting
- **Method family**: `multiscale_mlp`
- **Venue/status**: ICLR 2024
- **Source URL**: https://arxiv.org/abs/2405.14616
- **Lingxi transfer target**: Multiscale momentum/reversal/trend decomposition features
- **Local priority**: 4

## Proposed Local Proxy

The first local implementation should translate the method into a CPU-first score generator over existing OHLCV panels. The proxy must be evaluated as an auxiliary or replacement score for Lingxi10/Lingxi5, not as a generic forecasting benchmark only.

## Official Implementation Status

Not imported in the current repository. Any future official-code reproduction must be added as a separate experiment with explicit environment and config evidence.
