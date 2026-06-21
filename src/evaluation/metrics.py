"""Small evaluation metrics used by smoke tests."""

from __future__ import annotations

import math
from statistics import mean, pstdev
from typing import Iterable


def pearson_corr(left: Iterable[float], right: Iterable[float]) -> float:
    """Compute Pearson correlation without external dependencies."""

    x = list(left)
    y = list(right)
    if len(x) != len(y) or len(x) < 2:
        return float("nan")
    mx = mean(x)
    my = mean(y)
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    denom = math.sqrt(sum(v * v for v in dx) * sum(v * v for v in dy))
    if denom == 0:
        return float("nan")
    return sum(a * b for a, b in zip(dx, dy)) / denom


def rankdata(values: Iterable[float]) -> list[float]:
    """Return average ranks for a sequence of values."""

    pairs = sorted((value, i) for i, value in enumerate(values))
    ranks = [0.0] * len(pairs)
    start = 0
    while start < len(pairs):
        end = start + 1
        while end < len(pairs) and pairs[end][0] == pairs[start][0]:
            end += 1
        avg_rank = (start + 1 + end) / 2.0
        for _, original_index in pairs[start:end]:
            ranks[original_index] = avg_rank
        start = end
    return ranks


def spearman_corr(left: Iterable[float], right: Iterable[float]) -> float:
    """Compute Spearman rank correlation."""

    x = list(left)
    y = list(right)
    if len(x) != len(y) or len(x) < 2:
        return float("nan")
    return pearson_corr(rankdata(x), rankdata(y))


def safe_mean(values: Iterable[float]) -> float:
    clean = [v for v in values if not math.isnan(v)]
    return mean(clean) if clean else float("nan")


def safe_ir(values: Iterable[float]) -> float:
    clean = [v for v in values if not math.isnan(v)]
    if len(clean) < 2:
        return float("nan")
    std = pstdev(clean)
    if std == 0:
        return float("nan")
    return mean(clean) / std

