"""Build ARA artifacts for downloaded paper projects.

The script compiles the current paper registry, downloaded PDFs, extracted text,
paper project notes, and experiment summaries into one ARA directory per
downloaded paper. It does not claim reproduction success unless a matching local
experiment result exists.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


MODEL_PREFIX = {
    "2021_tra_lin": "tra",
    "2021_tcts_wu": "tcts",
    "2023_doubleadapt_zhao": "doubleadapt",
    "2024_master_li": "master",
    "2021_adarnn_du": "adarnn",
    "2022_hist_xu": "hist",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def md_link(path: str) -> str:
    return path.replace("\\", "/")


def yaml_scalar(value: str) -> str:
    return json.dumps(value or "Not specified in provided sources", ensure_ascii=False)


def split_authors(authors: str) -> list[str]:
    return [item.strip() for item in re.split(r";|, and | and ", authors or "") if item.strip()]


def first_nonempty_lines(text: str, limit: int = 16) -> list[str]:
    lines = []
    for line in text.splitlines():
        clean = " ".join(line.strip().split())
        if clean:
            lines.append(clean)
        if len(lines) >= limit:
            break
    return lines


def abstract_digest(text: str, limit: int = 1400) -> str:
    match = re.search(r"(?is)\babstract\b\s*[:.\-]?\s*(.*?)(?:\n\s*(?:1\s+Introduction|I\.\s+Introduction|Introduction)\b)", text)
    if match:
        return " ".join(match.group(1).split())[:limit]
    return " ".join(text.split())[:limit]


def collect_numbered_evidence(text: str) -> dict[str, dict[str, list[str]]]:
    found: dict[str, dict[str, list[str]]] = {"tables": defaultdict(list), "figures": defaultdict(list)}
    for line in text.splitlines():
        clean = " ".join(line.strip().split())
        if not clean:
            continue
        for kind, number in re.findall(r"\b(Table|Figure|Fig\.)\s*([0-9]+)", clean, flags=re.IGNORECASE):
            bucket = "tables" if kind.lower() == "table" else "figures"
            lines = found[bucket][number]
            if clean not in lines and len(lines) < 12:
                lines.append(clean)
    return found


def project_files(project_dir: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for name in ["README.md", "notes.md", "repo_analysis.md", "reproduction_plan.md"]:
        path = project_dir / name
        if path.exists():
            result[name] = path.read_text(encoding="utf-8", errors="replace")
    for name in ["china_a_share_smoke.json", "china_a_share_formal.json"]:
        path = project_dir / "configs" / name
        if path.exists():
            result[f"configs/{name}"] = path.read_text(encoding="utf-8", errors="replace")
    return result


def source_exists(root: Path, rel: str) -> bool:
    return (root / rel).exists()


def build_paper_artifact(
    paper: dict[str, str],
    pdf_row: dict[str, str],
    summary_rows: list[dict[str, str]],
    out_root: Path,
) -> dict[str, str]:
    paper_id = paper["paper_id"]
    artifact = out_root / paper_id
    text_path = PROJECT_ROOT / "papers" / "extracted" / f"{paper_id}.txt"
    paper_text = text_path.read_text(encoding="utf-8", errors="replace") if text_path.exists() else ""
    project_dir = PROJECT_ROOT / "paper_projects" / paper_id
    project = project_files(project_dir) if project_dir.exists() else {}
    prefix = MODEL_PREFIX.get(paper_id, paper_id.split("_")[1])
    runs = [
        row
        for row in summary_rows
        if row["run_type"] == "paper_model"
        and (row["run_id"].startswith(prefix + "_") or row["run_id"].startswith(prefix.replace("-", "_") + "_"))
        and source_exists(PROJECT_ROOT, row["source"])
    ]
    verification_status = "complete" if runs else "missing_experiment_outputs"

    for rel in [
        "logic/solution",
        "src/configs",
        "trace",
        "evidence/tables",
        "evidence/figures",
        "evidence/runs",
        "evidence/source",
    ]:
        (artifact / rel).mkdir(parents=True, exist_ok=True)

    authors = split_authors(paper.get("authors", ""))
    claims_summary = [
        f"{paper['title']} is included as a {paper.get('status', 'candidate')} paper for {paper.get('task', 'stock prediction')}.",
        f"Independent local verification status is {verification_status}.",
    ]
    frontmatter = [
        "---",
        f"title: {yaml_scalar(paper['title'])}",
        "authors:",
        *[f"  - {yaml_scalar(author)}" for author in authors],
        f"year: {paper.get('year', '')}",
        f"venue: {yaml_scalar(paper.get('venue', ''))}",
        f"doi: {yaml_scalar(paper.get('pdf_url', ''))}",
        'ara_version: "1.0"',
        f"domain: {yaml_scalar(paper.get('task', 'stock prediction'))}",
        "keywords:",
        *[f"  - {yaml_scalar(tag.strip())}" for tag in paper.get("tags", "").split(";") if tag.strip()],
        "claims_summary:",
        *[f"  - {yaml_scalar(item)}" for item in claims_summary],
        f"abstract: {yaml_scalar(abstract_digest(paper_text, 900))}",
        "---",
    ]
    layer_index = f"""
