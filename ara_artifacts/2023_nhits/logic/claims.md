# Claims

## C01: Candidate methodology is relevant to Lingxi upgrade design
- **Statement**: `N-HiTS: Neural Hierarchical Interpolation for Time Series Forecasting` is a relevant source for the local upgrade idea `Multi-rate sampling and interpolation-inspired features`.
- **Status**: hypothesis
- **Falsification criteria**: A local proxy based on this method fails to beat `Lingxi-LinearGuard` and provides no improvement over Lingxi10 or Lingxi5 in any market/variant.
- **Proof**: [E01, E02]
- **Evidence basis**: Local survey metadata and planned validation matrix.
- **Interpretation**: Relevance is methodological, not yet performance-proven.
- **Dependencies**: none
- **Tags**: methodology-transfer, Lingxi-upgrade

## C02: The method should not replace Lingxi without local trading evidence
- **Statement**: This method cannot be promoted over Lingxi10/Lingxi5 until it passes the repository's H5 Top10/Top5 multi-market protocol.
- **Status**: supported
- **Falsification criteria**: A completed local run shows consistent improvement according to the decision gates in `docs/reports/lingxi10_lingxi5_sota_upgrade_survey.md`.
- **Proof**: [E02]
- **Evidence basis**: Prior fusion validation showed external runner-up signals can degrade A-share performance.
- **Interpretation**: Conservative gating is required before strategy changes.
- **Dependencies**: C01
- **Tags**: trading-validation, risk-control
