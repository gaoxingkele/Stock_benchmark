"""Download PDFs for the 24-paper target source table."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", default=str(PROJECT_ROOT / "papers" / "metadata" / "paper_pdf_sources_24.csv"))
    parser.add_argument("--out-dir", default=str(PROJECT_ROOT / "papers" / "raw"))
    parser.add_argument("--paper-id", action="append")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def download(url: str, path: Path, force: bool) -> tuple[str, int, str]:
    if path.exists() and path.stat().st_size > 0 and not force:
        return "skipped", path.stat().st_size, ""
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 StockBenchmark/0.1",
            "Accept": "application/pdf,*/*",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            body = response.read()
            content_type = response.headers.get("Content-Type", "")
    except (urllib.error.URLError, OSError) as exc:
        raise RuntimeError(str(exc)) from exc
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(body)
    return "downloaded", len(body), content_type


def has_pdf_header(path: Path) -> bool:
    if not path.exists() or path.stat().st_size < 5:
        return False
    return path.read_bytes()[:5] == b"%PDF-"


def main() -> int:
    args = parse_args()
    selected = set(args.paper_id or [])
    sources_path = Path(args.sources)
    out_dir = Path(args.out_dir)
    manifest: list[dict[str, str | int | bool]] = []

    with sources_path.open("r", newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            paper_id = row["paper_id"]
            if selected and paper_id not in selected:
                continue
            out_path = out_dir / f"{paper_id}.pdf"
            try:
                status, size, content_type = download(row["pdf_url"], out_path, args.force)
                valid = has_pdf_header(out_path)
                print(f"{paper_id}: {status} bytes={size} valid_pdf={valid} path={out_path}")
                manifest.append(
                    {
                        "paper_id": paper_id,
                        "status": status,
                        "path": str(out_path),
                        "bytes": size,
                        "valid_pdf_header": valid,
                        "content_type": content_type,
                        "pdf_url": row["pdf_url"],
                    }
                )
            except RuntimeError as exc:
                print(f"{paper_id}: error {exc}", file=sys.stderr)
                manifest.append(
                    {
                        "paper_id": paper_id,
                        "status": "error",
                        "path": str(out_path),
                        "bytes": 0,
                        "valid_pdf_header": False,
                        "error": str(exc),
                        "pdf_url": row["pdf_url"],
                    }
                )

    manifest_path = out_dir / "target24_download_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"manifest={manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
