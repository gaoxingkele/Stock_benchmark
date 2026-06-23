# Method

The proposed method is **ARA-WQ Alpha Evolution**.

It has four layers:

1. **External alpha-mining skill layer**
   - Start from a WorldQuant-style self-evolving skill.
   - Treat BRAIN as an optional closed-platform validator.
   - Do not import credentials or private alpha records into the public repo.

2. **Sanitization layer**
   - Convert private run outcomes into aggregate rows.
   - Remove alpha IDs, raw expressions, raw daily PnL, account identifiers, cookies, and credentials.
   - Keep only run-level counts and distribution summaries.

3. **Public proxy layer**
   - Run local factor-generation or factor-selection experiments on public/repository data.
   - Use OOS IC, turnover, costs, drawdown, and novelty checks.
   - This layer is the only one that can be fully reproduced from the public repository.

4. **Cross-framework comparison layer**
   - Compare ARA-WQ against CASE-Lingxi by system layer and evidence type.
   - Report whether WQ-style memory ideas improve Lingxi only after a frozen OOS ablation.

## Comparison rules

1. Report WQ BRAIN metrics as private-platform evidence, not public reproducibility evidence.
2. Report proxy factor results as public reproducibility evidence.
3. Report CASE-Lingxi results from existing committed experiment summaries.
4. Keep production claims conservative: no WQ-derived live-trading claim is allowed without an independently reproducible proxy or a private audit trail.
