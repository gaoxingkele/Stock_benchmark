# Local Validation Evidence

## China A-share H1/H5 matrix row

Source: `experiments/summary/paper_24_comparison_matrix.csv`

| paper_id | china_experiment_status | china_h1_rankic | china_h1_ic | china_h5_rankic | china_h5_ic | original_best_ic | original_best_rankic | h5_rankic_delta_vs_original | comparison_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2020_doubleensemble_zhang | formal_h1_h5_complete | -0.00312869 | 0.00236500 | 0.05671244 | 0.06613830 | 0.11500000 |  |  | ready_for_metric_level_comparison |


## Structured original-paper metric rows

Source: `papers/metadata/original_experiment_results.csv`

| paper_id | source_table | dataset | model | method | horizon | metric | value | stderr_or_pm | rank_scope | source_text | extraction_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2020_doubleensemble_zhang | Table II | Daily stock trading MLP | DoubleEnsemble SR+FS | proposed | daily | Ann.Ret. | 0.5137 |  | portfolio | papers/extracted/2020_doubleensemble_zhang.txt:821 | verified_from_extracted_text |
| 2020_doubleensemble_zhang | Table II | Daily stock trading MLP | DoubleEnsemble SR+FS | proposed | daily | Sharpe | 4.941 |  | portfolio | papers/extracted/2020_doubleensemble_zhang.txt:821 | verified_from_extracted_text |
| 2020_doubleensemble_zhang | Table II | Daily stock trading MLP | DoubleEnsemble SR+FS | proposed | daily | MDD | 0.0598 |  | portfolio | papers/extracted/2020_doubleensemble_zhang.txt:821 | verified_from_extracted_text |
| 2020_doubleensemble_zhang | Table II | Daily stock trading MLP | DoubleEnsemble SR+FS | proposed | daily | IC | 0.115 |  | overall | papers/extracted/2020_doubleensemble_zhang.txt:821 | verified_from_extracted_text |
| 2020_doubleensemble_zhang | Table II | Daily stock trading MLP | DoubleEnsemble SR+FS | proposed | daily | IR | 1.035 |  | overall | papers/extracted/2020_doubleensemble_zhang.txt:821 | verified_from_extracted_text |
| 2020_doubleensemble_zhang | Table II | Weekly stock trading MLP | DoubleEnsemble SR+FS | proposed | weekly | Ann.Ret. | 0.2567 |  | portfolio | papers/extracted/2020_doubleensemble_zhang.txt:821 | verified_from_extracted_text |
| 2020_doubleensemble_zhang | Table II | Weekly stock trading MLP | DoubleEnsemble SR+FS | proposed | weekly | Sharpe | 4.448 |  | portfolio | papers/extracted/2020_doubleensemble_zhang.txt:821 | verified_from_extracted_text |
| 2020_doubleensemble_zhang | Table II | Weekly stock trading MLP | DoubleEnsemble SR+FS | proposed | weekly | MDD | 0.0241 |  | portfolio | papers/extracted/2020_doubleensemble_zhang.txt:821 | verified_from_extracted_text |
| 2020_doubleensemble_zhang | Table II | Weekly stock trading MLP | DoubleEnsemble SR+FS | proposed | weekly | IC | 0.078 |  | overall | papers/extracted/2020_doubleensemble_zhang.txt:821 | verified_from_extracted_text |
| 2020_doubleensemble_zhang | Table II | Weekly stock trading MLP | DoubleEnsemble SR+FS | proposed | weekly | IR | 0.773 |  | overall | papers/extracted/2020_doubleensemble_zhang.txt:821 | verified_from_extracted_text |
