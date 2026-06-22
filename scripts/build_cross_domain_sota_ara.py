"""Build ARA packages for cross-domain time-series SOTA candidates."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "papers/metadata/lingxi_cross_domain_ts_sota_candidates.csv"
DATASETS = ROOT / "papers/metadata/lingxi_cross_domain_ts_datasets.csv"
OUT_ROOT = ROOT / "ara_artifacts"


METHOD_SUMMARIES = {
    "patch_transformer": "Patch-token sequence modeling for long-context time-series forecasting.",
    "periodicity_2d_variation": "Temporal 2D variation modeling for multi-period time-series patterns.",
    "variate_attention": "Inverted attention over variate tokens for cross-variable representation.",
    "multiscale_mlp": "Decomposable multi-scale temporal mixing with efficient MLP blocks.",
    "multiresolution_pattern_machine": "Universal multi-resolution pattern modeling for time-series prediction.",
    "nonstationarity_correction": "Stationarization and de-stationary attention for shifted time-series distributions.",
    "frequency_decomposition": "Trend/seasonal decomposition with Fourier or wavelet frequency modules.",
    "hierarchical_interpolation": "Hierarchical interpolation and multi-rate sampling for long-horizon forecasting.",
    "decomposition_linear": "Simple seasonal-trend decomposition plus linear forecasting.",
    "foundation_forecaster": "Large pre-trained time-series foundation forecaster.",
    "tokenized_foundation_model": "Quantized value-token time-series language modeling.",
    "universal_forecasting_transformer": "Universal probabilistic transformer across heterogeneous time-series.",
    "foundation_model_multitask": "General-purpose pre-trained model across time-series tasks.",
    "tiny_pretrained_ts_model": "Compact pre-trained multivariate time-series model.",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def datasets_for(candidate_id: str, datasets: list[dict[str, str]]) -> list[dict[str, str]]:
    return [row for row in datasets if candidate_id in row["used_by_candidate_ids"].split(";")]


def keywords(row: dict[str, str]) -> str:
    items = [
        "time-series",
        row["method_family"].replace("_", "-"),
        "forecasting",
        "Lingxi-upgrade",
        "TopK-ranking",
        "ARA",
    ]
    return "[" + ", ".join(json.dumps(item) for item in items) + "]"


def build_paper(row: dict[str, str], dataset_rows: list[dict[str, str]]) -> str:
    dataset_names = ", ".join(ds["name"] for ds in dataset_rows) or "Not specified in provided sources"
    abstract = (
        f"Methodology-focused ARA package for {row['title']}. This package is compiled from the local "
        "SOTA survey metadata and source URL, and is intended to guide Lingxi10/Lingxi5 upgrade validation. "
        "It is not an official reproduction of the paper."
    )
    return f"""
---
title: "{row['title']}"
authors: ["Not specified in provided sources"]
year: {row['year']}
venue: "{row['venue_or_status']}"
doi: "{row['source_url']}"
ara_version: "1.0"
domain: "cross-domain time-series methodology"
keywords: {keywords(row)}
claims_summary:
  - "{row['title']} contributes a {row['method_family']} method family relevant to time-series modeling."
  - "The method is a candidate source for {row['primary_lingxi_use']}."
abstract: "{abstract}"
---

# {row['title']}

## Overview

This ARA captures the paper as a methodology source for continuous Lingxi10/Lingxi5 upgrades. The local repository has not yet run the official implementation. The package therefore separates source-grounded metadata from proposed local validation work.

Primary Lingxi use: `{row['primary_lingxi_use']}`.

Datasets registered for comparison: {dataset_names}.

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Methodology gap and Lingxi relevance |
| [claims.md](logic/claims.md) | Falsifiable local-transfer claims |
| [concepts.md](logic/concepts.md) | Method concepts and boundaries |
| [experiments.md](logic/experiments.md) | Local validation plans |
| [related_work.md](logic/related_work.md) | Relationship to Lingxi and 31-paper ARA pool |
| [solution/constraints.md](logic/solution/constraints.md) | Transfer constraints and limitations |
| [solution/method.md](logic/solution/method.md) | Method summary and proposed proxy |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | Local software/data assumptions | C01, C02 |

### Data Layer (`/data`)
| File | Description |
|------|-------------|
| [dataset.md](data/dataset.md) | Registered datasets mentioned in the survey metadata |
| [preprocessing.md](data/preprocessing.md) | Point-in-time preprocessing constraints |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | Research DAG |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Evidence index |
| [source/source_overview.md](evidence/source/source_overview.md) | Source and local metadata |
| [runs/local_validation.md](evidence/runs/local_validation.md) | Current validation status |
"""


def build_problem(row: dict[str, str]) -> str:
    return f"""
# Problem Specification

## Observations

