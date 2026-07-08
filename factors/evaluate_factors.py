"""Standalone factor evaluator for the exported SEMAS alpha library.

Usage:
    python evaluate_factors.py --data path/to/data.parquet --output out.parquet

The input DataFrame must have a MultiIndex (symbol, date) or columns `symbol`
and `date`, plus all variables referenced by the factor expressions (open,
high, low, close, volume, return, eps, net_mf_amount, etc.).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from semas_parser import parse_expression


def _zscore(s: pd.Series) -> pd.Series:
    """Cross-sectional z-score."""
    return s.groupby(level="date").transform(lambda x: (x - x.mean()) / (x.std() + 1e-8))


def evaluate_library(data: pd.DataFrame, expressions: dict[str, str], combined: list[str]) -> pd.DataFrame:
    """Evaluate each expression and the combined signals.

    Args:
        data: panel DataFrame indexed by (symbol, date).
        expressions: mapping from factor name to expression string.
        combined: list of combined signal names to compute (e.g. combined_5d).
                  Each name must be computable as the mean of matching columns.

    Returns:
        DataFrame with original index plus one column per factor and combined signal.
    """
    # Ensure MultiIndex
    if not isinstance(data.index, pd.MultiIndex):
        if {"symbol", "date"}.issubset(data.columns):
            data = data.set_index(["symbol", "date"]).sort_index()
        else:
            raise ValueError("Data must have MultiIndex (symbol, date) or columns 'symbol' and 'date'")

    results = {}
    for name, expr in expressions.items():
        try:
            f = parse_expression(expr).eval(data)
            results[name] = _zscore(f)
        except Exception as exc:
            print(f"Skipping {name}: {exc}")

    df = pd.DataFrame(results, index=data.index)

    # Compute combined signals as the equal-weight mean of columns sharing the prefix.
    for signal in combined:
        prefix = signal + "_"
        cols = [c for c in df.columns if c.startswith(prefix)]
        if cols:
            df[signal] = df[cols].mean(axis=1)

    return df


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True, help="Panel data parquet/csv")
    parser.add_argument("--meta", type=Path, default=Path(__file__).with_name("expressions.json"))
    parser.add_argument("--output", type=Path, default=Path("factor_values.parquet"))
    args = parser.parse_args()

    with open(args.meta, "r", encoding="utf-8") as f:
        meta = json.load(f)

    if args.data.suffix == ".parquet":
        data = pd.read_parquet(args.data)
    else:
        data = pd.read_csv(args.data)

    out = evaluate_library(data, meta["expressions"], meta["combined_signals"])

    if args.output.suffix == ".parquet":
        out.to_parquet(args.output)
    else:
        out.reset_index().to_csv(args.output, index=False)
    print(f"Wrote {args.output} ({len(out.columns)} columns)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
