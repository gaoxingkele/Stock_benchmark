# Neutralized Basic Factor IC Summary

Dataset: CSI300 by-date smoke sample  
Horizon: 1 trading day forward return  
Universe rows with labels: 1800  
Neutralized factors: 14

## Top Factors By Absolute RankIC

| Factor | N | Dates | IC | RankIC | ICIR | RankICIR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| pe_ind_size_neu | 1716 | 6 | 0.01350295 | 0.11556740 | 0.47168536 | 1.47941389 |
| intraday_ret_ind_size_neu | 1800 | 6 | 0.06684431 | 0.06836151 | 0.56033417 | 1.08627871 |
| size_log_circ_mv_ind_size_neu | 1800 | 6 | -0.06542067 | -0.05085646 | -1.64726634 | -1.21669639 |
| pb_ind_size_neu | 1800 | 6 | -0.03101003 | -0.04487278 | -0.28603946 | -0.95213866 |
| ret_1_ind_size_neu | 1500 | 5 | 0.05304906 | 0.04150307 | 0.42283557 | 0.57277756 |

## Notes

Compared with the raw basic factor run, absolute RankIC values are lower after industry and size neutralization. This is expected on a very short smoke sample because part of the original signal was broad valuation, size, and industry exposure rather than stock-specific residual alpha.
