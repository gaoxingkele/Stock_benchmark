# MASTER Reproduction Plan

## Local Code Entrypoints

```text
external_repos/SJTU-DMTai__qlib/examples/benchmarks/MASTER/
external_repos/SJTU-DMTai__qlib/qlib/contrib/model/pytorch_master_ts.py
external_repos/SJTU-DMTai__qlib/qlib/contrib/data/dataset.py
```

First config:

```text
examples/benchmarks/MASTER/workflow_config_master_Alpha158.yaml
```

## China A-Share Adaptation

1. Confirm MASTER-specific market feature requirements.
2. Map CSI300 index features into the market-guided component.
3. Use the same CSI300 split and label as TRA for first comparison.
4. Record any fork-specific Qlib changes needed for the main data path.

## Expected Outputs

- Shared alpha metrics.
- Comparison with Transformer and TRA.
- Market-gating ablation if feasible.

