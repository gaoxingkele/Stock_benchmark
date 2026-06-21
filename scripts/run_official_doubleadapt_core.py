"""Run the official DoubleAdapt core on the local panel without Qlib handlers."""

from __future__ import annotations

import argparse
import copy
import csv
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import torch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
QLIB_FORK = PROJECT_ROOT / "external_repos" / "SJTU-DMTai__qlib"
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
sys.path.insert(0, str(QLIB_FORK))

from run_paper_model_baseline import FEATURES, load_panel  # noqa: E402
from qlib.contrib.meta.incremental.model import DoubleAdaptManager  # noqa: E402


class LocalDoubleAdaptManager(DoubleAdaptManager):
    """Compatibility wrapper for running upstream DoubleAdapt on plain tensors."""

    def run_epoch(self, phase, task_list, tqdm_show=False):
        pred_y_all = []
        self.phase = phase
        indices = np.arange(len(task_list))
        if phase == "train":
            np.random.shuffle(indices)
        else:
            if phase == "test":
                checkpoint = copy.deepcopy(self.state_dict())
            lr_model = self.lr_model
            self.override_online_lr_()

        for i in indices:
            meta_input = task_list[i].get_meta_input()
            if not isinstance(meta_input["X_train"], torch.Tensor):
                meta_input = {
                    k: torch.tensor(v, device=self.framework.device, dtype=torch.float32) if "idx" not in k else v
                    for k, v in meta_input.items()
                }
            if isinstance(meta_input.get("meta_end"), torch.Tensor):
                meta_input["meta_end"] = int(meta_input["meta_end"].detach().cpu().item())
            pred = self.run_task(meta_input, phase)
            if phase != "train":
                test_idx = meta_input["test_idx"]
                pred_y_all.append(pd.DataFrame({"pred": pd.Series(pred, index=test_idx), "label": pd.Series(meta_input["y_test"], index=test_idx)}))
        if phase != "train":
            pred_y_all = pd.concat(pred_y_all)
        if phase == "test":
            self.lr_model = lr_model
            self.load_state_dict(checkpoint)
            ic = pred_y_all.groupby("datetime").apply(lambda df: df["pred"].corr(df["label"], method="pearson")).mean()
            print(ic)
            return pred_y_all, ic
        return pred_y_all, None


@dataclass
class SimpleTask:
    meta_input: dict

    def get_meta_input(self) -> dict:
        return self.meta_input


class SimpleMetaDataset:
    def __init__(self, train_tasks: list[SimpleTask], valid_tasks: list[SimpleTask], test_tasks: list[SimpleTask]):
        self.train_tasks = train_tasks
        self.valid_tasks = valid_tasks
        self.test_tasks = test_tasks

    def prepare_tasks(self, phases):
        if isinstance(phases, list):
            return [self.prepare_tasks(phase) for phase in phases]
        if phases == "train":
            return self.train_tasks
        if phases in {"test", "online"}:
            return self.valid_tasks if self.valid_tasks else self.test_tasks
        raise ValueError(phases)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--panel", default=str(PROJECT_ROOT / "data" / "processed" / "cn_a_share" / "csi300_2018_2024" / "panel.csv"))
    parser.add_argument("--horizon", type=int, default=5)
    parser.add_argument("--lookback", type=int, default=20)
    parser.add_argument("--train-start", default="2018-01-02")
    parser.add_argument("--train-end", default="2021-12-31")
    parser.add_argument("--valid-start", default="2022-01-04")
    parser.add_argument("--valid-end", default="2022-12-30")
    parser.add_argument("--test-start", default="2023-01-03")
    parser.add_argument("--test-end", default="2024-12-31")
    parser.add_argument("--task-train-days", type=int, default=60)
    parser.add_argument("--task-test-days", type=int, default=20)
    parser.add_argument("--max-train-tasks", type=int, default=12)
    parser.add_argument("--max-valid-tasks", type=int, default=4)
    parser.add_argument("--lr", type=float, default=0.001)
    parser.add_argument("--lr-da", type=float, default=0.001)
    parser.add_argument("--lr-ma", type=float, default=0.001)
    parser.add_argument("--num-head", type=int, default=4)
    parser.add_argument("--tau", type=float, default=10.0)
    parser.add_argument("--patience", type=int, default=2)
    parser.add_argument("--out", default=str(PROJECT_ROOT / "experiments" / "official_scores" / "doubleadapt_official_core_h5.csv"))
    return parser.parse_args()