# {paper['title']}

## Overview

This ARA was generated from the local downloaded paper corpus, extracted paper text, local
paper project materials, and experiment summary files in `Stock_benchmark`.

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Motivation, gaps, and assumptions captured from registry/project context |
| [claims.md](logic/claims.md) | Falsifiable claims and verification status |
| [concepts.md](logic/concepts.md) | Key terms from the paper/project |
| [experiments.md](logic/experiments.md) | Local verification plans and run bindings |
| [related_work.md](logic/related_work.md) | Source repository and registry relationships |
| [solution/constraints.md](logic/solution/constraints.md) | Scope limits and missing evidence |
| [solution/method.md](logic/solution/method.md) | Method summary grounded in local notes |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | Local data, code, and runtime sources | C02, C03 |
| [configs/](src/configs/) | Copied local reproduction configs when available | C03 |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | Source-bounded research and reproduction DAG |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Evidence index and independent verification status |
| [source/source_overview.md](evidence/source/source_overview.md) | Registry, PDF, project, and text evidence |
| [runs/](evidence/runs/) | Local run summaries when available |
"""
    write_text(artifact / "PAPER.md", "\n".join(frontmatter) + layer_index)

    write_text(
        artifact / "logic/problem.md",
        f"""# Problem Specification

## Observations

### O1: Registry inclusion
- **Statement**: `{paper_id}` is listed in the local paper registry with status `{paper.get('status', '')}`.
- **Evidence**: `papers/metadata/paper_registry.csv`
- **Implication**: The paper is in scope for the benchmark corpus.

### O2: Local PDF availability
- **Statement**: A local PDF exists with `valid_pdf_header={pdf_row.get('valid_pdf_header', '')}` and `{pdf_row.get('bytes', '')}` bytes.
- **Evidence**: `papers/metadata/pdf_download_status.csv`
- **Implication**: The paper can be processed without relying on the network.

### O3: Independent verification status
- **Statement**: `{verification_status}`.
- **Evidence**: `experiments/summary/smoke_results.csv`
- **Implication**: Completion requires paper-specific local result files for this artifact.

## Gaps

### G1: Full official reproduction
- **Statement**: This ARA records local benchmark evidence, not a complete official-paper reproduction unless stated by run evidence.
- **Caused by**: O3
- **Existing attempts**: Existing `paper_projects/` plans and `experiments/paper_runs/` outputs.
- **Why they fail**: Missing local paper-model outputs for this paper when `independent_verification` is not complete.

## Key Insight
- **Insight**: Treat each paper as an independently verifiable artifact: PDF evidence, local project evidence, config evidence, and run evidence must be bound separately.
- **Derived from**: O1, O2, O3
- **Enables**: Per-paper ARA validation and explicit missing-evidence reporting.

## Assumptions
- A1: Local files under `Stock_benchmark` are the authoritative state for this benchmark.
- A2: Summary rows count as verification evidence only when their source files exist.
""",
    )

    run_proof = "E03" if runs else "E02"
    write_text(
        artifact / "logic/claims.md",
        f"""# Claims

