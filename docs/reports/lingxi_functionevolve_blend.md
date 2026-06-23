# Lingxi FunctionEvolve-Memory Blend

Date: 2026-06-23

This report evaluates whether the FunctionEvolve-style AST proxy factor can feed back into Lingxi Top5/Top10.

## Command

```powershell
python scripts\run_lingxi_functionevolve_blend.py --max-symbols 80 --max-train-rows 50000
```

## Inputs

1. Lingxi base score: `rd_agent_quant` proxy predictions from the existing Lingxi validation stack.
2. FunctionEvolve proxy factor: the promoted AST factor from `experiments/wq_functionevolve_proxy/functionevolve_proxy_detail.csv`.
3. Promoted AST factor: `zscore10(ret5(close))`.
4. Market: China A-share CSI300 public local panel.
5. Test period: 2023-01-03 to 2024-12-31.
6. Cost: one-way 10 bps.
7. Smoke boundary: 80-symbol frozen public subset generated from the local panel during runtime.

## Results

Summary table:

```text
experiments/lingxi_functionevolve_blend/lingxi_functionevolve_blend_summary.csv
```

Key comparisons:

| TopK | Variant | Baseline Sharpe | Best blend Sharpe | Baseline ann return | Best blend ann return | Decision |
|---:|---|---:|---:|---:|---:|---|
| 5 | raw | 3.73372670 | 4.33878038 | 0.84142770 | 1.03163564 | improves |
| 5 | industry_size_neutral | 2.50165715 | 2.75303346 | 0.50755298 | 0.58751408 | improves at 0.15 weight |
| 10 | raw | 3.51898322 | 3.74895216 | 0.65444500 | 0.71232064 | improves |
| 10 | industry_size_neutral | 3.01713003 | 2.89877727 | 0.53065773 | 0.50453921 | does not improve |

## Interpretation

The first Lingxi-FunctionEvolve blend is positive but still research-only.

What improved:

1. Raw Top5 and Top10 both improved annualized return and Sharpe.
2. The best raw Top5 blend used 30% AST proxy weight.
3. Neutral Top5 improved at 15% AST proxy weight, while neutral Top10 did not improve.

What remains weak:

1. The test is smoke-scale with 80 symbols, not the full CSI300 universe.
2. The AST factor is a price-derived factor and can increase turnover.
3. Neutral results are mixed, so the signal should not be promoted as a universal replacement.
4. The result does not use real WorldQuant BRAIN feedback.

## Decision

Use **Lingxi-FunctionEvolve-Memory** as a research sleeve:

1. For raw Lingxi5/Lingxi10, the FunctionEvolve AST proxy is promising.
2. For neutral Lingxi5/Lingxi10, use only low blend weights unless future full-universe evidence supports stronger mixing.
3. Keep CASE-Lingxi production conclusion unchanged until full-universe and promotion-audit validation pass.

Expanded follow-up:

```text
docs/reports/lingxi_functionevolve_expanded.md
```