### O1: Lingxi10 and Lingxi5 need method-level upgrades, not blind ensembling
- **Statement**: Prior Qlib/FinTSB fusion did not justify replacing Lingxi10, so new methods must be tested as targeted modules.
- **Evidence**: `docs/reports/lingxi_fusion_upgrade_validation.md`
- **Implication**: {row['title']} should be translated into a falsifiable proxy module before any production claim.

### O2: The paper belongs to the `{row['method_family']}` family
- **Statement**: Local survey metadata classifies this candidate as `{row['method_family']}`.
- **Evidence**: `papers/metadata/lingxi_cross_domain_ts_sota_candidates.csv`
- **Implication**: The first local validation should test the corresponding Lingxi transfer idea: `{row['primary_lingxi_use']}`.

## Gaps

### G1: Official reproduction is not yet present
- **Statement**: The repository has not yet imported official code or exact hyperparameters for this candidate.
- **Caused by**: The current phase is method-selection and ARA engineering.
- **Existing attempts**: SOTA survey and Claude CLI ranking.
- **Why they fail**: A survey is not evidence that the method improves Top10/Top5 trading.

## Key Insight
- **Insight**: Treat cross-domain time-series SOTA as modular Lingxi upgrades and require them to beat Lingxi10/Lingxi5 under the existing trading protocol.
- **Derived from**: O1, O2
- **Enables**: A staged validation plan that avoids overfitting to generic forecasting benchmarks.

## Assumptions
- A1: OHLCV panels are sufficient for first-pass proxy validation.
- A2: Point-in-time feature construction is mandatory.
- A3: Generic forecasting improvements do not automatically transfer to TopK stock ranking.
"""


def build_claims(row: dict[str, str]) -> str:
    return f"""
# Claims

## C01: Candidate methodology is relevant to Lingxi upgrade design
- **Statement**: `{row['title']}` is a relevant source for the local upgrade idea `{row['primary_lingxi_use']}`.
- **Status**: hypothesis
- **Falsification criteria**: A local proxy based on this method fails to beat `Lingxi-LinearGuard` and provides no improvement over Lingxi10 or Lingxi5 in any market/variant.
- **Proof**: [E01, E02]
- **Evidence basis**: Local survey metadata and planned validation matrix.
- **Interpretation**: Relevance is methodological, not yet performance-proven.
- **Dependencies**: none
- **Tags**: methodology-transfer, Lingxi-upgrade

## C02: The method should not replace Lingxi without local trading evidence
- **Statement**: This method cannot be promoted over Lingxi10/Lingxi5 until it passes the repository's H5 Top10/Top5 multi-market protocol.
- **Status**: supported
- **Falsification criteria**: A completed local run shows consistent improvement according to the decision gates in `docs/reports/lingxi10_lingxi5_sota_upgrade_survey.md`.
- **Proof**: [E02]
- **Evidence basis**: Prior fusion validation showed external runner-up signals can degrade A-share performance.
- **Interpretation**: Conservative gating is required before strategy changes.
- **Dependencies**: C01
- **Tags**: trading-validation, risk-control
"""


def build_concepts(row: dict[str, str]) -> str:
    summary = METHOD_SUMMARIES.get(row["method_family"], "Not specified in provided sources")
    return f"""
# Concepts

## {row['method_family']}
- **Notation**: Not specified in provided sources
- **Definition**: {summary}
- **Boundary conditions**: Must be implemented with point-in-time features before use in Lingxi validation.
- **Related concepts**: Lingxi10, Lingxi5, H5 TopK ranking

## Lingxi transfer proxy
- **Notation**: Not specified in provided sources
- **Definition**: A lightweight local approximation of the paper's method idea, evaluated under the same trading protocol as Lingxi10/Lingxi5.
- **Boundary conditions**: It is not an official implementation unless official code and configs are imported.
- **Related concepts**: ARA engineering, cross-market validation
"""


def build_experiments(row: dict[str, str]) -> str:
    return f"""
# Experiments

## E01: ARA source and dataset audit
- **Verifies**: C01
- **Setup**:
  - Model: `{row['candidate_id']}` methodology audit
  - Hardware: n/a
  - Dataset: source metadata and registered benchmark datasets
  - System: local repository metadata
- **Procedure**:
  1. Confirm source URL, method family, and candidate Lingxi use.
  2. Map paper-mentioned benchmark datasets to local download or documented-only status.
- **Metrics**: ARA Level 1 validation pass/fail; dataset registry completeness.
- **Expected outcome**:
  - The ARA package has complete mandatory layers.
  - Downloadable small datasets are separated from large documented-only datasets.
- **Baselines**: existing 31-paper ARA pool
- **Dependencies**: none

