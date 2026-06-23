# FunctionEvolve/SIA/Godel Feedback Report

Date: 2026-06-23

This report records how the newly reviewed self-improvement and symbolic-evolution papers can feed back into WQ Alpha Evolution and Lingxi.

## Reviewed Sources

1. `arXiv:2410.04444`, **Godel Agent: A Self-Referential Agent Framework for Recursive Self-Improvement**
   - Useful layer: research-agent self-improvement.
   - Lingxi use: allow agents to propose changes to research logic, but keep trading promotion behind frozen OOS gates.

2. `arXiv:2606.07704`, **FunctionEvolve: Structure-Guided Symbolic Regression with LLMs**
   - Useful layer: factor-expression evolution.
   - Lingxi use: replace string-style factor generation with AST-structured search, local mutation, structural diversity, and explicit promotion gates.

3. `https://github.com/Phoinikas03/FunctionEvolve`
   - Useful layer: engineering reference for expression-tree generation, selection, mutation, and scoring.

4. `https://github.com/hexo-ai/sia`
   - Useful layer: self-improving harness architecture.
   - Lingxi use: separate Meta-Agent, Target Agent, and Feedback Agent around the experiment harness.

## Implemented Proxy Experiment

Script:

```powershell
python scripts\run_wq_functionevolve_proxy.py --max-candidates 18 --promotion-top 5 --max-symbols 25
```

Outputs:

```text
experiments/wq_functionevolve_proxy/functionevolve_proxy_summary.csv
experiments/wq_functionevolve_proxy/functionevolve_proxy_detail.csv
```

Current result:

| Metric | Value |
|---|---:|
| Candidate factors | 18 |
| Valid factors | 18 |
| Promoted factors | 1 |
| Promoted mean IC | 0.00963685 |
| Promoted rank IC | 0.02061124 |
| Promoted rank ICIR | 0.07696077 |
| Promoted turnover | 0.73185391 |
| Promoted long-short return | 0.00312373 |
| Promoted cost-adjusted return | 0.00239188 |
| Promoted max drawdown | -0.69279312 |

Interpretation:

The first public proxy run proves that FunctionEvolve-style AST factor search can be wired into the repository as a reproducible, privacy-safe experiment. The promoted factor is not production-ready because drawdown remains severe and the experiment is a small smoke-scale proxy, but it supplies the missing empirical bridge between WQ-style alpha evolution and Lingxi.

## Feedback Into Lingxi

Immediate transferable ideas:

1. Use AST factor representation instead of raw strings.
2. Preserve useful subexpressions across search rounds.
3. Select structurally diverse parents instead of only top IC parents.
4. Add pre-promotion correlation gates.
5. Freeze memory and candidate pools before OOS evaluation.
6. Treat Meta/Target/Feedback agents as research-loop components, not direct trade routers.

Implemented next empirical step:

`Lingxi-FunctionEvolve-Memory` has been implemented as a research-only sleeve:

1. generate AST proxy factors on the training window;
2. promote only factors passing IC, turnover, cost, and novelty gates;
3. blend promoted factors into Lingxi5/Lingxi10 scoring;
4. compare against current Lingxi5/Lingxi10 and CASE-Lingxi static menu under the existing promotion audit.

Current blend report:

```text
docs/reports/lingxi_functionevolve_blend.md
```

## Current Decision

FunctionEvolve is the highest-priority method to operationalize for factor evolution. SIA and Godel Agent should guide the self-improving research harness and ARA trace, but they should not be allowed to directly route trades without frozen OOS proof.
