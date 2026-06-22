# Local Validation Evidence

## China A-share H1/H5 matrix row

Source: `experiments/summary/paper_24_comparison_matrix.csv`

| paper_id | china_experiment_status | china_h1_rankic | china_h1_ic | china_h5_rankic | china_h5_ic | original_best_ic | original_best_rankic | h5_rankic_delta_vs_original | comparison_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2022_factorvae_duan | formal_h1_h5_complete | -0.01482999 | -0.00173863 | -0.01968499 | -0.01162947 |  | 0.05500000 | -0.07468499 | ready_for_metric_level_comparison |


## Structured original-paper metric rows

Source: `papers/metadata/original_experiment_results.csv`

| paper_id | source_table | dataset | model | method | horizon | metric | value | stderr_or_pm | rank_scope | source_text | extraction_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2022_factorvae_duan | Table 1 | China A-share test set | FactorVAE | proposed | main | RankIC | 0.055 | 0.004 | overall | papers/extracted/2022_factorvae_duan.txt:737 | verified_from_extracted_text |
| 2022_factorvae_duan | Table 1 | China A-share test set | FactorVAE | proposed | main | RankICIR | 0.568 | 0.044 | overall | papers/extracted/2022_factorvae_duan.txt:737 | verified_from_extracted_text |
| 2022_factorvae_duan | Table 3 | CSI300 excess return | FactorVAE | proposed | main | AR | 0.1532 |  | portfolio | papers/extracted/2022_factorvae_duan.txt:870 | verified_from_extracted_text |
| 2022_factorvae_duan | Table 3 | CSI300 excess return | FactorVAE | proposed | main | SR | 1.92 |  | portfolio | papers/extracted/2022_factorvae_duan.txt:870 | verified_from_extracted_text |
| 2022_factorvae_duan | Table 3 | CSI300 excess return | FactorVAE | proposed | main | MDD | 0.0447 |  | portfolio | papers/extracted/2022_factorvae_duan.txt:870 | verified_from_extracted_text |
| 2022_factorvae_duan | Table 3 | CSI300 excess return | FactorVAE(TDrisk) | proposed_variant | main | AR | 0.1632 |  | portfolio | papers/extracted/2022_factorvae_duan.txt:871 | verified_from_extracted_text |
| 2022_factorvae_duan | Table 3 | CSI300 excess return | FactorVAE(TDrisk) | proposed_variant | main | SR | 2.09 |  | portfolio | papers/extracted/2022_factorvae_duan.txt:871 | verified_from_extracted_text |
| 2022_factorvae_duan | Table 3 | CSI300 excess return | FactorVAE(TDrisk) | proposed_variant | main | MDD | 0.0450 |  | portfolio | papers/extracted/2022_factorvae_duan.txt:871 | verified_from_extracted_text |
