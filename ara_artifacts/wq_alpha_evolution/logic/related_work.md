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

## Newly Added Self-Evolution References

1. **Godel Agent: A Self-Referential Agent Framework for Recursive Self-Improvement** (`arXiv:2410.04444`)
   - Relevance: high-level recursive self-improvement framework for research agents.
   - Use in this repository: constrain self-modifying research logic with ARA trace and frozen OOS gates.

2. **FunctionEvolve: Structure-Guided Symbolic Regression with LLMs** (`arXiv:2606.07704`)
   - Relevance: AST-based symbolic search with structural diversity, local mutation, and structure-aware scoring.
   - Use in this repository: public proxy factor-mining experiment implemented in `scripts/run_wq_functionevolve_proxy.py`.

3. **FunctionEvolve GitHub implementation** (`Phoinikas03/FunctionEvolve`)
   - Relevance: engineering reference for expression-tree evolution.
   - Use in this repository: informs the AST candidate representation and structural metadata in the proxy run.

4. **SIA** (`hexo-ai/sia`)
   - Relevance: self-improving AI harness with Meta, Target, and Feedback agents.
   - Use in this repository: informs the proposed Lingxi research-loop upgrade, not direct trading.
