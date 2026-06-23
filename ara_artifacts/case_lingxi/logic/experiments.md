# Experiments

## E01: Benchmark master table

- **Verifies**: C01
- **Setup**:
  - Model: Lingxi, PITNorm, ReturnFloor, and SOTA-inspired proxy sleeves
  - Dataset: China A-share, US large cap, HK large cap, crypto major
  - Portfolio: H5 Top10/Top5, equal-weight long-only, daily rebalance, single-side 10 bps cost
- **Script/config**: existing Lingxi validation scripts indexed in `docs/reports/benchmark_master_table.md`
- **Primary artifact**: `experiments/lingxi_sota_upgrade_validation/lingxi_sota_upgrade_validation_summary.csv`
- **Rows**: 96
- **Procedure**:
  1. Run the Lingxi SOTA upgrade validation.
  2. Group by market, TopK, and variant.
  3. Compare annualized return, Sharpe, MDD, and cumulative return.
- **Metrics**: annualized return, Sharpe, MDD, cumulative return
- **Expected outcome**:
  - The production menu should only promote sleeves that beat or materially improve the relevant static baseline.
- **Outcome**: Lingxi remains the main production anchor; PITNorm is useful as a risk-control candidate.

## E02: Conservative context router validation

- **Verifies**: C02
- **Setup**:
  - Model: conservative context router over approved Lingxi-family sleeves
  - Dataset: same source daily sleeve files as `lingxi_pitnorm_tuned_gate_validation_2026_ytd`
  - Portfolio: H5 Top10/Top5, raw and neutral variants, single-side 10 bps cost
- **Script**: `scripts/run_case_lingxi_context_router.py`
- **Command**:

```powershell
python scripts\run_case_lingxi_context_router.py --out-dir experiments\case_lingxi_context_router_validation_2026_ytd
```

- **Primary artifact**: `experiments/case_lingxi_context_router_validation_2026_ytd/case_lingxi_context_router_validation_summary.csv`
- **Rows**: 112
- **Procedure**:
  1. Build lagged market context features.
  2. Route only among approved sleeves.
  3. Compare against the CASE static production menu.
- **Expected outcome**:
  - Promote only if return and Sharpe wins are broad enough and drawdown does not degrade materially.
- **Outcome**: annualized return wins 3/16, Sharpe wins 3/16, MDD wins 9/16 versus static menu.

## E03: Frozen tabular RL router validation

- **Verifies**: C03
- **Setup**:
  - Model: frozen tabular RL-style state-action router
  - Training period: 2023-2024
  - OOS period: 2025-2026 YTD
  - Actions: `lingxi`, `lingxi_pitnorm`, `lingxi_pitnorm_gate_return_floor`
- **Script**: `scripts/run_case_lingxi_rl_router_baseline.py`
- **Command**:

```powershell
python scripts\run_case_lingxi_rl_router_baseline.py --out-dir experiments\case_lingxi_rl_router_validation_2025_2026_ytd
```

- **Primary artifact**: `experiments/case_lingxi_rl_router_validation_2025_2026_ytd/case_lingxi_rl_router_validation_summary.csv`
- **Rows**: 128
- **Training period**: 2023-2024
- **OOS period**: 2025-2026 YTD
- **Procedure**:
  1. Discretize lagged market states.
  2. Estimate a small action-value table from the training period.
  3. Freeze the policy before OOS evaluation.
  4. Compare against the static production menu.
- **Expected outcome**:
  - The RL router must beat the static menu broadly before any production consideration.
- **Outcome**: annualized return wins 4/16, Sharpe wins 4/16, MDD wins 6/16 versus static menu.

## E04: Structured LLM-compatible market-tag ablation

- **Verifies**: C04
- **Setup**:
  - Model: structured market-tag router over approved Lingxi-family sleeves
  - Tag source: deterministic lagged context proxy, LLM-compatible schema
  - Schema: `case_lingxi_market_tags_v1`
- **Script**: `scripts/run_case_lingxi_llm_tag_ablation.py`
- **Command**:

```powershell
python scripts\run_case_lingxi_llm_tag_ablation.py --out-dir experiments\case_lingxi_llm_tag_ablation_2026_ytd
```

- **Primary artifact**: `experiments/case_lingxi_llm_tag_ablation_2026_ytd/case_lingxi_llm_tag_ablation_summary.csv`
- **Rows**: 128
- **Tag schema**: `case_lingxi_market_tags_v1`
- **Procedure**:
  1. Generate point-in-time tags from lagged market context.
  2. Write tag CSV files by market, TopK, and variant.
  3. Route among approved sleeves using tag-conditioned preferences.
  4. Compare against static menu and conservative context router.
- **Expected outcome**:
  - Tags remain research-only unless they beat the OOS promotion gate.
- **Outcome**: annualized return wins 0/16, Sharpe wins 2/16, MDD wins 7/16 versus static menu.

## E05: Validation-only meta-selector rejection

- **Verifies**: C05
- **Setup**:
  - Model: validation-only strategy selector
  - Selection window: validation period
  - Evaluation: frozen OOS comparison
- **Script**: `scripts/run_lingxi_meta_selector_validation.py`
- **Primary artifact**: `experiments/lingxi_meta_selector_validation/lingxi_meta_selector_validation_summary.csv`
- **Rows**: 416
- **Procedure**:
  1. Select methods by validation Sharpe.
  2. Freeze selected methods.
  3. Evaluate in 2025, 2026 YTD, and combined OOS windows.
- **Expected outcome**:
  - A robust selector should beat the static menu in OOS periods; otherwise it is rejected.
- **Outcome**: validation-only selector wins 2/16 in 2025, 0/16 in 2026 YTD, and 1/16 combined.

## E06: Unified promotion audit with paired bootstrap intervals

- **Verifies**: C01, C02, C03, C04
- **Setup**:
  - Candidates: conservative context router, frozen tabular RL router, structured market-tag router
  - Comparator: CASE static production menu
  - Data: aligned candidate and menu daily `net_return` files
  - Bootstrap: 1000 samples, block size 5, seed 20260623
- **Script**: `scripts/run_case_lingxi_promotion_audit.py`
- **Command**:

```powershell
python scripts\run_case_lingxi_promotion_audit.py --out-dir experiments\case_lingxi_promotion_audit
```

- **Primary artifact**: `experiments/case_lingxi_promotion_audit/case_lingxi_promotion_audit_summary.csv`
- **Detail artifact**: `experiments/case_lingxi_promotion_audit/case_lingxi_promotion_audit_detail.csv`
- **Rows**: 3 summary rows, 48 detail rows
- **Procedure**:
  1. Align candidate and static-menu daily returns by date.
  2. Recompute annualized return, Sharpe, and MDD differences.
  3. Bootstrap daily return differences with block sampling.
  4. Apply the promotion gate.
- **Expected outcome**:
  - A production candidate should have broad metric wins and positive annualized-difference confidence evidence.
- **Outcome**: no candidate has any positive annualized-difference CI lower-bound wins; no candidate is promoted to production.
