# Stock Benchmark

This workspace is for benchmarking recent stock/index trend prediction and alpha factor mining papers.

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

