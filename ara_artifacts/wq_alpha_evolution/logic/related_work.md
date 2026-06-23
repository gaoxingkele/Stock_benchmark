# Related Work

## Primary external repositories

1. `QuantML-Research/wq-alpha-research`
   - Public GitHub repository checked on 2026-06-23.
   - Describes a self-evolving WorldQuant BRAIN alpha research skill.
   - Scope: field lookup, FASTEXPR construction, simulation/submission workflow, IS diagnostics, self-correlation handling, and skill evolution from run feedback.

2. `QuantaAlpha/QuantaAlpha`
   - Public GitHub repository checked on 2026-06-23.
   - Describes LLM-driven factor mining with evolutionary trajectories.
   - Useful as a broader comparison point for self-evolving factor discovery systems.

3. Existing WorldQuant automation repositories
   - Several public repositories automate BRAIN submission or alpha expression workflows.
   - They are useful engineering references but usually lack ARA-style claim/evidence binding.

## Internal related work

1. `ara_artifacts/case_lingxi/`
   - Existing ARA for Conservative Agentic Strategy Evolution for Lingxi.
   - Provides the strategy-level comparison target.

2. `docs/design/case_lingxi_execution_plan.md`
   - Completed plan for CASE-Lingxi.

3. `docs/reports/case_lingxi_completion_audit.md`
   - Completion audit for the Lingxi project.

## Research gap

The missing piece is a layer-aware benchmark that compares:

1. alpha expression discovery systems;
2. strategy routing systems;
3. research-process ARA engineering.

This artifact addresses the gap at protocol level and prepares the repository for future empirical runs.
