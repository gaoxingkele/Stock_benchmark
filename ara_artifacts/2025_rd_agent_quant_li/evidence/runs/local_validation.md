# Local Validation Evidence

## China A-share H1/H5 matrix row

Source: `experiments/summary/paper_24_comparison_matrix.csv`

| paper_id | china_experiment_status | china_h1_rankic | china_h1_ic | china_h5_rankic | china_h5_ic | original_best_ic | original_best_rankic | h5_rankic_delta_vs_original | comparison_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2025_rd_agent_quant_li | formal_h1_h5_complete | -0.00312869 | 0.00236500 | 0.05671244 | 0.06613830 | 0.05320000 | 0.04990000 | 0.00681244 | ready_for_metric_level_comparison |


## Structured original-paper metric rows

Source: `papers/metadata/original_experiment_results.csv`

| paper_id | source_table | dataset | model | method | horizon | metric | value | stderr_or_pm | rank_scope | source_text | extraction_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2025_rd_agent_quant_li | Table 1 | CSI300 | R&D-Agent(Q) GPT-4o | proposed | main | IC | 0.0497 |  | overall | papers/extracted/2025_rd_agent_quant_li.txt:507 | verified_from_extracted_text |
| 2025_rd_agent_quant_li | Table 1 | CSI300 | R&D-Agent(Q) GPT-4o | proposed | main | ICIR | 0.4069 |  | overall | papers/extracted/2025_rd_agent_quant_li.txt:507 | verified_from_extracted_text |
| 2025_rd_agent_quant_li | Table 1 | CSI300 | R&D-Agent(Q) GPT-4o | proposed | main | RankIC | 0.0499 |  | overall | papers/extracted/2025_rd_agent_quant_li.txt:507 | verified_from_extracted_text |
| 2025_rd_agent_quant_li | Table 1 | CSI300 | R&D-Agent(Q) GPT-4o | proposed | main | RankICIR | 0.4122 |  | overall | papers/extracted/2025_rd_agent_quant_li.txt:507 | verified_from_extracted_text |
| 2025_rd_agent_quant_li | Table 1 | CSI300 | R&D-Agent(Q) GPT-4o | proposed | main | ARR | 0.1144 |  | portfolio | papers/extracted/2025_rd_agent_quant_li.txt:507 | verified_from_extracted_text |
| 2025_rd_agent_quant_li | Table 1 | CSI300 | R&D-Agent(Q) GPT-4o | proposed | main | IR | 1.3167 |  | portfolio | papers/extracted/2025_rd_agent_quant_li.txt:507 | verified_from_extracted_text |
| 2025_rd_agent_quant_li | Table 1 | CSI300 | R&D-Agent(Q) GPT-4o | proposed | main | MDD | -0.0811 |  | portfolio | papers/extracted/2025_rd_agent_quant_li.txt:507 | verified_from_extracted_text |
| 2025_rd_agent_quant_li | Table 1 | CSI300 | R&D-Agent(Q) GPT-4o | proposed | main | CR | 1.4108 |  | portfolio | papers/extracted/2025_rd_agent_quant_li.txt:507 | verified_from_extracted_text |
| 2025_rd_agent_quant_li | Table 1 | CSI300 | R&D-Agent(Q) o3-mini | proposed | main | IC | 0.0532 |  | overall | papers/extracted/2025_rd_agent_quant_li.txt:507 | verified_from_extracted_text |
| 2025_rd_agent_quant_li | Table 1 | CSI300 | R&D-Agent(Q) o3-mini | proposed | main | ICIR | 0.4278 |  | overall | papers/extracted/2025_rd_agent_quant_li.txt:507 | verified_from_extracted_text |
| 2025_rd_agent_quant_li | Table 1 | CSI300 | R&D-Agent(Q) o3-mini | proposed | main | RankIC | 0.0495 |  | overall | papers/extracted/2025_rd_agent_quant_li.txt:507 | verified_from_extracted_text |
| 2025_rd_agent_quant_li | Table 1 | CSI300 | R&D-Agent(Q) o3-mini | proposed | main | RankICIR | 0.4091 |  | overall | papers/extracted/2025_rd_agent_quant_li.txt:507 | verified_from_extracted_text |
