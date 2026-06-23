"""Build unified CASE-Lingxi promotion audit with paired bootstrap statistics."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]


CANDIDATES = {
    "case_lingxi_context_router": {
        "summary": PROJECT_ROOT / "experiments/case_lingxi_context_router_validation_2026_ytd/case_lingxi_context_router_validation_summary.csv",
        "base_dir": PROJECT_ROOT / "experiments/case_lingxi_context_router_validation_2026_ytd",
        "menu": "case_lingxi_static_menu",
        "label": "Conservative context router",
    },
    "case_lingxi_tabular_rl_router": {
        "summary": PROJECT_ROOT / "experiments/case_lingxi_rl_router_validation_2025_2026_ytd/case_lingxi_rl_router_validation_summary.csv",
        "base_dir": PROJECT_ROOT / "experiments/case_lingxi_rl_router_validation_2025_2026_ytd",
        "menu": "case_lingxi_static_menu",
        "label": "Frozen tabular RL router",
    },
    "case_lingxi_market_tag_router": {
        "summary": PROJECT_ROOT / "experiments/case_lingxi_llm_tag_ablation_2026_ytd/case_lingxi_llm_tag_ablation_summary.csv",
        "base_dir": PROJECT_ROOT / "experiments/case_lingxi_llm_tag_ablation_2026_ytd",
        "menu": "case_lingxi_static_menu",
        "label": "Structured market-tag router",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", default=str(PROJECT_ROOT / "experiments/case_lingxi_promotion_audit"))
    parser.add_argument("--bootstrap-samples", type=int, default=1000)
    parser.add_argument("--block-size", type=int, default=5)
    parser.add_argument("--seed", type=int, default=20260623)
    return parser.parse_args()


def resolve(path: str) -> Path:
    value = Path(path)
    return value if value.is_absolute() else PROJECT_ROOT / value


def read_summary(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def read_daily(path: Path) -> dict[str, float]:
    with path.open(newline="", encoding="utf-8") as file:
        return {row["date"]: float(row["net_return"]) for row in csv.DictReader(file)}


def max_drawdown(returns: np.ndarray) -> float:
    nav = 1.0
    peak = 1.0
    worst = 0.0
    for value in returns:
        nav *= 1.0 + float(value)
        peak = max(peak, nav)
        worst = min(worst, nav / peak - 1.0)
    return worst


def sharpe(returns: np.ndarray) -> float:
    if len(returns) < 2:
        return 0.0
    vol = float(np.std(returns))
    if vol <= 1e-12 or not math.isfinite(vol):
        return 0.0
    return float(np.mean(returns) / vol * math.sqrt(252.0))


def ann_return(returns: np.ndarray) -> float:
    if len(returns) == 0:
        return 0.0
    nav = float(np.prod(1.0 + returns))
    return nav ** (252.0 / len(returns)) - 1.0


def block_bootstrap_ci(diff: np.ndarray, samples: int, block_size: int, rng: np.random.Generator) -> tuple[float, float]:
    if len(diff) == 0:
        return 0.0, 0.0
    block_size = max(1, min(block_size, len(diff)))
    means = []
    starts = np.arange(0, len(diff))
    for _ in range(samples):
        sampled = []
        while len(sampled) < len(diff):
            start = int(rng.choice(starts))
            end = min(len(diff), start + block_size)
            sampled.extend(diff[start:end])
        means.append(float(np.mean(sampled[: len(diff)]) * 252.0))
    low, high = np.quantile(np.asarray(means), [0.025, 0.975])
    return float(low), float(high)


def status_for(candidate: str, ann_win: bool, sharpe_win: bool, mdd_win: bool, ann_diff_ci_low: float) -> str:
    if candidate == "case_lingxi_context_router" and mdd_win and ann_diff_ci_low < 0:
        return "risk_control_candidate"
    if ann_win and sharpe_win and ann_diff_ci_low > 0 and mdd_win:
        return "research_sleeve_candidate"
    return "negative_control"


def main() -> int:
    args = parse_args()
    out_dir = resolve(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.seed)

    detail_rows: list[dict[str, str]] = []
    aggregate: dict[str, dict[str, int | str]] = {}

    for candidate, meta in CANDIDATES.items():
        rows = read_summary(meta["summary"])
        by_key = {(row["market"], row["topk"], row["variant"], row["method"]): row for row in rows}
        aggregate[candidate] = {
            "candidate": candidate,
            "label": str(meta["label"]),
            "scenarios": 0,
            "ann_wins": 0,
            "sharpe_wins": 0,
            "mdd_wins": 0,
            "positive_ann_ci_wins": 0,
            "state": "",
        }
        candidate_rows = [row for row in rows if row["method"] == candidate]
        for row in candidate_rows:
            key = (row["market"], row["topk"], row["variant"], str(meta["menu"]))
            menu = by_key[key]
            daily_candidate = read_daily(PROJECT_ROOT / row["daily_source"])
            daily_menu = read_daily(PROJECT_ROOT / menu["daily_source"])
            dates = sorted(set(daily_candidate) & set(daily_menu))
            cand_returns = np.asarray([daily_candidate[date] for date in dates], dtype=float)
            menu_returns = np.asarray([daily_menu[date] for date in dates], dtype=float)
            diff = cand_returns - menu_returns
            ann_diff = ann_return(cand_returns) - ann_return(menu_returns)
            sharpe_diff = sharpe(cand_returns) - sharpe(menu_returns)
            mdd_diff = max_drawdown(cand_returns) - max_drawdown(menu_returns)
            ci_low, ci_high = block_bootstrap_ci(diff, args.bootstrap_samples, args.block_size, rng)
            ann_win = ann_diff > 0
            sharpe_win = sharpe_diff > 0
            mdd_win = mdd_diff > 0
            state = status_for(candidate, ann_win, sharpe_win, mdd_win, ci_low)

            aggregate[candidate]["scenarios"] = int(aggregate[candidate]["scenarios"]) + 1
            aggregate[candidate]["ann_wins"] = int(aggregate[candidate]["ann_wins"]) + int(ann_win)
            aggregate[candidate]["sharpe_wins"] = int(aggregate[candidate]["sharpe_wins"]) + int(sharpe_win)
            aggregate[candidate]["mdd_wins"] = int(aggregate[candidate]["mdd_wins"]) + int(mdd_win)
            aggregate[candidate]["positive_ann_ci_wins"] = int(aggregate[candidate]["positive_ann_ci_wins"]) + int(ci_low > 0)

            detail_rows.append(
                {
                    "candidate": candidate,
                    "candidate_label": str(meta["label"]),
                    "market": row["market"],
                    "topk": row["topk"],
                    "variant": row["variant"],
                    "days": str(len(dates)),
                    "candidate_ann_return": row["ann_return"],
                    "menu_ann_return": menu["ann_return"],
                    "ann_diff": f"{ann_diff:.8f}",
                    "candidate_sharpe": row["sharpe"],
                    "menu_sharpe": menu["sharpe"],
                    "sharpe_diff": f"{sharpe_diff:.8f}",
                    "candidate_mdd": row["mdd"],
                    "menu_mdd": menu["mdd"],
                    "mdd_diff": f"{mdd_diff:.8f}",
                    "ann_diff_bootstrap_ci_low": f"{ci_low:.8f}",
                    "ann_diff_bootstrap_ci_high": f"{ci_high:.8f}",
                    "ann_win": str(ann_win),
                    "sharpe_win": str(sharpe_win),
                    "mdd_win": str(mdd_win),
                    "positive_ann_ci": str(ci_low > 0),
                    "state": state,
                    "candidate_daily_source": row["daily_source"],
                    "menu_daily_source": menu["daily_source"],
                }
            )

    aggregate_rows: list[dict[str, str]] = []
    for candidate, row in aggregate.items():
        scenarios = int(row["scenarios"])
        ann_wins = int(row["ann_wins"])
        sharpe_wins = int(row["sharpe_wins"])
        mdd_wins = int(row["mdd_wins"])
        positive_ci = int(row["positive_ann_ci_wins"])
        if ann_wins >= 10 and sharpe_wins >= 10 and mdd_wins >= 12 and positive_ci >= 8:
            state = "production_candidate"
        elif candidate == "case_lingxi_context_router" and mdd_wins >= 8:
            state = "risk_control_candidate"
        else:
            state = "negative_control"
        aggregate_rows.append(
            {
                "candidate": candidate,
                "label": str(row["label"]),
                "scenarios": str(scenarios),
                "ann_wins": str(ann_wins),
                "sharpe_wins": str(sharpe_wins),
                "mdd_wins": str(mdd_wins),
                "positive_ann_ci_wins": str(positive_ci),
                "state": state,
            }
        )

    detail_path = out_dir / "case_lingxi_promotion_audit_detail.csv"
    with detail_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(detail_rows[0]))
        writer.writeheader()
        writer.writerows(detail_rows)

    aggregate_path = out_dir / "case_lingxi_promotion_audit_summary.csv"
    with aggregate_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(aggregate_rows[0]))
        writer.writeheader()
        writer.writerows(aggregate_rows)

    print(f"detail={detail_path} rows={len(detail_rows)}")
    print(f"summary={aggregate_path} rows={len(aggregate_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
