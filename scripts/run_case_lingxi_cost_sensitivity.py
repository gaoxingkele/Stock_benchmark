"""Run CASE-Lingxi candidate-vs-menu cost sensitivity audit."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMOTION_DETAIL = PROJECT_ROOT / "experiments/case_lingxi_promotion_audit/case_lingxi_promotion_audit_detail.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--promotion-detail", default=str(PROMOTION_DETAIL))
    parser.add_argument("--out-dir", default=str(PROJECT_ROOT / "experiments/case_lingxi_cost_sensitivity"))
    parser.add_argument("--cost-bps", type=float, nargs="+", default=[0.0, 5.0, 10.0, 20.0, 50.0])
    return parser.parse_args()


def resolve(path: str) -> Path:
    value = Path(path)
    return value if value.is_absolute() else PROJECT_ROOT / value


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def read_daily(path: Path) -> dict[str, dict[str, float]]:
    out = {}
    with path.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            out[row["date"]] = {
                "net_return": float(row["net_return"]),
                "cost": float(row.get("cost", 0.0)),
                "turnover": float(row.get("turnover", 0.0)),
            }
    return out


def adjusted_returns(rows: dict[str, dict[str, float]], dates: list[str], cost_bps: float) -> np.ndarray:
    values = []
    for date in dates:
        row = rows[date]
        gross = row["net_return"] + row["cost"]
        cost = row["turnover"] * cost_bps / 10000.0
        values.append(gross - cost)
    return np.asarray(values, dtype=float)


def ann_return(returns: np.ndarray) -> float:
    if len(returns) == 0:
        return 0.0
    nav = float(np.prod(1.0 + returns))
    return nav ** (252.0 / len(returns)) - 1.0


def sharpe(returns: np.ndarray) -> float:
    if len(returns) < 2:
        return 0.0
    vol = float(np.std(returns))
    if vol <= 1e-12 or not math.isfinite(vol):
        return 0.0
    return float(np.mean(returns) / vol * math.sqrt(252.0))


def mdd(returns: np.ndarray) -> float:
    nav = 1.0
    peak = 1.0
    worst = 0.0
    for value in returns:
        nav *= 1.0 + float(value)
        peak = max(peak, nav)
        worst = min(worst, nav / peak - 1.0)
    return worst


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    detail_rows = read_csv(resolve(args.promotion_detail))
    out_dir = resolve(args.out_dir)

    scenario_rows: list[dict[str, str]] = []
    aggregate: dict[tuple[str, float], dict[str, int | str]] = {}

    for row in detail_rows:
        candidate = row["candidate"]
        label = row["candidate_label"]
        candidate_daily = read_daily(PROJECT_ROOT / row["candidate_daily_source"])
        menu_daily = read_daily(PROJECT_ROOT / row["menu_daily_source"])
        dates = sorted(set(candidate_daily) & set(menu_daily))
        for cost_bps in args.cost_bps:
            cand = adjusted_returns(candidate_daily, dates, cost_bps)
            menu = adjusted_returns(menu_daily, dates, cost_bps)
            cand_ann = ann_return(cand)
            menu_ann = ann_return(menu)
            cand_sharpe = sharpe(cand)
            menu_sharpe = sharpe(menu)
            cand_mdd = mdd(cand)
            menu_mdd = mdd(menu)
            ann_win = cand_ann > menu_ann
            sharpe_win = cand_sharpe > menu_sharpe
            mdd_win = cand_mdd > menu_mdd
            key = (candidate, cost_bps)
            if key not in aggregate:
                aggregate[key] = {
                    "candidate": candidate,
                    "candidate_label": label,
                    "cost_bps": f"{cost_bps:.2f}",
                    "scenarios": 0,
                    "ann_wins": 0,
                    "sharpe_wins": 0,
                    "mdd_wins": 0,
                }
            aggregate[key]["scenarios"] = int(aggregate[key]["scenarios"]) + 1
            aggregate[key]["ann_wins"] = int(aggregate[key]["ann_wins"]) + int(ann_win)
            aggregate[key]["sharpe_wins"] = int(aggregate[key]["sharpe_wins"]) + int(sharpe_win)
            aggregate[key]["mdd_wins"] = int(aggregate[key]["mdd_wins"]) + int(mdd_win)

            scenario_rows.append(
                {
                    "candidate": candidate,
                    "candidate_label": label,
                    "market": row["market"],
                    "topk": row["topk"],
                    "variant": row["variant"],
                    "cost_bps": f"{cost_bps:.2f}",
                    "days": str(len(dates)),
                    "candidate_ann_return": f"{cand_ann:.8f}",
                    "menu_ann_return": f"{menu_ann:.8f}",
                    "ann_diff": f"{cand_ann - menu_ann:.8f}",
                    "candidate_sharpe": f"{cand_sharpe:.8f}",
                    "menu_sharpe": f"{menu_sharpe:.8f}",
                    "sharpe_diff": f"{cand_sharpe - menu_sharpe:.8f}",
                    "candidate_mdd": f"{cand_mdd:.8f}",
                    "menu_mdd": f"{menu_mdd:.8f}",
                    "mdd_diff": f"{cand_mdd - menu_mdd:.8f}",
                    "ann_win": str(ann_win),
                    "sharpe_win": str(sharpe_win),
                    "mdd_win": str(mdd_win),
                }
            )

    aggregate_rows = []
    for (_candidate, _cost), row in sorted(aggregate.items(), key=lambda item: (item[0][0], item[0][1])):
        scenarios = int(row["scenarios"])
        ann_wins = int(row["ann_wins"])
        sharpe_wins = int(row["sharpe_wins"])
        mdd_wins = int(row["mdd_wins"])
        state = "production_candidate" if ann_wins >= 10 and sharpe_wins >= 10 and mdd_wins >= 12 else "not_promoted"
        if row["candidate"] == "case_lingxi_context_router" and mdd_wins >= 8:
            state = "risk_control_candidate"
        aggregate_rows.append(
            {
                **{key: str(value) for key, value in row.items()},
                "ann_win_rate": f"{ann_wins / scenarios:.4f}",
                "sharpe_win_rate": f"{sharpe_wins / scenarios:.4f}",
                "mdd_win_rate": f"{mdd_wins / scenarios:.4f}",
                "state": state,
            }
        )

    write_csv(out_dir / "case_lingxi_cost_sensitivity_detail.csv", scenario_rows)
    write_csv(out_dir / "case_lingxi_cost_sensitivity_summary.csv", aggregate_rows)
    print(f"detail={out_dir / 'case_lingxi_cost_sensitivity_detail.csv'} rows={len(scenario_rows)}")
    print(f"summary={out_dir / 'case_lingxi_cost_sensitivity_summary.csv'} rows={len(aggregate_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
