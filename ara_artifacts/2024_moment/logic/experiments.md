# Experiments

## E01: ARA source and dataset audit
- **Verifies**: C01
- **Setup**:
  - Model: `2024_moment` methodology audit
  - Hardware: n/a
  - Dataset: source metadata and registered benchmark datasets
  - System: local repository metadata
- **Procedure**:
  1. Confirm source URL, method family, and candidate Lingxi use.
  2. Map paper-mentioned benchmark datasets to local download or documented-only status.
- **Metrics**: ARA Level 1 validation pass/fail; dataset registry completeness.
- **Expected outcome**:
  - The ARA package has complete mandatory layers.
  - Downloadable small datasets are separated from large documented-only datasets.
- **Baselines**: existing 31-paper ARA pool
- **Dependencies**: none

## E02: Lingxi10/Lingxi5 proxy validation
- **Verifies**: C01, C02
- **Setup**:
  - Model: `General TS representation candidate across tasks` proxy
  - Hardware: CPU-first local run
  - Dataset: China A-share, US large cap, HK large cap, crypto major
  - System: H5 Top10/Top5 equal-weight daily protocol
- **Procedure**:
  1. Implement a point-in-time proxy for the method family.
  2. Score all symbols on the same test period as existing Lingxi validation.
  3. Compare raw and neutral variants against Lingxi10, Lingxi5, and LinearGuard.
- **Metrics**: annualized return, Sharpe, maximum drawdown, active Sharpe, turnover, hit rate.
- **Expected outcome**:
  - The candidate is promoted only if it passes the decision gates in the SOTA survey report.
- **Baselines**: Lingxi10, Lingxi5, Lingxi-LinearGuard
- **Dependencies**: E01
