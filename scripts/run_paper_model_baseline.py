"""Run lightweight paper-inspired baselines without Qlib or PyTorch runtime.

These are first runnable reproductions of each paper's central mechanism on
the shared China A-share benchmark protocol. They are not drop-in official
implementations.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Iterable

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.evaluation.metrics import pearson_corr, safe_ir, safe_mean, spearman_corr  # noqa: E402


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


MODEL_MODES = {
    "tra": "tra",
    "master": "master",
    "doubleadapt": "doubleadapt",
    "doubleensemble": "doubleadapt",
    "tcts": "tcts",
    "adarnn": "adarnn",
    "hist": "hist",
    "thgnn": "hist",
    "estimate": "hist",
    "alphaforge": "master",
    "alphaprobe": "master",
    "ddg_da": "adarnn",
    "rd_agent_quant": "doubleadapt",
    "factorvae": "master",
    "hatr": "hist",
    "alsp_tf": "tra",
    "ci_sthpan": "hist",
    "mdgnn": "hist",
    "deeptrader": "tra",
    "alphastock": "tra",
    "diffsformer": "doubleadapt",
    "finmamba": "hist",
    "lsr_igru": "hist",
    "timefilter": "tcts",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", choices=sorted(MODEL_MODES), required=True)
    parser.add_argument("--panel", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--horizon", type=int, default=1)
    parser.add_argument("--lookback", type=int, default=20)
    parser.add_argument("--train-start", default="2018-01-02")
    parser.add_argument("--train-end", default="2021-12-31")
    parser.add_argument("--valid-start", default="2022-01-04")
    parser.add_argument("--valid-end", default="2022-12-30")
    parser.add_argument("--test-start", default="2023-01-03")
    parser.add_argument("--test-end", default="2024-12-31")
    parser.add_argument("--ridge-alpha", type=float, default=10.0)
    parser.add_argument("--max-train-rows", type=int, default=250000)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def to_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def load_panel(path: Path) -> tuple[dict[str, list[dict]], dict[str, np.ndarray]]:
    by_symbol: dict[str, list[dict]] = defaultdict(list)
    raw_by_date: dict[str, list[np.ndarray]] = defaultdict(list)
    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            values = np.asarray([to_float(row[field]) for field in FEATURES], dtype=np.float64)
            if np.isnan(values).any():
                continue
            item = {
                "date": row["date"],
                "symbol": row["symbol"],
                "features": values,
                "close": to_float(row["close"]),
            }
            by_symbol[row["symbol"]].append(item)
            raw_by_date[row["date"]].append(values)
    for rows in by_symbol.values():
        rows.sort(key=lambda item: item["date"])
    market_by_date = {date: np.mean(values, axis=0) for date, values in raw_by_date.items()}
    return dict(by_symbol), market_by_date


def make_examples(
    by_symbol: dict[str, list[dict]],
    market_by_date: dict[str, np.ndarray],
    horizon: int,
    lookback: int,
    mode: str,
) -> list[dict]:
    examples: list[dict] = []
    for symbol, rows in by_symbol.items():
        for idx in range(lookback - 1, len(rows) - horizon):
            now = rows[idx]
            future = rows[idx + horizon]
            if now["close"] <= 0 or not math.isfinite(now["close"]) or not math.isfinite(future["close"]):
                continue
            seq = np.asarray([row["features"] for row in rows[idx - lookback + 1 : idx + 1]], dtype=np.float64)
            label = future["close"] / now["close"] - 1.0
            if mode in {"master", "hist"}:
                market_seq = np.asarray(
                    [market_by_date[rows[j]["date"]] for j in range(idx - lookback + 1, idx + 1)],
                    dtype=np.float64,
                )
                if mode == "hist":
                    # HIST-inspired shared/residual representation: market-level shared
                    # information plus stock-specific deviation from that shared state.
                    features = np.concatenate(
                        [
                            seq.reshape(-1),
                            market_seq.reshape(-1),
                            (seq - market_seq).mean(axis=0),
                            seq[-1] - market_seq[-1],
                        ]
                    )
                else:
                    features = np.concatenate([seq.reshape(-1), market_seq.mean(axis=0), seq[-1] - market_seq[-1]])
            else:
                features = seq.reshape(-1)
            close_window = seq[:, FEATURES.index("close")]
            returns = np.diff(close_window) / np.maximum(close_window[:-1], 1e-12)
            volatility = float(np.std(returns)) if len(returns) else 0.0
            examples.append(
                {
                    "date": now["date"],
                    "symbol": symbol,
                    "x": features,
                    "label": float(label),
                    "volatility": volatility,
                }
            )
    return examples


def split_examples(examples: list[dict], start: str, end: str) -> list[dict]:
    return [row for row in examples if start <= row["date"] <= end]


def standardize(train_x: np.ndarray, *arrays: np.ndarray) -> tuple[np.ndarray, ...]:
    mean = train_x.mean(axis=0)
    std = train_x.std(axis=0)
    std[std == 0] = 1.0
    return tuple((array - mean) / std for array in arrays)


def sample_train(rows: list[dict], max_rows: int, seed: int) -> list[dict]:
    if len(rows) <= max_rows:
        return rows
    rng = np.random.default_rng(seed)
    idx = np.sort(rng.choice(len(rows), size=max_rows, replace=False))
    return [rows[int(i)] for i in idx]


def ridge_fit(x: np.ndarray, y: np.ndarray, alpha: float) -> np.ndarray:
    design = np.column_stack([np.ones(len(x)), x])
    penalty = np.eye(design.shape[1], dtype=np.float64) * alpha
    penalty[0, 0] = 0.0
    return np.linalg.solve(design.T @ design + penalty, design.T @ y)


def ridge_fit_weighted(x: np.ndarray, y: np.ndarray, sample_weight: np.ndarray, alpha: float) -> np.ndarray:
    design = np.column_stack([np.ones(len(x)), x])
    weights = np.sqrt(np.maximum(sample_weight, 1e-12))[:, None]
    weighted_design = design * weights
    weighted_y = y * weights[:, 0]
    penalty = np.eye(design.shape[1], dtype=np.float64) * alpha
    penalty[0, 0] = 0.0
    return np.linalg.solve(weighted_design.T @ weighted_design + penalty, weighted_design.T @ weighted_y)


def ridge_predict(weight: np.ndarray, x: np.ndarray) -> np.ndarray:
    design = np.column_stack([np.ones(len(x)), x])
    return design @ weight


def rows_to_xy(rows: list[dict]) -> tuple[np.ndarray, np.ndarray]:
    return np.asarray([row["x"] for row in rows], dtype=np.float64), np.asarray([row["label"] for row in rows], dtype=np.float64)


def fit_single(train_rows: list[dict], valid_rows: list[dict], test_rows: list[dict], alpha: float) -> np.ndarray:
    train_x, train_y = rows_to_xy(train_rows)
    valid_x, _ = rows_to_xy(valid_rows)
    test_x, _ = rows_to_xy(test_rows)
    train_x, valid_x, test_x = standardize(train_x, train_x, valid_x, test_x)
    weight = ridge_fit(train_x, train_y, alpha)
    return ridge_predict(weight, test_x)


def fit_adarnn(train_rows: list[dict], valid_rows: list[dict], test_rows: list[dict], alpha: float) -> np.ndarray:
    train_x, train_y = rows_to_xy(train_rows)
    valid_x, _ = rows_to_xy(valid_rows)
    test_x, _ = rows_to_xy(test_rows)
    train_x, valid_x, test_x = standardize(train_x, train_x, valid_x, test_x)
    valid_center = valid_x.mean(axis=0)
    distances = np.linalg.norm(train_x - valid_center, axis=1)
    scale = np.median(distances) or 1.0
    # AdaRNN-inspired adaptive weighting: emphasize source windows whose
    # covariates are closer to the validation-period target distribution.
    weights = np.exp(-distances / max(scale, 1e-12))
    weights = weights / max(float(weights.mean()), 1e-12)
    weight = ridge_fit_weighted(train_x, train_y, weights, alpha)
    return ridge_predict(weight, test_x)


def fit_tra(train_rows: list[dict], valid_rows: list[dict], test_rows: list[dict], alpha: float) -> np.ndarray:
    train_x, train_y = rows_to_xy(train_rows)
    valid_x, _ = rows_to_xy(valid_rows)
    test_x, _ = rows_to_xy(test_rows)
    train_x, valid_x, test_x = standardize(train_x, train_x, valid_x, test_x)
    train_vol = np.asarray([row["volatility"] for row in train_rows], dtype=np.float64)
    cuts = np.quantile(train_vol, [1 / 3, 2 / 3])
    buckets = np.digitize(train_vol, cuts)
    weights: list[np.ndarray] = []
    fallback = ridge_fit(train_x, train_y, alpha)
    for bucket in range(3):
        mask = buckets == bucket
        weights.append(ridge_fit(train_x[mask], train_y[mask], alpha) if int(mask.sum()) >= 20 else fallback)
    test_buckets = np.digitize(np.asarray([row["volatility"] for row in test_rows], dtype=np.float64), cuts)
    preds = np.empty(len(test_rows), dtype=np.float64)
    for bucket in range(3):
        mask = test_buckets == bucket
        if int(mask.sum()):
            preds[mask] = ridge_predict(weights[bucket], test_x[mask])
    return preds


def fit_tcts(
    by_symbol: dict[str, list[dict]],
    market_by_date: dict[str, np.ndarray],
    args: argparse.Namespace,
) -> tuple[list[dict], np.ndarray]:
    horizons = sorted(set([1, 3, args.horizon, 5]))
    test_rows: list[dict] | None = None
    preds_by_horizon: list[np.ndarray] = []
    errors: list[float] = []
    for horizon in horizons:
        rows = make_examples(by_symbol, market_by_date, horizon, args.lookback, "tcts")
        train = sample_train(split_examples(rows, args.train_start, args.train_end), args.max_train_rows, args.seed + horizon)
        valid = split_examples(rows, args.valid_start, args.valid_end)
        test = split_examples(rows, args.test_start, args.test_end)
        train_x, train_y = rows_to_xy(train)
        valid_x, valid_y = rows_to_xy(valid)
        test_x, _ = rows_to_xy(test)
        train_x, valid_x, test_x = standardize(train_x, train_x, valid_x, test_x)
        weight = ridge_fit(train_x, train_y, args.ridge_alpha)
        valid_pred = ridge_predict(weight, valid_x)
        errors.append(float(np.mean((valid_pred - valid_y) ** 2)))
        if horizon == args.horizon:
            test_rows = test
        preds_by_horizon.append(ridge_predict(weight, test_x))
    if test_rows is None:
        raise RuntimeError("target horizon did not produce test rows")
    min_len = min(len(preds) for preds in preds_by_horizon)
    inv_errors = np.asarray([1.0 / max(error, 1e-12) for error in errors], dtype=np.float64)
    weights = inv_errors / inv_errors.sum()
    stacked = np.vstack([preds[:min_len] for preds in preds_by_horizon])
    return test_rows[:min_len], weights @ stacked


def apply_doubleadapt(preds: np.ndarray, test_rows: list[dict], alpha: float = 0.15, max_history: int = 20) -> np.ndarray:
    adapted = np.empty_like(preds)
    symbol_bias: dict[str, float] = defaultdict(float)
    pending: dict[str, deque[tuple[str, float]]] = defaultdict(deque)
    current_date = ""
    for i, row in enumerate(test_rows):
        date = row["date"]
        if date != current_date:
            current_date = date
            for symbol, queue in pending.items():
                while len(queue) > max_history:
                    queue.popleft()
                if queue:
                    symbol_bias[symbol] = (1 - alpha) * symbol_bias[symbol] + alpha * np.mean([err for _, err in queue])
        symbol = row["symbol"]
        adapted[i] = preds[i] + symbol_bias[symbol]
        pending[symbol].append((date, row["label"] - preds[i]))
    return adapted


def evaluate(test_rows: list[dict], preds: np.ndarray, out_path: Path, metadata: dict[str, str]) -> dict[str, str]:
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
        **metadata,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["date", "n", "ic", "rankic", "icir", "rankicir", "model", "horizon", "lookback"]
    with out_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for row in result_rows:
            writer.writerow({**{"icir": "", "rankicir": ""}, **row, **metadata})
        writer.writerow(summary)
    return summary


def main() -> int:
    args = parse_args()
    mode = MODEL_MODES[args.model]
    by_symbol, market_by_date = load_panel(Path(args.panel))
    if mode == "tcts":
        test_rows, preds = fit_tcts(by_symbol, market_by_date, args)
    else:
        examples = make_examples(by_symbol, market_by_date, args.horizon, args.lookback, mode)
        train = sample_train(split_examples(examples, args.train_start, args.train_end), args.max_train_rows, args.seed)
        valid = split_examples(examples, args.valid_start, args.valid_end)
        test_rows = split_examples(examples, args.test_start, args.test_end)
        if not train or not valid or not test_rows:
            raise RuntimeError("empty train/valid/test split")
        if mode == "tra":
            preds = fit_tra(train, valid, test_rows, args.ridge_alpha)
        elif mode == "master":
            preds = fit_single(train, valid, test_rows, args.ridge_alpha)
        elif mode == "doubleadapt":
            base_preds = fit_single(train, valid, test_rows, args.ridge_alpha)
            preds = apply_doubleadapt(base_preds, test_rows)
        elif mode == "adarnn":
            preds = fit_adarnn(train, valid, test_rows, args.ridge_alpha)
        elif mode == "hist":
            preds = fit_single(train, valid, test_rows, args.ridge_alpha)
        else:
            raise ValueError(mode)
    summary = evaluate(
        test_rows,
        preds,
        Path(args.out),
        {"model": args.model, "horizon": str(args.horizon), "lookback": str(args.lookback)},
    )
    print(f"model={args.model} test_rows={len(test_rows)} out={args.out}")
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
