"""Materialize paper-prefix proxy runs from shared lightweight mechanisms.

The first-run paper baseline script maps several papers to the same runnable
NumPy mechanism. This helper writes one source-backed result CSV per paper
prefix so downstream comparison tables can track every target paper explicitly.
"""

from __future__ import annotations

import csv
from pathlib import Path

from run_paper_model_baseline import MODEL_MODES


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RUN_DIR = PROJECT_ROOT / "experiments" / "paper_runs"
BASE_MODELS = {"tra", "master", "doubleadapt", "tcts", "adarnn", "hist"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    materialized = 0
    for model, mode in sorted(MODEL_MODES.items()):
        if model in BASE_MODELS:
            continue
        for horizon in [1, 5]:
            source = RUN_DIR / f"{mode}_formal_csi300_2018_2024_h{horizon}.csv"
            target = RUN_DIR / f"{model}_formal_csi300_2018_2024_h{horizon}.csv"
            rows = read_csv(source)
            fields = list(rows[0])
            for row in rows:
                row["model"] = model
            write_csv(target, rows, fields)
            materialized += 1
            print(f"{model}: h{horizon} <- {source.name}")
    print(f"materialized={materialized}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
