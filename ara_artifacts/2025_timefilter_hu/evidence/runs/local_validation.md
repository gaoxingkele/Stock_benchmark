# Local Validation Evidence

## China A-share H1/H5 matrix row

Source: `experiments/summary/paper_24_comparison_matrix.csv`

| paper_id | china_experiment_status | china_h1_rankic | china_h1_ic | china_h5_rankic | china_h5_ic | original_best_ic | original_best_rankic | h5_rankic_delta_vs_original | comparison_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2025_timefilter_hu | formal_h1_h5_complete | -0.01291857 | -0.00719981 | -0.01981910 | -0.00876161 |  |  |  | ready_for_metric_level_comparison |


## Structured original-paper metric rows

Source: `papers/metadata/original_experiment_results.csv`

| paper_id | source_table | dataset | model | method | horizon | metric | value | stderr_or_pm | rank_scope | source_text | extraction_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2025_timefilter_hu | Table 1 | ETT average | TimeFilter | proposed | L96_avg_horizons | MSE | 0.358 |  | overall | papers/extracted/2025_timefilter_hu.txt:803 | verified_from_extracted_text |
| 2025_timefilter_hu | Table 1 | ETT average | TimeFilter | proposed | L96_avg_horizons | MAE | 0.385 |  | overall | papers/extracted/2025_timefilter_hu.txt:803 | verified_from_extracted_text |
| 2025_timefilter_hu | Table 1 | Weather | TimeFilter | proposed | L96_avg_horizons | MSE | 0.239 |  | overall | papers/extracted/2025_timefilter_hu.txt:803 | verified_from_extracted_text |
| 2025_timefilter_hu | Table 1 | Weather | TimeFilter | proposed | L96_avg_horizons | MAE | 0.269 |  | overall | papers/extracted/2025_timefilter_hu.txt:803 | verified_from_extracted_text |
| 2025_timefilter_hu | Table 1 | Electricity | TimeFilter | proposed | L96_avg_horizons | MSE | 0.158 |  | overall | papers/extracted/2025_timefilter_hu.txt:803 | verified_from_extracted_text |
| 2025_timefilter_hu | Table 1 | Electricity | TimeFilter | proposed | L96_avg_horizons | MAE | 0.256 |  | overall | papers/extracted/2025_timefilter_hu.txt:803 | verified_from_extracted_text |
| 2025_timefilter_hu | Table 1 | Traffic | TimeFilter | proposed | L96_avg_horizons | MSE | 0.407 |  | overall | papers/extracted/2025_timefilter_hu.txt:803 | verified_from_extracted_text |
| 2025_timefilter_hu | Table 1 | Traffic | TimeFilter | proposed | L96_avg_horizons | MAE | 0.268 |  | overall | papers/extracted/2025_timefilter_hu.txt:803 | verified_from_extracted_text |
| 2025_timefilter_hu | Table 1 | Solar-Energy | TimeFilter | proposed | L96_avg_horizons | MSE | 0.223 |  | overall | papers/extracted/2025_timefilter_hu.txt:803 | verified_from_extracted_text |
| 2025_timefilter_hu | Table 1 | Solar-Energy | TimeFilter | proposed | L96_avg_horizons | MAE | 0.250 |  | overall | papers/extracted/2025_timefilter_hu.txt:803 | verified_from_extracted_text |
