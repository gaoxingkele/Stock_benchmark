# DoubleAdapt Reproduction Plan

## Local Code Entrypoints

```text
external_repos/SJTU-DMTai__qlib/examples/benchmarks_dynamic/incremental/
external_repos/SJTU-DMTai__qlib/qlib/contrib/meta/incremental/
```

## China A-Share Adaptation

1. Build the static CSI300 dataset first.
2. Add rolling/incremental split definitions after baseline results exist.
3. Start from the fork's incremental README commands.
4. Use monthly retraining plus 2-3 trading day adaptation as a candidate practical setting.
5. Compare against rolling retraining baseline.

## Expected Outputs

- Offline baseline result.
- Online/incremental adaptation result.
- Concept drift period analysis for China A shares.

