"""Run a Qlib DatasetH + LightGBM baseline without Qlib's mlflow workflow layer."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

import lightgbm as lgb
import numpy as np
import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
QLIB_ROOT = PROJECT_ROOT / "external_repos" / "microsoft__qlib"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(QLIB_ROOT))

from src.evaluation.metrics import pearson_corr, safe_ir, safe_mean, spearman_corr  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", help="Qlib workflow YAML config.")
    parser.add_argument("--out", required=True, help="Output daily IC CSV.")
    parser.add_argument("--num-boost-round", type=int, default=200)
    parser.add_argument("--early-stopping-rounds", type=int, default=20)
    return parser.parse_args()


def normalize_frame(df):
    if hasattr(df.columns, "get_level_values") and "feature" in df.columns.get_level_values(0):
        x = df["feature"]
        y = df["label"]
    else:
        raise RuntimeError("expected Qlib prepared frame with feature/label column groups")
    y_values = np.squeeze(y.values)
    return x, y_values


def index_dates(index) -> list[str]:
    if hasattr(index, "get_level_values") and "datetime" in index.names:
        values = index.get_level_values("datetime")
    else:
        values = index.get_level_values(0)
    return [str(value.date() if hasattr(value, "date") else value) for value in values]


def main() -> int:
    args = parse_args()
    with Path(args.config).open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    from qlib.data.dataset import DatasetH
    from qlib.data.dataset.handler import DataHandlerLP
    from qlib.config import C
    from qlib.data.cache import H
    from qlib.data.data import register_all_wrappers
    from qlib.data.ops import register_all_ops
    from qlib.utils import init_instance_by_config

    qlib_init = config["qlib_init"]
    H.clear()
    C.set("client", provider_uri=qlib_init["provider_uri"], region=qlib_init.get("region", "cn"))
    C["kernels"] = 1
    register_all_ops(C)
    register_all_wrappers(C)
    C._registered = True

    dataset_conf = config["task"]["dataset"]
    handler_conf = dataset_conf["kwargs"]["handler"]
    handler_conf = {
        **handler_conf,
        "kwargs": {
            key: value
            for key, value in handler_conf["kwargs"].items()
            if key not in {"fit_start_time", "fit_end_time"}
        },
    }
    handler = init_instance_by_config(handler_conf)
    dataset = DatasetH(handler=handler, segments=dataset_conf["kwargs"]["segments"])

    train_df = dataset.prepare("train", col_set=["feature", "label"], data_key=DataHandlerLP.DK_L)
    valid_df = dataset.prepare("valid", col_set=["feature", "label"], data_key=DataHandlerLP.DK_L)
    test_df = dataset.prepare("test", col_set=["feature", "label"], data_key=DataHandlerLP.DK_I)
    if train_df.empty or valid_df.empty or test_df.empty:
        raise RuntimeError("empty Qlib train/valid/test data")

    train_x, train_y = normalize_frame(train_df)
    valid_x, valid_y = normalize_frame(valid_df)
    test_x, test_y = normalize_frame(test_df)

    model_kwargs = dict(config["task"]["model"]["kwargs"])
    model_kwargs.setdefault("objective", model_kwargs.pop("loss", "mse"))
    params = {"verbosity": -1, **model_kwargs}
    train_set = lgb.Dataset(train_x.values, label=train_y, feature_name=list(train_x.columns))
    valid_set = lgb.Dataset(valid_x.values, label=valid_y, feature_name=list(valid_x.columns), reference=train_set)
    model = lgb.train(
        params,
        train_set,
        num_boost_round=args.num_boost_round,
        valid_sets=[train_set, valid_set],
        valid_names=["train", "valid"],
        callbacks=[lgb.early_stopping(args.early_stopping_rounds), lgb.log_evaluation(period=20)],
    )
    preds = model.predict(test_x.values)

    by_date: dict[str, list[tuple[float, float]]] = defaultdict(list)
    for date, pred, label in zip(index_dates(test_df.index), preds, test_y):
        by_date[date].append((float(pred), float(label)))

    result_rows: list[dict[str, str]] = []
    ic_values: list[float] = []
    rankic_values: list[float] = []
    for date in sorted(by_date):
        pairs = by_date[date]
        scores = [score for score, _ in pairs]
        labels = [label for _, label in pairs]
        ic = pearson_corr(scores, labels)
        rankic = spearman_corr(scores, labels)
        ic_values.append(ic)
        rankic_values.append(rankic)
        result_rows.append({"date": date, "n": str(len(pairs)), "ic": f"{ic:.8f}", "rankic": f"{rankic:.8f}"})

    summary = {
        "date": "SUMMARY",
        "n": str(len(test_df)),
        "ic": f"{safe_mean(ic_values):.8f}",
        "rankic": f"{safe_mean(rankic_values):.8f}",
        "icir": f"{safe_ir(ic_values):.8f}",
        "rankicir": f"{safe_ir(rankic_values):.8f}",
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "n", "ic", "rankic", "icir", "rankicir"])
        writer.writeheader()
        for row in result_rows:
            writer.writerow({**{"icir": "", "rankicir": ""}, **row})
        writer.writerow(summary)
    print(f"train_rows={len(train_df)} valid_rows={len(valid_df)} test_rows={len(test_df)} out={out_path}")
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
