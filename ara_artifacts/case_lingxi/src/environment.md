# Environment

Repository:

```text
https://github.com/gaoxingkele/Stock_benchmark
```

Local path used during artifact creation:

```text
C:\aicoding\Stock_benchmark
```

Core scripts:

```text
scripts/run_lingxi_sota_upgrade_validation.py
scripts/run_lingxi_pitnorm_tuned_gate_validation.py
scripts/run_lingxi_meta_selector_validation.py
scripts/run_case_lingxi_context_router.py
scripts/run_case_lingxi_rl_router_baseline.py
scripts/run_case_lingxi_llm_tag_ablation.py
```

Core reports:

```text
docs/reports/benchmark_master_table.md
docs/reports/case_lingxi_context_router_validation.md
docs/reports/case_lingxi_rl_router_validation.md
docs/reports/case_lingxi_llm_tag_ablation.md
docs/theory/case_lingxi_framework.md
docs/design/case_lingxi_execution_plan.md
```

Primary result directories:

```text
experiments/lingxi_sota_upgrade_validation/
experiments/lingxi_pitnorm_tuned_gate_validation_2026_ytd/
experiments/case_lingxi_context_router_validation_2026_ytd/
experiments/case_lingxi_rl_router_validation_2025_2026_ytd/
experiments/case_lingxi_llm_tag_ablation_2026_ytd/
experiments/lingxi_meta_selector_validation/
```

Validation command for this ARA:

```powershell
python C:/Users/xmupt/.codex/skills/ara-paper/scripts/validate_ara.py ara_artifacts/case_lingxi
```

