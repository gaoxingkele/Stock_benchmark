"""Validate the current CSI300 smoke universe, split, and labels."""

from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.labels.forward_returns import build_forward_return_labels  # noqa: E402
from src.splits.date_splits import DateSplit, calendar_coverage, count_panel_rows_by_split, read_calendar  # noqa: E402
from src.universe.instruments import read_instruments, summarize_instruments  # noqa: E402


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def main() -> int:
    universe_config = load_json(PROJECT_ROOT / "configs" / "universes" / "csi300_smoke.json")
    split_config = load_json(PROJECT_ROOT / "configs" / "splits" / "csi300_by_date_smoke.json")
    panel_path = PROJECT_ROOT / "data" / "processed" / "cn_a_share" / "csi300_by_date_smoke" / "panel.csv"

    instruments = read_instruments(PROJECT_ROOT.parent / universe_config["instrument_file"])
    summary = summarize_instruments(instruments)
    expected_count = int(universe_config["expected_symbol_count"])
    if len(instruments) != expected_count:
        raise RuntimeError(f"expected {expected_count} instruments, got {len(instruments)}")

    calendar = read_calendar(PROJECT_ROOT.parent / universe_config["calendar_file"])
    split_defs = [
        DateSplit(name=name, start_date=dates[0], end_date=dates[1])
        for name, dates in split_config["splits"].items()
    ]
    coverage = calendar_coverage(calendar, split_defs)
    panel_counts = count_panel_rows_by_split(panel_path, split_defs)

    h1 = build_forward_return_labels(panel_path, horizon=1)
    h5 = build_forward_return_labels(panel_path, horizon=5)
    if len(h1) != 1800:
        raise RuntimeError(f"expected 1800 h1 labels, got {len(h1)}")
    if len(h5) != 600:
        raise RuntimeError(f"expected 600 h5 labels, got {len(h5)}")

    print(f"instruments={summary}")
    print(f"calendar_dates={len(calendar)} split_calendar_coverage={coverage}")
    print(f"panel_rows_by_split={panel_counts}")
    print(f"labels_h1={len(h1)} labels_h5={len(h5)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
