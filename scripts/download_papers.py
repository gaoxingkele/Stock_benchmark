"""Download paper PDFs listed in the paper registry."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--registry",
        default=str(PROJECT_ROOT / "papers" / "metadata" / "paper_registry.csv"),
        help="Paper registry CSV.",
    )
    parser.add_argument("--out-dir", default=str(PROJECT_ROOT / "papers" / "raw"))
    parser.add_argument("--paper-id", action="append", help="Download only selected paper_id. Can be repeated.")
    parser.add_argument("--status", action="append", help="Download only selected status. Can be repeated.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing PDFs.")
    return parser.parse_args()


def pdf_url(url: str) -> str:
    """Convert common abstract URLs into direct PDF URLs."""

    url = url.strip()
    if not url:
        return ""
    parsed = urlparse(url)
    if parsed.netloc == "arxiv.org" and parsed.path.startswith("/abs/"):
        arxiv_id = parsed.path.removeprefix("/abs/")
        return f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    return url


def download(url: str, path: Path, force: bool) -> tuple[str, int]:
    if path.exists() and path.stat().st_size > 0 and not force:
        return "skipped", path.stat().st_size
    request = urllib.request.Request(url, headers={"User-Agent": "StockBenchmark/0.1"})
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            body = response.read()
    except urllib.error.URLError as exc:
        raise RuntimeError(f"download failed: {url}: {exc}") from exc
    path.write_bytes(body)
    return "downloaded", len(body)


def main() -> int:
    args = parse_args()
    registry_path = Path(args.registry)
    out_dir = Path(args.out_dir)
    selected_ids = set(args.paper_id or [])
    selected_status = set(args.status or [])
    manifest: list[dict[str, str | int]] = []

    with registry_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            paper_id = row["paper_id"]
            if selected_ids and paper_id not in selected_ids:
                continue
            if selected_status and row["status"] not in selected_status:
                continue
            url = pdf_url(row.get("pdf_url", ""))
            if not url:
                manifest.append({"paper_id": paper_id, "status": "missing_url", "path": "", "bytes": 0})
                continue
            out_path = out_dir / f"{paper_id}.pdf"
            try:
                status, size = download(url, out_path, args.force)
                manifest.append({"paper_id": paper_id, "status": status, "path": str(out_path), "bytes": size})
                print(f"{paper_id}: {status} bytes={size} path={out_path}")
            except RuntimeError as exc:
                manifest.append({"paper_id": paper_id, "status": "error", "path": str(out_path), "bytes": 0, "error": str(exc)})
                print(f"{paper_id}: error {exc}", file=sys.stderr)

    manifest_path = out_dir / "download_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"manifest={manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