## E02: Lingxi10/Lingxi5 proxy validation
- **Verifies**: C01, C02
- **Setup**:
  - Model: `{row['primary_lingxi_use']}` proxy
  - Hardware: CPU-first local run
  - Dataset: China A-share, US large cap, HK large cap, crypto major
  - System: H5 Top10/Top5 equal-weight daily protocol
- **Procedure**:
  1. Implement a point-in-time proxy for the method family.
  2. Score all symbols on the same test period as existing Lingxi validation.
  3. Compare raw and neutral variants against Lingxi10, Lingxi5, and LinearGuard.
- **Metrics**: annualized return, Sharpe, maximum drawdown, active Sharpe, turnover, hit rate.
- **Expected outcome**:
  - The candidate is promoted only if it passes the decision gates in the SOTA survey report.
- **Baselines**: Lingxi10, Lingxi5, Lingxi-LinearGuard
- **Dependencies**: E01
"""


def build_method(row: dict[str, str]) -> str:
    return f"""
# Method Summary

- **Paper ID**: `{row['candidate_id']}`
- **Title**: {row['title']}
- **Method family**: `{row['method_family']}`
- **Venue/status**: {row['venue_or_status']}
- **Source URL**: {row['source_url']}
- **Lingxi transfer target**: {row['primary_lingxi_use']}
- **Local priority**: {row['priority']}

## Proposed Local Proxy

The first local implementation should translate the method into a CPU-first score generator over existing OHLCV panels. The proxy must be evaluated as an auxiliary or replacement score for Lingxi10/Lingxi5, not as a generic forecasting benchmark only.

## Official Implementation Status

Not imported in the current repository. Any future official-code reproduction must be added as a separate experiment with explicit environment and config evidence.
"""


def build_constraints(row: dict[str, str]) -> str:
    return f"""
# Constraints

## Boundary Conditions

- The package is a methodology-transfer ARA, not an official reproduction.
- The source URL is recorded, but full paper table/figure extraction has not yet been performed.
- Exact paper hyperparameters are `Not specified in provided sources` unless later extracted from the paper or official code.
- Local trading claims require H5 Top10/Top5 validation on China A-share, US, HK, and crypto.

## Lingxi-Specific Limitations

- A generic forecasting objective may not improve cross-sectional stock ranking.
- Any module that hurts China A-share cannot replace the default Lingxi10 strategy.
- Heavy foundation-model inference must remain optional until a lightweight proxy demonstrates value.
"""


def build_related(row: dict[str, str]) -> str:
    return f"""
# Related Work

## RW01: Existing 31-paper finance ARA pool
- **DOI**: local ARA registry
- **Type**: baseline
- **Delta**:
  - What changed: `{row['title']}` is added as cross-domain time-series methodology, not finance-specific prior art.
  - Why: The user requested 2020+ SOTA ideas beyond financial tasks for Lingxi upgrades.
- **Claims affected**: C01, C02
- **Adopted elements**: ARA engineering protocol and local H5 TopK validation discipline.

## RW02: Lingxi-Fusion validation
- **DOI**: local report
- **Type**: bounds
- **Delta**:
  - What changed: Prior Qlib/FinTSB fusion showed fixed auxiliary signals can degrade A-share performance.
  - Why: It motivates gated, module-level validation for `{row['method_family']}`.
- **Claims affected**: C02
- **Adopted elements**: Multi-market raw/neutral validation and conservative promotion gates.
"""


def build_environment(row: dict[str, str], dataset_rows: list[dict[str, str]]) -> str:
    data = "\n".join(f"- {ds['name']}: {ds['local_target']} ({ds['download_status']})" for ds in dataset_rows) or "- Not specified"
    return f"""
# Environment

- **Language/runtime**: Python 3 local repository environment
- **Framework**: pandas/numpy for first-pass proxy validation; official framework not yet imported
- **Hardware**: CPU-first for proxy validation; GPU requirements not specified in provided sources
- **Data sources**:
{data}
- **Key dependencies**: repository default Python dependencies
- **Protocols**: H5 Top10/Top5 equal-weight long-only daily rebalance; single-side 10 bps cost
- **Random seeds**: repository default seed 42 when applicable
"""


def build_dataset(row: dict[str, str], dataset_rows: list[dict[str, str]]) -> str:
    lines = [
        "# Dataset Registry",
        "",
        "The following datasets are registered from the cross-domain SOTA survey metadata. Download status is separated from paper claims.",
        "",
        "| Dataset | Task | Source | Local target | Status | Notes |",
        "|---|---|---|---|---|---|",
    ]
    for ds in dataset_rows:
        lines.append(
            f"| {ds['name']} | {ds['task_type']} | {ds['source_url']} | {ds['local_target']} | {ds['download_status']} | {ds['notes']} |"
        )
    if not dataset_rows:
        lines.append("| Not specified | Not specified | Not specified | Not specified | Not specified | Not specified |")
    return "\n".join(lines)


def build_preprocessing() -> str:
    return """
