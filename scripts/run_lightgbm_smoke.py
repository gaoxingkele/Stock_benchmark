"""Run a minimal LightGBM regression smoke baseline on a processed panel."""

from __future__ import annotations

import argparse
import csv
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.evaluation.metrics import pearson_corr, safe_ir, safe_mean, spearman_corr  # noqa: E402
from src.utils.benchmark_config import load_benchmark_config  # noqa: E402


FEATURES = [
    "open",
    "high",
    "low",
    "close",
    "pre_close",
    "volume",
    "amount",
    "change",
    "pct_chg",
    "turnover_rate",
    "volume_ratio",
    "pe",
    "pb",
    "total_mv",
    "circ_mv",
    "factor",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", help="Optional benchmark config JSON file.")
    parser.add_argument("--panel", default=str(PROJECT_ROOT / "data" / "processed" / "cn_a_share" / "csi300_smoke" / "panel.csv"))
    parser.add_argument("--horizon", type=int, default=1)
    parser.add_argument("--train-end", default="2024-01-03")
    parser.add_argument("--out", default=str(PROJECT_ROOT / "experiments" / "baselines" / "lightgbm_smoke_csi300.csv"))
    return parser.parse_args()


def resolve_run_settings(args: argparse.Namespace) -> dict[str, Any]:
    if not args.config:
        return {
            "panel": args.panel,
            "horizon": args.horizon,
            "train_end": args.train_end,
            "out": args.out,
            "features": FEATURES,
            "params": {
                "objective": "regression",
                "learning_rate": 0.1,
                "num_leaves": 4,
                "min_data_in_leaf": 1,
                "verbosity": -1,
                "seed": 42,
            },
            "num_boost_round": 10,
        }

    config = load_benchmark_config(args.config)
    payload = config.payload
    model = payload["model"]
    return {
        "panel": str(config.panel_path),
        "horizon": config.horizon,
        "train_end": config.train_end,
        "out": str(config.result_path),
        "features": list(payload["features"]["columns"]),
        "params": dict(model.get("params", {})),
        "num_boost_round": int(model.get("num_boost_round", 10)),
    }


def to_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def build_rows(panel_path: Path, horizon: int, feature_names: list[str]) -> list[dict]:
    rows_by_symbol: dict[str, list[dict[str, str]]] = defaultdict(list)
    with panel_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows_by_symbol[row["symbol"]].append(row)

    rows: list[dict] = []
    for symbol, symbol_rows in rows_by_symbol.items():
        symbol_rows = sorted(symbol_rows, key=lambda row: row["date"])
        for i, row in enumerate(symbol_rows):
            j = i + horizon
            if j >= len(symbol_rows):
                continue
            close_now = to_float(row["close"])
            close_future = to_float(symbol_rows[j]["close"])
            if close_now <= 0:
                continue
            features = [to_float(row[field]) for field in feature_names]
            if any(math.isnan(value) for value in features):
                continue
            rows.append(
                {
                    "date": row["date"],
                    "symbol": symbol,
                    "features": features,
                    "label": close_future / close_now - 1.0,
                }
            )
    return rows


def main() -> int:
    args = parse_args()
    settings = resolve_run_settings(args)
    import lightgbm as lgb
    import numpy as np

    feature_names = settings["features"]
    rows = build_rows(Path(settings["panel"]), settings["horizon"], feature_names)
    train_rows = [row for row in rows if row["date"] <= settings["train_end"]]
    test_rows = [row for row in rows if row["date"] > settings["train_end"]]
    if not train_rows or not test_rows:
        raise RuntimeError("Not enough rows for train/test split")

    train_x = np.asarray([row["features"] for row in train_rows], dtype=float)
    train_y = np.asarray([row["label"] for row in train_rows], dtype=float)
    test_x = np.asarray([row["features"] for row in test_rows], dtype=float)

    dataset = lgb.Dataset(train_x, label=train_y, feature_name=feature_names)
    model = lgb.train(
        settings["params"],
        dataset,
        num_boost_round=settings["num_boost_round"],
    )
    preds = model.predict(test_x)

    by_date: dict[str, list[tuple[float, float]]] = defaultdict(list)
    for row, pred in zip(test_rows, preds):
        by_date[row["date"]].append((float(pred), float(row["label"])))

    result_rows: list[dict[str, str]] = []
    ic_values: list[float] = []
    rankic_values: list[float] = []
    for date in sorted(by_date):
        pairs = by_date[date]
        scores = [score for score, _ in pairs]
        labels = [label for _, label in pairs]
        ic = pearson_corr(scores, labels)
        rankic = spearman_corr(scores, labels)
        ic_values.append(ic)
        rankic_values.append(rankic)
        result_rows.append({"date": date, "n": str(len(pairs)), "ic": f"{ic:.8f}", "rankic": f"{rankic:.8f}"})

    summary = {
        "date": "SUMMARY",
        "n": str(len(test_rows)),
        "ic": f"{safe_mean(ic_values):.8f}",
        "rankic": f"{safe_mean(rankic_values):.8f}",
        "icir": f"{safe_ir(ic_values):.8f}",
        "rankicir": f"{safe_ir(rankic_values):.8f}",
    }

    out_path = Path(settings["out"])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "n", "ic", "rankic", "icir", "rankicir"])
        writer.writeheader()
        for row in result_rows:
            writer.writerow({**{"icir": "", "rankicir": ""}, **row})
        writer.writerow(summary)

    print(f"train_rows={len(train_rows)} test_rows={len(test_rows)} out={out_path}")
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
