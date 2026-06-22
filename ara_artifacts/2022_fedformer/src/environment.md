# Environment

- **Language/runtime**: Python 3 local repository environment
- **Framework**: pandas/numpy for first-pass proxy validation; official framework not yet imported
- **Hardware**: CPU-first for proxy validation; GPU requirements not specified in provided sources
- **Data sources**:
- ETTh1: data/external/time_series_sota/ett/ETTh1.csv (downloaded)
- ETTh2: data/external/time_series_sota/ett/ETTh2.csv (downloaded)
- ETTm1: data/external/time_series_sota/ett/ETTm1.csv (downloaded)
- ETTm2: data/external/time_series_sota/ett/ETTm2.csv (downloaded)
- Electricity: not_downloaded (documented_only)
- Traffic: not_downloaded (documented_only)
- **Key dependencies**: repository default Python dependencies
- **Protocols**: H5 Top10/Top5 equal-weight long-only daily rebalance; single-side 10 bps cost
- **Random seeds**: repository default seed 42 when applicable
