"""Validate the committed CASE-Lingxi research bundle."""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

ROW_COUNT_CHECKS = {
    "experiments/case_lingxi_context_router_validation_2026_ytd/case_lingxi_context_router_validation_summary.csv": 112,
    "experiments/case_lingxi_rl_router_validation_2025_2026_ytd/case_lingxi_rl_router_validation_summary.csv": 128,
    "experiments/case_lingxi_llm_tag_ablation_2026_ytd/case_lingxi_llm_tag_ablation_summary.csv": 128,
    "experiments/case_lingxi_promotion_audit/case_lingxi_promotion_audit_summary.csv": 3,
    "experiments/case_lingxi_promotion_audit/case_lingxi_promotion_audit_detail.csv": 48,
    "experiments/case_lingxi_cost_sensitivity/case_lingxi_cost_sensitivity_summary.csv": 15,
    "experiments/case_lingxi_cost_sensitivity/case_lingxi_cost_sensitivity_detail.csv": 240,
    "experiments/case_lingxi_capacity_slippage/case_lingxi_capacity_slippage_summary.csv": 60,
    "experiments/case_lingxi_capacity_slippage/case_lingxi_capacity_slippage_detail.csv": 960,
    "papers/metadata/case_lingxi_citation_coverage.csv": 31,
}


def count_csv_rows(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as file:
        return sum(1 for _row in csv.DictReader(file))


def run_command(command: list[str]) -> None:
    result = subprocess.run(command, cwd=PROJECT_ROOT, text=True, capture_output=True)
    print(f"$ {' '.join(command)}")
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip(), file=sys.stderr)
    if result.returncode:
        raise SystemExit(result.returncode)


def main() -> int:
    for relative, expected in ROW_COUNT_CHECKS.items():
        path = PROJECT_ROOT / relative
        if not path.exists():
            print(f"ERROR missing artifact: {relative}")
            return 1
        actual = count_csv_rows(path)
        print(f"rows {relative} actual={actual} expected={expected}")
        if actual != expected:
            print(f"ERROR row count mismatch: {relative}")
            return 1

    run_command([sys.executable, "scripts/validate_case_lingxi_citations.py"])
    run_command([sys.executable, "scripts/validate_references_bib.py"])
    run_command(
        [
            sys.executable,
            "C:/Users/xmupt/.codex/skills/ara-paper/scripts/validate_ara.py",
            "ara_artifacts/case_lingxi",
        ]
    )
    print("CASE_LINGXI_BUNDLE_VALIDATION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
