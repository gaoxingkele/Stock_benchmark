# Related Work

## RW01: Existing 31-paper finance ARA pool
- **DOI**: local ARA registry
- **Type**: baseline
- **Delta**:
  - What changed: `TimesNet: Temporal 2D-Variation Modeling for General Time Series Analysis` is added as cross-domain time-series methodology, not finance-specific prior art.
  - Why: The user requested 2020+ SOTA ideas beyond financial tasks for Lingxi upgrades.
- **Claims affected**: C01, C02
- **Adopted elements**: ARA engineering protocol and local H5 TopK validation discipline.

## RW02: Lingxi-Fusion validation
- **DOI**: local report
- **Type**: bounds
- **Delta**:
  - What changed: Prior Qlib/FinTSB fusion showed fixed auxiliary signals can degrade A-share performance.
  - Why: It motivates gated, module-level validation for `periodicity_2d_variation`.
- **Claims affected**: C02
- **Adopted elements**: Multi-market raw/neutral validation and conservative promotion gates.
