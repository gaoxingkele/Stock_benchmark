# Problem Specification

## Observations

### O1: Lingxi10 and Lingxi5 need method-level upgrades, not blind ensembling
- **Statement**: Prior Qlib/FinTSB fusion did not justify replacing Lingxi10, so new methods must be tested as targeted modules.
- **Evidence**: `docs/reports/lingxi_fusion_upgrade_validation.md`
- **Implication**: A Decoder-Only Foundation Model for Time-Series Forecasting should be translated into a falsifiable proxy module before any production claim.

### O2: The paper belongs to the `foundation_forecaster` family
- **Statement**: Local survey metadata classifies this candidate as `foundation_forecaster`.
- **Evidence**: `papers/metadata/lingxi_cross_domain_ts_sota_candidates.csv`
- **Implication**: The first local validation should test the corresponding Lingxi transfer idea: `Later-stage foundation-model feature source`.

## Gaps

### G1: Official reproduction is not yet present
- **Statement**: The repository has not yet imported official code or exact hyperparameters for this candidate.
- **Caused by**: The current phase is method-selection and ARA engineering.
- **Existing attempts**: SOTA survey and Claude CLI ranking.
- **Why they fail**: A survey is not evidence that the method improves Top10/Top5 trading.

## Key Insight
- **Insight**: Treat cross-domain time-series SOTA as modular Lingxi upgrades and require them to beat Lingxi10/Lingxi5 under the existing trading protocol.
- **Derived from**: O1, O2
- **Enables**: A staged validation plan that avoids overfitting to generic forecasting benchmarks.

## Assumptions
- A1: OHLCV panels are sufficient for first-pass proxy validation.
- A2: Point-in-time feature construction is mandatory.
- A3: Generic forecasting improvements do not automatically transfer to TopK stock ranking.
