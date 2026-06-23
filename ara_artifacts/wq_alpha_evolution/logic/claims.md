# Claims

## C1: Layer-aware comparison is required

Statement:
WorldQuant-style alpha-mining skills and CASE-Lingxi should not be compared only by annualized return because one system discovers alpha expressions and the other selects strategy sleeves.

Required evidence:

1. `E-WQ-PROTOCOL`: experiment protocol showing separate loop-efficiency and trading-proxy metrics.
2. `E-CASE-LINGXI`: existing CASE-Lingxi completion audit and bundle validation.

Status:
Protocol supported. Empirical WQ results are not yet committed.

Falsification:
A future artifact may falsify this if both systems are converted into the same executable portfolio protocol with identical data, costs, universe, and OOS period.

Proof:
Current proof is protocol-level: the comparison plan separates alpha-discovery, strategy-routing, and ARA-audit layers.

## C2: Self-evolution can be evaluated without leaking private alpha records

Statement:
The evolution loop can be assessed through sanitized aggregates: candidate count, simulation success rate, failure taxonomy, pass rate, self-correlation rejection rate, and lesson adoption rate.

Required evidence:

1. `E-WQ-SCHEMA`: sanitized WQ schema.
2. `E-WQ-PRIVATE-RUN`: future locally stored or private aggregate run table.

Status:
Schema supported. Private empirical run not present.

Falsification:
This claim fails if sanitized aggregates cannot distinguish improved learning from repeated random search.

Proof:
Current proof is schema-level only.

## C3: ARA engineering adds scientific value

Statement:
ARA adds value by binding claims to evidence, preserving rejected paths, separating private and public evidence, and making future runs comparable.

Required evidence:

1. `E-ARA-STRUCTURE`: Level 1 ARA validation pass.
2. `E-TRACE`: exploration tree containing rejected shortcuts.

Status:
Pending validation until the bundle validator is run.

Falsification:
This claim fails if Level 1 validation fails or if claims cannot be mapped to evidence files.

Proof:
Proof requires `scripts/validate_wq_alpha_evolution_bundle.py` to pass.

## C4: CASE-Lingxi can absorb useful WQ-style ideas

Statement:
The WQ self-evolution loop contributes reusable ideas to Lingxi: failure-memory, correlation-aware novelty checks, loop-level promotion gates, and research-rule distillation.

Required evidence:

1. `E-CROSS-FRAMEWORK`: cross-framework comparison schema and design report.
2. `E-FUTURE-ABLATION`: future Lingxi ablation with WQ-style memory components.

Status:
Design supported. Empirical ablation not yet present.

Falsification:
This claim fails empirically if a frozen Lingxi memory-ablation does not improve promotion-gate metrics.

Proof:
Current proof is design-level only; empirical proof requires `E-FUTURE-ABLATION`.
