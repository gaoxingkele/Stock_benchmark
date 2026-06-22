# Local Validation Evidence

## China A-share H1/H5 matrix row

Source: `experiments/summary/paper_24_comparison_matrix.csv`

| paper_id | china_experiment_status | china_h1_rankic | china_h1_ic | china_h5_rankic | china_h5_ic | original_best_ic | original_best_rankic | h5_rankic_delta_vs_original | comparison_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024_mdgnn_li | formal_h1_h5_complete | -0.01433130 | -0.00457830 | -0.03030684 | -0.01629816 | 0.03220000 |  |  | ready_for_metric_level_comparison |


## Structured original-paper metric rows

Source: `papers/metadata/original_experiment_results.csv`

| paper_id | source_table | dataset | model | method | horizon | metric | value | stderr_or_pm | rank_scope | source_text | extraction_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024_mdgnn_li | Table 2 | CSI100 | MDGNN | proposed | main | IC | 0.0123 | 0.00275 | overall | papers/extracted/2024_mdgnn_li.txt:593 | verified_from_extracted_text |
| 2024_mdgnn_li | Table 2 | CSI100 | MDGNN | proposed | main | IR | 0.0746 | 0.0159 | overall | papers/extracted/2024_mdgnn_li.txt:593 | verified_from_extracted_text |
| 2024_mdgnn_li | Table 2 | CSI100 | MDGNN | proposed | main | CR | 0.2741 | 0.0811 | portfolio | papers/extracted/2024_mdgnn_li.txt:593 | verified_from_extracted_text |
| 2024_mdgnn_li | Table 2 | CSI100 | MDGNN | proposed | main | Prec@30 | 0.5081 | 0.00322 | overall | papers/extracted/2024_mdgnn_li.txt:593 | verified_from_extracted_text |
| 2024_mdgnn_li | Table 2 | CSI300 | MDGNN | proposed | main | IC | 0.0322 | 0.00243 | overall | papers/extracted/2024_mdgnn_li.txt:593 | verified_from_extracted_text |
| 2024_mdgnn_li | Table 2 | CSI300 | MDGNN | proposed | main | IR | 0.2488 | 0.00419 | overall | papers/extracted/2024_mdgnn_li.txt:593 | verified_from_extracted_text |
| 2024_mdgnn_li | Table 2 | CSI300 | MDGNN | proposed | main | CR | 0.9828 | 0.0113 | portfolio | papers/extracted/2024_mdgnn_li.txt:593 | verified_from_extracted_text |
| 2024_mdgnn_li | Table 2 | CSI300 | MDGNN | proposed | main | Prec@30 | 0.5232 | 0.00301 | overall | papers/extracted/2024_mdgnn_li.txt:593 | verified_from_extracted_text |
