"""Validate a sanitized WorldQuant BRAIN aggregate run table.

This validator is intentionally strict about privacy. It accepts only aggregate
run metrics and rejects columns or values that look like alpha IDs, expressions,
credentials, cookies, sessions, or raw PnL records.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PROJECT_ROOT / "ara_artifacts/wq_alpha_evolution/evidence/schemas/sanitized_wq_run_schema.csv"

INTEGER_COLUMNS = {
    "candidate_count",
    "simulation_success_count",
    "submission_count",
    "accepted_count",
    "spectacular_count",
    "invalid_field_count",
    "turnover_fail_count",
    "fitness_fail_count",
    "self_correlation_fail_count",
    "other_fail_count",
    "lesson_count",
    "lesson_reused_count",
}

FORBIDDEN_COLUMNS = {
    "alpha_id",
    "alpha_ids",
    "expression",
    "fastexpr",
    "pnl",
    "daily_pnl",
    "username",
    "password",
    "cookie",
    "session",
    "token",
    "authorization",
}

FORBIDDEN_VALUE_PATTERNS = [
    re.compile(r"alpha[_-]?[0-9a-f]{6,}", re.IGNORECASE),
    re.compile(r"Authorization:\s*Bearer\s+", re.IGNORECASE),
    re.compile(r"Cookie:\s*", re.IGNORECASE),
    re.compile(r"session[_-]?token\s*=", re.IGNORECASE),
    re.compile(r"(ts_|group_|rank\(|delay\(|trade_when\(|winsorize\()", re.IGNORECASE),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Path to sanitized WQ aggregate CSV")
    parser.add_argument("--allow-empty", action="store_true", help="Allow header-only template validation")
    return parser.parse_args()


def required_columns() -> set[str]:
    with SCHEMA_PATH.open(newline="", encoding="utf-8") as file:
        return {row["column"] for row in csv.DictReader(file) if row["required"].lower() == "true"}


def validate(path: Path, allow_empty: bool = False) -> int:
    required = required_columns()
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        columns = set(reader.fieldnames or [])
        rows = list(reader)

    print(f"file={path}")
    print(f"columns={sorted(columns)}")
    print(f"rows={len(rows)}")

    missing = required - columns
    if missing:
        print(f"ERROR missing required columns: {sorted(missing)}")
        return 1

    forbidden_columns = {column for column in columns if column.lower() in FORBIDDEN_COLUMNS}
    if forbidden_columns:
        print(f"ERROR forbidden private columns: {sorted(forbidden_columns)}")
        return 1

    if not rows and not allow_empty:
        print("ERROR no data rows; use --allow-empty only for committed templates")
        return 1

    for index, row in enumerate(rows, start=1):
        for column in INTEGER_COLUMNS:
            value = row.get(column, "")
            try:
                parsed = int(value)
            except ValueError:
                print(f"ERROR row {index} column {column} is not integer: {value!r}")
                return 1
            if parsed < 0:
                print(f"ERROR row {index} column {column} is negative: {value!r}")
                return 1

        if int(row["simulation_success_count"]) > int(row["candidate_count"]):
            print(f"ERROR row {index} simulation_success_count exceeds candidate_count")
            return 1
        if int(row["submission_count"]) > int(row["simulation_success_count"]):
            print(f"ERROR row {index} submission_count exceeds simulation_success_count")
            return 1
        if int(row["accepted_count"]) > int(row["submission_count"]):
            print(f"ERROR row {index} accepted_count exceeds submission_count")
            return 1
        if int(row["spectacular_count"]) > int(row["accepted_count"]):
            print(f"ERROR row {index} spectacular_count exceeds accepted_count")
            return 1

        for column, value in row.items():
            for pattern in FORBIDDEN_VALUE_PATTERNS:
                if value and pattern.search(value):
                    print(f"ERROR row {index} column {column} contains private-looking value")
                    return 1

    print("SANITIZED_WQ_RUN_VALIDATION_PASS")
    return 0


def main() -> int:
    args = parse_args()
    return validate(Path(args.path), args.allow_empty)


if __name__ == "__main__":
    raise SystemExit(main())
