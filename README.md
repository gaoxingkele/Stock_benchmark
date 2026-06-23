# Stock Benchmark

This workspace is for benchmarking recent stock/index trend prediction and alpha factor mining papers.

## Current Best Result: Lingxi Adaptive Suite

The current best validated solution is **Lingxi Adaptive Suite**, a conservative scenario-specific strategy menu rather than a universal dynamic router.

Main production conclusion:

- Use fixed/scene-specific sleeves as the production proxy.
- Keep dynamic routers only as research sleeves where repeated evidence supports them.
- Do not use validation-Sharpe meta-selection or direct LLM routing for production decisions.

Recommended production proxy by market:

| Market | Scenario | Recommended proxy |
|---|---|---|
| China A-share | raw Top10/Top5 | Lingxi |
| China A-share | neutral Top10/Top5 | Lingxi; dynamic routers only as research sleeves |
| US large cap | Top10/Top5 | Fixed/static baselines: PITNorm, ReturnFloor-Gate, static ensemble, or Lingxi depending scenario |
| HK large cap | Top10/Top5 | PITNorm |
| Crypto major | raw Top10/Top5 | ReturnFloor-Gate |
| Crypto major | neutral Top10/Top5 | Lingxi or PITNorm; no production dynamic router |

Key validation result:

- Adaptive router: useful in a few cases, not a global replacement.
- Market-regime router: beats contextual ridge in some cases, but only beats fixed/static baselines in 2/16 scenarios.
- Sparse/feature-capped regime router: improves over dynamic routers, but only beats fixed/static baselines in 3/16 scenarios.
- Validation-only meta-selector: rejected. It wins 2/16 in 2025, 0/16 in 2026 YTD, and 1/16 in combined 2025-2026 YTD.

Primary documents:

- Final suite: `docs/strategies/lingxi_adaptive_suite.md`
- Router strategy notes: `docs/strategies/lingxi_adaptive_router.md`
- Project memory: `PROJECT_MEMORY.md`
- Meta-selector rejection report: `docs/reports/lingxi_meta_selector_validation.md`

Important latest commits:

- `fc9066b` Validate Lingxi meta selector
- `c01aab6` Validate sparse Lingxi regime router
- `cf7d842` Validate market-regime Lingxi router
- `2728e7c` Validate Lingxi adaptive router
- `546ad2f` Validate tuned PITNorm gates for Lingxi

To recover the latest research state after cloning:

```powershell
git clone https://github.com/gaoxingkele/Stock_benchmark
cd Stock_benchmark
git checkout main
git log --oneline -5
```

Then read `PROJECT_MEMORY.md` and `docs/strategies/lingxi_adaptive_suite.md`.

## Directory Map

```text
Stock_benchmark/
  configs/                 Shared benchmark, dataset, model, and experiment configs.
  data/                    Shared local data area. Keep large/raw data out of git.
  docs/                    Academic notes, discussions, comparison tables, and reports.
  env/                     Environment files and reproducibility notes.
  experiments/             Runnable experiment definitions and result summaries.
  external_repos/          Cloned upstream GitHub repositories, one repo per directory.
  factor_lab/              Shared alpha factor mining, validation, and factor library code.
  notebooks/               Exploratory analysis notebooks.
  paper_projects/          One independent project directory per paper.
  papers/                  Downloaded PDFs, metadata, BibTeX, and extracted text.
  scripts/                 Utility scripts for downloading, preprocessing, and running jobs.
  src/                     Shared benchmark code used across paper implementations.
  tests/                   Tests for shared benchmark utilities.
```

## Workflow

1. Register candidate papers in `papers/metadata/paper_registry.csv`.
2. Download PDFs into `papers/raw/`.
3. Create one project from `paper_projects/_template/` for each selected paper.
4. If a paper has an official or strong community GitHub repo, clone it into `external_repos/`.
5. Analyze each repo in its matching paper project under `repo_analysis.md`.
6. Reimplement missing methods under the paper project while reusing shared code in `src/`.
7. Run comparable experiments through `experiments/` and write results into `docs/reports/`.

## Naming Convention

Use stable paper IDs:

```text
YYYY_short_title_first_author
```

Example:

```text
2023_stocknet_zhang
```

Use stable GitHub repo IDs:

```text
owner__repo
```

Example:

```text
microsoft__qlib
```
