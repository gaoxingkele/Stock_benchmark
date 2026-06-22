# Method Summary

- **Paper ID**: `2023_dlinear`
- **Title**: Are Transformers Effective for Time Series Forecasting?
- **Method family**: `decomposition_linear`
- **Venue/status**: AAAI 2023
- **Source URL**: https://ojs.aaai.org/index.php/AAAI/article/view/26317
- **Lingxi transfer target**: LinearGuard baseline every neural upgrade must beat
- **Local priority**: 0

## Proposed Local Proxy

The first local implementation should translate the method into a CPU-first score generator over existing OHLCV panels. The proxy must be evaluated as an auxiliary or replacement score for Lingxi10/Lingxi5, not as a generic forecasting benchmark only.

## Official Implementation Status

Not imported in the current repository. Any future official-code reproduction must be added as a separate experiment with explicit environment and config evidence.