# Preprocessing

- Use only information available at or before the scoring date.
- Rolling normalization windows must not include future observations.
- Generic benchmark forecasting splits must not be mixed with stock trading evaluation unless clearly labeled.
- For Lingxi validation, features are recomputed from local OHLCV panels and evaluated through the existing trading backtester.
"""


def build_evidence(row: dict[str, str], dataset_rows: list[dict[str, str]]) -> tuple[str, str, str]:
    source = f"""
# Source Overview

| Field | Value |
|---|---|
| Candidate ID | `{row['candidate_id']}` |
| Title | {row['title']} |
| Year | {row['year']} |
| Venue/status | {row['venue_or_status']} |
| Method family | `{row['method_family']}` |
| Source URL | {row['source_url']} |
| Lingxi use | {row['primary_lingxi_use']} |
| Priority | {row['priority']} |

Source basis: `papers/metadata/lingxi_cross_domain_ts_sota_candidates.csv` and `papers/metadata/lingxi_cross_domain_ts_datasets.csv`.
"""
    local = f"""
# Local Validation Status

| Item | Status |
|---|---|
| ARA package generated | complete |
| Level 1 validation | pending until validator run |
| Official implementation imported | not yet |
| Local Lingxi proxy run | not yet |
| Registered datasets | {len(dataset_rows)} |

No local performance claim is made for `{row['candidate_id']}` until the proxy validation experiment is run.
"""
    readme = """
# Evidence Index

## Source Evidence
| File | Source | Claims | Description |
|---|---|---|---|
| [source/source_overview.md](source/source_overview.md) | Local candidate metadata | C01 | Source URL, method family, priority, and Lingxi transfer target |

## Run Evidence
| File | Source | Claims | Description |
|---|---|---|---|
| [runs/local_validation.md](runs/local_validation.md) | Local ARA generation status | C01, C02 | Current validation status and missing official/proxy runs |
"""
    return readme, source, local


def build_trace(row: dict[str, str]) -> str:
    return f"""
tree:
  - id: N01
    type: question
    support_level: inferred
    title: "Can {row['candidate_id']} inform Lingxi10/Lingxi5 upgrades?"
    description: "Assess whether the method family {row['method_family']} can become a local, point-in-time proxy module."
    children:
      - id: N02
        type: decision
        support_level: explicit
        source_refs: ["papers/metadata/lingxi_cross_domain_ts_sota_candidates.csv"]
        title: "Classify candidate method family"
        description: "The candidate is classified as {row['method_family']} with priority {row['priority']}."
      - id: N03
        type: experiment
        support_level: inferred
        title: "Run Lingxi proxy validation"
        description: "Future work: implement {row['primary_lingxi_use']} and compare against Lingxi10/Lingxi5."
"""


def build_all() -> None:
    candidates = read_csv(CANDIDATES)
    datasets = read_csv(DATASETS)
    summary_rows = []
    for row in candidates:
        out = OUT_ROOT / row["candidate_id"]
        ds_rows = datasets_for(row["candidate_id"], datasets)
        write(out / "PAPER.md", build_paper(row, ds_rows))
        write(out / "logic/problem.md", build_problem(row))
        write(out / "logic/claims.md", build_claims(row))
        write(out / "logic/concepts.md", build_concepts(row))
        write(out / "logic/experiments.md", build_experiments(row))
        write(out / "logic/related_work.md", build_related(row))
        write(out / "logic/solution/method.md", build_method(row))
        write(out / "logic/solution/constraints.md", build_constraints(row))
        write(out / "src/environment.md", build_environment(row, ds_rows))
        write(out / "data/dataset.md", build_dataset(row, ds_rows))
        write(out / "data/preprocessing.md", build_preprocessing())
        evidence_readme, source, local = build_evidence(row, ds_rows)
        write(out / "evidence/README.md", evidence_readme)
        write(out / "evidence/source/source_overview.md", source)
        write(out / "evidence/runs/local_validation.md", local)
        write(out / "trace/exploration_tree.yaml", build_trace(row))
        summary_rows.append(
            {
                "candidate_id": row["candidate_id"],
                "artifact_dir": str(out.relative_to(ROOT)),
                "method_family": row["method_family"],
                "priority": row["priority"],
                "dataset_count": str(len(ds_rows)),
                "ara_dir_exists": "True",
            }
        )

    summary = OUT_ROOT / "cross_domain_sota_ara_summary.csv"
    with summary.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(summary_rows[0]))
        writer.writeheader()
        writer.writerows(summary_rows)
    print(f"generated={len(summary_rows)} summary={summary}")


if __name__ == "__main__":
    build_all()
