# Local Validation Evidence

## Three-market H5 Top30 validation rows

Source: `experiments/unvalidated_candidates/combined_candidate_vs_best_proxy_summary.csv`

| market | method | proxy_detail | variant | ann_return | sharpe | mdd | cum_return | best_proxy_ann_return | best_proxy_sharpe | ann_return_delta_vs_proxy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cn_a_share | 2025_cogalpha_liu | code-generated formula feature ridge: mom_60,alpha_value_mom,alpha_quality_liquidity,alpha_price_volume,rsi_14,macd_proxy,rev_5,volume_z_20,tin_boll_mom,vol_20,price_range | raw | -0.02269845 | -0.16311805 | -0.45830846 | -0.06409177 | 0.60057198 | 4.29542912 | -0.62327043 |
| cn_a_share | 2025_cogalpha_liu | code-generated formula feature ridge: mom_60,alpha_value_mom,alpha_quality_liquidity,alpha_price_volume,rsi_14,macd_proxy,rev_5,volume_z_20,tin_boll_mom,vol_20,price_range | industry_size_neutral | 0.05217390 | 0.40623420 | -0.35636877 | 0.15803253 | 0.47563429 | 3.66218450 | -0.42346039 |
| us_large_cap | 2025_cogalpha_liu | code-generated formula feature ridge: mom_60,atr_14,tin_boll_mom,price_range,macd_proxy,tin_vol_rev,rsi_14,volume_z_20,alpha_quality_liquidity,vol_20,alpha_price_volume | raw | 0.24299613 | 3.77465253 | -0.14791848 | 0.91385843 | 0.32608218 | 5.23605824 | -0.08308605 |
| us_large_cap | 2025_cogalpha_liu | code-generated formula feature ridge: mom_60,atr_14,tin_boll_mom,price_range,macd_proxy,tin_vol_rev,rsi_14,volume_z_20,alpha_quality_liquidity,vol_20,alpha_price_volume | industry_size_neutral | 0.23050268 | 3.80238189 | -0.13970315 | 0.85702527 | 0.31264383 | 5.16555426 | -0.08214115 |
| hk_large_cap | 2025_cogalpha_liu | code-generated formula feature ridge: alpha_price_volume,atr_14,alpha_quality_liquidity,price_range,boll_z_20,mom_60,tin_vol_rev,volume_z_20,vol_20,mom_20,tin_boll_mom | raw | 0.08531331 | 0.77520141 | -0.29777188 | 0.26970393 | 0.22593851 | 2.16622709 | -0.14062520 |
| hk_large_cap | 2025_cogalpha_liu | code-generated formula feature ridge: alpha_price_volume,atr_14,alpha_quality_liquidity,price_range,boll_z_20,mom_60,tin_vol_rev,volume_z_20,vol_20,mom_20,tin_boll_mom | industry_size_neutral | 0.09207112 | 0.87300014 | -0.28606018 | 0.29290076 | 0.17534518 | 1.74935394 | -0.08327406 |
