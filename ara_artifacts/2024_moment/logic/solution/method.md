# Method Summary

- **Paper ID**: `2024_moment`
- **Title**: MOMENT: A Family of Open Time-series Foundation Models
- **Method family**: `foundation_model_multitask`
- **Venue/status**: ICML 2024
- **Source URL**: https://arxiv.org/abs/2402.03885
- **Lingxi transfer target**: General TS representation candidate across tasks
- **Local priority**: 6

## Proposed Local Proxy

The first local implementation should translate the method into a CPU-first score generator over existing OHLCV panels. The proxy must be evaluated as an auxiliary or replacement score for Lingxi10/Lingxi5, not as a generic forecasting benchmark only.

## Official Implementation Status

Not imported in the current repository. Any future official-code reproduction must be added as a separate experiment with explicit environment and config evidence.
