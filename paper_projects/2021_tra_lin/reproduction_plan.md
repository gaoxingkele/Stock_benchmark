# TRA Reproduction Plan

## Local Code Entrypoints

```text
external_repos/microsoft__qlib/examples/benchmarks/TRA/
external_repos/microsoft__qlib/qlib/contrib/model/pytorch_tra.py
```

First config:

```text
examples/benchmarks/TRA/workflow_config_tra_Alpha360.yaml
```

## China A-Share Adaptation

1. Run Qlib LightGBM on CSI300 first to validate the dataset.
2. Use Alpha360 initially because Qlib has a standard TRA config for it.
3. Replace default Qlib data path with `data/processed/cn_a_share/qlib`.
4. Start with 1-day return ranking label, then add 5-day label.
5. Compare against ALSTM/Transformer backbone where feasible.

## Expected Outputs

- IC, ICIR, RankIC, RankICIR.
- Top-k/dropout portfolio report.
- Runtime and GPU/CPU memory notes.

