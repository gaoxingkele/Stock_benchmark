"""Generate forward-return label CSV files from a processed panel."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.labels.forward_returns import build_forward_return_labels, write_labels  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--panel", default=str(PROJECT_ROOT / "data" / "processed" / "cn_a_share" / "csi300_by_date_smoke" / "panel.csv"))
    parser.add_argument("--horizon", type=int, default=1)
    parser.add_argument("--price-field", default="close")
    parser.add_argument("--out", default=str(PROJECT_ROOT / "data" / "processed" / "cn_a_share" / "csi300_by_date_smoke" / "labels_h1.csv"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    labels = build_forward_return_labels(args.panel, horizon=args.horizon, price_field=args.price_field)
    write_labels(labels, args.out)
    print(f"labels={args.out} rows={len(labels)} horizon={args.horizon}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
