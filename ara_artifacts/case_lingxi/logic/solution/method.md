# Method

CASE-Lingxi has four layers.

## 1. Production Menu

The production layer uses the current Lingxi Adaptive Suite:

1. A-share Top10/Top5: Lingxi, with PITNorm as risk-control candidate for raw portfolios.
2. US large cap Top10: PITNorm may be used as risk control; US Top5 remains Lingxi.
3. HK Top10/Top5: PITNorm.
4. Crypto Top10/Top5 raw: Lingxi or ReturnFloor-gated Lingxi.

## 2. Candidate Router Layer

Candidate routers may choose only from approved sleeves:

1. `lingxi`
2. `lingxi_pitnorm`
3. `lingxi_pitnorm_gate_return_floor`

Routers are not allowed to select individual stocks directly.

## 3. Agentic Research Layer

Agents may:

1. propose strategy candidates;
2. generate market-context tags;
3. write experiments;
4. critique leakage and overfitting;
5. update ARA memory.

Agents may not:

1. bypass frozen OOS validation;
2. promote a strategy by narrative plausibility;
3. directly emit production trades.

## 4. Conservative Promotion Gate

A candidate enters production only when it beats the static menu under:

1. transaction costs;
2. frozen OOS periods;
3. scenario breadth appropriate to the claim;
4. acceptable drawdown and turnover behavior.

Current evidence does not promote context router, RL router, or structured market-tag router.

The current numeric gate is maintained in:

```text
docs/theory/case_lingxi_promotion_gate.md
```
