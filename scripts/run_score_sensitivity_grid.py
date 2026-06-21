"""Run TopK and cost sensitivity for an external score CSV."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from run_score_trade_validation import add_neutral_scores, load_scored_rows  # noqa: E402
from run_trade_validation import backtest, performance_stats  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scores", required=True)
    parser.add_argument("--panel", required=True)
    parser.add_argument("--stock-basic", required=True)
    parser.add_argument("--method", required=True)
    parser.add_argument("--horizon", type=int, default=5)
    parser.add_argument("--topk-grid", default="20,30,50")
    parser.add_argument("--cost-bps-grid", default="5,10,20")
    parser.add_argument("--test-start", default="2023-01-03")
    parser.add_argument("--test-end", default="2024-12-31")
    parser.add_argument("--out", required=True)
    parser.add_argument("--date-column", default="date")
    parser.add_argument("--symbol-column", default="symbol")
    parser.add_argument("--score-column", default="score")
    parser.add_argument("--label-column", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    scored_rows = load_scored_rows(args)
    if not scored_rows:
        raise RuntimeError("no scored rows after joining scores, labels, and test window")
    add_neutral_scores(scored_rows)
    topk_values = [int(item.strip()) for item in args.topk_grid.split(",") if item.strip()]
    cost_values = [float(item.strip()) for item in args.cost_bps_grid.split(",") if item.strip()]
    rows: list[dict[str, str]] = []
    for topk in topk_values:
        for cost_bps in cost_values:
            for variant, score_field in [("raw", "score"), ("industry_size_neutral", "neutral_score")]:
                daily = backtest(scored_rows, score_field, topk, args.horizon, cost_bps)
                stats = performance_stats(daily, "net_return")
                active_stats = performance_stats(daily, "net_active_return")
                rows.append(
                    {
                        "method": args.method,
                        "variant": variant,
                        "horizon": str(args.horizon),
                        "topk": str(topk),
                        "cost_bps": f"{cost_bps:.2f}",
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
                    }
                )
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
