# Lingxi FunctionEvolve Expanded Experiment

Date: 2026-06-24

This report expands the local FunctionEvolve-style factor evolution and Lingxi blend from the initial 25-symbol proxy run to an 80-symbol aligned proxy run.

## Commands

```powershell
python scripts\run_wq_functionevolve_proxy.py --max-candidates 18 --promotion-top 5 --max-symbols 80 --out-dir experiments\wq_functionevolve_proxy_expanded
python scripts\run_lingxi_functionevolve_blend.py --proxy-detail experiments\wq_functionevolve_proxy_expanded\functionevolve_proxy_detail.csv --max-symbols 80 --max-train-rows 50000 --out-dir experiments\lingxi_functionevolve_blend_expanded
```

## Expanded Factor Evolution Result

Output:

```text
experiments/wq_functionevolve_proxy_expanded/functionevolve_proxy_summary.csv
experiments/wq_functionevolve_proxy_expanded/functionevolve_proxy_detail.csv
```

Result:

| Metric | Value |
|---|---:|
| AST candidates | 18 |
| Valid factors | 18 |
| Promoted factors | 2 |
| Promoted mean IC | 0.00902681 |
| Promoted rank IC | 0.01204159 |
| Promoted rank ICIR | 0.06197736 |
| Promoted turnover | 0.83592961 |

Promoted factors:

1. `zscore3(ret5(close))`
2. `zscore10(ret5(close))`

## Expanded Lingxi Blend Result

Output:

```text
experiments/lingxi_functionevolve_blend_expanded/lingxi_functionevolve_blend_summary.csv
```

Key comparisons:

| TopK | Variant | Baseline Sharpe | Best blend Sharpe | Baseline ann return | Best blend ann return | Decision |
|---:|---|---:|---:|---:|---:|---|
| 5 | raw | 3.10388546 | 3.64388088 | 0.37328694 | 0.45924200 | improves at 0.15 |
| 5 | industry_size_neutral | 2.16249018 | 2.35966641 | 0.23647204 | 0.27400412 | improves at 0.15 |
| 10 | raw | 3.24419907 | 3.62531010 | 0.32943436 | 0.36278179 | improves at 0.15 |
| 10 | industry_size_neutral | 1.82230126 | 1.84100294 | 0.17696504 | 0.17525806 | slight Sharpe improvement, return flat/down |

## Decision

The expanded local evidence supports a conservative research sleeve:

1. Use FunctionEvolve-memory blend weight `0.15` as the default research setting.
2. Avoid `0.30` as a default because it increases turnover and weakens neutral variants.
3. Keep the sleeve research-only until full-universe and promotion-audit validation are added.

This result answers whether local factor evolution can be performed and fed back into Lingxi: yes, the local pipeline now evolves AST proxy factors and uses them in Lingxi5/Lingxi10 blend tests.
