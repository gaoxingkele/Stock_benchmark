# Experiments

## E01: ARA Level 1 structural validation
- **Verifies**: C01
- **Setup**:
  - Model: n/a
  - Hardware: local filesystem
  - Dataset: `ara_artifacts/2024_ci_sthpan_xia`
  - System: `C:/Users/xmupt/.codex/skills/ara-paper/scripts/validate_ara.py`
- **Procedure**:
  1. Run the Level 1 validator on this artifact directory.
  2. Confirm all mandatory files are present and non-empty.
- **Metrics**: PASS/FAIL and validator warnings
- **Expected outcome**:
  - The artifact passes Level 1 structural validation.
- **Baselines**: ARA mandatory core schema
- **Dependencies**: none

## E02: Source provenance check
- **Verifies**: C02
- **Setup**:
  - Model: n/a
  - Hardware: local filesystem
  - Dataset: repository metadata and reports
  - System: `Stock_benchmark`
- **Procedure**:
  1. Read paper metadata rows.
  2. Check PDF and extracted text availability.
  3. Preserve exact source availability in the evidence layer.
- **Metrics**: source rows present, PDF flag, extracted text flag
- **Expected outcome**:
  - Source availability is explicit and reproducible.
- **Baselines**: none
- **Dependencies**: E01

## E03: Local validation binding check
- **Verifies**: C03
- **Setup**:
  - Model: paper-inspired proxy or matrix mapping
  - Hardware: local CPU/NumPy workflow
  - Dataset: China A-share, US large-cap, and HK large-cap as applicable
  - System: local validation scripts and summary CSVs
- **Procedure**:
  1. Locate matching paper rows in the authoritative validation CSV.
  2. Copy exact rows into `evidence/runs/local_validation.md`.
  3. Compare against the best proxy where the protocol provides that comparator.
- **Metrics**: IC, RankIC, annualized return, Sharpe, MDD, cumulative return, delta versus best proxy where available
- **Expected outcome**:
  - Matching validation evidence exists for this paper.
- **Baselines**: current best proxy `RDA-Adapt30` where available
- **Dependencies**: E01, E02
