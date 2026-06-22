# Local Validation Evidence

## China A-share H1/H5 matrix row

Source: `experiments/summary/paper_24_comparison_matrix.csv`

| paper_id | china_experiment_status | china_h1_rankic | china_h1_ic | china_h5_rankic | china_h5_ic | original_best_ic | original_best_rankic | h5_rankic_delta_vs_original | comparison_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2025_finmamba_hu | formal_h1_h5_complete | -0.01433130 | -0.00457830 | -0.03030684 | -0.01629816 |  |  |  | ready_for_metric_level_comparison |


## Structured original-paper metric rows

Source: `papers/metadata/original_experiment_results.csv`

| paper_id | source_table | dataset | model | method | horizon | metric | value | stderr_or_pm | rank_scope | source_text | extraction_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2025_finmamba_hu | Table 1 | CSI300 | FinMamba | proposed | main | ARR | 0.106 |  | portfolio | papers/extracted/2025_finmamba_hu.txt:694 | verified_from_extracted_text |
| 2025_finmamba_hu | Table 1 | CSI300 | FinMamba | proposed | main | AVol | 0.163 |  | portfolio | papers/extracted/2025_finmamba_hu.txt:694 | verified_from_extracted_text |
| 2025_finmamba_hu | Table 1 | CSI300 | FinMamba | proposed | main | MDD | -0.102 |  | portfolio | papers/extracted/2025_finmamba_hu.txt:694 | verified_from_extracted_text |
| 2025_finmamba_hu | Table 1 | CSI300 | FinMamba | proposed | main | ASR | 0.653 |  | portfolio | papers/extracted/2025_finmamba_hu.txt:694 | verified_from_extracted_text |
| 2025_finmamba_hu | Table 1 | CSI300 | FinMamba | proposed | main | IR | 0.705 |  | portfolio | papers/extracted/2025_finmamba_hu.txt:694 | verified_from_extracted_text |
| 2025_finmamba_hu | Table 1 | CSI500 | FinMamba | proposed | main | ARR | 0.227 |  | portfolio | papers/extracted/2025_finmamba_hu.txt:694 | verified_from_extracted_text |
| 2025_finmamba_hu | Table 1 | CSI500 | FinMamba | proposed | main | AVol | 0.163 |  | portfolio | papers/extracted/2025_finmamba_hu.txt:694 | verified_from_extracted_text |
| 2025_finmamba_hu | Table 1 | CSI500 | FinMamba | proposed | main | MDD | -0.106 |  | portfolio | papers/extracted/2025_finmamba_hu.txt:694 | verified_from_extracted_text |
| 2025_finmamba_hu | Table 1 | CSI500 | FinMamba | proposed | main | ASR | 1.389 |  | portfolio | papers/extracted/2025_finmamba_hu.txt:694 | verified_from_extracted_text |
| 2025_finmamba_hu | Table 1 | CSI500 | FinMamba | proposed | main | IR | 1.339 |  | portfolio | papers/extracted/2025_finmamba_hu.txt:694 | verified_from_extracted_text |
| 2025_finmamba_hu | Table 1 | S&P500 | FinMamba | proposed | main | ARR | 0.341 |  | portfolio | papers/extracted/2025_finmamba_hu.txt:694 | verified_from_extracted_text |
| 2025_finmamba_hu | Table 1 | S&P500 | FinMamba | proposed | main | AVol | 0.164 |  | portfolio | papers/extracted/2025_finmamba_hu.txt:694 | verified_from_extracted_text |
