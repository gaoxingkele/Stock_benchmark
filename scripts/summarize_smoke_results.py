"""Create a unified summary table for verified benchmark experiments."""

from __future__ import annotations

import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT = PROJECT_ROOT / "experiments" / "summary" / "smoke_results.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def model_summary(name: str, path: Path, dataset: str, run_type: str = "model", selection: str = "SUMMARY") -> dict[str, str]:
    rows = read_csv(path)
    summary = next(row for row in rows if row.get("date") == "SUMMARY")
    return {
        "run_id": name,
        "run_type": run_type,
        "dataset": dataset,
        "selection": selection,
        "n": summary["n"],
        "dates": "",
        "ic": summary["ic"],
        "rankic": summary["rankic"],
        "icir": summary.get("icir", ""),
        "rankicir": summary.get("rankicir", ""),
        "source": str(path.relative_to(PROJECT_ROOT)),
    }


def best_factor_summary(name: str, path: Path) -> dict[str, str]:
    rows = read_csv(path)
    if not rows:
        raise RuntimeError(f"empty factor result: {path}")
    best = rows[0]
    return {
        "run_id": name,
        "run_type": "factor",
        "dataset": "csi300_by_date_smoke",
        "selection": best["factor"],
        "n": best["n"],
        "dates": best["dates"],
        "ic": best["ic"],
        "rankic": best["rankic"],
        "icir": best["icir"],
        "rankicir": best["rankicir"],
        "source": str(path.relative_to(PROJECT_ROOT)),
    }


def main() -> int:
    rows = [
        model_summary(
            "lightgbm_panel_h1",
            PROJECT_ROOT / "experiments" / "baselines" / "lightgbm_smoke_csi300_by_date.csv",
            "csi300_by_date_smoke",
        ),
        best_factor_summary(
            "basic_factor_best_raw_h1",
            PROJECT_ROOT / "factor_lab" / "validation" / "basic_factor_ic_csi300_by_date.csv",
        ),
        best_factor_summary(
            "basic_factor_best_ind_size_neutralized_h1",
            PROJECT_ROOT / "factor_lab" / "validation" / "basic_factor_ic_csi300_by_date_neutralized.csv",
        ),
        best_factor_summary(
            "alpha158_best_formal_h1",
            PROJECT_ROOT / "factor_lab" / "validation" / "alpha158_ic_csi300_2018_2024_h1.csv",
        )
        | {"dataset": "csi300_2018_2024"},
        best_factor_summary(
            "alpha360_best_formal_h1",
            PROJECT_ROOT / "factor_lab" / "validation" / "alpha360_ic_csi300_2018_2024_h1.csv",
        )
        | {"dataset": "csi300_2018_2024"},
        model_summary(
            "lightgbm_formal_h1",
            PROJECT_ROOT / "experiments" / "baselines" / "lightgbm_formal_csi300_2018_2024_h1.csv",
            "csi300_2018_2024",
        ),
        model_summary(
            "lightgbm_formal_h5",
            PROJECT_ROOT / "experiments" / "baselines" / "lightgbm_formal_csi300_2018_2024_h5.csv",
            "csi300_2018_2024",
        ),
        model_summary(
            "qlib_direct_lightgbm_formal_h1",
            PROJECT_ROOT / "experiments" / "baselines" / "qlib_direct_lightgbm_csi300_2018_2024_h1.csv",
            "csi300_2018_2024",
            selection="QlibDataHandler",
        ),
        model_summary(
            "tra_formal_h1",
            PROJECT_ROOT / "experiments" / "paper_runs" / "tra_formal_csi300_2018_2024_h1.csv",
            "csi300_2018_2024",
            run_type="paper_model",
            selection="lookback20",
        ),
        model_summary(
            "tra_formal_h5",
            PROJECT_ROOT / "experiments" / "paper_runs" / "tra_formal_csi300_2018_2024_h5.csv",
            "csi300_2018_2024",
            run_type="paper_model",
            selection="lookback20",
        ),
        model_summary(
            "master_formal_h1",
            PROJECT_ROOT / "experiments" / "paper_runs" / "master_formal_csi300_2018_2024_h1.csv",
            "csi300_2018_2024",
            run_type="paper_model",
            selection="lookback20",
        ),
        model_summary(
            "master_formal_h5",
            PROJECT_ROOT / "experiments" / "paper_runs" / "master_formal_csi300_2018_2024_h5.csv",
            "csi300_2018_2024",
            run_type="paper_model",
            selection="lookback20",
        ),
        model_summary(
            "doubleadapt_formal_h1",
            PROJECT_ROOT / "experiments" / "paper_runs" / "doubleadapt_formal_csi300_2018_2024_h1.csv",
            "csi300_2018_2024",
            run_type="paper_model",
            selection="lookback20",
        ),
        model_summary(
            "doubleadapt_formal_h5",
            PROJECT_ROOT / "experiments" / "paper_runs" / "doubleadapt_formal_csi300_2018_2024_h5.csv",
            "csi300_2018_2024",
            run_type="paper_model",
            selection="lookback20",
        ),
        model_summary(
            "tcts_formal_h1",
            PROJECT_ROOT / "experiments" / "paper_runs" / "tcts_formal_csi300_2018_2024_h1.csv",
            "csi300_2018_2024",
            run_type="paper_model",
            selection="lookback20",
        ),
        model_summary(
            "tcts_formal_h5",
            PROJECT_ROOT / "experiments" / "paper_runs" / "tcts_formal_csi300_2018_2024_h5.csv",
            "csi300_2018_2024",
            run_type="paper_model",
            selection="lookback20",
        ),
        model_summary(
            "adarnn_formal_h1",
            PROJECT_ROOT / "experiments" / "paper_runs" / "adarnn_formal_csi300_2018_2024_h1.csv",
            "csi300_2018_2024",
            run_type="paper_model",
            selection="lookback20",
        ),
        model_summary(
            "adarnn_formal_h5",
            PROJECT_ROOT / "experiments" / "paper_runs" / "adarnn_formal_csi300_2018_2024_h5.csv",
            "csi300_2018_2024",
            run_type="paper_model",
            selection="lookback20",
        ),
        model_summary(
            "hist_formal_h1",
            PROJECT_ROOT / "experiments" / "paper_runs" / "hist_formal_csi300_2018_2024_h1.csv",
            "csi300_2018_2024",
            run_type="paper_model",
            selection="lookback20",
        ),
        model_summary(
            "hist_formal_h5",
            PROJECT_ROOT / "experiments" / "paper_runs" / "hist_formal_csi300_2018_2024_h5.csv",
            "csi300_2018_2024",
            run_type="paper_model",
            selection="lookback20",
        ),
    ]
    known_sources = {row["source"] for row in rows}
    for path in sorted((PROJECT_ROOT / "experiments" / "paper_runs").glob("*_formal_csi300_2018_2024_h*.csv")):
        rel = str(path.relative_to(PROJECT_ROOT))
        if rel in known_sources:
            continue
        run_id = path.stem.replace("_csi300_2018_2024", "")
        rows.append(
            model_summary(
                run_id,
                path,
                "csi300_2018_2024",
                run_type="paper_model",
                selection="lookback20",
            )
        )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["run_id", "run_type", "dataset", "selection", "n", "dates", "ic", "rankic", "icir", "rankicir", "source"],
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"summary={OUT} rows={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
