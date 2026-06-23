"""Run a FunctionEvolve-style proxy factor-mining experiment.

This is a public proxy for the WQ Alpha Evolution ARA. It does not use
WorldQuant BRAIN. Candidate factors are represented as small expression trees,
selected on an in-sample window, and evaluated on a frozen out-of-sample window.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, pstdev


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.evaluation.metrics import pearson_corr, safe_ir, safe_mean, spearman_corr  # noqa: E402


BASE_FIELDS = [
    "close",
    "open",
    "high",
    "low",
    "volume",
    "amount",
    "turnover_rate",
    "volume_ratio",
    "pe",
    "pb",
    "total_mv",
    "circ_mv",
]


@dataclass(frozen=True)
class Expr:
    op: str
    args: tuple["Expr", ...] = ()
    value: str | int | None = None

    def name(self) -> str:
        if self.op == "field":
            return str(self.value)
        if self.op == "const":
            return str(self.value)
        args = ",".join(arg.name() for arg in self.args)
        if self.value is None:
            return f"{self.op}({args})"
        return f"{self.op}{self.value}({args})"

    def depth(self) -> int:
        if not self.args:
            return 1
        return 1 + max(arg.depth() for arg in self.args)

    def node_count(self) -> int:
        return 1 + sum(arg.node_count() for arg in self.args)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--panel", default=str(PROJECT_ROOT / "data/processed/cn_a_share/csi300_2018_2024/panel.csv"))
    parser.add_argument("--market", default="cn_a_share")
    parser.add_argument("--horizon", type=int, default=5)
    parser.add_argument("--train-start", default="2018-01-02")
    parser.add_argument("--train-end", default="2021-12-31")
    parser.add_argument("--test-start", default="2022-01-04")
    parser.add_argument("--test-end", default="2024-12-31")
    parser.add_argument("--cost-bps", type=float, default=10.0)
    parser.add_argument("--topk", type=int, default=30)
    parser.add_argument("--max-candidates", type=int, default=72)
    parser.add_argument("--promotion-top", type=int, default=12)
    parser.add_argument("--max-symbols", type=int, default=80)
    parser.add_argument("--out-dir", default=str(PROJECT_ROOT / "experiments/wq_functionevolve_proxy"))
    return parser.parse_args()


def to_float(value: str | float | int | None) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float("nan")


def safe_div(left: float, right: float) -> float:
    if math.isnan(left) or math.isnan(right) or right == 0:
        return float("nan")
    return left / right


def winsor(value: float, limit: float = 10.0) -> float:
    if math.isnan(value):
        return value
    return max(-limit, min(limit, value))


def load_panel(path: Path) -> dict[str, list[dict[str, float | str]]]:
    rows_by_symbol: dict[str, list[dict[str, float | str]]] = defaultdict(list)
    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for raw in reader:
            row: dict[str, float | str] = {"date": raw["date"], "symbol": raw["symbol"]}
            for field in BASE_FIELDS:
                row[field] = to_float(raw.get(field))
            rows_by_symbol[raw["symbol"]].append(row)
    for symbol in rows_by_symbol:
        rows_by_symbol[symbol].sort(key=lambda row: str(row["date"]))
    return rows_by_symbol


def limit_symbols(rows_by_symbol: dict[str, list[dict[str, float | str]]], max_symbols: int) -> dict[str, list[dict[str, float | str]]]:
    if max_symbols <= 0 or len(rows_by_symbol) <= max_symbols:
        return rows_by_symbol
    selected = sorted(rows_by_symbol)[:max_symbols]
    return {symbol: rows_by_symbol[symbol] for symbol in selected}


def rolling(values: list[float], index: int, window: int) -> list[float]:
    return values[max(0, index - window + 1) : index + 1]


def eval_expr(expr: Expr, series: dict[str, list[float]], index: int, cache: dict[tuple[str, int], float]) -> float:
    key = (expr.name(), index)
    if key in cache:
        return cache[key]
    if expr.op == "field":
        result = series[str(expr.value)][index]
    elif expr.op == "ret":
        window = int(expr.value or 1)
        cur = eval_expr(expr.args[0], series, index, cache)
        prev = eval_expr(expr.args[0], series, index - window, cache) if index >= window else float("nan")
        result = safe_div(cur, prev) - 1.0
    elif expr.op == "ts_mean":
        values = [eval_expr(expr.args[0], series, i, cache) for i in range(max(0, index - int(expr.value) + 1), index + 1)]
        clean = [v for v in values if not math.isnan(v)]
        result = mean(clean) if clean else float("nan")
    elif expr.op == "ts_std":
        values = [eval_expr(expr.args[0], series, i, cache) for i in range(max(0, index - int(expr.value) + 1), index + 1)]
        clean = [v for v in values if not math.isnan(v)]
        result = pstdev(clean) if len(clean) >= 2 else float("nan")
    elif expr.op == "zscore":
        base = eval_expr(expr.args[0], series, index, cache)
        values = [eval_expr(expr.args[0], series, i, cache) for i in range(max(0, index - int(expr.value) + 1), index + 1)]
        clean = [v for v in values if not math.isnan(v)]
        if len(clean) < 2:
            result = float("nan")
        else:
            std = pstdev(clean)
            result = safe_div(base - mean(clean), std)
    elif expr.op == "sub":
        result = eval_expr(expr.args[0], series, index, cache) - eval_expr(expr.args[1], series, index, cache)
    elif expr.op == "add":
        result = eval_expr(expr.args[0], series, index, cache) + eval_expr(expr.args[1], series, index, cache)
    elif expr.op == "mul":
        result = winsor(eval_expr(expr.args[0], series, index, cache)) * winsor(eval_expr(expr.args[1], series, index, cache))
    elif expr.op == "div":
        result = safe_div(eval_expr(expr.args[0], series, index, cache), eval_expr(expr.args[1], series, index, cache))
    elif expr.op == "neg":
        result = -eval_expr(expr.args[0], series, index, cache)
    elif expr.op == "log":
        value = eval_expr(expr.args[0], series, index, cache)
        result = math.log(value) if value > 0 else float("nan")
    else:
        raise ValueError(f"unknown op: {expr.op}")
    cache[key] = result
    return result


def build_candidates(max_candidates: int) -> list[Expr]:
    f = {name: Expr("field", value=name) for name in BASE_FIELDS}
    seeds = [
        Expr("ret", (f["close"],), 1),
        Expr("ret", (f["close"],), 5),
        Expr("ret", (f["volume"],), 5),
        Expr("ret", (f["amount"],), 5),
        Expr("div", (f["close"], f["open"])),
        Expr("div", (f["high"], f["low"])),
        Expr("div", (f["close"], f["high"])),
        Expr("div", (f["close"], f["low"])),
        Expr("log", (f["total_mv"],)),
        Expr("log", (f["circ_mv"],)),
        f["turnover_rate"],
        f["volume_ratio"],
        f["pe"],
        f["pb"],
    ]
    candidates: list[Expr] = []
    seen: set[str] = set()

    def add(expr: Expr) -> None:
        name = expr.name()
        if name not in seen and len(candidates) < max_candidates:
            seen.add(name)
            candidates.append(expr)

    for seed in seeds:
        add(seed)
        for window in [3, 5, 10, 20]:
            add(Expr("ts_mean", (seed,), window))
            add(Expr("zscore", (seed,), window))
    parent_pool = list(candidates)
    for left in parent_pool[:18]:
        for right in parent_pool[18:36]:
            add(Expr("sub", (left, right)))
            add(Expr("add", (left, right)))
            if len(candidates) >= max_candidates:
                return candidates
    return candidates


def materialize(
    rows_by_symbol: dict[str, list[dict[str, float | str]]],
    expressions: list[Expr],
    horizon: int,
) -> tuple[dict[str, dict[str, dict[str, float]]], dict[tuple[str, str], float]]:
    by_date: dict[str, dict[str, dict[str, float]]] = defaultdict(dict)
    labels: dict[tuple[str, str], float] = {}
    for symbol, rows in rows_by_symbol.items():
        series = {field: [to_float(row[field]) for row in rows] for field in BASE_FIELDS}
        cache: dict[tuple[str, int], float] = {}
        for i, row in enumerate(rows):
            date = str(row["date"])
            close = to_float(row["close"])
            if i + horizon < len(rows) and close > 0:
                future_close = to_float(rows[i + horizon]["close"])
                labels[(date, symbol)] = future_close / close - 1.0
            values = {}
            for expr in expressions:
                values[expr.name()] = eval_expr(expr, series, i, cache)
            by_date[date][symbol] = values
    return by_date, labels


def date_range_values(
    factor_values: dict[str, dict[str, dict[str, float]]],
    labels: dict[tuple[str, str], float],
    factor: str,
    start: str,
    end: str,
) -> tuple[list[float], list[float], list[float], list[float]]:
    ic_values: list[float] = []
    rankic_values: list[float] = []
    returns: list[float] = []
    turnovers: list[float] = []
    prev_selection: set[str] = set()
    for date in sorted(factor_values):
        if date < start or date > end:
            continue
        pairs = []
        for symbol, values in factor_values[date].items():
            label = labels.get((date, symbol), float("nan"))
            value = values.get(factor, float("nan"))
            if not math.isnan(value) and not math.isnan(label):
                pairs.append((symbol, value, label))
        if len(pairs) < 10:
            continue
        scores = [score for _symbol, score, _label in pairs]
        day_labels = [label for _symbol, _score, label in pairs]
        ic_values.append(pearson_corr(scores, day_labels))
        rankic_values.append(spearman_corr(scores, day_labels))
        ordered = sorted(pairs, key=lambda item: item[1], reverse=True)
        k = min(30, max(1, len(ordered) // 10))
        longs = ordered[:k]
        shorts = ordered[-k:]
        day_return = mean(label for _symbol, _score, label in longs) - mean(label for _symbol, _score, label in shorts)
        selection = {symbol for symbol, _score, _label in longs}
        turnover = 1.0 if not prev_selection else 1.0 - len(selection & prev_selection) / len(selection | prev_selection)
        returns.append(day_return)
        turnovers.append(turnover)
        prev_selection = selection
    return ic_values, rankic_values, returns, turnovers


def max_abs_corr(candidate: str, promoted: list[str], factor_values: dict[str, dict[str, dict[str, float]]], start: str, end: str) -> float:
    if not promoted:
        return 0.0
    candidate_series: list[float] = []
    promoted_series: dict[str, list[float]] = {name: [] for name in promoted}
    for date in sorted(factor_values):
        if date < start or date > end:
            continue
        for _symbol, values in factor_values[date].items():
            value = values.get(candidate, float("nan"))
            if math.isnan(value):
                continue
            candidate_series.append(value)
            for name in promoted:
                promoted_series[name].append(values.get(name, float("nan")))
    corrs = []
    for name, series in promoted_series.items():
        pairs = [(x, y) for x, y in zip(candidate_series, series) if not math.isnan(x) and not math.isnan(y)]
        if len(pairs) >= 10:
            corrs.append(abs(pearson_corr([x for x, _y in pairs], [y for _x, y in pairs])))
    clean = [v for v in corrs if not math.isnan(v)]
    return max(clean) if clean else 0.0


def summarize_factor(
    factor: str,
    factor_values: dict[str, dict[str, dict[str, float]]],
    labels: dict[tuple[str, str], float],
    train_start: str,
    train_end: str,
    test_start: str,
    test_end: str,
    cost_bps: float,
    promoted: list[str],
) -> dict[str, float | str]:
    train_ic, train_rankic, train_returns, _train_turnovers = date_range_values(factor_values, labels, factor, train_start, train_end)
    test_ic, test_rankic, test_returns, test_turnovers = date_range_values(factor_values, labels, factor, test_start, test_end)
    avg_turnover = safe_mean(test_turnovers)
    net_returns = [ret - (cost_bps / 10000.0) * avg_turnover for ret in test_returns]
    max_corr = max_abs_corr(factor, promoted, factor_values, train_start, train_end)
    return {
        "factor": factor,
        "train_rank_ic": safe_mean(train_rankic),
        "train_rank_icir": safe_ir(train_rankic),
        "mean_ic": safe_mean(test_ic),
        "icir": safe_ir(test_ic),
        "rank_ic": safe_mean(test_rankic),
        "rank_icir": safe_ir(test_rankic),
        "turnover": avg_turnover,
        "long_short_return": safe_mean(test_returns),
        "cost_adjusted_return": safe_mean(net_returns),
        "max_drawdown": max_drawdown(net_returns),
        "max_prior_factor_corr": max_corr,
        "test_days": len(test_returns),
    }


def max_drawdown(returns: list[float]) -> float:
    equity = 1.0
    peak = 1.0
    drawdown = 0.0
    for ret in returns:
        if math.isnan(ret):
            continue
        equity *= 1.0 + ret
        peak = max(peak, equity)
        drawdown = min(drawdown, equity / peak - 1.0)
    return drawdown


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = PROJECT_ROOT / out_dir

    rows_by_symbol = limit_symbols(load_panel(Path(args.panel)), args.max_symbols)
    expressions = build_candidates(args.max_candidates)
    factor_values, labels = materialize(rows_by_symbol, expressions, args.horizon)
    promoted: list[str] = []
    detail_rows: list[dict[str, str]] = []
    scored = []
    for expr in expressions:
        factor = expr.name()
        row = summarize_factor(
            factor,
            factor_values,
            labels,
            args.train_start,
            args.train_end,
            args.test_start,
            args.test_end,
            args.cost_bps,
            promoted,
        )
        score = abs(float(row["train_rank_ic"])) * max(0.0, float(row["train_rank_icir"]) if not math.isnan(float(row["train_rank_icir"])) else 0.0)
        scored.append((score, expr, row))
    scored.sort(key=lambda item: item[0], reverse=True)

    valid_count = 0
    promoted_count = 0
    for rank, (_score, expr, row) in enumerate(scored, start=1):
        valid = int(row["test_days"]) > 50 and not math.isnan(float(row["rank_ic"]))
        status = "rejected"
        if valid:
            valid_count += 1
            if (
                promoted_count < args.promotion_top
                and float(row["rank_ic"]) >= 0.01
                and float(row["cost_adjusted_return"]) > 0.0
                and abs(float(row["max_prior_factor_corr"])) <= 0.95
                and float(row["turnover"]) <= 0.95
            ):
                status = "promoted"
                promoted.append(str(row["factor"]))
                promoted_count += 1
            else:
                status = "research_only"
        detail_rows.append(
            {
                "rank": str(rank),
                "factor": str(row["factor"]),
                "depth": str(expr.depth()),
                "node_count": str(expr.node_count()),
                "train_rank_ic": f"{float(row['train_rank_ic']):.8f}",
                "train_rank_icir": f"{float(row['train_rank_icir']):.8f}",
                "mean_ic": f"{float(row['mean_ic']):.8f}",
                "icir": f"{float(row['icir']):.8f}",
                "rank_ic": f"{float(row['rank_ic']):.8f}",
                "rank_icir": f"{float(row['rank_icir']):.8f}",
                "turnover": f"{float(row['turnover']):.8f}",
                "cost_bps": f"{args.cost_bps:.2f}",
                "long_short_return": f"{float(row['long_short_return']):.8f}",
                "cost_adjusted_return": f"{float(row['cost_adjusted_return']):.8f}",
                "max_drawdown": f"{float(row['max_drawdown']):.8f}",
                "max_prior_factor_corr": f"{float(row['max_prior_factor_corr']):.8f}",
                "promotion_status": status,
                "test_days": str(row["test_days"]),
            }
        )

    summary_row = {
        "run_id": "functionevolve_proxy_cn_a_share_v1",
        "market": args.market,
        "train_period": f"{args.train_start}:{args.train_end}",
        "test_period": f"{args.test_start}:{args.test_end}",
        "generator": "functionevolve_style_ast_v1",
        "candidate_count": str(len(expressions)),
        "valid_factor_count": str(valid_count),
        "promoted_factor_count": str(promoted_count),
        "mean_ic": f"{safe_mean([float(row['mean_ic']) for row in detail_rows if row['promotion_status'] == 'promoted']):.8f}",
        "icir": f"{safe_mean([float(row['icir']) for row in detail_rows if row['promotion_status'] == 'promoted']):.8f}",
        "rank_ic": f"{safe_mean([float(row['rank_ic']) for row in detail_rows if row['promotion_status'] == 'promoted']):.8f}",
        "rank_icir": f"{safe_mean([float(row['rank_icir']) for row in detail_rows if row['promotion_status'] == 'promoted']):.8f}",
        "turnover": f"{safe_mean([float(row['turnover']) for row in detail_rows if row['promotion_status'] == 'promoted']):.8f}",
        "cost_bps": f"{args.cost_bps:.2f}",
        "long_short_return": f"{safe_mean([float(row['long_short_return']) for row in detail_rows if row['promotion_status'] == 'promoted']):.8f}",
        "max_drawdown": f"{safe_mean([float(row['max_drawdown']) for row in detail_rows if row['promotion_status'] == 'promoted']):.8f}",
        "max_prior_factor_corr": f"{safe_mean([float(row['max_prior_factor_corr']) for row in detail_rows if row['promotion_status'] == 'promoted']):.8f}",
        "promotion_status": "research_only" if promoted_count else "rejected",
        "notes": "Public AST proxy run; no WorldQuant private records used.",
    }

    detail_fields = [
        "rank",
        "factor",
        "depth",
        "node_count",
        "train_rank_ic",
        "train_rank_icir",
        "mean_ic",
        "icir",
        "rank_ic",
        "rank_icir",
        "turnover",
        "cost_bps",
        "long_short_return",
        "cost_adjusted_return",
        "max_drawdown",
        "max_prior_factor_corr",
        "promotion_status",
        "test_days",
    ]
    summary_fields = [
        "run_id",
        "market",
        "train_period",
        "test_period",
        "generator",
        "candidate_count",
        "valid_factor_count",
        "promoted_factor_count",
        "mean_ic",
        "icir",
        "rank_ic",
        "rank_icir",
        "turnover",
        "cost_bps",
        "long_short_return",
        "max_drawdown",
        "max_prior_factor_corr",
        "promotion_status",
        "notes",
    ]
    write_csv(out_dir / "functionevolve_proxy_detail.csv", detail_rows, detail_fields)
    write_csv(out_dir / "functionevolve_proxy_summary.csv", [summary_row], summary_fields)
    print(f"summary={out_dir / 'functionevolve_proxy_summary.csv'} rows=1")
    print(f"detail={out_dir / 'functionevolve_proxy_detail.csv'} rows={len(detail_rows)} promoted={promoted_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
