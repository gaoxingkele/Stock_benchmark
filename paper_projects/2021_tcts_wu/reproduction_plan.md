# TCTS Reproduction Plan

## Local Code Entrypoints

```text
external_repos/microsoft__qlib/examples/benchmarks/TCTS/
```

First config:

```text
examples/benchmarks/TCTS/workflow_config_tcts_Alpha360.yaml
```

## China A-Share Adaptation

1. Use as a strong Transformer-style baseline after LightGBM and Transformer.
2. Run on the same CSI300 Alpha360 feature set as TRA.
3. Keep paper URL/venue metadata verification as a source-collection task.

## Expected Outputs

- Shared alpha metrics.
- Comparison against vanilla Transformer, TRA, and MASTER.

