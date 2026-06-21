"""Summarize factor decay and turnover smoke outputs."""

from __future__ import annotations

import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT = PROJECT_ROOT / "experiments" / "summary" / "factor_stability_smoke.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def best_abs_rankic(rows: list[dict[str, str]], horizon: str) -> dict[str, str]:
    candidates = [row for row in rows if row["horizon"] == horizon and row["rankic"] != "nan"]
    return max(candidates, key=lambda row: abs(float(row["rankic"])))


def lowest_turnover(rows: list[dict[str, str]]) -> dict[str, str]:
    candidates = [row for row in rows if row["avg_turnover"] != "nan"]
    return min(candidates, key=lambda row: float(row["avg_turnover"]))


def add_decay_summary(out_rows: list[dict[str, str]], group: str, rows: list[dict[str, str]], horizon: str) -> None:
    best = best_abs_rankic(rows, horizon)
    out_rows.append(
        {
            "group": group,
            "metric": f"best_abs_rankic_h{horizon}",
            "factor": best["factor"],
            "value": best["rankic"],
            "n": best["n"],
            "dates": best["dates"],
            "extra": f"rankicir={best['rankicir']}",
        }
    )


def add_turnover_summary(out_rows: list[dict[str, str]], group: str, rows: list[dict[str, str]]) -> None:
    best = lowest_turnover(rows)
    out_rows.append(
        {
            "group": group,
            "metric": "lowest_top20_turnover",
            "factor": best["factor"],
            "value": best["avg_turnover"],
            "n": best["avg_top_size"],
            "dates": best["dates"],
            "extra": f"turnover_obs={best['turnover_obs']}",
        }
    )


def main() -> int:
    raw_decay = read_csv(PROJECT_ROOT / "factor_lab" / "validation" / "basic_factor_decay_csi300_by_date.csv")
    raw_turnover = read_csv(PROJECT_ROOT / "factor_lab" / "validation" / "basic_factor_turnover_csi300_by_date.csv")
    neutral_decay = read_csv(PROJECT_ROOT / "factor_lab" / "validation" / "basic_factor_decay_csi300_by_date_neutralized.csv")
    neutral_turnover = read_csv(PROJECT_ROOT / "factor_lab" / "validation" / "basic_factor_turnover_csi300_by_date_neutralized.csv")

    rows: list[dict[str, str]] = []
    for horizon in ["1", "5"]:
        add_decay_summary(rows, "raw", raw_decay, horizon)
        add_decay_summary(rows, "neutralized", neutral_decay, horizon)
    add_turnover_summary(rows, "raw", raw_turnover)
    add_turnover_summary(rows, "neutralized", neutral_turnover)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["group", "metric", "factor", "value", "n", "dates", "extra"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"summary={OUT} rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
