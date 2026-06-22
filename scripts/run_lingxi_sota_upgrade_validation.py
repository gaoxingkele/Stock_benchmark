"""Validate lightweight SOTA-inspired Lingxi10/Lingxi5 upgrade proxies."""

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

import run_lingxi_topk_comparison as topk_comparison  # noqa: E402
from run_lingxi_fusion_validation import MARKETS  # noqa: E402
from run_lingxi_topk_comparison import (  # noqa: E402
    add_lingxi_neutral_scores,
    build_lingxi_scores,
    summarize_daily,
)
from run_unvalidated_paper_candidates import (  # noqa: E402
    add_meta,
    build_examples,
    formula_score,
    load_panel,
    ridge_fit_predict,
    rows_to_matrix,
    select_formula_features,
    zscore,
)


topk_comparison.MARKETS.update(MARKETS)


METHOD_LABELS = {
    "lingxi": "Lingxi / RDA-Adapt",
    "lingxi_linear_guard": "Lingxi-LinearGuard / DLinear-style",
    "lingxi_pitnorm": "Lingxi-PITNorm / non-stationary score norm",
    "lingxi_mscale": "Lingxi-MScale / multiscale decomposition",
    "lingxi_patch": "Lingxi-Patch / patch summary proxy",
    "lingxi_varattn": "Lingxi-VarAttn / cross-sectional attention proxy",
}

