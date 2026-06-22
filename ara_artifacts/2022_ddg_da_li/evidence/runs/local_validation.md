# Local Validation Evidence

## China A-share H1/H5 matrix row

Source: `experiments/summary/paper_24_comparison_matrix.csv`

| paper_id | china_experiment_status | china_h1_rankic | china_h1_ic | china_h5_rankic | china_h5_ic | original_best_ic | original_best_rankic | h5_rankic_delta_vs_original | comparison_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2022_ddg_da_li | formal_h1_h5_complete | -0.02718109 | -0.01077460 | -0.04531338 | -0.02084717 | 0.13120000 |  |  | ready_for_metric_level_comparison |


## Structured original-paper metric rows

Source: `papers/metadata/original_experiment_results.csv`

| paper_id | source_table | dataset | model | method | horizon | metric | value | stderr_or_pm | rank_scope | source_text | extraction_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2022_ddg_da_li | Table 1 | Stock Price Trend Forecasting | DDG-DA | proposed | main | IC | 0.1312 |  | overall | papers/extracted/2022_ddg_da_li.txt:641 | verified_from_extracted_text |
| 2022_ddg_da_li | Table 1 | Stock Price Trend Forecasting | DDG-DA | proposed | main | ICIR | 1.1299 |  | overall | papers/extracted/2022_ddg_da_li.txt:641 | verified_from_extracted_text |
| 2022_ddg_da_li | Table 1 | Stock Price Trend Forecasting | DDG-DA | proposed | main | Ann.Ret. | 0.2565 |  | portfolio | papers/extracted/2022_ddg_da_li.txt:641 | verified_from_extracted_text |
| 2022_ddg_da_li | Table 1 | Stock Price Trend Forecasting | DDG-DA | proposed | main | Sharpe | 2.4063 |  | portfolio | papers/extracted/2022_ddg_da_li.txt:641 | verified_from_extracted_text |
| 2022_ddg_da_li | Table 1 | Stock Price Trend Forecasting | DDG-DA | proposed | main | MDD | -0.1381 |  | portfolio | papers/extracted/2022_ddg_da_li.txt:641 | verified_from_extracted_text |
