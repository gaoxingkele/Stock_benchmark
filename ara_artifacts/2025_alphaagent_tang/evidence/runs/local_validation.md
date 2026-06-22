# Local Validation Evidence

## Three-market H5 Top30 validation rows

Source: `experiments/unvalidated_candidates/combined_candidate_vs_best_proxy_summary.csv`

| market | method | proxy_detail | variant | ann_return | sharpe | mdd | cum_return | best_proxy_ann_return | best_proxy_sharpe | ann_return_delta_vs_proxy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cn_a_share | 2025_alphaagent_tang | regularized formula-alpha selection: mom_60,alpha_value_mom,alpha_quality_liquidity,alpha_price_volume,ma_gap_20,rev_5,volume_z_20,mom_20 | raw | 0.01675385 | 0.15462889 | -0.28748942 | 0.04910048 | 0.60057198 | 4.29542912 | -0.58381813 |
| cn_a_share | 2025_alphaagent_tang | regularized formula-alpha selection: mom_60,alpha_value_mom,alpha_quality_liquidity,alpha_price_volume,ma_gap_20,rev_5,volume_z_20,mom_20 | industry_size_neutral | 0.06047224 | 0.48942151 | -0.36431219 | 0.18457749 | 0.47563429 | 3.66218450 | -0.41516205 |
| us_large_cap | 2025_alphaagent_tang | regularized formula-alpha selection: mom_60,price_range,mom_20,rev_5,ma_gap_20,volume_z_20,alpha_quality_liquidity,vol_20 | raw | 0.24453859 | 3.95892548 | -0.14763751 | 0.92095431 | 0.32608218 | 5.23605824 | -0.08154359 |
| us_large_cap | 2025_alphaagent_tang | regularized formula-alpha selection: mom_60,price_range,mom_20,rev_5,ma_gap_20,volume_z_20,alpha_quality_liquidity,vol_20 | industry_size_neutral | 0.24818733 | 4.12066403 | -0.14544478 | 0.93780942 | 0.31264383 | 5.16555426 | -0.06445650 |
| hk_large_cap | 2025_alphaagent_tang | regularized formula-alpha selection: alpha_price_volume,alpha_quality_liquidity,price_range,boll_z_20,mom_60,volume_z_20,vol_20,mom_20 | raw | 0.09603531 | 0.86714582 | -0.29512285 | 0.30663692 | 0.22593851 | 2.16622709 | -0.12990320 |
| hk_large_cap | 2025_alphaagent_tang | regularized formula-alpha selection: alpha_price_volume,alpha_quality_liquidity,price_range,boll_z_20,mom_60,volume_z_20,vol_20,mom_20 | industry_size_neutral | 0.08182434 | 0.79202060 | -0.27681279 | 0.25783551 | 0.17534518 | 1.74935394 | -0.09352084 |
