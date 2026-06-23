# Claims

## C01: Lingxi Adaptive Suite is the current supported production proxy

- **Statement**: The current best supported production state is a conservative scenario-specific Lingxi Adaptive Suite, not a universal dynamic router.
- **Status**: supported
- **Falsification criteria**: A future OOS experiment satisfies the numeric production gate in `docs/theory/case_lingxi_promotion_gate.md`: annualized return wins at least 10/16, Sharpe wins at least 10/16, MDD is not worse in more than 4/16, and transaction costs are included.
- **Proof**: E01, E02, E03, E04, E05
- **Evidence basis**: `docs/reports/benchmark_master_table.md`, `docs/strategies/lingxi_adaptive_suite.md`, and committed experiment summaries.
- **Dependencies**: none
- **Tags**: production, benchmark

## C02: Conservative context routing is research-only

- **Statement**: The conservative CASE-Lingxi context router is useful as a drawdown-control research sleeve but does not replace the static menu.
- **Status**: supported
- **Falsification criteria**: Re-running or extending `scripts/run_case_lingxi_context_router.py` satisfies the production gate in `docs/theory/case_lingxi_promotion_gate.md`.
- **Proof**: E02
- **Evidence basis**: It wins annualized return 3/16, Sharpe 3/16, and MDD 9/16 versus the static menu.
- **Dependencies**: C01
- **Tags**: router, risk-control

## C03: Frozen RL routing is research-only

- **Statement**: The first frozen tabular RL router does not supersede the static menu.
- **Status**: supported
- **Falsification criteria**: A future frozen RL policy satisfies the production gate in `docs/theory/case_lingxi_promotion_gate.md` on OOS data.
- **Proof**: E03
- **Evidence basis**: It wins annualized return 4/16, Sharpe 4/16, and MDD 6/16 on 2025-2026 YTD OOS.
- **Dependencies**: C01
- **Tags**: reinforcement-learning, negative-control

## C04: Structured market tags are an audit/context interface, not a production signal yet

- **Statement**: The first LLM-compatible market-tag router does not beat the production menu and should not be promoted.
- **Status**: supported
- **Falsification criteria**: Timestamped LLM debate tags or improved deterministic tags satisfy the production gate in `docs/theory/case_lingxi_promotion_gate.md` while preserving leakage constraints.
- **Proof**: E04
- **Evidence basis**: It wins annualized return 0/16, Sharpe 2/16, and MDD 7/16 versus the static menu.
- **Dependencies**: C01
- **Tags**: llm, market-context, ablation

## C05: Validation-only meta-selection is a named failure mode

- **Statement**: Selecting strategy sleeves by validation Sharpe alone is unstable and should be treated as a validation echo trap.
- **Status**: supported
- **Falsification criteria**: A validation-only selector repeatedly beats the static menu on independent future OOS windows.
- **Proof**: E05
- **Evidence basis**: The validation-only selector wins 2/16 in 2025, 0/16 in 2026 YTD, and 1/16 combined.
- **Dependencies**: none
- **Tags**: overfitting, validation-echo-trap
