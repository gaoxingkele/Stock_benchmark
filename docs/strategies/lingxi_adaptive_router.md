# Lingxi Adaptive Router

This document defines the portable version of the Lingxi Adaptive Router experiment.

## Purpose

The router tries to choose between three already validated strategy sleeves:

- `lingxi`: original Lingxi / RDA-Adapt proxy
- `lingxi_pitnorm`: PITNorm risk-control sleeve
- `lingxi_pitnorm_gate_return_floor`: ReturnFloor-Gate sleeve

It does not generate stock scores directly. It consumes daily strategy-level returns and diagnostics, then outputs either a selected sleeve or a dynamic blend.

## Required Inputs

For each market, TopK, and variant, provide one daily CSV per sleeve:

```text
{source_dir}/{market}/{method}_h5_top{topk}_{variant}_daily.csv
```

Required columns:

- `date`
- `net_return`
- `benchmark_return`
- `net_active_return`
- `turnover`
- `cost`
- `max_industry_weight`
- `size_exposure`

Supported variants:

- `raw`
- `industry_size_neutral`

## Routers

### Static Equal Ensemble

Weights all sleeves equally. This is a strong baseline and should not be skipped.

### Rolling Selector

Selects the sleeve with the best lagged risk-adjusted metric:

```text
score = mean_return
      - risk_aversion * volatility
      - drawdown_penalty * drawdown / window
      - turnover_penalty * turnover_cost_proxy
      - switch_penalty
```

Only data at least `horizon` days behind the decision date is used.

### Hedge Router

Maintains multiplicative weights over sleeves:

```text
weight_i <- weight_i * exp(eta * clipped_lagged_reward_i)
```

The output is a dynamic weighted portfolio rather than a hard switch.

### Contextual Ridge Router

Fits a rolling ridge model per sleeve using lagged context features, then selects the sleeve with the highest predicted reward.

Feature groups:

- lagged benchmark mean return
- lagged benchmark volatility
- lagged benchmark drawdown
- lagged benchmark Sharpe
- lagged sleeve return
- lagged sleeve volatility
- lagged sleeve drawdown
- lagged sleeve Sharpe
- lagged sleeve turnover
- lagged industry concentration
- lagged size exposure
- sleeve identity flags

The model is refit every 5 trading days by default.

## Reproduction

Base 2023-2025 sample:

```powershell
python scripts\run_lingxi_adaptive_router_validation.py --out-dir experiments\lingxi_adaptive_router_validation
```

2026 YTD source generation:

```powershell
python scripts\run_lingxi_pitnorm_tuned_gate_validation.py --test-end 2026-06-18 --out-dir experiments\lingxi_pitnorm_tuned_gate_validation_2026_ytd
```

2026 YTD router validation:

```powershell
python scripts\run_lingxi_adaptive_router_validation.py --source-dir experiments\lingxi_pitnorm_tuned_gate_validation_2026_ytd --out-dir experiments\lingxi_adaptive_router_validation_2026_ytd
```

## Current Decision Rule

The adaptive router is not yet the production default.

Use it as a research sleeve only in:

- A-share Top10 raw, where contextual ridge improved the 2023-2025 Sharpe and drawdown.
- Crypto Top5 neutral, where contextual ridge improved Sharpe in both 2023-2025 and 2023-2026 YTD.
- Crypto Top10 raw, where rolling selector showed a small 2026 YTD improvement.

Use fixed or static baselines elsewhere:

- A-share Top5 neutral: ReturnFloor-Gate
- US Top10/Top5: fixed/static baselines
- HK Top10/Top5: PITNorm
- Crypto Top5 raw: ReturnFloor-Gate

## LLM Extension Policy

LLMs should not directly choose the route in the current version.

Allowed use:

- produce structured macro tags
- explain router decisions
- audit risk narratives
- compare independent model opinions for research notes

Disallowed use:

- directly override a route without a backtested structured signal
- use non-reproducible free-form text as the sole decision input
- mix current or future information into historical backtests

The next valid upgrade is an `LLM macro context adapter` whose tags are saved as dated structured features and evaluated out of sample.

## Market-Regime Router Update

The second-stage market-regime router adds lagged panel-derived features:

- market return and 20/60 day momentum
- 20/60 day volatility
- 60 day drawdown
- market breadth
- cross-sectional dispersion
- liquidity change
- size concentration

Validation result: useful but still selective.

- It beats the previous contextual ridge router in 9 of 16 scenarios.
- It beats the best fixed/static baseline in only 2 of 16 scenarios.
- Keep it only for A-share Top5 neutral and crypto Top5 raw research sleeves.
- Do not use it for US, HK, A-share raw, or crypto neutral production routing.

Reproduction:

```powershell
python scripts\run_lingxi_regime_router_validation.py --out-dir experiments\lingxi_regime_router_validation_2026_ytd
```

## Sparse Regime Router Update

The third-stage router adds rolling feature selection before ridge fitting. It ranks contextual and regime features by lagged reward correlation, keeps at most 20 non-intercept features, and fits ridge on that capped subset.

Validation result:

- Beats the best fixed/static baseline in 3 of 16 scenarios.
- Beats full market-regime ridge in 8 of 16 scenarios.
- Beats non-regime contextual ridge in 10 of 16 scenarios.
- Usually keeps about 19 features, so it is a feature-capped router rather than a truly sparse model.

Keep only these research sleeves:

- A-share Top5 neutral sparse regime
- Crypto Top10 raw sparse regime
- HK Top5 raw sparse regime

Do not promote sparse regime routing as a global production router.

Reproduction:

```powershell
python scripts\run_lingxi_sparse_regime_router_validation.py --out-dir experiments\lingxi_sparse_regime_router_validation_2026_ytd
```
