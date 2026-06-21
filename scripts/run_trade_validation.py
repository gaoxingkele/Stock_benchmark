"""Run trading validation for paper-inspired China A-share scores."""

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

from run_paper_model_baseline import (  # noqa: E402
    MODEL_MODES,
    apply_doubleadapt,
    fit_adarnn,
    fit_single,
    fit_tcts,
    fit_tra,
    load_panel,
    make_examples,
    sample_train,
    split_examples,
)


DEFAULT_MODELS = [
    "rd_agent_quant",
    "diffsformer",
    "doubleadapt",
    "doubleensemble",
    "alphaprobe",
    "master",
    "tcts",
    "hist",
    "tra",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--panel", default=str(PROJECT_ROOT / "data" / "processed" / "cn_a_share" / "csi300_2018_2024" / "panel.csv"))
    parser.add_argument("--stock-basic", default=str(PROJECT_ROOT / "data" / "raw" / "tushare" / "csi300_2018_2024" / "stock_basic.csv"))
    parser.add_argument("--model", action="append", choices=sorted(MODEL_MODES))
    parser.add_argument("--horizon", type=int, default=5)
    parser.add_argument("--lookback", type=int, default=20)
    parser.add_argument("--topk", type=int, default=30)
    parser.add_argument("--cost-bps", type=float, default=10.0)
    parser.add_argument("--train-start", default="2018-01-02")
    parser.add_argument("--train-end", default="2021-12-31")
    parser.add_argument("--valid-start", default="2022-01-04")
    parser.add_argument("--valid-end", default="2022-12-30")
    parser.add_argument("--test-start", default="2023-01-03")
    parser.add_argument("--test-end", default="2024-12-31")
    parser.add_argument("--ridge-alpha", type=float, default=10.0)
    parser.add_argument("--max-train-rows", type=int, default=250000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out-dir", default=str(PROJECT_ROOT / "experiments" / "trade_validation"))
    return parser.parse_args()


def read_industry(path: Path) -> dict[str, str]:
    mapping: dict[str, str] = {}
    with path.open("r", newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            mapping[row["ts_code"]] = row.get("industry") or "UNKNOWN"
    return mapping


def read_meta(panel_path: Path, industry: dict[str, str]) -> dict[tuple[str, str], dict[str, str | float]]:
    meta: dict[tuple[str, str], dict[str, str | float]] = {}
    with panel_path.open("r", newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            try:
                total_mv = float(row["total_mv"])
            except (TypeError, ValueError):
                total_mv = float("nan")
            meta[(row["date"], row["symbol"])] = {
                "ts_code": row["ts_code"],
                "industry": industry.get(row["ts_code"], "UNKNOWN"),
                "total_mv": total_mv,
            }
    return meta


def fit_predictions(args: argparse.Namespace, model: str) -> tuple[list[dict], np.ndarray]:
    mode = MODEL_MODES[model]
    by_symbol, market_by_date = load_panel(Path(args.panel))
    if mode == "tcts":
        return fit_tcts(by_symbol, market_by_date, args)
    examples = make_examples(by_symbol, market_by_date, args.horizon, args.lookback, mode)
    train = sample_train(split_examples(examples, args.train_start, args.train_end), args.max_train_rows, args.seed)
    valid = split_examples(examples, args.valid_start, args.valid_end)
    test = split_examples(examples, args.test_start, args.test_end)
    if mode == "tra":
        preds = fit_tra(train, valid, test, args.ridge_alpha)
    elif mode == "master":
        preds = fit_single(train, valid, test, args.ridge_alpha)
    elif mode == "doubleadapt":
        base_preds = fit_single(train, valid, test, args.ridge_alpha)
        preds = apply_doubleadapt(base_preds, test)
    elif mode == "adarnn":
        preds = fit_adarnn(train, valid, test, args.ridge_alpha)
    elif mode == "hist":
        preds = fit_single(train, valid, test, args.ridge_alpha)
    else:
        raise ValueError(mode)
    return test, preds


def residualize_scores(rows: list[dict]) -> np.ndarray:
    scores = np.asarray([row["score"] for row in rows], dtype=float)
    sizes = np.asarray([math.log(max(row["total_mv"], 1.0)) if math.isfinite(row["total_mv"]) else 0.0 for row in rows], dtype=float)
    industries = sorted(set(str(row["industry"]) for row in rows))
    columns = [np.ones(len(rows)), sizes]
    for industry in industries[1:]:
        columns.append(np.asarray([1.0 if row["industry"] == industry else 0.0 for row in rows], dtype=float))
    design = np.column_stack(columns)
    try:
        beta, *_ = np.linalg.lstsq(design, scores, rcond=None)
        return scores - design @ beta
    except np.linalg.LinAlgError:
        return scores - np.nanmean(scores)


def max_drawdown(returns: list[float]) -> float:
    nav = 1.0
    peak = 1.0
    worst = 0.0
    for ret in returns:
        nav *= 1.0 + ret
        peak = max(peak, nav)
        worst = min(worst, nav / peak - 1.0)
    return worst


def performance_stats(rows: list[dict], key: str) -> dict[str, float]:
    values = [float(row[key]) for row in rows]
    if not values:
        return {name: float("nan") for name in ["ann_return", "ann_vol", "sharpe", "mdd", "avg_turnover", "hit_rate", "cum_return"]}
    nav = float(np.prod([1.0 + value for value in values]))
    ann_return = nav ** (252.0 / len(values)) - 1.0
    ann_vol = float(np.std(values, ddof=0) * math.sqrt(252.0))
    sharpe = ann_return / ann_vol if ann_vol else float("nan")
    return {
        "ann_return": ann_return,
        "ann_vol": ann_vol,
        "sharpe": sharpe,
        "mdd": max_drawdown(values),
        "avg_turnover": float(np.mean([float(row["turnover"]) for row in rows])),
        "hit_rate": float(np.mean([value > 0 for value in values])),
        "cum_return": nav - 1.0,
    }


def backtest(scored_rows: list[dict], score_field: str, topk: int, horizon: int, cost_bps: float) -> list[dict]:
    by_date: dict[str, list[dict]] = defaultdict(list)
    for row in scored_rows:
        by_date[row["date"]].append(row)
    previous_weights: dict[str, float] = {}
    daily_rows: list[dict] = []
    cost_rate = cost_bps / 10000.0
    for date in sorted(by_date):
        rows = by_date[date]
        rows = [row for row in rows if math.isfinite(float(row[score_field])) and math.isfinite(float(row["label"]))]
        if len(rows) < topk:
            continue
        selected = sorted(rows, key=lambda row: float(row[score_field]), reverse=True)[:topk]
        weight = 1.0 / topk
        weights = {row["symbol"]: weight for row in selected}
        symbols = set(weights) | set(previous_weights)
        turnover = 0.5 * sum(abs(weights.get(symbol, 0.0) - previous_weights.get(symbol, 0.0)) for symbol in symbols)
        gross = float(np.mean([float(row["label"]) for row in selected]) / horizon)
        benchmark = float(np.mean([float(row["label"]) for row in rows]) / horizon)
        net = gross - turnover * cost_rate
        industry_weights: dict[str, float] = defaultdict(float)
        selected_size = []
        universe_size = []
        for row in selected:
            industry_weights[str(row["industry"])] += weight
            if math.isfinite(row["total_mv"]):
                selected_size.append(math.log(max(row["total_mv"], 1.0)))
        for row in rows:
            if math.isfinite(row["total_mv"]):
                universe_size.append(math.log(max(row["total_mv"], 1.0)))
        daily_rows.append(
            {
                "date": date,
                "n": len(rows),
                "topk": topk,
                "gross_return": gross,
                "benchmark_return": benchmark,
                "active_return": gross - benchmark,
                "net_return": net,
                "net_active_return": net - benchmark,
                "turnover": turnover,
                "cost": turnover * cost_rate,
                "max_industry_weight": max(industry_weights.values()) if industry_weights else float("nan"),
                "size_exposure": float(np.mean(selected_size) - np.mean(universe_size)) if selected_size and universe_size else float("nan"),
            }
        )
        previous_weights = weights
    return daily_rows


def write_daily(path: Path, rows: list[dict]) -> None:
    fields = [
        "date",
        "n",
        "topk",
        "gross_return",
        "benchmark_return",
        "active_return",
        "net_return",
        "net_active_return",
        "turnover",
        "cost",
        "max_industry_weight",
        "size_exposure",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    models = args.model or DEFAULT_MODELS
    meta = read_meta(Path(args.panel), read_industry(Path(args.stock_basic)))
    summary_rows: list[dict[str, str]] = []
    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = PROJECT_ROOT / out_dir
    prediction_cache: dict[str, tuple[list[dict], np.ndarray]] = {}
    for model in models:
        mode = MODEL_MODES[model]
        if mode not in prediction_cache:
            prediction_cache[mode] = fit_predictions(args, model)
        test_rows, preds = prediction_cache[mode]
        scored_rows = []
        for row, score in zip(test_rows, preds):
            row_meta = meta.get((row["date"], row["symbol"]), {})
            scored_rows.append(
                {
                    "date": row["date"],
                    "symbol": row["symbol"],
                    "score": float(score),
                    "label": float(row["label"]),
                    "industry": row_meta.get("industry", "UNKNOWN"),
                    "total_mv": float(row_meta.get("total_mv", float("nan"))),
                }
            )
        by_date: dict[str, list[dict]] = defaultdict(list)
        for row in scored_rows:
            by_date[row["date"]].append(row)
        for rows in by_date.values():
            residuals = residualize_scores(rows)
            for row, residual in zip(rows, residuals):
                row["neutral_score"] = float(residual)
        for variant, score_field in [("raw", "score"), ("industry_size_neutral", "neutral_score")]:
            daily = backtest(scored_rows, score_field, args.topk, args.horizon, args.cost_bps)
            write_daily(out_dir / f"{model}_h{args.horizon}_top{args.topk}_{variant}_daily.csv", daily)
            stats = performance_stats(daily, "net_return")
            active_stats = performance_stats(daily, "net_active_return")
            years = sorted(set(row["date"][:4] for row in daily))
            yearly_returns = []
            for year in years:
                year_rows = [row for row in daily if row["date"].startswith(year)]
                yearly_returns.append((year, performance_stats(year_rows, "net_return")["ann_return"]))
            summary_rows.append(
                {
                    "model": model,
                    "proxy_mode": mode,
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
                    "daily_source": str((out_dir / f"{model}_h{args.horizon}_top{args.topk}_{variant}_daily.csv").relative_to(PROJECT_ROOT)),
                }
            )
            print(model, variant, stats)
    summary_path = out_dir / "trade_validation_summary.csv"
    fields = list(summary_rows[0])
    with summary_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(summary_rows)
    print(f"summary={summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
