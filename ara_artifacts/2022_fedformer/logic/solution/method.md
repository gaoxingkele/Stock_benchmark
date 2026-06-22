# Method Summary

- **Paper ID**: `2022_fedformer`
- **Title**: FEDformer: Frequency Enhanced Decomposed Transformer for Long-term Series Forecasting
- **Method family**: `frequency_decomposition`
- **Venue/status**: ICML 2022
- **Source URL**: https://proceedings.mlr.press/v162/zhou22g.html
- **Lingxi transfer target**: Frequency/seasonal-trend features for multiscale proxy
- **Local priority**: 4

## Proposed Local Proxy

The first local implementation should translate the method into a CPU-first score generator over existing OHLCV panels. The proxy must be evaluated as an auxiliary or replacement score for Lingxi10/Lingxi5, not as a generic forecasting benchmark only.

## Official Implementation Status

Not imported in the current repository. Any future official-code reproduction must be added as a separate experiment with explicit environment and config evidence.