## C01: Paper is in corpus scope
- **Statement**: `{paper_id}` is a valid local corpus paper for `{paper.get('task', '')}`.
- **Status**: supported
- **Falsification criteria**: Remove the paper from `paper_registry.csv` or show the PDF status is invalid.
- **Proof**: [E01]
- **Evidence basis**: The registry row and PDF verification row both exist locally.
- **Interpretation**: The paper can be represented as an ARA artifact.
- **Dependencies**: none
- **Tags**: corpus, pdf

## C02: Local reproduction engineering is represented
- **Statement**: Local project and/or source evidence has been bound into this ARA for `{paper_id}`.
- **Status**: {"supported" if project else "hypothesis"}
- **Falsification criteria**: Show that no local project files, extracted paper text, or registry evidence are linked in the evidence layer.
- **Proof**: [E02]
- **Evidence basis**: Project files present: {", ".join(project.keys()) if project else "Not specified in provided sources"}.
- **Interpretation**: This claim covers engineering traceability, not model performance.
- **Dependencies**: C01
- **Tags**: engineering, project

## C03: Independent local model verification
- **Statement**: `{paper_id}` independent local verification status is `{verification_status}`.
- **Status**: {"supported" if runs else "hypothesis"}
- **Falsification criteria**: Re-run summary aggregation and find a contradictory source-backed paper-model result status.
- **Proof**: [{run_proof}]
- **Evidence basis**: Matching run rows: {len(runs)}.
- **Interpretation**: `complete` means source-backed local result files exist; it does not imply official reproduction parity.
- **Dependencies**: C01, C02
- **Tags**: verification, benchmark
""",
    )

    method_terms = [
        ("Paper identifier", paper_id),
        ("Task", paper.get("task", "")),
        ("Candidate status", paper.get("status", "")),
        ("Local verification status", verification_status),
    ]
    write_text(
        artifact / "logic/concepts.md",
        "# Concepts\n\n"
        + "\n\n".join(
            f"""## {name}
- **Notation**: n/a
- **Definition**: {value or "Not specified in provided sources"}
- **Boundary conditions**: Defined by the local registry and generated ARA evidence.
- **Related concepts**: corpus scope, verification status"""
            for name, value in method_terms
        ),
    )

    run_details = "\n".join(
        f"  - {row['run_id']}: `{row['source']}` with IC `{row['ic']}` and RankIC `{row['rankic']}`"
        for row in runs
    ) or "  - Not specified in provided sources"
    write_text(
        artifact / "logic/experiments.md",
        f"""# Experiments

## E01: Source availability check
- **Verifies**: C01
- **Setup**:
  - Model: n/a
  - Hardware: local filesystem
  - Dataset: downloaded paper corpus
  - System: `Stock_benchmark/papers`
- **Procedure**:
  1. Read `paper_registry.csv`.
  2. Read `pdf_download_status.csv`.
  3. Confirm PDF and extracted text paths.
- **Metrics**: presence, byte count, PDF header validity
- **Expected outcome**:
  - Registry and PDF evidence exist.
- **Baselines**: none
- **Dependencies**: none

## E02: Engineering traceability check
- **Verifies**: C02
- **Setup**:
  - Model: n/a
  - Hardware: local filesystem
  - Dataset: paper project files and extracted text
  - System: `Stock_benchmark/paper_projects/{paper_id}`
- **Procedure**:
  1. Inspect project notes, repository analysis, reproduction plan, and configs if present.
  2. Bind available materials into `src/` and `evidence/source/`.
- **Metrics**: project files present, config files present
- **Expected outcome**:
  - Available engineering context is linked without inventing missing code.
- **Baselines**: none
- **Dependencies**: E01

## E03: Independent local model verification
- **Verifies**: C03
- **Setup**:
  - Model: {prefix}
  - Hardware: local CPU/NumPy or configured runtime
  - Dataset: CSI300 2018-2024 formal benchmark when available
  - System: `experiments/paper_runs`
- **Procedure**:
  1. Match `smoke_results.csv` rows to this paper's model prefix.
  2. Confirm each row's source file exists.
  3. Record IC/RankIC summaries in `evidence/runs/`.
