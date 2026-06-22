"""Run a small DLinear-style sanity benchmark on downloaded ETT datasets."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "data/external/time_series_sota/dataset_profile.csv"
OUT = ROOT / "experiments/cross_domain_ts_datasets/ett_linear_guard_summary.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", default=str(PROFILE))
    parser.add_argument("--lookback", type=int, default=96)
    parser.add_argument("--horizon", type=int, default=96)
    parser.add_argument("--ridge-alpha", type=float, default=10.0)
    parser.add_argument("--out", default=str(OUT))
    return parser.parse_args()


def read_series(path: Path, target: str = "OT") -> np.ndarray:
    values: list[float] = []
    with path.open("r", newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            values.append(float(row[target]))
    return np.asarray(values, dtype=float)


def make_examples(values: np.ndarray, lookback: int, horizon: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    xs, y, naive = [], [], []
    for idx in range(lookback, len(values) - horizon):
        window = values[idx - lookback : idx]
        target = values[idx + horizon - 1]
        trend = window[-1] - window[0]
        features = [
            window[-1],
            float(np.mean(window)),
            float(np.std(window)),
            float(np.mean(window[-24:])),
            float(np.mean(window[-48:])),
            float(trend),
            float(window[-1] - np.mean(window)),
        ]
        xs.append(features)
        y.append(target)
        naive.append(window[-1])
    return np.asarray(xs, dtype=float), np.asarray(y, dtype=float), np.asarray(naive, dtype=float)


def ridge_predict(train_x: np.ndarray, train_y: np.ndarray, test_x: np.ndarray, alpha: float) -> np.ndarray:
    mean = train_x.mean(axis=0)
    std = train_x.std(axis=0)
    std[std <= 1e-12] = 1.0
    x = (train_x - mean) / std
    tx = (test_x - mean) / std
    design = np.column_stack([np.ones(len(x)), x])
    penalty = np.eye(design.shape[1]) * alpha
    penalty[0, 0] = 0.0
    weight = np.linalg.solve(design.T @ design + penalty, design.T @ train_y)
    return np.column_stack([np.ones(len(tx)), tx]) @ weight


def metrics(pred: np.ndarray, true: np.ndarray) -> dict[str, float]:
    err = pred - true
    mae = float(np.mean(np.abs(err)))
    mse = float(np.mean(err * err))
    rmse = math.sqrt(mse)
    denom = np.maximum(np.abs(true), 1e-12)
    mape = float(np.mean(np.abs(err) / denom))
    smape_denom = np.maximum(np.abs(pred) + np.abs(true), 1e-12)
    smape = float(np.mean(2.0 * np.abs(err) / smape_denom))
    return {"mae": mae, "mse": mse, "rmse": rmse, "mape": mape, "smape": smape}


def main() -> int:
    args = parse_args()
    rows: list[dict[str, str]] = []
    with Path(args.profile).open("r", newline="", encoding="utf-8") as file:
        profiles = list(csv.DictReader(file))
    for profile in profiles:
        path = ROOT / profile["local_path"]
        values = read_series(path)
        x, y, naive = make_examples(values, args.lookback, args.horizon)
        n = len(y)
        train_end = int(n * 0.6)
        valid_end = int(n * 0.8)
        pred = ridge_predict(x[:train_end], y[:train_end], x[valid_end:], args.ridge_alpha)
        ridge_stats = metrics(pred, y[valid_end:])
        naive_stats = metrics(naive[valid_end:], y[valid_end:])
        for method, stats in [("naive_last_value", naive_stats), ("dlinear_style_ridge", ridge_stats)]:
            rows.append(
                {
                    "dataset_id": profile["dataset_id"],
                    "method": method,
                    "lookback": str(args.lookback),
                    "horizon": str(args.horizon),
                    "train_examples": str(train_end),
                    "valid_examples": str(valid_end - train_end),
                    "test_examples": str(n - valid_end),
                    **{key: f"{value:.8f}" for key, value in stats.items()},
                }
            )
            print(profile["dataset_id"], method, stats)

    out = Path(args.out)
    if not out.is_absolute():
        out = ROOT / out
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as file:
        fields = [
            "dataset_id",
            "method",
            "lookback",
            "horizon",
            "train_examples",
            "valid_examples",
            "test_examples",
            "mae",
            "mse",
            "rmse",
            "mape",
            "smape",
        ]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"summary={out} rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
