# Constraints

## Platform constraints

WorldQuant BRAIN is a closed platform. Its fields, simulations, submission statuses, and PnL outputs may depend on account state and platform rules.

The public repository must not include:

1. usernames or passwords;
2. cookies or sessions;
3. alpha IDs;
4. raw private expressions submitted to BRAIN;
5. raw daily PnL series;
6. account-linked accepted or rejected submission records.

## Evidence constraints

Sanitized aggregates can support research-loop claims but cannot prove that another user will reproduce the same BRAIN acceptances.

Public proxy runs can support reproducibility claims but cannot prove WQ platform performance.

## Comparison constraints

CASE-Lingxi and WQ-style alpha mining operate at different layers. A fair comparison must avoid these invalid shortcuts:

1. comparing Spectacular count directly to annualized portfolio return;
2. treating WQ acceptance as live-trading readiness;
3. treating a proxy factor IC result as equivalent to a WorldQuant submission;
4. using LLM-generated lessons after seeing OOS results without freezing them before evaluation.
