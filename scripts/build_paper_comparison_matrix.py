"""Build the 24-paper progress and China A-share comparison matrix."""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGETS = ROOT / "papers" / "metadata" / "paper_target_24.csv"
REGISTRY = ROOT / "papers" / "metadata" / "paper_registry.csv"
PDF_STATUS = ROOT / "papers" / "metadata" / "pdf_download_status.csv"
RESULTS = ROOT / "experiments" / "summary" / "smoke_results.csv"
ORIGINAL_RESULTS = ROOT / "papers" / "metadata" / "original_experiment_results.csv"
OUT_CSV = ROOT / "experiments" / "summary" / "paper_24_comparison_matrix.csv"
OUT_QUEUE = ROOT / "papers" / "metadata" / "paper_24_acquisition_queue.csv"
OUT_MD = ROOT / "docs" / "reports" / "paper_24_comparison_matrix.md"


MODEL_PREFIX = {
    "2021_tra_lin": "tra",
    "2021_tcts_wu": "tcts",
    "2023_doubleadapt_zhao": "doubleadapt",
    "2024_master_li": "master",
    "2021_adarnn_du": "adarnn",
    "2022_hist_xu": "hist",
    "2022_thgnn_xiang": "thgnn",
    "2023_estimate_huynh": "estimate",
    "2024_alphaforge_shi": "alphaforge",
    "2026_alphaprobe_guo": "alphaprobe",
    "2022_ddg_da_li": "ddg_da",
    "2025_rd_agent_quant_li": "rd_agent_quant",
    "2022_factorvae_duan": "factorvae",
    "2021_hatr_wang": "hatr",
    "2022_alsp_tf_wang": "alsp_tf",
    "2024_ci_sthpan_xia": "ci_sthpan",
    "2024_mdgnn_li": "mdgnn",
    "2021_deeptrader_wang": "deeptrader",
    "2019_alphastock_wang": "alphastock",
    "2020_doubleensemble_zhang": "doubleensemble",
    "2024_diffsformer_gao": "diffsformer",
    "2025_finmamba_hu": "finmamba",
    "2024_lsr_igru_zhu": "lsr_igru",
    "2025_timefilter_hu": "timefilter",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_csv_with_fields(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def fmt_float(value: str) -> str:
    if not value:
        return ""
    return f"{float(value):.8f}"


def table_count(paper_id: str) -> int:
    table_dir = ROOT / "ara_artifacts" / paper_id / "evidence" / "tables"
    if not table_dir.exists():
        text_path = ROOT / "papers" / "extracted" / f"{paper_id}.txt"
        if not text_path.exists():
            return 0
        text = text_path.read_text(encoding="utf-8", errors="replace")
        return len(set(re.findall(r"\bTable\s+([0-9]+)", text, flags=re.IGNORECASE)))
    return len(list(table_dir.glob("table*_text_mentions.md")))


def figure_count(paper_id: str) -> int:
    figure_dir = ROOT / "ara_artifacts" / paper_id / "evidence" / "figures"
    if not figure_dir.exists():
        text_path = ROOT / "papers" / "extracted" / f"{paper_id}.txt"
        if not text_path.exists():
            return 0
        text = text_path.read_text(encoding="utf-8", errors="replace")
        return len(set(re.findall(r"\b(?:Figure|Fig\.)\s+([0-9]+)", text, flags=re.IGNORECASE)))
    return len(list(figure_dir.glob("figure*_text_mentions.md")))


def best_by_horizon(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    best: dict[str, dict[str, str]] = {}
    for row in rows:
        horizon = "h5" if row["run_id"].endswith("_h5") else "h1" if row["run_id"].endswith("_h1") else ""
        if not horizon:
            continue
        if horizon not in best or float(row["rankic"]) > float(best[horizon]["rankic"]):
            best[horizon] = row
    return best


def best_original_metric(rows: list[dict[str, str]], metric: str) -> str:
    values = [float(row["value"]) for row in rows if row["metric"] == metric and row.get("value")]
    if not values:
        return ""
    return f"{max(values):.8f}"


def delta(left: str, right: str) -> str:
    if not left or not right:
        return ""
    return f"{float(left) - float(right):.8f}"


def main() -> None:
    targets = read_csv(TARGETS)
    registry = {row["paper_id"]: row for row in read_csv(REGISTRY)}
    pdf_rows = {row["paper_id"]: row for row in read_csv(PDF_STATUS)}
    result_rows = read_csv(RESULTS)
    original_rows = read_csv(ORIGINAL_RESULTS) if ORIGINAL_RESULTS.exists() else []
    original_by_paper: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in original_rows:
        original_by_paper[row["paper_id"]].append(row)

    rows_by_prefix: dict[str, list[dict[str, str]]] = defaultdict(list)
    for result in result_rows:
        if result["run_type"] != "paper_model":
            continue
        prefix = result["run_id"].split("_formal_")[0]
        rows_by_prefix[prefix].append(result)

    matrix: list[dict[str, str]] = []
    for target in targets:
        paper_id = target["paper_id"]
        pdf = pdf_rows.get(paper_id)
        extracted = (ROOT / "papers" / "extracted" / f"{paper_id}.txt").exists()
        tables = table_count(paper_id)
        figures = figure_count(paper_id)
        prefix = MODEL_PREFIX.get(paper_id, "")
        china_runs = rows_by_prefix.get(prefix, [])
        best = best_by_horizon(china_runs)
        local_registered = "yes" if paper_id in registry else "no"
        paper_original_rows = original_by_paper.get(paper_id, [])
        original_metric_count = len(paper_original_rows)
        original_best_ic = best_original_metric(paper_original_rows, "IC")
        original_best_rankic = best_original_metric(paper_original_rows, "RankIC")
        china_h5_rankic = fmt_float(best.get("h5", {}).get("rankic", ""))

        if original_metric_count:
            original_status = "structured_original_metrics_available"
        elif tables:
            original_status = "table_mentions_extracted_pending_numeric_transcription"
        elif pdf or extracted:
            original_status = "pdf_or_text_present_pending_table_extraction"
        else:
            original_status = "missing_pdf_text_and_original_result_data"

        if "h1" in best and "h5" in best:
            china_status = "formal_h1_h5_complete"
        elif china_runs:
            china_status = "partial_china_run"
        else:
            china_status = "missing_china_run"

        if original_status == "structured_original_metrics_available" and china_status == "formal_h1_h5_complete":
            comparison_status = "ready_for_metric_level_comparison"
        elif original_status.startswith("table_mentions") and china_status == "formal_h1_h5_complete":
            comparison_status = "partial_ready_needs_original_numeric_values"
        elif china_status != "missing_china_run":
            comparison_status = "needs_original_experiment_data"
        else:
            comparison_status = "not_ready"

        matrix.append(
            {
                "paper_id": paper_id,
                "title": target["title"],
                "year": target["year"],
                "venue_bucket": target["venue_bucket"],
                "task_bucket": target["task_bucket"],
                "local_registered": local_registered,
                "pdf_valid": str(bool(pdf and pdf.get("valid_pdf_header") == "True")),
                "extracted_text": str(extracted),
                "original_tables_detected": str(tables),
                "original_figures_detected": str(figures),
                "structured_original_metric_rows": str(original_metric_count),
                "original_experiment_data_status": original_status,
                "china_experiment_status": china_status,
                "china_h1_rankic": fmt_float(best.get("h1", {}).get("rankic", "")),
                "china_h1_ic": fmt_float(best.get("h1", {}).get("ic", "")),
                "china_h5_rankic": china_h5_rankic,
                "china_h5_ic": fmt_float(best.get("h5", {}).get("ic", "")),
                "original_best_ic": original_best_ic,
                "original_best_rankic": original_best_rankic,
                "h5_rankic_delta_vs_original": delta(china_h5_rankic, original_best_rankic),
                "comparison_status": comparison_status,
                "code_url": target["code_url"],
                "inclusion_source": target["inclusion_source"],
            }
        )

    write_csv(OUT_CSV, matrix)
    queue = [row for row in matrix if row["comparison_status"] != "ready_for_metric_level_comparison"]
    write_csv_with_fields(OUT_QUEUE, queue, list(matrix[0]))

    summary = {
        "target_papers": len(matrix),
        "registered": sum(row["local_registered"] == "yes" for row in matrix),
        "valid_pdfs": sum(row["pdf_valid"] == "True" for row in matrix),
        "extracted_texts": sum(row["extracted_text"] == "True" for row in matrix),
        "original_table_mentions": sum(int(row["original_tables_detected"]) > 0 for row in matrix),
        "structured_original_metrics": sum(int(row["structured_original_metric_rows"]) > 0 for row in matrix),
        "china_h1_h5_complete": sum(row["china_experiment_status"] == "formal_h1_h5_complete" for row in matrix),
        "metric_compare_ready": sum(row["comparison_status"] == "ready_for_metric_level_comparison" for row in matrix),
        "partial_compare_ready": sum(row["comparison_status"] == "partial_ready_needs_original_numeric_values" for row in matrix),
        "missing_pdf_text_original": sum(
            row["original_experiment_data_status"] == "missing_pdf_text_and_original_result_data" for row in matrix
        ),
        "pending_numeric_transcription": sum(
            row["original_experiment_data_status"] == "table_mentions_extracted_pending_numeric_transcription"
            for row in matrix
        ),
        "pending_table_extraction": sum(
            row["original_experiment_data_status"] == "pdf_or_text_present_pending_table_extraction" for row in matrix
        ),
        "missing_china_runs": sum(row["china_experiment_status"] == "missing_china_run" for row in matrix),
    }

    lines = [
        "# 24-Paper Original-vs-China Experiment Matrix",
        "",
        "This report is generated from `papers/metadata/paper_target_24.csv`, `papers/metadata/original_experiment_results.csv`, local PDF/extracted-text status, ARA evidence folders, and `experiments/summary/smoke_results.csv`.",
        "",
        "## Coverage Summary",
        "",
        f"- Target papers: {summary['target_papers']}",
        f"- Locally registered papers: {summary['registered']}",
        f"- Valid local PDFs: {summary['valid_pdfs']}",
        f"- Extracted text files: {summary['extracted_texts']}",
        f"- Papers with original table mentions detected: {summary['original_table_mentions']}",
        f"- Papers with structured original metric rows: {summary['structured_original_metrics']}",
        f"- Papers with China A-share H1/H5 runs complete: {summary['china_h1_h5_complete']}",
        f"- Papers ready for metric-level comparison: {summary['metric_compare_ready']}",
        f"- Papers partially ready for comparison: {summary['partial_compare_ready']}",
        "",
        "## Matrix",
        "",
        "| Paper | Venue | Original data status | Original best IC | Original best RankIC | China H1 RankIC | China H5 RankIC | H5 RankIC delta | Comparison status |",
        "|---|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in matrix:
        lines.append(
            "| {paper_id} | {venue_bucket} | {original_experiment_data_status} | {original_best_ic} | {original_best_rankic} | {china_h1_rankic} | {china_h5_rankic} | {h5_rankic_delta_vs_original} | {comparison_status} |".format(
                **row
            )
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `formal_h1_h5_complete` means the local China A-share CSI300 2018-2024 protocol has both H1 and H5 paper-inspired runs in the summary table.",
            "- `structured_original_metrics_available` means at least one original-paper experiment table has been transcribed into `papers/metadata/original_experiment_results.csv`.",
            "- `table_mentions_extracted_pending_numeric_transcription` means original paper experiment tables were found in extracted text, but the numeric table contents still need manual or stronger PDF-table extraction before final comparison.",
            "- `missing_pdf_text_and_original_result_data` marks the next acquisition queue: download the paper, extract text/tables, then bind official metrics.",
            "- `H5 RankIC delta` is `China A-share H5 RankIC - original best RankIC`; blank values mean the original paper did not report RankIC in the transcribed rows.",
            "",
            "## Next Data Work",
            "",
        ]
    )
    next_steps: list[str] = []
    if summary["missing_pdf_text_original"]:
        next_steps.append(
            f"Download and extract PDFs/text for the {summary['missing_pdf_text_original']} papers with no local PDF/text/original result data."
        )
    if summary["pending_numeric_transcription"]:
        next_steps.append(
            f"Transcribe numeric experiment tables for the {summary['pending_numeric_transcription']} papers with detected table mentions."
        )
    if summary["pending_table_extraction"]:
        next_steps.append(
            f"Improve table extraction for the {summary['pending_table_extraction']} papers with PDF/text present but no standard table mentions."
        )
    if summary["missing_china_runs"]:
        next_steps.append(f"Run China A-share H1/H5 experiments for the {summary['missing_china_runs']} papers without local results.")
    next_steps.append(
        "Add metric-family normalization so classification, ranking, portfolio, and alpha-mining papers can be compared without mixing incompatible scores."
    )
    lines.extend(f"{index}. {step}" for index, step in enumerate(next_steps, start=1))
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"wrote {OUT_CSV.relative_to(ROOT)} rows={len(matrix)}")
    print(f"wrote {OUT_QUEUE.relative_to(ROOT)} rows={len(queue)}")
    print(f"wrote {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
