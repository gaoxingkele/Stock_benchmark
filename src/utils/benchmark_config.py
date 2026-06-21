"""Benchmark configuration loading and validation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = {
    "id",
    "task",
    "market",
    "universe",
    "data",
    "features",
    "label",
    "split",
    "model",
    "evaluation",
    "outputs",
}


@dataclass(frozen=True)
class BenchmarkConfig:
    """A validated benchmark config backed by the original JSON payload."""

    path: Path
    payload: dict[str, Any]

    @property
    def experiment_id(self) -> str:
        return str(self.payload["id"])

    @property
    def panel_path(self) -> Path:
        return Path(self.payload["data"]["panel"])

    @property
    def horizon(self) -> int:
        return int(self.payload["label"]["horizon"])

    @property
    def train_end(self) -> str:
        return str(self.payload["split"]["train"][1])

    @property
    def result_path(self) -> Path:
        return Path(self.payload["outputs"]["predictions_or_scores"])


def _require_mapping(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be an object")
    return value


def _require_list(value: Any, name: str) -> list[Any]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{name} must be a non-empty list")
    return value


def _require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} must be a non-empty string")
    return value


def _require_date_range(value: Any, name: str) -> list[str]:
    items = _require_list(value, name)
    if len(items) != 2:
        raise ValueError(f"{name} must contain [start_date, end_date]")
    for i, item in enumerate(items):
        _require_string(item, f"{name}[{i}]")
    return [str(items[0]), str(items[1])]


def validate_payload(payload: dict[str, Any]) -> None:
    missing = sorted(REQUIRED_TOP_LEVEL - set(payload))
    if missing:
        raise ValueError(f"missing required fields: {', '.join(missing)}")

    _require_string(payload["id"], "id")
    task = _require_string(payload["task"], "task")
    if task not in {"trend_prediction", "alpha_factor"}:
        raise ValueError("task must be trend_prediction or alpha_factor")

    market = _require_string(payload["market"], "market")
    if market != "cn_a_share":
        raise ValueError("only cn_a_share is supported in the current benchmark")

    universe = _require_mapping(payload["universe"], "universe")
    _require_string(universe.get("name"), "universe.name")
    _require_string(universe.get("index_code"), "universe.index_code")

    data = _require_mapping(payload["data"], "data")
    _require_string(data.get("provider"), "data.provider")
    _require_string(data.get("frequency"), "data.frequency")
    _require_string(data.get("panel"), "data.panel")

    features = _require_mapping(payload["features"], "features")
    _require_string(features.get("kind"), "features.kind")
    _require_list(features.get("columns"), "features.columns")

    label = _require_mapping(payload["label"], "label")
    _require_string(label.get("kind"), "label.kind")
    horizon = label.get("horizon")
    if not isinstance(horizon, int) or horizon <= 0:
        raise ValueError("label.horizon must be a positive integer")

    split = _require_mapping(payload["split"], "split")
    _require_date_range(split.get("train"), "split.train")
    if "valid" in split:
        _require_date_range(split.get("valid"), "split.valid")
    _require_date_range(split.get("test"), "split.test")

    model = _require_mapping(payload["model"], "model")
    _require_string(model.get("name"), "model.name")
    _require_string(model.get("family"), "model.family")

    evaluation = _require_mapping(payload["evaluation"], "evaluation")
    metrics = _require_list(evaluation.get("metrics"), "evaluation.metrics")
    for i, metric in enumerate(metrics):
        _require_string(metric, f"evaluation.metrics[{i}]")

    outputs = _require_mapping(payload["outputs"], "outputs")
    _require_string(outputs.get("predictions_or_scores"), "outputs.predictions_or_scores")
    _require_string(outputs.get("summary"), "outputs.summary")


def load_benchmark_config(path: str | Path) -> BenchmarkConfig:
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as file:
        payload = json.load(file)
    if not isinstance(payload, dict):
        raise ValueError("benchmark config root must be an object")
    validate_payload(payload)
    return BenchmarkConfig(path=config_path, payload=payload)
