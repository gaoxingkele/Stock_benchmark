"""Verify downloaded paper PDFs by checking file size and header."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf-dir", default=str(PROJECT_ROOT / "papers" / "raw"))
    parser.add_argument("--out", default=str(PROJECT_ROOT / "papers" / "metadata" / "pdf_download_status.csv"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pdf_dir = Path(args.pdf_dir)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str | int]] = []
    for pdf in sorted(pdf_dir.glob("*.pdf")):
        header = pdf.read_bytes()[:5]
        valid = header == b"%PDF-"
        rows.append(
            {
                "paper_id": pdf.stem,
                "path": str(pdf),
                "bytes": pdf.stat().st_size,
                "valid_pdf_header": str(valid),
            }
        )

    with out_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["paper_id", "path", "bytes", "valid_pdf_header"])
        writer.writeheader()
        writer.writerows(rows)

    for row in rows:
        print(f"{row['paper_id']}: valid={row['valid_pdf_header']} bytes={row['bytes']} path={row['path']}")
    print(f"status={out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

