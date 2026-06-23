# Lingxi Adaptive Suite

Date: 2026-06-23

## Purpose

This document consolidates the Lingxi strategy family after the TopK, PITNorm, ReturnFloor, adaptive-router, regime-router, sparse-router, and meta-selector validations.

It separates production proxies from research sleeves. A method is not promoted just because it wins one backtest; it must survive cross-market and 2025/2026 YTD checks.

## Candidate Methods

| Method | Role |
|---|---|
| Lingxi | Main return-seeking proxy |
| PITNorm | Risk-control / stable cross-sectional normalization sleeve |
| ReturnFloor-Gate | Dynamic PITNorm blend with return-protection penalty |
| Static equal ensemble | Strong simple ensemble baseline |
| Contextual ridge router | Dynamic router using lagged strategy state |
| Market-regime ridge router | Dynamic router with market trend/volatility/breadth/liquidity context |
| Sparse regime ridge router | Feature-capped regime router |
| Validation-only meta-selector | Rejected selector; validation Sharpe did not transfer |

## Production Menu

| Market | TopK | Variant | Production proxy | Reason |
|---|---:|---|---|---|
| A-share | 10 | raw | Lingxi | Best return profile; dynamic selectors did not transfer reliably |
| A-share | 10 | neutral | Lingxi | Strongest fixed baseline after 2026 YTD |
| A-share | 5 | raw | Lingxi | Return dominates; risk sleeves are optional overlays |
| A-share | 5 | neutral | Lingxi | Best OOS fixed/static baseline; sparse regime is research only |
| US | 10 | raw | PITNorm or static ensemble | Stable risk-adjusted fixed baselines |
| US | 10 | neutral | Lingxi | 2026 YTD favors Lingxi over validation-selected PITNorm |
| US | 5 | raw | ReturnFloor-Gate or static ensemble | Strong fixed/static results; routers weaker |
| US | 5 | neutral | Lingxi / static ensemble | Dynamic routing did not improve enough |
| HK | 10 | raw | PITNorm | Repeatedly strongest HK fixed baseline |
| HK | 10 | neutral | PITNorm | Repeatedly strongest HK fixed baseline |
| HK | 5 | raw | PITNorm | Repeatedly strongest HK fixed baseline |
| HK | 5 | neutral | PITNorm | Repeatedly strongest HK fixed baseline |
| Crypto | 10 | raw | ReturnFloor-Gate | Best fixed/static raw sleeve, sparse regime only research |
| Crypto | 10 | neutral | Lingxi or PITNorm | Dynamic routers unstable in 2026 YTD |
| Crypto | 5 | raw | ReturnFloor-Gate | Strongest raw sleeve across router comparisons |
| Crypto | 5 | neutral | Lingxi / PITNorm | Dynamic routers did not transfer reliably |

## Research Sleeves

These are not production defaults, but remain worth tracking:

| Sleeve | Why keep it |
|---|---|
| A-share Top5 neutral sparse regime | High Sharpe in 2026 YTD experiment, but drawdown not improved |
| Crypto Top10 raw sparse regime | Beat fixed/static baseline in sparse-router validation |
| Crypto Top5 raw market-regime ridge | Strong full-regime case, but 2026 transfer mixed |
| HK Top5 raw sparse regime | Beat fixed/static baseline in sparse-router validation |
| A-share Top10 raw contextual ridge | Useful risk-adjusted research sleeve in earlier router tests |

## Rejected Routes

| Route | Decision |
|---|---|
| Universal dynamic router | Rejected; wins too few scenarios |
| Full market-regime router everywhere | Rejected; adds useful context but too much noise |
| Sparse regime router everywhere | Rejected; improves dynamic routers but still only wins 3/16 vs fixed/static |
| Validation-only Sharpe meta-selector | Rejected; 2025 wins 2/16, 2026 YTD wins 0/16 |
| Direct LLM trading router | Rejected for now; not reproducible and not yet shown to beat fixed baselines |

## LLM Policy

LLMs may be used only as structured context adapters or auditors.

Allowed:

- produce dated macro tags,
- summarize policy/liquidity/risk regime,
- explain why a conservative menu chooses a sleeve,
- audit router decisions.

Not allowed:

- directly choose trades,
- override the production menu without backtested structured evidence,
- select winners from a short validation window.

Any LLM macro adapter must beat the conservative fixed/static baseline out of sample.

## Reproduction Index

```powershell
python scripts\run_lingxi_pitnorm_tuned_gate_validation.py --test-end 2026-06-18 --out-dir experiments\lingxi_pitnorm_tuned_gate_validation_2026_ytd
python scripts\run_lingxi_adaptive_router_validation.py --source-dir experiments\lingxi_pitnorm_tuned_gate_validation_2026_ytd --out-dir experiments\lingxi_adaptive_router_validation_2026_ytd
python scripts\run_lingxi_regime_router_validation.py --out-dir experiments\lingxi_regime_router_validation_2026_ytd
python scripts\run_lingxi_sparse_regime_router_validation.py --out-dir experiments\lingxi_sparse_regime_router_validation_2026_ytd
python scripts\run_lingxi_meta_selector_validation.py --out-dir experiments\lingxi_meta_selector_validation
```

## Final Practical Conclusion

The strongest practical result is not a sophisticated universal router. It is a conservative, evidence-based strategy suite:

1. Use Lingxi, PITNorm, ReturnFloor-Gate, and static ensemble as the main deployable tools.
2. Use dynamic routers only where repeated OOS evidence supports a research sleeve.
3. Treat LLM and richer regime routing as research context, not production authority.
