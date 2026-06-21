# Qlib Entrypoints

Date: 2026-06-19

## Cloned Repositories

| Repo | Local path | Current commit | Role |
| --- | --- | --- | --- |
| `microsoft/qlib` | `external_repos/microsoft__qlib` | `d5379c5` | Main benchmark framework and model zoo. |
| `SJTU-DMTai/qlib` | `external_repos/SJTU-DMTai__qlib` | `fbd067c` | MASTER and DoubleAdapt reproduction source. |

Both repositories are shallow checkouts in detached HEAD state.

## Main Qlib Benchmark Pool

Local path:

```text
external_repos/microsoft__qlib/examples/benchmarks/
```

Observed benchmark directories:

```text
ADARNN, ADD, ALSTM, CatBoost, DoubleEnsemble, GATs, GeneralPtNN,
GRU, HIST, IGMTF, KRNN, LightGBM, Linear, Localformer, LSTM, MLP,
Sandwich, SFM, TabNet, TCN, TCTS, TFT, TRA, Transformer, XGBoost
```

Important first configs:

```text
examples/benchmarks/LightGBM/workflow_config_lightgbm_Alpha158.yaml
examples/benchmarks/MLP/workflow_config_mlp_Alpha360.yaml
examples/benchmarks/Transformer/workflow_config_transformer_Alpha360.yaml
examples/benchmarks/TRA/workflow_config_tra_Alpha360.yaml
examples/benchmarks/TCTS/workflow_config_tcts_Alpha360.yaml
examples/benchmarks/HIST/workflow_config_hist_Alpha360.yaml
```

## SJTU Fork Entrypoints

MASTER:

```text
external_repos/SJTU-DMTai__qlib/examples/benchmarks/MASTER/
external_repos/SJTU-DMTai__qlib/qlib/contrib/model/pytorch_master_ts.py
external_repos/SJTU-DMTai__qlib/qlib/contrib/data/dataset.py
```

DoubleAdapt:

```text
external_repos/SJTU-DMTai__qlib/examples/benchmarks_dynamic/incremental/
external_repos/SJTU-DMTai__qlib/qlib/contrib/meta/incremental/
```

TRA is also present in the fork, but the main reproduction source should be `microsoft/qlib` unless MASTER/DoubleAdapt require fork-specific compatibility.

## Next Repo Tasks

1. Inspect Qlib data format requirements for local China A-share data.
2. Decide whether to install Qlib editable from `microsoft__qlib` or use source path execution.
3. Create local configs that point to `data/processed/cn_a_share/qlib`.
4. Run LightGBM first to validate the data-to-metrics loop.

