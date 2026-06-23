# Experiments

## E01: Sanitized WQ run protocol

Verifies:
Claims C1 and C2.

Goal:
Measure a WorldQuant-style self-evolving skill without leaking private records.

Setup:
Use a private WorldQuant BRAIN account and a local self-evolving skill run. Keep raw logs outside this repository.

Procedure:
Aggregate each run segment into the sanitized schema, then remove all account-linked records before committing.

Required table:
`evidence/schemas/sanitized_wq_run_schema.csv`

Template:
`evidence/templates/sanitized_wq_run_template.csv`

Validation:

```powershell
python scripts\validate_sanitized_wq_run.py path\to\sanitized_wq_run.csv
```

Metrics:

1. `candidate_count`
2. `simulation_success_count`
3. `submission_count`
4. `accepted_count`
5. `spectacular_count`
6. `invalid_field_count`
7. `turnover_fail_count`
8. `fitness_fail_count`
9. `self_correlation_fail_count`
10. `lesson_count`
11. `lesson_reused_count`

Gate:
The run is reportable only if each row is aggregated by date or run segment and contains no raw alpha IDs, expressions, or PnL series.

Expected:
If the self-evolution loop works, repeated failure rates should decline and lesson reuse should increase over later run segments.

Current result:
No private WQ empirical aggregate is committed. The repository contains a validator and template only.

## E02: Public proxy factor-mining loop

Verifies:
Claims C2 and C4.

Goal:
Run a local expression/factor search on public or repository-managed market panels.

Setup:
Use public or repository-managed market panels and freeze the generation memory before the OOS segment.

Procedure:
Generate candidate factors, filter invalid candidates, evaluate OOS IC/return/correlation metrics, then apply a predeclared promotion gate.

Required table:
`evidence/schemas/proxy_factor_run_schema.csv`

Current implementation:

```powershell
python scripts\run_wq_functionevolve_proxy.py --max-candidates 18 --promotion-top 5 --max-symbols 25
```

Current output:

```text
experiments/wq_functionevolve_proxy/functionevolve_proxy_summary.csv
experiments/wq_functionevolve_proxy/functionevolve_proxy_detail.csv
```

Candidate metrics:

1. IC mean and ICIR;
2. rank IC mean and rank ICIR;
3. turnover;
4. long-short return;
5. cost-adjusted return;
6. maximum drawdown;
7. correlation to previously accepted factors.

Gate:
A factor is promoted only if it passes OOS IC, turnover, cost, and novelty thresholds defined before the evaluation segment.

Expected:
Successful proxy runs should show better candidate efficiency or novelty control than a non-memory baseline.

Current result:
The smoke-scale public proxy generated 18 AST candidates, 18 valid factors, and 1 factor passing the strict OOS IC, cost-adjusted return, turnover, and novelty promotion gate. The result is research-only because the experiment is small-scale and the promoted factor still has severe drawdown.

Expanded result:
The 80-symbol aligned proxy run generated 18 AST candidates, 18 valid factors, and 2 promoted research-only factors: `zscore3(ret5(close))` and `zscore10(ret5(close))`.

## E03: WQ-vs-Lingxi comparison

Verifies:
Claims C1, C3, and C4.

Goal:
Compare the WQ-style skill, ARA-WQ protocol, and CASE-Lingxi without confusing research-loop quality with trading-strategy quality.

Setup:
Use sanitized WQ metrics if available, public proxy factor metrics if available, and existing CASE-Lingxi validation artifacts.

Procedure:
Fill the cross-framework comparison schema and label each result by layer and evidence type.

Required table:
`evidence/schemas/cross_framework_comparison_schema.csv`

Current table:
`evidence/current_cross_framework_comparison.csv`

Comparison axes:

1. layer: alpha discovery, strategy routing, or ARA audit;
2. loop autonomy;
3. reproducibility;
4. data openness;
5. failure-memory strength;
6. correlation-control strength;
7. production-readiness status.

Current baseline:
CASE-Lingxi is the existing local validated benchmark. Its validator is `scripts/validate_case_lingxi_bundle.py`.

Expected:
The comparison should identify which ideas are transferable to Lingxi without overstating WQ platform results.

## E04: Future Lingxi memory upgrade

Verifies:
Claim C4.

Goal:
Test whether WQ-style failure-memory and novelty checks improve Lingxi Top5/Top10 selection or router promotion gates.

Setup:
Add a frozen memory component to the Lingxi experiment scripts and compare against the current static menu and routers.

Procedure:
Train or build memory only before the OOS segment, run the same markets and costs, then evaluate promotion-gate metrics.

Current implementation:

```powershell
python scripts\run_lingxi_functionevolve_blend.py --max-symbols 80 --max-train-rows 50000
```

Current output:

```text
experiments/lingxi_functionevolve_blend/lingxi_functionevolve_blend_summary.csv
docs/reports/lingxi_functionevolve_blend.md
```

Expected:
If transferable, the memory upgrade should improve promotion-gate pass rates without increasing drawdown or correlation concentration.

Current result:
Smoke-scale evidence is positive for raw Lingxi5/Lingxi10 and mixed for neutral variants. The sleeve remains research-only until full-universe validation and promotion-audit checks pass.

Expanded result:
The 80-symbol aligned blend supports a conservative `0.15` FunctionEvolve-memory weight. It improves raw Lingxi5/Lingxi10 and neutral Lingxi5, while neutral Lingxi10 remains weak.

## E05: Self-improving research harness

Verifies:
Claims C3 and C4.

Goal:
Use SIA and Godel-Agent ideas to improve the research harness without allowing agents to directly route trades.

Setup:
Separate Meta-Agent, Target Agent, and Feedback Agent roles. All proposed harness or factor-search changes must be written to ARA trace and frozen before OOS evaluation.

Procedure:
Meta-Agent proposes the next research direction, Target Agent runs the experiment, Feedback Agent classifies failures and proposes rule updates. Rule updates are accepted only if later frozen OOS evidence improves the promotion gate.

Expected:
The harness should reduce repeated invalid or high-correlation factor attempts and make the research trace more reusable.