def build_examples(panel_path: Path, horizon: int, lookback: int) -> list[dict]:
    by_symbol, _ = load_panel(panel_path)
    rows: list[dict] = []
    for symbol, values in by_symbol.items():
        for idx in range(lookback - 1, len(values) - horizon):
            now = values[idx]
            future = values[idx + horizon]
            if now["close"] <= 0 or future["close"] <= 0:
                continue
            seq = np.asarray([row["features"] for row in values[idx - lookback + 1 : idx + 1]], dtype=np.float32)
            label = float(future["close"] / now["close"] - 1.0)
            rows.append({"date": now["date"], "symbol": symbol, "x": seq, "label": label})
    rows.sort(key=lambda row: (row["date"], row["symbol"]))
    return rows


def make_task(rows: list[dict], train_dates: list[str], test_dates: list[str]) -> SimpleTask | None:
    train = [row for row in rows if row["date"] in train_dates]
    test = [row for row in rows if row["date"] in test_dates]
    if not train or not test:
        return None
    train_idx = pd.MultiIndex.from_tuples([(pd.Timestamp(row["date"]), row["symbol"]) for row in train], names=["datetime", "instrument"])
    test_idx = pd.MultiIndex.from_tuples([(pd.Timestamp(row["date"]), row["symbol"]) for row in test], names=["datetime", "instrument"])
    meta_input = {
        "X_train": np.asarray([row["x"] for row in train], dtype=np.float32),
        "y_train": np.asarray([row["label"] for row in train], dtype=np.float32),
        "train_idx": train_idx,
        "X_test": np.asarray([row["x"] for row in test], dtype=np.float32),
        "y_test": np.asarray([row["label"] for row in test], dtype=np.float32),
        "test_idx": test_idx,
        "meta_end": len(test),
    }
    return SimpleTask(meta_input)


def rolling_tasks(rows: list[dict], start: str, end: str, train_days: int, test_days: int, max_tasks: int) -> list[SimpleTask]:
    dates = sorted({row["date"] for row in rows if start <= row["date"] <= end})
    tasks: list[SimpleTask] = []
    for test_start_idx in range(train_days, len(dates), test_days):
        train_dates = dates[test_start_idx - train_days : test_start_idx]
        test_dates = dates[test_start_idx : test_start_idx + test_days]
        task = make_task(rows, train_dates, test_dates)
        if task is not None:
            tasks.append(task)
        if max_tasks and len(tasks) >= max_tasks:
            break
    return tasks


def write_scores(path: Path, pred: pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "symbol", "score", "label"])
        writer.writeheader()
        for (date, symbol), row in pred.iterrows():
            writer.writerow(
                {
                    "date": pd.Timestamp(date).strftime("%Y-%m-%d"),
                    "symbol": symbol,
                    "score": f"{float(row['pred']):.10f}",
                    "label": f"{float(row['label']):.10f}",
                }
            )


def main() -> int:
    args = parse_args()
    rows = build_examples(Path(args.panel), args.horizon, args.lookback)
    train_rows = [row for row in rows if args.train_start <= row["date"] <= args.train_end]
    valid_rows = [row for row in rows if args.valid_start <= row["date"] <= args.valid_end]
    test_rows = [row for row in rows if args.test_start <= row["date"] <= args.test_end]
    train_tasks = rolling_tasks(train_rows, args.train_start, args.train_end, args.task_train_days, args.task_test_days, args.max_train_tasks)
    valid_tasks = rolling_tasks(valid_rows, args.valid_start, args.valid_end, args.task_train_days, args.task_test_days, args.max_valid_tasks)
    test_tasks = rolling_tasks(test_rows, args.test_start, args.test_end, args.task_train_days, args.task_test_days, 0)
    if not train_tasks or not valid_tasks or not test_tasks:
        raise RuntimeError(f"empty tasks: train={len(train_tasks)} valid={len(valid_tasks)} test={len(test_tasks)}")

    x_dim = args.lookback * len(FEATURES)
    task_config = {"model": {"class": "LinearModel"}}
    model = LocalDoubleAdaptManager(
        task_config=task_config,
        lr_model=args.lr,
        lr_da=args.lr_da,
        lr_ma=args.lr_ma,
        online_lr={"lr_model": args.lr, "lr_da": args.lr_da, "lr_ma": args.lr_ma},
        first_order=True,
        factor_num=len(FEATURES),
        x_dim=x_dim,
        alpha=158,
        num_head=args.num_head,
        temperature=args.tau,
        begin_valid_epoch=0,
        adapt_x=True,
        adapt_y=True,
        reg=0.5,
    )
    # Upstream LinearModel does not initialize this flag, while
    # ForecastModel.forward expects it for sequence tensors.
    model.framework.need_permute = False
    model.over_patience = args.patience
    meta_dataset = SimpleMetaDataset(train_tasks, valid_tasks, test_tasks)
    model.fit(meta_dataset)
    pred, ic = model.inference(SimpleMetaDataset([], [], test_tasks))
    write_scores(Path(args.out), pred)
    print(f"wrote {args.out} rows={len(pred)} ic={ic}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
