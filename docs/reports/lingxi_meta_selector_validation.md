# Lingxi Validation-Only Meta-Selector Validation

Date: 2026-06-23

## Objective

Test whether a frozen scenario-level selector can choose the best Lingxi sleeve using only a validation window.

The motivation was practical: instead of forcing one dynamic router everywhere, choose one method per market/topk/variant from a validation period, freeze that choice, then evaluate out of sample.

## Protocol

| Item | Setting |
|---|---|
| Selection window | 2023-01-01 to 2024-12-31 |
| OOS windows | 2025, 2026 YTD, 2025-2026 YTD |
| Candidate methods | Lingxi, PITNorm, ReturnFloor-Gate, static equal ensemble, contextual ridge, market-regime ridge, sparse regime ridge |
| Selection metric | validation Sharpe |
| Oracle | excluded from selection |
| Output | `experiments/lingxi_meta_selector_validation/` |

Reproduction:

```powershell
python scripts\run_lingxi_meta_selector_validation.py --out-dir experiments\lingxi_meta_selector_validation
```

## Main Conclusion

The validation-only meta-selector **fails as a deployment method**.

It selected plausible methods in 2023-2024, but those choices did not transfer:

- 2025: meta-selector beats the best fixed/static baseline in only 2 of 16 scenarios.
- 2026 YTD: 0 of 16.
- Combined 2025-2026 YTD: 1 of 16.

This is a strong negative result. A simple "pick the validation Sharpe winner" rule overfits regime-specific noise and should not be used.

## Frozen Selections

| Market | TopK | Variant | Selected method | Validation Sharpe |
|---|---:|---|---|---:|
| A-share | 10 | raw | PITNorm | 5.87 |
| A-share | 10 | neutral | Market-regime ridge | 3.56 |
| A-share | 5 | raw | PITNorm | 6.65 |
| A-share | 5 | neutral | Contextual ridge | 3.61 |
| US | 10 | raw | PITNorm | 6.44 |
| US | 10 | neutral | PITNorm | 6.06 |
| US | 5 | raw | Static ensemble | 7.20 |
| US | 5 | neutral | Static ensemble | 6.47 |
| HK | 10 | raw | PITNorm | 2.90 |
| HK | 10 | neutral | Contextual ridge | 1.51 |
| HK | 5 | raw | Contextual ridge | 3.43 |
| HK | 5 | neutral | Market-regime ridge | 1.96 |
| Crypto | 10 | raw | Sparse regime ridge | 6.94 |
| Crypto | 10 | neutral | Lingxi | 5.06 |
| Crypto | 5 | raw | Market-regime ridge | 9.22 |
| Crypto | 5 | neutral | Contextual ridge | 6.01 |

## OOS Result Summary

| OOS period | Wins vs best fixed/static baseline |
|---|---:|
| 2025 | 2 / 16 |
| 2026 YTD | 0 / 16 |
| 2025-2026 YTD | 1 / 16 |

The few wins are not stable:

- Crypto Top10 raw wins slightly in 2025, then loses in 2026 YTD.
- Crypto Top5 raw wins in 2025 and combined OOS, but loses in 2026 YTD.

## Interpretation

The selector overfits because validation Sharpe is not stable enough across regimes.

Observed failure modes:

- A-share validation prefers PITNorm in raw scenarios, but Lingxi dominates in 2025 and 2026.
- HK validation selects dynamic routers in neutral/Top5 cases, but PITNorm remains the stronger fixed baseline.
- Crypto validation selects dynamic routers during favorable regimes, but 2026 YTD reversal damages transfer.
- US selections are more conservative, but fixed baselines still often beat the frozen selection.

## Updated Decision

Do not deploy a validation-Sharpe meta-selector.

Use the accumulated evidence to define a conservative strategy menu:

| Scenario | Recommended production proxy |
|---|---|
| A-share raw Top10/Top5 | Lingxi for return; static ensemble/PITNorm only as risk sleeves |
| A-share Top5 neutral | Lingxi remains strongest return proxy; sparse/regime only research |
| US Top10/Top5 | Static/fixed baselines; no dynamic router |
| HK Top10/Top5 | PITNorm |
| Crypto raw | ReturnFloor-Gate; sparse/regime only as research sleeve |
| Crypto neutral | Lingxi or PITNorm depending risk target; no dynamic router |

## LLM Implication

This makes the LLM route stricter:

1. LLM tags must not be used to select the single best method from a short validation window.
2. LLM tags need a stability test across 2025 and 2026 YTD.
3. The evaluation target must be "incremental lift over conservative fixed baseline", not "better than a weak dynamic router".

## Next Step

The next useful artifact is a final **Lingxi Adaptive Suite** document:

- summarize all validated candidates,
- mark production vs research sleeves,
- define the conservative strategy menu,
- document why naive dynamic routing and validation-only selection were rejected.
