# Environment

## Public repository mode

Required:

1. Python 3.11+ or the repository's active Python environment.
2. Existing `Stock_benchmark` data and experiment outputs.
3. ARA validator:
   `C:/Users/xmupt/.codex/skills/ara-paper/scripts/validate_ara.py`

Validation command:

```powershell
python C:/Users/xmupt/.codex/skills/ara-paper/scripts/validate_ara.py ara_artifacts/wq_alpha_evolution
```

Bundle command:

```powershell
python scripts\validate_wq_alpha_evolution_bundle.py
```

## Optional private WQ mode

Optional private mode may use a local clone of `QuantML-Research/wq-alpha-research` and WorldQuant BRAIN credentials.

Do not commit private mode files:

1. `.env`
2. `credential.txt`
3. cookies or sessions
4. `alpha_db.json`
5. raw `batch_submit_results.json`
6. raw alpha expressions
7. alpha IDs
8. raw PnL time series

Only aggregate sanitized tables should be copied into this repository.
