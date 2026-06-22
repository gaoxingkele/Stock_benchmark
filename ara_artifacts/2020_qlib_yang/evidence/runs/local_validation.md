# Local Validation Evidence

## Three-market H5 Top30 validation rows

Source: `experiments/unvalidated_candidates/combined_candidate_vs_best_proxy_summary.csv`

| market | method | proxy_detail | variant | ann_return | sharpe | mdd | cum_return | best_proxy_ann_return | best_proxy_sharpe | ann_return_delta_vs_proxy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cn_a_share | 2020_qlib_yang | Alpha158-style OHLCV/value ridge proxy | raw | -0.00325161 | -0.02388069 | -0.43596526 | -0.00935190 | 0.60057198 | 4.29542912 | -0.60382359 |
| cn_a_share | 2020_qlib_yang | Alpha158-style OHLCV/value ridge proxy | industry_size_neutral | 0.05468973 | 0.46586269 | -0.32427193 | 0.16603872 | 0.47563429 | 3.66218450 | -0.42094456 |
| us_large_cap | 2020_qlib_yang | Alpha158-style OHLCV/value ridge proxy | raw | 0.31864470 | 4.91577027 | -0.15181536 | 1.28284585 | 0.32608218 | 5.23605824 | -0.00743748 |
| us_large_cap | 2020_qlib_yang | Alpha158-style OHLCV/value ridge proxy | industry_size_neutral | 0.31864470 | 4.91577027 | -0.15181536 | 1.28284585 | 0.31264383 | 5.16555426 | 0.00600087 |
| hk_large_cap | 2020_qlib_yang | Alpha158-style OHLCV/value ridge proxy | raw | 0.11892287 | 1.23085903 | -0.24211644 | 0.38782201 | 0.22593851 | 2.16622709 | -0.10701564 |
| hk_large_cap | 2020_qlib_yang | Alpha158-style OHLCV/value ridge proxy | industry_size_neutral | 0.11892287 | 1.23085903 | -0.24211644 | 0.38782201 | 0.17534518 | 1.74935394 | -0.05642231 |
