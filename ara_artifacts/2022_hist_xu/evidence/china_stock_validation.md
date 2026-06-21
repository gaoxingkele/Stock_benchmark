# China A-Share Performance Validation

## Dataset

- Source: Tushare CSI300 A-share historical data
- Panel rows: 514449
- Symbols: 328
- Panel period: 2018-01-02 to 2024-12-31
- H1 label rows: 514121
- H5 label rows: 512809

## Validation Result

- Status: complete
- Numeric performance rows: 2
- Domain applicability rows: 0

## Interpretation

`numeric_performance` rows are direct A-share performance tests with IC/RankIC metrics.
`domain_applicability` rows are completed negative applicability checks: the ARA has no
stock prediction output interface, so direct China stock-market performance is not
mathematically defined without introducing a new adaptation model.


## Rows

- **numeric_performance H1**: status=complete; IC=-0.00457830; RankIC=-0.01433130; source=`C:\aicoding\Stock_benchmark\experiments\paper_runs\hist_formal_csi300_2018_2024_h1.csv`; reason=Paper-inspired model emits stock-level predictions evaluated by daily IC/RankIC.
- **numeric_performance H5**: status=complete; IC=-0.01629816; RankIC=-0.03030684; source=`C:\aicoding\Stock_benchmark\experiments\paper_runs\hist_formal_csi300_2018_2024_h5.csv`; reason=Paper-inspired model emits stock-level predictions evaluated by daily IC/RankIC.
