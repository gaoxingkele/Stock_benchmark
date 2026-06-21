# TCTS Notes

## Source Verification

- Paper: Temporally Correlated Task Scheduling for Sequence Learning.
- Venue: ICML 2021, PMLR 139.
- PDF: `https://proceedings.mlr.press/v139/wu21e/wu21e.pdf`.
- Reproduction code referenced by Qlib: `https://github.com/lwwang1995/tcts`.
- Qlib baseline code: `external_repos/microsoft__qlib/examples/benchmarks/TCTS`.

## Core Idea

TCTS treats sequence forecasting as a multi-task problem where auxiliary tasks are temporally correlated with the main task. In stock forecasting, these tasks correspond to returns at different future horizons. A learnable scheduler selects which auxiliary task should guide training at each step, and the forecasting model plus scheduler are optimized through a bilevel training process.

## Qlib Setting

The local Qlib benchmark config uses:

```text
external_repos/microsoft__qlib/examples/benchmarks/TCTS/workflow_config_tcts_Alpha360.yaml
```

The Qlib config defines three labels:

```text
Ref($close, -2) / Ref($close, -1) - 1
Ref($close, -3) / Ref($close, -1) - 1
Ref($close, -4) / Ref($close, -1) - 1
```

For the China A-share benchmark, the first smoke config is recorded at:

```text
configs/china_a_share_smoke.json
```

## Reproduction Notes

- Start from the same CSI300 provider as LightGBM and TRA.
- Use TCTS after a vanilla Transformer baseline, because TCTS adds a scheduler on top of multi-horizon sequence learning.
- The current 7-trading-day smoke sample can validate config wiring but is too short for a meaningful multi-horizon TCTS run.
