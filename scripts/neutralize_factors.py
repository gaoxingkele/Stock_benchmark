"""Industry demean and size-neutralize factor values by date."""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ID_FIELDS = {"date", "symbol", "ts_code"}
SIZE_FIELD = "size_log_total_mv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--factors", default=str(PROJECT_ROOT / "data" / "features" / "basic_factors" / "csi300_by_date_smoke.csv"))
    parser.add_argument("--stock-basic", default=str(PROJECT_ROOT / "data" / "raw" / "tushare" / "csi300_by_date_smoke" / "stock_basic.csv"))
    parser.add_argument("--out", default=str(PROJECT_ROOT / "data" / "features" / "basic_factors" / "csi300_by_date_smoke_neutralized.csv"))
    return parser.parse_args()


def to_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def read_industry(path: Path) -> dict[str, str]:
    mapping: dict[str, str] = {}
    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            mapping[row["ts_code"]] = row.get("industry", "") or "UNKNOWN"
    return mapping


def mean(values: list[float]) -> float:
    clean = [v for v in values if not math.isnan(v)]
    if not clean:
        return float("nan")
    return sum(clean) / len(clean)


def residualize_size(values: list[float], sizes: list[float]) -> list[float]:
    pairs = [(v, s) for v, s in zip(values, sizes) if not math.isnan(v) and not math.isnan(s)]
    if len(pairs) < 3:
        return values
    mean_v = sum(v for v, _ in pairs) / len(pairs)
    mean_s = sum(s for _, s in pairs) / len(pairs)
    var_s = sum((s - mean_s) ** 2 for _, s in pairs)
    if var_s == 0:
        return values
    beta = sum((s - mean_s) * (v - mean_v) for v, s in pairs) / var_s
    alpha = mean_v - beta * mean_s
    return [float("nan") if math.isnan(v) or math.isnan(s) else v - (alpha + beta * s) for v, s in zip(values, sizes)]


def main() -> int:
    args = parse_args()
    industry = read_industry(Path(args.stock_basic))
    by_date: dict[str, list[dict[str, str]]] = defaultdict(list)
    with Path(args.factors).open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames or []
        factor_names = [name for name in fieldnames if name not in ID_FIELDS]
        for row in reader:
            row["industry"] = industry.get(row["ts_code"], "UNKNOWN")
            by_date[row["date"]].append(row)

    out_rows: list[dict[str, str]] = []
    out_factor_names = [f"{name}_ind_size_neu" for name in factor_names if name != SIZE_FIELD]
    for date in sorted(by_date):
        rows = by_date[date]
        sizes = [to_float(row.get(SIZE_FIELD, "")) for row in rows]
        neutralized_by_factor: dict[str, list[float]] = {}

        for factor in factor_names:
            if factor == SIZE_FIELD:
                continue
            raw_values = [to_float(row.get(factor, "")) for row in rows]
            industry_values: dict[str, list[float]] = defaultdict(list)
            for row, value in zip(rows, raw_values):
                industry_values[row["industry"]].append(value)
            industry_means = {key: mean(values) for key, values in industry_values.items()}
            demeaned = [
                float("nan") if math.isnan(value) else value - industry_means.get(row["industry"], 0.0)
                for row, value in zip(rows, raw_values)
            ]
            neutralized_by_factor[factor] = residualize_size(demeaned, sizes)

        for i, row in enumerate(rows):
            out = {"date": date, "symbol": row["symbol"], "ts_code": row["ts_code"]}
            for factor in factor_names:
                if factor == SIZE_FIELD:
                    continue
                value = neutralized_by_factor[factor][i]
                out[f"{factor}_ind_size_neu"] = "" if math.isnan(value) else f"{value:.10f}"
            out_rows.append(out)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "symbol", "ts_code"] + out_factor_names)
        writer.writeheader()
        writer.writerows(out_rows)

    print(f"neutralized={out_path} rows={len(out_rows)} factor_count={len(out_factor_names)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

