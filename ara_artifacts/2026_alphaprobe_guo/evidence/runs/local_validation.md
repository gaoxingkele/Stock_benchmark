# Local Validation Evidence

## China A-share H1/H5 matrix row

Source: `experiments/summary/paper_24_comparison_matrix.csv`

| paper_id | china_experiment_status | china_h1_rankic | china_h1_ic | china_h5_rankic | china_h5_ic | original_best_ic | original_best_rankic | h5_rankic_delta_vs_original | comparison_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026_alphaprobe_guo | formal_h1_h5_complete | -0.01482999 | -0.00173863 | -0.01968499 | -0.01162947 | 0.09040000 | 0.11350000 | -0.13318499 | ready_for_metric_level_comparison |


## Structured original-paper metric rows

Source: `papers/metadata/original_experiment_results.csv`

| paper_id | source_table | dataset | model | method | horizon | metric | value | stderr_or_pm | rank_scope | source_text | extraction_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026_alphaprobe_guo | Table 1 | CSI300 | AlphaPROBE | proposed | main | IC | 0.0584 |  | overall | papers/extracted/2026_alphaprobe_guo.txt:614 | verified_from_extracted_text |
| 2026_alphaprobe_guo | Table 1 | CSI300 | AlphaPROBE | proposed | main | ICIR | 39.02 |  | overall | papers/extracted/2026_alphaprobe_guo.txt:614 | verified_from_extracted_text |
| 2026_alphaprobe_guo | Table 1 | CSI300 | AlphaPROBE | proposed | main | RankIC | 0.0720 |  | overall | papers/extracted/2026_alphaprobe_guo.txt:614 | verified_from_extracted_text |
| 2026_alphaprobe_guo | Table 1 | CSI300 | AlphaPROBE | proposed | main | RankICIR | 46.94 |  | overall | papers/extracted/2026_alphaprobe_guo.txt:614 | verified_from_extracted_text |
| 2026_alphaprobe_guo | Table 1 | CSI300 | AlphaPROBE | proposed | main | AR | 0.0750 |  | portfolio | papers/extracted/2026_alphaprobe_guo.txt:630 | verified_from_extracted_text |
| 2026_alphaprobe_guo | Table 1 | CSI300 | AlphaPROBE | proposed | main | MDD | 0.2225 |  | portfolio | papers/extracted/2026_alphaprobe_guo.txt:630 | verified_from_extracted_text |
| 2026_alphaprobe_guo | Table 1 | CSI300 | AlphaPROBE | proposed | main | SR | 0.4411 |  | portfolio | papers/extracted/2026_alphaprobe_guo.txt:630 | verified_from_extracted_text |
| 2026_alphaprobe_guo | Table 1 | CSI500 | AlphaPROBE | proposed | main | IC | 0.0626 |  | overall | papers/extracted/2026_alphaprobe_guo.txt:614 | verified_from_extracted_text |
| 2026_alphaprobe_guo | Table 1 | CSI500 | AlphaPROBE | proposed | main | ICIR | 52.39 |  | overall | papers/extracted/2026_alphaprobe_guo.txt:614 | verified_from_extracted_text |
| 2026_alphaprobe_guo | Table 1 | CSI500 | AlphaPROBE | proposed | main | RankIC | 0.0878 |  | overall | papers/extracted/2026_alphaprobe_guo.txt:614 | verified_from_extracted_text |
| 2026_alphaprobe_guo | Table 1 | CSI500 | AlphaPROBE | proposed | main | RankICIR | 73.18 |  | overall | papers/extracted/2026_alphaprobe_guo.txt:614 | verified_from_extracted_text |
| 2026_alphaprobe_guo | Table 1 | CSI500 | AlphaPROBE | proposed | main | AR | 0.1745 |  | portfolio | papers/extracted/2026_alphaprobe_guo.txt:630 | verified_from_extracted_text |
