"""Extract draft citation metadata for rows missing from paper_registry.

This script reads `references_draft_missing_registry.csv`, looks for matching
ARA `PAPER.md` files, and extracts frontmatter fields into a patch CSV. It does
not promote entries to references.bib because many generated ARAs explicitly
mark authors/DOI as not specified.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MISSING = PROJECT_ROOT / "papers/metadata/references_draft_missing_registry.csv"
OUT = PROJECT_ROOT / "papers/metadata/references_missing_metadata_from_ara.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--missing", default=str(MISSING))
    parser.add_argument("--out", default=str(OUT))
    return parser.parse_args()


def resolve(path: str) -> Path:
    value = Path(path)
    return value if value.is_absolute() else PROJECT_ROOT / value


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---", text, flags=re.S)
    if not match:
        return {}
    block = match.group(1).splitlines()
    data: dict[str, str] = {}
    current_key = None
    list_values: list[str] = []
    for line in block:
        if line.startswith("  - ") and current_key:
            list_values.append(line[4:].strip().strip('"'))
            data[current_key] = "; ".join(list_values)
            continue
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            current_key = key.strip()
            list_values = []
            value = value.strip().strip('"')
            data[current_key] = value
    return data


def status_for(data: dict[str, str]) -> str:
    required = ["title", "authors", "year", "venue"]
    if not all(data.get(key) for key in required):
        return "missing_required_fields"
    if "Not specified" in data.get("authors", ""):
        return "incomplete_authors"
    if "Not specified" in data.get("venue", ""):
        return "incomplete_venue"
    return "draft_from_ara_complete_needs_primary_verification"


def main() -> int:
    args = parse_args()
    missing_rows = read_csv(resolve(args.missing))
    output_rows = []
    for row in missing_rows:
        paper_id = row["paper_id"]
        paper_path = PROJECT_ROOT / "ara_artifacts" / paper_id / "PAPER.md"
        data = parse_frontmatter(paper_path) if paper_path.exists() else {}
        output_rows.append(
            {
                "paper_id": paper_id,
                "ara_paper_exists": str(paper_path.exists()),
                "title": data.get("title", ""),
                "authors": data.get("authors", ""),
                "year": data.get("year", ""),
                "venue": data.get("venue", ""),
                "doi_or_url": data.get("doi", ""),
                "metadata_status": status_for(data),
                "source": str(paper_path.relative_to(PROJECT_ROOT)) if paper_path.exists() else "",
            }
        )

    out = resolve(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "paper_id",
            "ara_paper_exists",
            "title",
            "authors",
            "year",
            "venue",
            "doi_or_url",
            "metadata_status",
            "source",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)
    print(f"metadata_patch={out} rows={len(output_rows)}")
    for status in sorted({row["metadata_status"] for row in output_rows}):
        count = sum(1 for row in output_rows if row["metadata_status"] == status)
        print(f"{status}={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
