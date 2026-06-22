# Method Summary

- **Paper ID**: `2023_patchtst`
- **Title**: PatchTST: A Time Series is Worth 64 Words
- **Method family**: `patch_transformer`
- **Venue/status**: ICLR 2023
- **Source URL**: https://arxiv.org/abs/2211.14730
- **Lingxi transfer target**: Patch-token OHLCV feature proxy for Lingxi10/Lingxi5
- **Local priority**: 3

## Proposed Local Proxy

The first local implementation should translate the method into a CPU-first score generator over existing OHLCV panels. The proxy must be evaluated as an auxiliary or replacement score for Lingxi10/Lingxi5, not as a generic forecasting benchmark only.

## Official Implementation Status

Not imported in the current repository. Any future official-code reproduction must be added as a separate experiment with explicit environment and config evidence.
