"""Build draft BibTeX entries from local CASE-Lingxi citation coverage.

The output is intentionally not the manuscript-ready references.bib. It is a
work queue generated from local registry metadata so each pending citation can
be verified against primary sources before promotion to references.bib.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PAPER_REGISTRY = PROJECT_ROOT / "papers/metadata/paper_registry.csv"
COVERAGE = PROJECT_ROOT / "papers/metadata/case_lingxi_citation_coverage.csv"
OUT = PROJECT_ROOT / "papers/metadata/references_draft_from_registry.bib"
MISSING_OUT = PROJECT_ROOT / "papers/metadata/references_draft_missing_registry.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-registry", default=str(PAPER_REGISTRY))
    parser.add_argument("--coverage", default=str(COVERAGE))
    parser.add_argument("--out", default=str(OUT))
    parser.add_argument("--missing-out", default=str(MISSING_OUT))
    return parser.parse_args()


def resolve(path: str) -> Path:
    value = Path(path)
    return value if value.is_absolute() else PROJECT_ROOT / value


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def slug(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "", value)
    return value.lower()[:24] or "paper"


def key_for(row: dict[str, str]) -> str:
    year = row.get("year", "0000")
    first_author = row.get("authors", "").split(";")[0].strip().split(" ")[-1]
    return f"{slug(first_author)}{year}{slug(row['title'].split(':')[0])}"


def authors_to_bibtex(authors: str) -> str:
    parts = [part.strip() for part in authors.split(";") if part.strip()]
    return " and ".join(parts) if parts else "UNKNOWN"


def entry_type(venue: str) -> str:
    lower = venue.lower()
    if "preprint" in lower or "unverified" in lower or "arxiv" in lower:
        return "article"
    return "inproceedings"


def journal_or_booktitle(entry_kind: str, venue: str) -> str:
    if entry_kind == "article":
        if "arxiv" in venue.lower() or "preprint" in venue.lower() or "unverified" in venue.lower():
            return "  journal = {preprint / venue unverified},"
        return f"  journal = {{{venue}}},"
    return f"  booktitle = {{{venue}}},"


def make_entry(row: dict[str, str]) -> str:
    kind = entry_type(row.get("venue", ""))
    key = key_for(row)
    lines = [
        f"@{kind}{{{key},",
        f"  title = {{{row['title']}}},",
        f"  author = {{{authors_to_bibtex(row.get('authors', ''))}}},",
        f"  year = {{{row.get('year', '')}}},",
        journal_or_booktitle(kind, row.get("venue", "")),
    ]
    if row.get("pdf_url"):
        lines.append(f"  url = {{{row['pdf_url']}}},")
    lines.extend(
        [
            f"  note = {{DRAFT from local registry; verify primary source before citing. paper_id={row['paper_id']}}}",
            "}",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    registry = {row["paper_id"]: row for row in read_csv(resolve(args.paper_registry))}
    coverage = read_csv(resolve(args.coverage))
    pending = [row for row in coverage if row["bibtex_status"] == "pending"]

    entries = []
    missing = []
    for row in pending:
        paper = registry.get(row["paper_id"])
        if not paper:
            missing.append(row["paper_id"])
            continue
        entries.append(make_entry(paper))

    out = resolve(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    header = [
        "% Draft BibTeX generated from papers/metadata/paper_registry.csv.",
        "% Do not cite these entries until verified against primary sources.",
        f"% pending_entries={len(entries)}",
        "",
    ]
    out.write_text("\n\n".join(["\n".join(header), *entries]) + "\n", encoding="utf-8")
    missing_out = resolve(args.missing_out)
    with missing_out.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["paper_id", "reason"])
        writer.writeheader()
        writer.writerows({"paper_id": paper_id, "reason": "not_found_in_paper_registry"} for paper_id in missing)
    print(f"draft_bib={out} entries={len(entries)}")
    print(f"missing_registry={missing_out} rows={len(missing)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
