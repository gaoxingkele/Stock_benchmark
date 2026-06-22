# Concepts

## Paper ID
- **Notation**: `2022_alsp_tf_wang`
- **Definition**: Stable identifier used across repository metadata, reports, and ARA directories.
- **Boundary conditions**: Valid only within this benchmark repository.
- **Related concepts**: benchmark pool, evidence binding

## Local Proxy Validation
- **Notation**: E03
- **Definition**: A repository-run experiment that maps a paper direction to a local H1/H5 or H5 TopK protocol.
- **Boundary conditions**: Does not claim official implementation parity unless separately stated.
- **Related concepts**: paper-inspired proxy, validation CSV

## Best Proxy Comparator
- **Notation**: RDA-Adapt30
- **Definition**: The current best local `rd_agent_quant / DoubleAdapt-family` Top30 proxy used as a reference in expansion-candidate validation.
- **Boundary conditions**: Applies to local benchmark protocols and current data snapshots.
- **Related concepts**: DoubleAdapt-family, RD-Agent-Quant

## Source Group
- **Notation**: `paper_24_matrix`
- **Definition**: The evidence path through which this paper entered the 31-paper pool.
- **Boundary conditions**: Determined by current repository metadata.
- **Related concepts**: 24-paper matrix, expansion-only candidates

## ARA Evidence Layer
- **Notation**: `evidence/`
- **Definition**: Files that preserve exact source rows, validation metrics, and provenance used by claims.
- **Boundary conditions**: Interpretation belongs in `logic/`; exact values belong in `evidence/`.
- **Related concepts**: claims, experiments, trace