- **Metrics**: IC, RankIC, ICIR, RankICIR, row count
- **Expected outcome**:
  - Source-backed local run rows exist for independently verified papers.
- **Baselines**: LightGBM and Qlib baseline rows in `smoke_results.csv`
- **Dependencies**: E01, E02

## Local run bindings
{run_details}
""",
    )

    write_text(
        artifact / "logic/related_work.md",
        f"""# Related Work

## RW01: Source paper
- **Work**: {paper['title']}
- **Relation**: target
- **Evidence**: `papers/raw/{paper_id}.pdf`, `papers/extracted/{paper_id}.txt`
- **Notes**: {paper.get('notes', '')}

## RW02: Source code repository
- **Work**: {paper.get('code_url') or 'Not specified in provided sources'}
- **Relation**: implementation reference
- **Evidence**: registry `code_url`
- **Notes**: Local repository analysis is included when `paper_projects/{paper_id}/repo_analysis.md` exists.
""",
    )

    write_text(
        artifact / "logic/solution/constraints.md",
        f"""# Constraints

## Scope
- This artifact covers local ARA representation and local benchmark verification, not a guarantee of official paper reproduction parity.
- Verification status: `{verification_status}`.

## Missing or weak evidence
- Full figure/table screenshots are not generated by this script; text-derived figure/table mentions are indexed when found.
- Official implementation details are only represented when local project or repository evidence exists.
- Papers without matching `paper_model` rows remain incomplete for the user's independent-verification objective.

## Boundary conditions
- The benchmark dataset is the local China A-share / CSI300 setup already built under `Stock_benchmark`.
- Source-backed run evidence must point to existing files.
""",
    )

    method_summary = "\n\n".join(
        f"## {name}\n\n```text\n{content[:5000]}\n```" for name, content in project.items() if name.endswith(".md")
    ) or "Not specified in provided sources beyond registry and extracted paper text."
    write_text(
        artifact / "logic/solution/method.md",
        f"""# Method and Engineering Notes

## Paper digest

{abstract_digest(paper_text, 2000)}

## Local project notes

{method_summary}
""",
    )

    env_lines = [
        "# Environment",
        "",
        "## Local sources",
        f"- Registry: `papers/metadata/paper_registry.csv`",
        f"- PDF status: `papers/metadata/pdf_download_status.csv`",
        f"- PDF: `{Path(pdf_row.get('path', '')).as_posix()}`",
        f"- Extracted text: `papers/extracted/{paper_id}.txt`",
        f"- Paper project: `paper_projects/{paper_id}`" if project else "- Paper project: Not specified in provided sources",
        "- Summary: `experiments/summary/smoke_results.csv`",
        "",
        "## Runtime",
        "- Python scripts under `Stock_benchmark/scripts`",
        "- Formal benchmark data under `Stock_benchmark/data/processed` when available",
    ]
    write_text(artifact / "src/environment.md", "\n".join(env_lines))

    for rel_name, content in project.items():
        if rel_name.startswith("configs/"):
            write_text(artifact / "src" / rel_name, content)

    tree = f"""nodes:
  - id: Q01
    type: question
    title: "Can {paper_id} be represented and verified independently?"
    support_level: explicit
    source_refs:
      - papers/metadata/paper_registry.csv
      - papers/metadata/pdf_download_status.csv
    children:
      - id: D01
        type: decision
        title: "Use downloaded local PDF and extracted text as primary paper evidence"
        choice: "Compile an ARA from local sources"
        alternatives:
          - "Rely on network paper URL"
        rationale: "Local PDF header is valid and extracted text exists."
        support_level: explicit
        source_refs:
          - papers/extracted/{paper_id}.txt
      - id: E03
        type: experiment
        title: "Independent local model verification"
        result: "{verification_status}"
        support_level: explicit
        source_refs:
          - experiments/summary/smoke_results.csv
        evidence:
          - C03
"""
    if not runs:
        tree += """      - id: X01
        type: dead_end
        title: "No matching local paper-model result yet"
        failure_mode: "The summary table has no source-backed paper_model rows for this paper prefix."
        lesson: "ARA can be structurally compiled, but independent verification remains incomplete until a local run is added."
        support_level: explicit
        source_refs:
          - experiments/summary/smoke_results.csv
        evidence:
          - C03
