"""Validate one or more benchmark config JSON files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.benchmark_config import load_benchmark_config  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("configs", nargs="+", help="Benchmark config JSON files.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    for config_path in args.configs:
        config = load_benchmark_config(config_path)
        print(
            "ok "
            f"id={config.experiment_id} "
            f"panel={config.panel_path} "
            f"horizon={config.horizon} "
            f"train_end={config.train_end} "
            f"out={config.result_path}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
