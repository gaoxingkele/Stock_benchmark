"""Validate the WQ Alpha Evolution protocol bundle."""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "ara_artifacts/wq_alpha_evolution/PAPER.md",
    "ara_artifacts/wq_alpha_evolution/logic/problem.md",
    "ara_artifacts/wq_alpha_evolution/logic/claims.md",
    "ara_artifacts/wq_alpha_evolution/logic/concepts.md",
    "ara_artifacts/wq_alpha_evolution/logic/experiments.md",
    "ara_artifacts/wq_alpha_evolution/logic/related_work.md",
    "ara_artifacts/wq_alpha_evolution/logic/solution/method.md",
    "ara_artifacts/wq_alpha_evolution/logic/solution/constraints.md",
    "ara_artifacts/wq_alpha_evolution/src/environment.md",
    "ara_artifacts/wq_alpha_evolution/trace/exploration_tree.yaml",
    "ara_artifacts/wq_alpha_evolution/evidence/README.md",
    "ara_artifacts/wq_alpha_evolution/evidence/source_checks.md",
    "ara_artifacts/wq_alpha_evolution/evidence/current_cross_framework_comparison.csv",
    "ara_artifacts/wq_alpha_evolution/evidence/schemas/sanitized_wq_run_schema.csv",
    "ara_artifacts/wq_alpha_evolution/evidence/schemas/proxy_factor_run_schema.csv",
    "ara_artifacts/wq_alpha_evolution/evidence/schemas/cross_framework_comparison_schema.csv",
    "docs/reports/wq_alpha_evolution_comparison_plan.md",
]

SCHEMA_FILES = {
    "ara_artifacts/wq_alpha_evolution/evidence/schemas/sanitized_wq_run_schema.csv": {
        "column",
        "required",
        "description",
    },
    "ara_artifacts/wq_alpha_evolution/evidence/schemas/proxy_factor_run_schema.csv": {
        "column",
        "required",
        "description",
    },
    "ara_artifacts/wq_alpha_evolution/evidence/schemas/cross_framework_comparison_schema.csv": {
        "column",
        "required",
        "description",
    },
}

ROW_COUNT_CHECKS = {
    "ara_artifacts/wq_alpha_evolution/evidence/current_cross_framework_comparison.csv": 4,
}


FORBIDDEN_SECRET_PATTERNS = [
    "WQ_BRAIN_PASSWORD=",
    "WQ_BRAIN_USERNAME=",
    "Authorization: Bearer ",
    "Cookie: ",
    "session_token=",
]


def run_command(command: list[str]) -> None:
    result = subprocess.run(command, cwd=PROJECT_ROOT, text=True, capture_output=True)
    print(f"$ {' '.join(command)}")
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip(), file=sys.stderr)
    if result.returncode:
        raise SystemExit(result.returncode)


def validate_schema(path: Path, required_columns: set[str]) -> bool:
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        actual_columns = set(reader.fieldnames or [])
        row_count = sum(1 for _row in reader)
    print(f"schema {path.relative_to(PROJECT_ROOT)} columns={sorted(actual_columns)} rows={row_count}")
    if not required_columns.issubset(actual_columns):
        print(f"ERROR schema columns missing: {path}")
        return False
    if row_count == 0:
        print(f"ERROR empty schema: {path}")
        return False
    return True


def main() -> int:
    for relative in REQUIRED_FILES:
        path = PROJECT_ROOT / relative
        print(f"exists {relative} actual={path.exists()} expected=True")
        if not path.exists():
            print(f"ERROR missing required file: {relative}")
            return 1

    for relative, columns in SCHEMA_FILES.items():
        if not validate_schema(PROJECT_ROOT / relative, columns):
            return 1

    for relative, expected_rows in ROW_COUNT_CHECKS.items():
        path = PROJECT_ROOT / relative
        with path.open(newline="", encoding="utf-8") as file:
            actual_rows = sum(1 for _row in csv.DictReader(file))
        print(f"rows {relative} actual={actual_rows} expected={expected_rows}")
        if actual_rows != expected_rows:
            print(f"ERROR row count mismatch: {relative}")
            return 1

    searchable_files = [
        PROJECT_ROOT / "ara_artifacts/wq_alpha_evolution/PAPER.md",
        PROJECT_ROOT / "ara_artifacts/wq_alpha_evolution/logic/solution/constraints.md",
        PROJECT_ROOT / "docs/reports/wq_alpha_evolution_comparison_plan.md",
    ]
    for path in searchable_files:
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_SECRET_PATTERNS:
            if pattern in text:
                print(f"ERROR forbidden secret-like pattern found in public text: {pattern} in {path}")
                return 1

    run_command(
        [
            sys.executable,
            "C:/Users/xmupt/.codex/skills/ara-paper/scripts/validate_ara.py",
            "ara_artifacts/wq_alpha_evolution",
        ]
    )
    print("WQ_ALPHA_EVOLUTION_BUNDLE_VALIDATION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
