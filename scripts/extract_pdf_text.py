"""Extract text from downloaded PDFs into papers/extracted."""

from __future__ import annotations

import argparse
from pathlib import Path

from pypdf import PdfReader


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf-dir", default=str(PROJECT_ROOT / "papers" / "raw"))
    parser.add_argument("--out-dir", default=str(PROJECT_ROOT / "papers" / "extracted"))
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def extract_one(pdf_path: Path, out_path: Path, force: bool) -> tuple[str, int, int]:
    if out_path.exists() and out_path.stat().st_size > 0 and not force:
        return "skipped", out_path.stat().st_size, -1
    reader = PdfReader(str(pdf_path))
    pages: list[str] = []
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append(f"\n\n--- page {i} ---\n\n{text}")
    content = "".join(pages).strip() + "\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8", errors="replace")
    return "extracted", len(content), len(reader.pages)


def main() -> int:
    args = parse_args()
    pdf_dir = Path(args.pdf_dir)
    out_dir = Path(args.out_dir)
    for pdf_path in sorted(pdf_dir.glob("*.pdf")):
        out_path = out_dir / f"{pdf_path.stem}.txt"
        status, size, pages = extract_one(pdf_path, out_path, args.force)
        page_text = "unknown" if pages < 0 else str(pages)
        print(f"{pdf_path.stem}: {status} bytes={size} pages={page_text} path={out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
