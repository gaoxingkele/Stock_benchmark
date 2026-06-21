"""Validate local Qlib workflow config prerequisites without importing qlib."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config")
    parser.add_argument("--allow-missing-data", action="store_true", help="Validate YAML structure while reporting missing provider files.")
    return parser.parse_args()


def as_path(value: str) -> Path:
    return Path(value).expanduser()


def main() -> int:
    args = parse_args()
    config_path = Path(args.config)
    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    provider_uri = as_path(config["qlib_init"]["provider_uri"])
    market = config["market"]
    instruments = provider_uri / "instruments" / f"{market}.txt"
    calendar = provider_uri / "calendars" / "day.txt"
    features = provider_uri / "features"

    missing = [path for path in [provider_uri, instruments, calendar, features] if not path.exists()]
    if missing and not args.allow_missing_data:
        raise RuntimeError("missing Qlib prerequisites: " + ", ".join(str(path) for path in missing))

    feature_fields = config["data_handler_config"]["data_loader"]["kwargs"]["config"]["feature"]
    if len(feature_fields) != 2 or len(feature_fields[0]) != len(feature_fields[1]):
        raise RuntimeError("feature expressions and names must have the same length")

    segments = config["task"]["dataset"]["kwargs"]["segments"]
    for name in ["train", "valid", "test"]:
        if name not in segments:
            raise RuntimeError(f"missing segment: {name}")

    print(f"ok config={config_path}")
    print(f"provider_uri={provider_uri}")
    print(f"market={market} instruments={instruments}")
    print(f"feature_count={len(feature_fields[0])} segments={segments}")
    if missing:
        print("missing_prerequisites=" + ",".join(str(path) for path in missing))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
