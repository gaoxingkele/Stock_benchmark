"""Extract nearby text around table mentions for target papers."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", default=str(PROJECT_ROOT / "experiments" / "summary" / "paper_24_comparison_matrix.csv"))
    parser.add_argument("--out", default=str(PROJECT_ROOT / "papers" / "metadata" / "target24_table_contexts.md"))
    parser.add_argument("--window", type=int, default=14)
    return parser.parse_args()


def context_blocks(text: str, window: int) -> list[tuple[int, list[str]]]:
    lines = text.splitlines()
    hits: list[tuple[int, list[str]]] = []
    seen = set()
    for i, line in enumerate(lines):
        if not re.search(r"\bTable\s+[0-9]+", line, flags=re.IGNORECASE):
            continue
        start = max(0, i - window)
        end = min(len(lines), i + window + 1)
        key = (start, end)
        if key in seen:
            continue
        seen.add(key)
        hits.append((i + 1, lines[start:end]))
    return hits


def main() -> int:
    args = parse_args()
    matrix_rows = list(csv.DictReader(Path(args.matrix).open("r", newline="", encoding="utf-8")))
    pending_ids = [
        row["paper_id"]
        for row in matrix_rows
        if row["original_experiment_data_status"] == "table_mentions_extracted_pending_numeric_transcription"
    ]
    out_lines = ["# Target-24 Table Contexts", ""]
    for paper_id in pending_ids:
        text_path = PROJECT_ROOT / "papers" / "extracted" / f"{paper_id}.txt"
        out_lines.extend([f"## {paper_id}", ""])
        if not text_path.exists():
            out_lines.extend(["Missing extracted text.", ""])
            continue
        text = text_path.read_text(encoding="utf-8", errors="replace")
        blocks = context_blocks(text, args.window)
        if not blocks:
            out_lines.extend(["No `Table N` contexts detected.", ""])
            continue
        for line_no, block in blocks:
            out_lines.extend([f"### line {line_no}", "", "```text", *block, "```", ""])
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"wrote {out_path.relative_to(PROJECT_ROOT)} papers={len(pending_ids)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
