# Private WQ Run Entrypoint

Date: 2026-06-23

This repository cannot contain raw WorldQuant BRAIN records. The allowed public artifact is a sanitized aggregate CSV matching:

```text
ara_artifacts/wq_alpha_evolution/evidence/schemas/sanitized_wq_run_schema.csv
```

Template:

```text
ara_artifacts/wq_alpha_evolution/evidence/templates/sanitized_wq_run_template.csv
```

Validation command:

```powershell
python scripts\validate_sanitized_wq_run.py path\to\sanitized_wq_run.csv
```

Template validation command:

```powershell
python scripts\validate_sanitized_wq_run.py ara_artifacts\wq_alpha_evolution\evidence\templates\sanitized_wq_run_template.csv --allow-empty
```

## Allowed

Only aggregate run-level or segment-level counts:

1. candidate count;
2. simulation success count;
3. submission count;
4. accepted count;
5. Spectacular count;
6. failure taxonomy counts;
7. lesson count and lesson reuse count;
8. sanitized notes.

## Forbidden

Do not commit:

1. WorldQuant username, password, cookie, token, or session;
2. alpha IDs;
3. raw FASTEXPR expressions;
4. raw daily PnL;
5. account-linked submission logs;
6. screenshots containing private account state.

## Current Status

No real private WorldQuant aggregate run has been committed. The repository currently contains:

1. public FunctionEvolve-style proxy factor-mining evidence;
2. Lingxi-FunctionEvolve-Memory smoke ablation evidence;
3. a safe validation path for future private WQ aggregate evidence.
