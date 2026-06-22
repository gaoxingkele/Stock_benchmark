# Method Summary

- **Paper ID**: `2022_nonstationary_transformer`
- **Title**: Non-stationary Transformers: Exploring the Stationarity in Time Series Forecasting
- **Method family**: `nonstationarity_correction`
- **Venue/status**: NeurIPS 2022
- **Source URL**: https://proceedings.neurips.cc/paper_files/paper/2022/hash/4054556fcaa934b0bf76da52cf4f92cb-Abstract-Conference.html
- **Lingxi transfer target**: Point-in-time normalization and de-stationary score restoration
- **Local priority**: 2

## Proposed Local Proxy

The first local implementation should translate the method into a CPU-first score generator over existing OHLCV panels. The proxy must be evaluated as an auxiliary or replacement score for Lingxi10/Lingxi5, not as a generic forecasting benchmark only.

## Official Implementation Status

Not imported in the current repository. Any future official-code reproduction must be added as a separate experiment with explicit environment and config evidence.
