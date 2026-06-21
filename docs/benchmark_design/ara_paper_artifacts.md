# ARA Paper Artifacts

This benchmark now compiles every locally downloaded paper into an independent Agent-Native Research Artifact (ARA).

## Scope

- Downloaded valid PDFs: 6
- Generated ARA artifacts: 6
- Level 1 structural validation: 6 passed
- Paper-model formal runs: 12
- Independent verification coverage: 6/6 downloaded papers

## Artifact Summary

Source of truth:

```text
ara_artifacts/ara_verification_summary.csv
```

| Paper | ARA | Formal paper-model runs | Independent verification |
|---|---|---:|---|
| 2021_adarnn_du | `ara_artifacts/2021_adarnn_du` | 2 | complete |
| 2021_tcts_wu | `ara_artifacts/2021_tcts_wu` | 2 | complete |
| 2021_tra_lin | `ara_artifacts/2021_tra_lin` | 2 | complete |
| 2022_hist_xu | `ara_artifacts/2022_hist_xu` | 2 | complete |
| 2023_doubleadapt_zhao | `ara_artifacts/2023_doubleadapt_zhao` | 2 | complete |
| 2024_master_li | `ara_artifacts/2024_master_li` | 2 | complete |

## Generated Files

Each paper artifact contains the ARA core:

```text
PAPER.md
logic/problem.md
logic/claims.md
logic/concepts.md
logic/experiments.md
logic/related_work.md
logic/solution/constraints.md
logic/solution/method.md
src/environment.md
trace/exploration_tree.yaml
evidence/README.md
level2_report.json
```

Evidence files include source overview, local project evidence when present, text-derived table/figure mention files, and run summaries for each matching formal paper-model result.

## Verification Commands

Build or refresh all artifacts:

```bash
python scripts/build_ara_paper_artifacts.py
```

Validate one artifact:

```bash
python C:/Users/xmupt/.codex/skills/ara-paper/scripts/validate_ara.py ara_artifacts/2021_tra_lin
```

Validate all artifacts:

```powershell
$validator='C:\Users\xmupt\.codex\skills\ara-paper\scripts\validate_ara.py'
foreach ($dir in Get-ChildItem .\ara_artifacts -Directory) {
  python $validator $dir.FullName
}
```

## Notes

The runs are paper-inspired first runnable baselines on the shared CSI300 2018-2024 formal protocol. They are deliberately labeled as local independent verification, not as official implementation parity.
