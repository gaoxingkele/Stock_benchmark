# WQ Alpha Evolution Comparison Plan

Date: 2026-06-23

This report turns the WorldQuant self-evolving alpha-mining idea into an executable comparison plan against CASE-Lingxi.

## Decision

Build a separate ARA project:

```text
ara_artifacts/wq_alpha_evolution/
```

Do not merge raw WorldQuant outputs into the Lingxi benchmark. WorldQuant BRAIN is a closed platform and any account-linked alpha IDs, expressions, credentials, and PnL records must remain private.

## Systems To Compare

| System | Layer | Current status | Valid comparison target |
|---|---|---|---|
| WQ alpha research skill | Alpha expression discovery | External open-source skill, private WQ execution optional | Research-loop efficiency |
| ARA-WQ Alpha Evolution | ARA protocol and proxy harness | Added as protocol ARA | Reproducibility and auditability |
| CASE-Lingxi | Strategy selection and routing | Existing validated local ARA | Strategy-level OOS performance |
| Future Lingxi memory upgrade | Hybrid research-loop plus strategy routing | Planned | Whether WQ-style memory improves Lingxi promotion gates |

## Required Experiments

### Experiment 1: Sanitized WQ Run

Input:
Private run logs from a local WorldQuant BRAIN session.

Output:
Aggregate table matching:

```text
ara_artifacts/wq_alpha_evolution/evidence/schemas/sanitized_wq_run_schema.csv
```

Primary metrics:

1. candidate-to-simulation success rate;
2. candidate-to-accepted rate;
3. spectacular rate;
4. self-correlation failure rate;
5. lesson reuse rate;
6. failure mix by run segment.

Acceptance:
The table contains no alpha IDs, raw expressions, raw PnL, credentials, cookies, or account-linked records.

### Experiment 2: Public Proxy Factor-Mining Run

Input:
Public or repository-managed market panels.

Output:
Aggregate table matching:

```text
ara_artifacts/wq_alpha_evolution/evidence/schemas/proxy_factor_run_schema.csv
```

Primary metrics:

1. OOS IC and ICIR;
2. OOS rank IC and rank ICIR;
3. turnover;
4. cost-adjusted long-short return;
5. max drawdown;
6. maximum correlation to previously promoted factors.

Acceptance:
The generation memory and promotion gate must be frozen before OOS evaluation.

### Experiment 3: Cross-Framework Comparison

Input:

1. sanitized WQ run summary;
2. public proxy factor-mining summary;
3. existing CASE-Lingxi validation summaries;
4. CASE-Lingxi completion audit.

Output:
Table matching:

```text
ara_artifacts/wq_alpha_evolution/evidence/schemas/cross_framework_comparison_schema.csv
```

Interpretation:
The WQ skill can beat CASE-Lingxi only on research-loop metrics unless a public proxy or private audited strategy backtest proves strategy-level superiority.

## Promotion Rules

1. A WQ-derived result can be called a strong alpha-discovery result if sanitized WQ metrics show high accepted rate, low repeated failure rate, and high lesson reuse.
2. It can be called reproducible only if a public proxy run reproduces the discovery-loop advantage.
3. It can influence Lingxi only if a frozen OOS ablation shows improved Lingxi Top5/Top10 or router promotion metrics.
4. It cannot be called a production trading strategy from WQ acceptance alone.

## Current Completion State

Completed in this repository:

1. independent ARA scaffold;
2. claim/evidence map;
3. privacy constraints;
4. sanitized CSV schemas;
5. cross-framework comparison protocol;
6. current layer-aware baseline comparison table;
7. bundle validator.

Current baseline table:

```text
ara_artifacts/wq_alpha_evolution/evidence/current_cross_framework_comparison.csv
```

Not yet completed:

1. private sanitized WQ empirical run;
2. public proxy factor-mining run;
3. Lingxi memory-ablation implementation.

These are empirical follow-up experiments, not blockers for the current comparison-plan artifact.
