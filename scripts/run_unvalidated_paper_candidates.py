"""Validate expansion-only paper candidates against the local TopK protocol.

These are paper-inspired engineering proxies for the seven expansion papers
that were not yet bound to local experiments. They are not official
implementations. The script produces per-method scores and TopK trade
validation summaries compatible with the rest of this repository.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from run_trade_validation import backtest, performance_stats, read_industry, read_meta, residualize_scores, write_daily  # noqa: E402


CANDIDATE_METHODS = [
    "2020_qlib_yang",
    "2025_alphaagent_tang",
    "2025_cogalpha_liu",
    "2025_quantbench_wang",
    "2025_fintsb",
    "2024_technical_indicator_impact",
    "2025_tin",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--panel", required=True)
    parser.add_argument("--stock-basic", required=True)
    parser.add_argument("--market", required=True)
    parser.add_argument("--method", action="append", choices=CANDIDATE_METHODS)
    parser.add_argument("--horizon", type=int, default=5)
    parser.add_argument("--topk", type=int, default=30)
    parser.add_argument("--cost-bps", type=float, default=10.0)
    parser.add_argument("--train-start", default="2018-01-02")
    parser.add_argument("--train-end", default="2021-12-31")
    parser.add_argument("--valid-start", default="2022-01-03")
    parser.add_argument("--valid-end", default="2022-12-30")
    parser.add_argument("--test-start", default="2023-01-03")
    parser.add_argument("--test-end", default="2025-12-31")
    parser.add_argument("--ridge-alpha", type=float, default=25.0)
    parser.add_argument("--max-train-rows", type=int, default=250000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out-dir", required=True)
    return parser.parse_args()


def to_float(value: str | None) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def safe_div(left: float, right: float) -> float:
    if not math.isfinite(left) or not math.isfinite(right) or abs(right) < 1e-12:
        return float("nan")
    return left / right


def mean(values: list[float]) -> float:
    items = [value for value in values if math.isfinite(value)]
    return float(np.mean(items)) if items else float("nan")


def std(values: list[float]) -> float:
    items = [value for value in values if math.isfinite(value)]
    return float(np.std(items, ddof=0)) if len(items) >= 2 else float("nan")


def zscore(values: np.ndarray) -> np.ndarray:
    out = values.astype(float).copy()
    finite = np.isfinite(out)
    if not finite.any():
        return np.zeros_like(out)
    center = np.nanmean(out[finite])
    scale = np.nanstd(out[finite])
    if scale <= 1e-12 or not math.isfinite(scale):
        out[finite] = out[finite] - center
    else:
        out[finite] = (out[finite] - center) / scale
    out[~finite] = 0.0
    return out


def rank_corr(x: np.ndarray, y: np.ndarray) -> float:
    mask = np.isfinite(x) & np.isfinite(y)
    if int(mask.sum()) < 3:
        return 0.0
    xr = np.argsort(np.argsort(x[mask])).astype(float)
    yr = np.argsort(np.argsort(y[mask])).astype(float)
    xsd = float(np.std(xr))
    ysd = float(np.std(yr))
    if xsd <= 1e-12 or ysd <= 1e-12:
        return 0.0
    return float(np.corrcoef(xr, yr)[0, 1])


def ridge_fit_predict(train_x: np.ndarray, train_y: np.ndarray, test_x: np.ndarray, alpha: float) -> np.ndarray:
    finite_train = np.isfinite(train_x).all(axis=1) & np.isfinite(train_y)
    finite_test = np.isfinite(test_x).all(axis=1)
    train_x = train_x[finite_train]
    train_y = train_y[finite_train]
    if len(train_x) < 50:
        return np.zeros(len(test_x), dtype=float)
    mean_x = train_x.mean(axis=0)
    std_x = train_x.std(axis=0)
    std_x[std_x <= 1e-12] = 1.0
    x = (train_x - mean_x) / std_x
    tx = (np.where(np.isfinite(test_x), test_x, mean_x) - mean_x) / std_x
    design = np.column_stack([np.ones(len(x)), x])
    penalty = np.eye(design.shape[1], dtype=float) * alpha
    penalty[0, 0] = 0.0
    try:
        weight = np.linalg.solve(design.T @ design + penalty, design.T @ train_y)
    except np.linalg.LinAlgError:
        weight = np.linalg.lstsq(design.T @ design + penalty, design.T @ train_y, rcond=None)[0]
    out = np.column_stack([np.ones(len(tx)), tx]) @ weight
    out[~finite_test] = 0.0
    return out


def load_panel(path: Path) -> dict[str, list[dict[str, float | str]]]:
    fields = ["open", "high", "low", "close", "pre_close", "volume", "amount", "pct_chg", "turnover_rate", "volume_ratio", "pe", "pb", "total_mv", "circ_mv"]
    by_symbol: dict[str, list[dict[str, float | str]]] = defaultdict(list)
    with path.open("r", newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            item: dict[str, float | str] = {"date": row["date"], "symbol": row["symbol"]}
            for field in fields:
                item[field] = to_float(row.get(field))
            by_symbol[row["symbol"]].append(item)
    for rows in by_symbol.values():
        rows.sort(key=lambda item: str(item["date"]))
    return dict(by_symbol)


def window(values: list[float], idx: int, n: int) -> list[float]:
    return values[max(0, idx - n + 1) : idx + 1]


def compute_row_features(
    rows: list[dict[str, float | str]],
    series: dict[str, list[float]],
    idx: int,
    horizon: int,
) -> dict[str, float | str] | None:
    if idx < 60 or idx + horizon >= len(rows):
        return None
    row = rows[idx]
    close = series["close"]
    high = series["high"]
    low = series["low"]
    open_ = series["open"]
    volume = series["volume"]
    amount = series["amount"]
    ret1 = series["ret1"]
    delta = series["delta"]
    tr = series["tr"]
    cur = close[idx]
    fut = close[idx + horizon]
    if not math.isfinite(cur) or cur <= 0 or not math.isfinite(fut):
        return None
    gain14 = mean([max(x, 0.0) for x in window(delta, idx, 14)])
    loss14 = mean([max(-x, 0.0) for x in window(delta, idx, 14)])
    rs = safe_div(gain14, loss14)
    rsi14 = 100.0 - 100.0 / (1.0 + rs) if math.isfinite(rs) else 50.0
    ma12 = mean(window(close, idx, 12))
    ma26 = mean(window(close, idx, 26))
    ma20 = mean(window(close, idx, 20))
    sd20 = std(window(close, idx, 20))
    atr14 = mean(window(tr, idx, 14))
    features: dict[str, float | str] = {
        "date": str(row["date"]),
        "symbol": str(row["symbol"]),
        "label": fut / cur - 1.0,
        "mom_5": safe_div(cur, close[idx - 5]) - 1.0,
        "mom_10": safe_div(cur, close[idx - 10]) - 1.0,
        "mom_20": safe_div(cur, close[idx - 20]) - 1.0,
        "mom_60": safe_div(cur, close[idx - 60]) - 1.0,
        "rev_5": -(safe_div(cur, close[idx - 5]) - 1.0),
        "ma_gap_5": safe_div(cur, mean(window(close, idx, 5))) - 1.0,
        "ma_gap_20": safe_div(cur, ma20) - 1.0,
        "vol_20": std(window(ret1, idx, 20)),
        "vol_60": std(window(ret1, idx, 60)),
        "range_20": safe_div(max(window(high, idx, 20)), min(window(low, idx, 20))) - 1.0,
        "rsi_14": rsi14 / 100.0,
        "macd_proxy": safe_div(ma12 - ma26, cur),
        "boll_z_20": safe_div(cur - ma20, sd20),
        "atr_14": safe_div(atr14, cur),
        "volume_z_20": safe_div(volume[idx] - mean(window(volume, idx, 20)), std(window(volume, idx, 20))),
        "amount_z_20": safe_div(amount[idx] - mean(window(amount, idx, 20)), std(window(amount, idx, 20))),
        "turnover_rate": float(row["turnover_rate"]),
        "volume_ratio": float(row["volume_ratio"]),
        "pe_z": math.log(max(float(row["pe"]), 1e-12)) if math.isfinite(float(row["pe"])) and float(row["pe"]) > 0 else float("nan"),
        "pb_z": math.log(max(float(row["pb"]), 1e-12)) if math.isfinite(float(row["pb"])) and float(row["pb"]) > 0 else float("nan"),
        "size": math.log(max(float(row["total_mv"]), 1.0)) if math.isfinite(float(row["total_mv"])) else float("nan"),
        "price_range": safe_div(high[idx], low[idx]) - 1.0,
        "oc_return": safe_div(close[idx], open_[idx]) - 1.0,
    }
    features["tin_rsi_macd"] = float(features["rsi_14"]) * float(features["macd_proxy"])
    features["tin_boll_mom"] = float(features["boll_z_20"]) * float(features["mom_20"])
    features["tin_vol_rev"] = float(features["vol_20"]) * float(features["rev_5"])
    features["alpha_price_volume"] = float(features["mom_20"]) * float(features["volume_z_20"])
    features["alpha_value_mom"] = -float(features["pe_z"]) + float(features["mom_60"])
    features["alpha_quality_liquidity"] = -float(features["vol_60"]) + float(features["turnover_rate"])
    return features


def build_examples(by_symbol: dict[str, list[dict[str, float | str]]], horizon: int) -> list[dict[str, float | str]]:
    rows: list[dict[str, float | str]] = []
    for symbol_rows in by_symbol.values():
        close = [float(item["close"]) for item in symbol_rows]
        high = [float(item["high"]) for item in symbol_rows]
        low = [float(item["low"]) for item in symbol_rows]
        series = {
            "open": [float(item["open"]) for item in symbol_rows],
            "high": high,
            "low": low,
            "close": close,
            "volume": [float(item["volume"]) for item in symbol_rows],
            "amount": [float(item["amount"]) for item in symbol_rows],
            "ret1": [safe_div(close[j], close[j - 1]) - 1.0 if j > 0 else float("nan") for j in range(len(close))],
            "delta": [close[j] - close[j - 1] if j > 0 else float("nan") for j in range(len(close))],
            "tr": [
                max(
                    high[j] - low[j],
                    abs(high[j] - close[j - 1]) if j > 0 else float("nan"),
                    abs(low[j] - close[j - 1]) if j > 0 else float("nan"),
                )
                for j in range(len(close))
            ],
        }
        for idx in range(len(symbol_rows)):
            features = compute_row_features(symbol_rows, series, idx, horizon)
            if features is not None:
                rows.append(features)
    return rows


QLIB_FEATURES = [
    "mom_5",
    "mom_10",
    "mom_20",
    "mom_60",
    "rev_5",
    "ma_gap_5",
    "ma_gap_20",
    "vol_20",
    "vol_60",
    "range_20",
    "volume_z_20",
    "amount_z_20",
    "turnover_rate",
    "volume_ratio",
    "pe_z",
    "pb_z",
    "size",
    "price_range",
    "oc_return",
]
TA_FEATURES = ["rsi_14", "macd_proxy", "boll_z_20", "atr_14", "ma_gap_20", "vol_20", "volume_z_20", "price_range"]
TS_FEATURES = ["mom_5", "mom_20", "mom_60", "rev_5", "vol_20", "vol_60", "range_20"]
TIN_FEATURES = TA_FEATURES + ["tin_rsi_macd", "tin_boll_mom", "tin_vol_rev"]
FORMULA_FEATURES = [
    "mom_20",
    "mom_60",
    "rev_5",
    "ma_gap_20",
    "vol_20",
    "boll_z_20",
    "alpha_price_volume",
    "alpha_value_mom",
    "alpha_quality_liquidity",
    "volume_z_20",
    "price_range",
]


def rows_to_matrix(rows: list[dict[str, float | str]], features: list[str]) -> np.ndarray:
    return np.asarray([[float(row.get(name, float("nan"))) for name in features] for row in rows], dtype=float)


def select_formula_features(valid_rows: list[dict[str, float | str]], candidates: list[str], max_features: int = 8) -> tuple[list[str], list[float]]:
    y = np.asarray([float(row["label"]) for row in valid_rows], dtype=float)
    values = {name: np.asarray([float(row.get(name, float("nan"))) for row in valid_rows], dtype=float) for name in candidates}
    scored = sorted(((name, rank_corr(values[name], y)) for name in candidates), key=lambda item: abs(item[1]), reverse=True)
    selected: list[str] = []
    weights: list[float] = []
    for name, ic in scored:
        if not math.isfinite(ic) or abs(ic) < 1e-6:
            continue
        if selected:
            max_corr = max(abs(rank_corr(values[name], values[old])) for old in selected)
            if max_corr > 0.85:
                continue
        selected.append(name)
        weights.append(ic)
        if len(selected) >= max_features:
            break
    if not selected:
        selected = ["mom_20", "rev_5", "vol_20"]
        weights = [1.0, 1.0, -1.0]
    return selected, weights


def formula_score(rows: list[dict[str, float | str]], features: list[str], weights: list[float]) -> np.ndarray:
    matrix = rows_to_matrix(rows, features)
    normalized = np.column_stack([zscore(matrix[:, idx]) for idx in range(matrix.shape[1])])
    w = np.asarray(weights, dtype=float)
    if np.sum(np.abs(w)) <= 1e-12:
        w = np.ones(len(features), dtype=float)
    w = w / np.sum(np.abs(w))
    return normalized @ w


def generate_scores(args: argparse.Namespace, method: str, rows: list[dict[str, float | str]]) -> tuple[list[dict], dict[str, str]]:
    train = [row for row in rows if args.train_start <= str(row["date"]) <= args.train_end]
    valid = [row for row in rows if args.valid_start <= str(row["date"]) <= args.valid_end]
    test = [row for row in rows if args.test_start <= str(row["date"]) <= args.test_end]
    if len(train) > args.max_train_rows:
        rng = np.random.default_rng(args.seed)
        idx = np.sort(rng.choice(len(train), size=args.max_train_rows, replace=False))
        train = [train[int(i)] for i in idx]
    y = np.asarray([float(row["label"]) for row in train], dtype=float)

    if method == "2020_qlib_yang":
        score = ridge_fit_predict(rows_to_matrix(train, QLIB_FEATURES), y, rows_to_matrix(test, QLIB_FEATURES), args.ridge_alpha)
        detail = "Alpha158-style OHLCV/value ridge proxy"
    elif method == "2024_technical_indicator_impact":
        score = ridge_fit_predict(rows_to_matrix(train, TA_FEATURES), y, rows_to_matrix(test, TA_FEATURES), args.ridge_alpha)
        detail = "TA-Lib-style indicator ridge proxy"
    elif method == "2025_tin":
        score = ridge_fit_predict(rows_to_matrix(train, TIN_FEATURES), y, rows_to_matrix(test, TIN_FEATURES), args.ridge_alpha)
        detail = "technical indicator interaction network proxy"
    elif method == "2025_fintsb":
        score = ridge_fit_predict(rows_to_matrix(train, TS_FEATURES), y, rows_to_matrix(test, TS_FEATURES), args.ridge_alpha)
        detail = "financial time-series momentum/volatility benchmark proxy"
    elif method == "2025_alphaagent_tang":
        selected, weights = select_formula_features(valid, FORMULA_FEATURES, max_features=8)
        score = formula_score(test, selected, weights)
        detail = "regularized formula-alpha selection: " + ",".join(selected)
    elif method == "2025_cogalpha_liu":
        selected, _ = select_formula_features(valid, FORMULA_FEATURES + TIN_FEATURES, max_features=12)
        score = ridge_fit_predict(rows_to_matrix(train, selected), y, rows_to_matrix(test, selected), args.ridge_alpha)
        detail = "code-generated formula feature ridge: " + ",".join(selected)
    elif method == "2025_quantbench_wang":
        qlib = ridge_fit_predict(rows_to_matrix(train, QLIB_FEATURES), y, rows_to_matrix(test, QLIB_FEATURES), args.ridge_alpha)
        ta = ridge_fit_predict(rows_to_matrix(train, TA_FEATURES), y, rows_to_matrix(test, TA_FEATURES), args.ridge_alpha)
        ts = ridge_fit_predict(rows_to_matrix(train, TS_FEATURES), y, rows_to_matrix(test, TS_FEATURES), args.ridge_alpha)
        score = (zscore(qlib) + zscore(ta) + zscore(ts)) / 3.0
        detail = "QuantBench-style Alpha/indicator/time-series ensemble proxy"
    else:
        raise ValueError(method)

    scored = [{"date": str(row["date"]), "symbol": str(row["symbol"]), "score": float(value), "label": float(row["label"])} for row, value in zip(test, score)]
    return scored, {"proxy_detail": detail}


def add_meta(scored_rows: list[dict], panel_path: Path, stock_basic_path: Path) -> None:
    meta = read_meta(panel_path, read_industry(stock_basic_path))
    for row in scored_rows:
        row_meta = meta.get((row["date"], row["symbol"]), {})
        row["industry"] = row_meta.get("industry", "UNKNOWN")
        row["total_mv"] = float(row_meta.get("total_mv", float("nan")))


def add_neutral_scores(scored_rows: list[dict]) -> None:
    by_date: dict[str, list[dict]] = defaultdict(list)
    for row in scored_rows:
        by_date[row["date"]].append(row)
    for date_rows in by_date.values():
        residuals = residualize_scores(date_rows)
        for row, residual in zip(date_rows, residuals):
            row["neutral_score"] = float(residual)


def write_scores(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "symbol", "score", "label"])
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row[name] for name in ["date", "symbol", "score", "label"]})


def write_summary(path: Path, rows: list[dict]) -> None:
    fields = [
        "market",
        "method",
        "proxy_detail",
        "variant",
        "horizon",
        "topk",
        "cost_bps",
        "days",
        "ann_return",
        "ann_vol",
        "sharpe",
        "mdd",
        "cum_return",
        "active_ann_return",
        "active_sharpe",
        "avg_turnover",
        "hit_rate",
        "avg_max_industry_weight",
        "avg_size_exposure",
        "yearly_ann_returns",
        "daily_source",
        "score_source",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = PROJECT_ROOT / out_dir
    panel_path = Path(args.panel)
    stock_basic_path = Path(args.stock_basic)
    methods = args.method or CANDIDATE_METHODS
    rows = build_examples(load_panel(panel_path), args.horizon)
    if not rows:
        raise RuntimeError("no feature rows built from panel")

    summary_rows: list[dict] = []
    for method in methods:
        scored_rows, info = generate_scores(args, method, rows)
        add_meta(scored_rows, panel_path, stock_basic_path)
        add_neutral_scores(scored_rows)
        score_path = out_dir / f"{method}_scores.csv"
        write_scores(score_path, scored_rows)
        for variant, score_field in [("raw", "score"), ("industry_size_neutral", "neutral_score")]:
            daily = backtest(scored_rows, score_field, args.topk, args.horizon, args.cost_bps)
            daily_path = out_dir / f"{method}_h{args.horizon}_top{args.topk}_{variant}_daily.csv"
            write_daily(daily_path, daily)
            stats = performance_stats(daily, "net_return")
            active_stats = performance_stats(daily, "net_active_return")
            years = sorted(set(row["date"][:4] for row in daily))
            yearly_returns = []
            for year in years:
                year_rows = [row for row in daily if row["date"].startswith(year)]
                yearly_returns.append((year, performance_stats(year_rows, "net_return")["ann_return"]))
            summary_rows.append(
                {
                    "market": args.market,
                    "method": method,
                    "proxy_detail": info["proxy_detail"],
                    "variant": variant,
                    "horizon": str(args.horizon),
                    "topk": str(args.topk),
                    "cost_bps": f"{args.cost_bps:.2f}",
                    "days": str(len(daily)),
                    "ann_return": f"{stats['ann_return']:.8f}",
                    "ann_vol": f"{stats['ann_vol']:.8f}",
                    "sharpe": f"{stats['sharpe']:.8f}",
                    "mdd": f"{stats['mdd']:.8f}",
                    "cum_return": f"{stats['cum_return']:.8f}",
                    "active_ann_return": f"{active_stats['ann_return']:.8f}",
                    "active_sharpe": f"{active_stats['sharpe']:.8f}",
                    "avg_turnover": f"{stats['avg_turnover']:.8f}",
                    "hit_rate": f"{stats['hit_rate']:.8f}",
                    "avg_max_industry_weight": f"{float(np.mean([row['max_industry_weight'] for row in daily])):.8f}",
                    "avg_size_exposure": f"{float(np.mean([row['size_exposure'] for row in daily])):.8f}",
                    "yearly_ann_returns": ";".join(f"{year}:{value:.4f}" for year, value in yearly_returns),
                    "daily_source": str(daily_path.relative_to(PROJECT_ROOT)),
                    "score_source": str(score_path.relative_to(PROJECT_ROOT)),
                }
            )
            print(method, args.market, variant, stats)

    write_summary(out_dir / "unvalidated_candidate_trade_validation_summary.csv", summary_rows)
    print(f"wrote {out_dir / 'unvalidated_candidate_trade_validation_summary.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
