"""Validate CASE-Lingxi citation coverage files."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REGISTRY = PROJECT_ROOT / "data/ara_method_registry.csv"
COVERAGE = PROJECT_ROOT / "papers/metadata/case_lingxi_citation_coverage.csv"
BIB = PROJECT_ROOT / "papers/metadata/references.bib"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", default=str(REGISTRY))
    parser.add_argument("--coverage", default=str(COVERAGE))
    parser.add_argument("--bib", default=str(BIB))
    return parser.parse_args()


def resolve(path: str) -> Path:
    value = Path(path)
    return value if value.is_absolute() else PROJECT_ROOT / value


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def read_bib_keys(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    return set(re.findall(r"@\w+\{([^,\s]+)", text))


def main() -> int:
    args = parse_args()
    registry = read_csv(resolve(args.registry))
    coverage = read_csv(resolve(args.coverage))
    bib_keys = read_bib_keys(resolve(args.bib))

    errors: list[str] = []
    registry_ids = {row["paper_id"] for row in registry}
    coverage_ids = {row["paper_id"] for row in coverage}

    missing_coverage = sorted(registry_ids - coverage_ids)
    extra_coverage = sorted(coverage_ids - registry_ids)
    if missing_coverage:
        errors.append(f"missing coverage rows: {', '.join(missing_coverage)}")
    if extra_coverage:
        errors.append(f"extra coverage rows: {', '.join(extra_coverage)}")

    added = 0
    pending = 0
    for row in coverage:
        status = row["bibtex_status"]
        key = row["bibtex_key"].strip()
        if status == "added":
            added += 1
            if not key:
                errors.append(f"{row['paper_id']} marked added but has empty bibtex_key")
            elif key not in bib_keys:
                errors.append(f"{row['paper_id']} key {key} missing from references.bib")
        elif status == "pending":
            pending += 1
            if key:
                errors.append(f"{row['paper_id']} marked pending but has bibtex_key {key}")
        else:
            errors.append(f"{row['paper_id']} has invalid bibtex_status {status}")

    print(f"registry_rows={len(registry)}")
    print(f"coverage_rows={len(coverage)}")
    print(f"bib_keys={len(bib_keys)}")
    print(f"coverage_added={added}")
    print(f"coverage_pending={pending}")

    if errors:
        print("VALIDATION_FAILED")
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("VALIDATION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
