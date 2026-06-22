# Local Validation Evidence

## China A-share H1/H5 matrix row

Source: `experiments/summary/paper_24_comparison_matrix.csv`

| paper_id | china_experiment_status | china_h1_rankic | china_h1_ic | china_h5_rankic | china_h5_ic | original_best_ic | original_best_rankic | h5_rankic_delta_vs_original | comparison_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2022_thgnn_xiang | formal_h1_h5_complete | -0.01433130 | -0.00457830 | -0.03030684 | -0.01629816 |  |  |  | ready_for_metric_level_comparison |


## Structured original-paper metric rows

Source: `papers/metadata/original_experiment_results.csv`

| paper_id | source_table | dataset | model | method | horizon | metric | value | stderr_or_pm | rank_scope | source_text | extraction_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2022_thgnn_xiang | Table 2 | S&P500 | THGNN | proposed | 2020 | ACC | 0.579 |  | overall | papers/extracted/2022_thgnn_xiang.txt:593 | verified_from_extracted_text |
| 2022_thgnn_xiang | Table 2 | S&P500 | THGNN | proposed | 2020 | ARR | 0.665 |  | portfolio | papers/extracted/2022_thgnn_xiang.txt:593 | verified_from_extracted_text |
| 2022_thgnn_xiang | Table 2 | S&P500 | THGNN | proposed | 2020 | AV | 0.468 |  | portfolio | papers/extracted/2022_thgnn_xiang.txt:593 | verified_from_extracted_text |
| 2022_thgnn_xiang | Table 2 | S&P500 | THGNN | proposed | 2020 | MDD | -0.369 |  | portfolio | papers/extracted/2022_thgnn_xiang.txt:593 | verified_from_extracted_text |
| 2022_thgnn_xiang | Table 2 | S&P500 | THGNN | proposed | 2020 | ASR | 1.421 |  | portfolio | papers/extracted/2022_thgnn_xiang.txt:593 | verified_from_extracted_text |
| 2022_thgnn_xiang | Table 2 | S&P500 | THGNN | proposed | 2020 | CR | 1.804 |  | portfolio | papers/extracted/2022_thgnn_xiang.txt:593 | verified_from_extracted_text |
| 2022_thgnn_xiang | Table 2 | S&P500 | THGNN | proposed | 2020 | IR | 1.340 |  | portfolio | papers/extracted/2022_thgnn_xiang.txt:593 | verified_from_extracted_text |
| 2022_thgnn_xiang | Table 2 | CSI300 | THGNN | proposed | 2020 | ACC | 0.551 |  | overall | papers/extracted/2022_thgnn_xiang.txt:593 | verified_from_extracted_text |
| 2022_thgnn_xiang | Table 2 | CSI300 | THGNN | proposed | 2020 | ARR | 0.632 |  | portfolio | papers/extracted/2022_thgnn_xiang.txt:593 | verified_from_extracted_text |
| 2022_thgnn_xiang | Table 2 | CSI300 | THGNN | proposed | 2020 | AV | 0.336 |  | portfolio | papers/extracted/2022_thgnn_xiang.txt:593 | verified_from_extracted_text |
| 2022_thgnn_xiang | Table 2 | CSI300 | THGNN | proposed | 2020 | MDD | -0.237 |  | portfolio | papers/extracted/2022_thgnn_xiang.txt:593 | verified_from_extracted_text |
| 2022_thgnn_xiang | Table 2 | CSI300 | THGNN | proposed | 2020 | ASR | 1.881 |  | portfolio | papers/extracted/2022_thgnn_xiang.txt:593 | verified_from_extracted_text |