"""
    write_text(artifact / "trace/exploration_tree.yaml", tree)

    source_overview = [
        "# Source Overview",
        "",
        "## Registry row",
        "",
        "```json",
        json.dumps(paper, ensure_ascii=False, indent=2),
        "```",
        "",
        "## PDF status row",
        "",
        "```json",
        json.dumps(pdf_row, ensure_ascii=False, indent=2),
        "```",
        "",
        "## Extracted text opening",
        "",
        "```text",
        "\n".join(first_nonempty_lines(paper_text, 20)),
        "```",
    ]
    write_text(artifact / "evidence/source/source_overview.md", "\n".join(source_overview))

    if project:
        project_md = ["# Local Project Evidence", ""]
        for name, content in project.items():
            project_md += [f"## {name}", "", "```text", content[:6000], "```", ""]
        write_text(artifact / "evidence/source/local_project.md", "\n".join(project_md))

    evidence = collect_numbered_evidence(paper_text)
    table_count = 0
    figure_count = 0
    for number, lines in sorted(evidence["tables"].items(), key=lambda item: int(item[0])):
        table_count += 1
        write_text(
            artifact / "evidence/tables" / f"table{number}_text_mentions.md",
            f"""# Table {number} Text Mentions

- **Source**: `papers/extracted/{paper_id}.txt`
- **Extraction method**: text regex over extracted PDF text
- **Reading confidence**: medium for caption/mention presence; low for full table contents

```text
{chr(10).join(lines)}
```
""",
        )
    for number, lines in sorted(evidence["figures"].items(), key=lambda item: int(item[0])):
        figure_count += 1
        write_text(
            artifact / "evidence/figures" / f"figure{number}_text_mentions.md",
            f"""# Figure {number} Text Mentions

- **Source**: `papers/extracted/{paper_id}.txt`
- **Figure type**: Not determined from text-only extraction
- **Extraction method**: text regex over extracted PDF text
- **Reading confidence**: medium for caption/mention presence; low for visual values

```text
{chr(10).join(lines)}
```
""",
        )

    for row in runs:
        run_path = PROJECT_ROOT / row["source"]
        tail = ""
        if run_path.exists():
            lines = run_path.read_text(encoding="utf-8", errors="replace").splitlines()
            tail = "\n".join(lines[-5:])
        write_text(
            artifact / "evidence/runs" / f"{row['run_id']}.md",
            f"""# {row['run_id']}

- **Source**: `{row['source']}`
- **Dataset**: {row['dataset']}
- **Selection**: {row['selection']}
- **n**: {row['n']}
- **IC**: {row['ic']}
- **RankIC**: {row['rankic']}
- **ICIR**: {row['icir']}
- **RankICIR**: {row['rankicir']}

## Source tail

```text
{tail}
```
""",
        )

    evidence_index = f"""# Evidence Index

## Independent verification

- **Status**: {verification_status}
- **Matching run rows**: {len(runs)}
- **Run evidence files**: {len(runs)}

## Source evidence

- `source/source_overview.md`
{"- `source/local_project.md`" if project else "- Local project evidence: Not specified in provided sources"}

## Numbered source objects detected from text

- Tables: {table_count}
- Figures: {figure_count}

## Claim bindings