LINEAR_FEATURES = ["mom_20", "ma_gap_20", "rev_5", "vol_20", "size"]
MSCALE_FEATURES = [
    "mom_5",
    "mom_10",
    "mom_20",
    "mom_60",
    "ma_gap_5",
    "ma_gap_20",
    "vol_20",
    "vol_60",
    "range_20",
    "rsi_14",
    "macd_proxy",
]
PATCH_FEATURES = [
    "mom_5",
    "mom_10",
    "mom_20",
    "rev_5",
    "ma_gap_5",
    "ma_gap_20",
    "vol_20",
    "range_20",
    "volume_z_20",
    "price_range",
    "oc_return",
]
VARATTN_FEATURES = [
    "mom_5",
    "mom_10",
    "mom_20",
    "mom_60",
    "rev_5",
    "ma_gap_20",
    "vol_20",
    "vol_60",
    "range_20",
    "volume_z_20",
    "amount_z_20",
    "turnover_rate",
    "pe_z",
    "pb_z",
    "size",
    "price_range",
    "oc_return",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--market", action="append", choices=sorted(MARKETS))
    parser.add_argument("--topk", action="append", type=int)
    parser.add_argument("--horizon", type=int, default=5)
    parser.add_argument("--lookback", type=int, default=20)
    parser.add_argument("--cost-bps", type=float, default=10.0)
    parser.add_argument("--train-start", default="2018-01-02")
    parser.add_argument("--train-end", default="2021-12-31")
    parser.add_argument("--valid-end", default="2022-12-30")
    parser.add_argument("--test-start", default="2023-01-03")
    parser.add_argument("--test-end", default="2025-12-31")
    parser.add_argument("--ridge-alpha", type=float, default=10.0)
    parser.add_argument("--candidate-ridge-alpha", type=float, default=25.0)
    parser.add_argument("--max-train-rows", type=int, default=250000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out-dir", default=str(PROJECT_ROOT / "experiments/lingxi_sota_upgrade_validation"))
    return parser.parse_args()


def sample_train(rows: list[dict[str, float | str]], max_rows: int, seed: int) -> list[dict[str, float | str]]:
    if len(rows) <= max_rows:
        return rows
    rng = np.random.default_rng(seed)
    idx = np.sort(rng.choice(len(rows), size=max_rows, replace=False))
    return [rows[int(i)] for i in idx]


def split(rows: list[dict[str, float | str]], start: str, end: str) -> list[dict[str, float | str]]:
    return [row for row in rows if start <= str(row["date"]) <= end]


def make_scored(test: list[dict[str, float | str]], score: np.ndarray) -> list[dict]:
    return [
        {"date": str(row["date"]), "symbol": str(row["symbol"]), "score": float(value), "label": float(row["label"])}
        for row, value in zip(test, score)
    ]


def ridge_scores(
    rows: list[dict[str, float | str]],
    args: argparse.Namespace,
    features: list[str],
) -> tuple[list[dict], np.ndarray, list[dict[str, float | str]]]:
    train = sample_train(split(rows, args.train_start, args.train_end), args.max_train_rows, args.seed)
    test = split(rows, args.test_start, args.test_end)
    y = np.asarray([float(row["label"]) for row in train], dtype=float)
    score = ridge_fit_predict(rows_to_matrix(train, features), y, rows_to_matrix(test, features), args.candidate_ridge_alpha)
    return make_scored(test, score), score, test


def make_varattn_scores(rows: list[dict[str, float | str]], args: argparse.Namespace) -> list[dict]:
    train = sample_train(split(rows, args.train_start, args.train_end), args.max_train_rows, args.seed)
    valid = split(rows, args.valid_start, args.valid_end)
    test = split(rows, args.test_start, args.test_end)
    y = np.asarray([float(row["label"]) for row in train], dtype=float)
    ridge = ridge_fit_predict(rows_to_matrix(train, VARATTN_FEATURES), y, rows_to_matrix(test, VARATTN_FEATURES), args.candidate_ridge_alpha)
    selected, weights = select_formula_features(valid, VARATTN_FEATURES, max_features=10)
    attention = formula_score(test, selected, weights)
    score = zscore(ridge) + 0.35 * zscore(attention)
    return make_scored(test, score)


def make_pitnorm_scores(lingxi_rows: list[dict], min_history: int = 20) -> list[dict]:
    by_symbol: dict[str, list[dict]] = defaultdict(list)
    for row in lingxi_rows:
        by_symbol[row["symbol"]].append(row)
    out: list[dict] = []
    for rows in by_symbol.values():
        rows.sort(key=lambda row: row["date"])
        history: list[float] = []
        for row in rows:
            score = float(row["score"])
            if len(history) >= min_history:
                mean = float(np.mean(history[-60:]))
                std = float(np.std(history[-60:]))
                norm = (score - mean) / std if std > 1e-12 else score - mean
            else:
                norm = score
            out.append({**row, "score": float(norm)})
            history.append(score)
    out.sort(key=lambda row: (row["date"], row["symbol"]))
    add_lingxi_neutral_scores(out)
    return out


def build_sota_scores(args: argparse.Namespace, market: str, panel: Path, stock_basic: Path, lingxi_rows: list[dict]) -> dict[str, list[dict]]:
    candidate_args = argparse.Namespace(**vars(args))
    candidate_args.panel = str(panel)
    candidate_args.stock_basic = str(stock_basic)
    candidate_args.market = market
    candidate_args.valid_start = MARKETS[market]["valid_start"]
    candidate_args.ridge_alpha = args.candidate_ridge_alpha
    rows = build_examples(load_panel(panel), args.horizon)

    outputs: dict[str, list[dict]] = {
        "lingxi_pitnorm": make_pitnorm_scores(lingxi_rows),
    }
    for method, features in [
        ("lingxi_linear_guard", LINEAR_FEATURES),
        ("lingxi_mscale", MSCALE_FEATURES),
        ("lingxi_patch", PATCH_FEATURES),
    ]:
        scored, _, _ = ridge_scores(rows, candidate_args, features)
        add_meta(scored, panel, stock_basic)
        add_lingxi_neutral_scores(scored)
        outputs[method] = scored
        print(f"{market} {method} scored_rows={len(scored)}")

    varattn = make_varattn_scores(rows, candidate_args)
    add_meta(varattn, panel, stock_basic)
    add_lingxi_neutral_scores(varattn)
    outputs["lingxi_varattn"] = varattn
    print(f"{market} lingxi_varattn scored_rows={len(varattn)}")
    return outputs


def write_summary(path: Path, rows: list[dict[str, str]]) -> None:
    fields = list(rows[0])
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    markets = args.market or ["cn_a_share", "us_large_cap", "hk_large_cap", "crypto_major"]
    requested_topks = sorted(set(args.topk or [5, 10]), reverse=True)
    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = PROJECT_ROOT / out_dir

    summary_rows: list[dict[str, str]] = []
    for market in markets:
        config = MARKETS[market]
        args.valid_start = config["valid_start"]
        panel = config["panel"]
        stock_basic = config["stock_basic"]
        market_topks = [topk for topk in requested_topks if topk <= int(config.get("max_topk", topk))]

        lingxi = build_lingxi_scores(args, market, panel, stock_basic)
        method_scores = {"lingxi": lingxi}
        method_scores.update(build_sota_scores(args, market, panel, stock_basic, lingxi))

        for method, scored_rows in method_scores.items():
            for topk in market_topks:
                for variant, score_field in [("raw", "score"), ("industry_size_neutral", "neutral_score")]:
                    row = summarize_daily(out_dir, market, method, topk, variant, score_field, scored_rows, args)
                    row["method_label"] = METHOD_LABELS[method]
                    summary_rows.append(row)
                    print(market, method, f"top{topk}", variant, row["ann_return"], row["sharpe"], row["mdd"])

    write_summary(out_dir / "lingxi_sota_upgrade_validation_summary.csv", summary_rows)
    print(f"summary={out_dir / 'lingxi_sota_upgrade_validation_summary.csv'} rows={len(summary_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
