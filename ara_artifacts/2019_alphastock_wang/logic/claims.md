# Claims

## C01: ARA structural completeness
- **Statement**: `2019_alphastock_wang` has the mandatory ARA layers and core files.
- **Status**: supported
- **Falsification criteria**: Run the Level 1 validator and observe missing required files.
- **Proof**: [E01]
- **Evidence basis**: This artifact contains `PAPER.md`, `logic/`, `src/`, `trace/`, and `evidence/`.
- **Interpretation**: Structural completeness is not the same as official reproduction parity.
- **Dependencies**: none
- **Tags**: ARA, structure

## C02: Source grounding
- **Statement**: `2019_alphastock_wang` is grounded in current repository metadata and available source files.
- **Status**: supported
- **Falsification criteria**: Remove the cited source rows/files and regenerate the evidence index.
- **Proof**: [E02]
- **Evidence basis**: `evidence/source/source_overview.md` records source rows and availability flags.
- **Interpretation**: Missing PDF or extracted text is explicitly recorded rather than hidden.
- **Dependencies**: C01
- **Tags**: provenance, source

## C03: Local validation binding
- **Statement**: Local China A-share H1/H5 proxy validation status is `formal_h1_h5_complete`.
- **Status**: supported
- **Falsification criteria**: Re-read the cited validation CSV and find no matching paper rows.
- **Proof**: [E03]
- **Evidence basis**: `evidence/runs/local_validation.md` contains exact validation rows.
- **Interpretation**: This supports local proxy validation, not universal trading validity.
- **Dependencies**: C01, C02
- **Tags**: validation, benchmark
