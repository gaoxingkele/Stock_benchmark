# Paper Reading Index

Date: 2026-06-19

## Downloaded And Extracted

| Paper ID | PDF | Extracted text | Code | Priority |
| --- | --- | --- | --- | --- |
| `2021_tra_lin` | `papers/raw/2021_tra_lin.pdf` | `papers/extracted/2021_tra_lin.txt` | `external_repos/microsoft__qlib/examples/benchmarks/TRA` | Core |
| `2023_doubleadapt_zhao` | `papers/raw/2023_doubleadapt_zhao.pdf` | `papers/extracted/2023_doubleadapt_zhao.txt` | `external_repos/SJTU-DMTai__qlib/examples/benchmarks_dynamic/incremental` | Core |
| `2024_master_li` | `papers/raw/2024_master_li.pdf` | `papers/extracted/2024_master_li.txt` | `external_repos/SJTU-DMTai__qlib/examples/benchmarks/MASTER` | Core |
| `2021_tcts_wu` | `papers/raw/2021_tcts_wu.pdf` | `papers/extracted/2021_tcts_wu.txt` | `external_repos/microsoft__qlib/examples/benchmarks/TCTS` | Core |
| `2022_hist_xu` | `papers/raw/2022_hist_xu.pdf` | `papers/extracted/2022_hist_xu.txt` | `external_repos/microsoft__qlib/examples/benchmarks/HIST` | Expanded baseline |
| `2021_adarnn_du` | `papers/raw/2021_adarnn_du.pdf` | `papers/extracted/2021_adarnn_du.txt` | `external_repos/microsoft__qlib/examples/benchmarks/ADARNN` | Expanded baseline |

## Pending

| Paper ID | Reason |
| --- | --- |
| `2022_ddg_da_li` | arXiv download currently fails in this environment. Retry or find alternate source. |

## Reading Order

1. TRA: first full paper note because it is stock-specific, CCF-A, and Qlib-integrated.
2. MASTER: second because it is the target Transformer architecture.
3. DoubleAdapt: third because it adds incremental/online workflow complexity.
4. TCTS: multi-horizon task scheduling after Transformer/TRA setup is stable.
5. HIST and AdaRNN: expanded baselines after the core models.
