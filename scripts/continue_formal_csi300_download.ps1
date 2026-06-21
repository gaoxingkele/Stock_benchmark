param(
    [int]$BatchSize = 50,
    [double]$Sleep = 0.5
)

python Stock_benchmark\scripts\download_csi300_by_date_fragments.py `
  --start-date 20180102 `
  --end-date 20241231 `
  --sleep $Sleep `
  --retries 5 `
  --retry-sleep 3 `
  --complete-triplet-batch $BatchSize `
  --continue-on-error `
  --out-dir Stock_benchmark\data\raw\tushare\csi300_2018_2024

python Stock_benchmark\scripts\report_tushare_fragment_progress.py `
  --raw-dir Stock_benchmark\data\raw\tushare\csi300_2018_2024