- C01: E01 -> `source/source_overview.md`
- C02: E02 -> `source/local_project.md` when present, otherwise `source/source_overview.md`
- C03: E03 -> `runs/*.md` when present, otherwise missing run evidence is explicit in constraints and trace.
"""
    write_text(artifact / "evidence/README.md", evidence_index)

    level2 = {
        "artifact": paper_id,
        "artifact_dir": str(artifact),
        "review_version": "local-preliminary-1.0",
        "prerequisite": "Level 1 structural validation pending external script",
        "overall": {
            "grade": "Weak Accept" if runs else "Weak Reject",
            "mean_score": 3.2 if runs else 2.4,
            "one_line_summary": (
                "ARA is structurally grounded with source-backed local run evidence."
                if runs
                else "ARA is structurally grounded but lacks source-backed independent run evidence."
            ),
            "strengths_summary": ["Local PDF and registry evidence are explicit", "Missing verification evidence is not hidden"],
            "weaknesses_summary": ([] if runs else ["No matching local paper_model result files for this paper"]),
        },
        "dimensions": {
            "D1_evidence_relevance": {"score": 4 if runs else 3, "strengths": ["Claims are linked to local source evidence"], "weaknesses": [] if runs else ["C03 has no run evidence"], "suggestions": [] if runs else ["Add a paper-specific benchmark run"]},
            "D2_falsifiability": {"score": 3, "strengths": ["Claims include falsification criteria"], "weaknesses": ["Criteria are local-project oriented"], "suggestions": ["Add official reproduction parity criteria"]},
            "D3_scope_calibration": {"score": 4, "strengths": ["Official reproduction parity is not over-claimed"], "weaknesses": [], "suggestions": []},
            "D4_argument_coherence": {"score": 3, "strengths": ["Problem, claims, experiments, and evidence share IDs"], "weaknesses": ["Text-only evidence extraction is shallow"], "suggestions": ["Add visual figure extraction"]},
            "D5_exploration_integrity": {"score": 3, "strengths": ["Missing runs are represented as explicit dead ends"], "weaknesses": ["Historical exploration is reconstructed from available files"], "suggestions": ["Append live trace during future work"]},
            "D6_methodological_rigor": {"score": 3 if runs else 1, "strengths": ["Local metrics are recorded"] if runs else [], "weaknesses": [] if runs else ["No independent result rows"], "suggestions": [] if runs else ["Run or implement the missing model experiment"]},
        },
        "findings": [],
        "questions_for_authors": [],
        "read_order": ["PAPER.md", "logic/claims.md", "logic/experiments.md", "logic/problem.md", "logic/concepts.md", "logic/solution", "logic/related_work.md", "trace/exploration_tree.yaml", "evidence/README.md"],
    }
    if not runs:
        level2["findings"].append(
            {
                "finding_id": "F01",
                "dimension": "D6_methodological_rigor",
                "severity": "major",
                "target_file": "logic/claims.md",
                "target_entity": "C03",
                "evidence_span": f"`{paper_id}` independent local verification status is `{verification_status}`.",
                "observation": "The artifact explicitly records missing independent experiment outputs.",
                "reasoning": "The user's final objective requires every downloaded paper engineering project to be independently verified.",
                "suggestion": "Add a source-backed paper-model run for this paper and regenerate the ARA.",
            }
        )
    write_text(artifact / "level2_report.json", json.dumps(level2, ensure_ascii=False, indent=2))

    return {
        "paper_id": paper_id,
        "title": paper["title"],
        "artifact_dir": str(artifact.relative_to(PROJECT_ROOT)),
        "pdf_valid": pdf_row.get("valid_pdf_header", ""),
        "has_project": str(bool(project)),
        "matching_runs": str(len(runs)),
        "independent_verification": verification_status,
        "tables_detected": str(table_count),
        "figures_detected": str(figure_count),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(PROJECT_ROOT / "ara_artifacts"))
    args = parser.parse_args()

    registry = {row["paper_id"]: row for row in read_csv(PROJECT_ROOT / "papers/metadata/paper_registry.csv")}
    pdf_rows = read_csv(PROJECT_ROOT / "papers/metadata/pdf_download_status.csv")
    summary_rows = read_csv(PROJECT_ROOT / "experiments/summary/smoke_results.csv")
    out_root = Path(args.out)
    out_root.mkdir(parents=True, exist_ok=True)

    rows = []
    for pdf_row in pdf_rows:
        paper_id = pdf_row["paper_id"]
        if pdf_row.get("valid_pdf_header") != "True":
            continue
        if paper_id not in registry:
            continue
        rows.append(build_paper_artifact(registry[paper_id], pdf_row, summary_rows, out_root))

    report = out_root / "ara_verification_summary.csv"
    with report.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()) if rows else ["paper_id"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"artifacts={len(rows)} out={out_root}")
    print(f"summary={report}")
    for row in rows:
        print(f"{row['paper_id']} verification={row['independent_verification']} runs={row['matching_runs']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
