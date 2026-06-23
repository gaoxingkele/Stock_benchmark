# Problem

The user-provided source describes a self-evolving WorldQuant BRAIN alpha-mining skill that ran for three days, generated more than 300 candidate alphas, passed 24 submissions, and reportedly produced more than 20 Spectacular-grade alphas.

The scientific question for this repository is narrower:

> Can the self-evolving factor-mining loop be converted into a reproducible, privacy-preserving ARA project and compared fairly with CASE-Lingxi?

Directly comparing reported Spectacular alpha counts with Lingxi portfolio returns is not valid because the systems operate at different layers:

1. WorldQuant-style skill: expression-level alpha discovery and platform submission feedback.
2. CASE-Lingxi: strategy-level selection, routing, and production-gate validation across markets.
3. ARA protocol: research-process reproducibility, claim-evidence binding, and negative-result preservation.

The comparison must therefore evaluate both:

1. **research-loop efficiency**: how quickly and cleanly the agent discovers usable candidates;
2. **trading proxy quality**: whether generated or selected signals survive public out-of-sample tests under costs and correlation controls.

## Requirements

1. Do not commit credentials, cookies, alpha IDs, raw private expressions, raw PnL, or account-linked WorldQuant records.
2. Store WorldQuant outcomes only as aggregate sanitized statistics.
3. Preserve failed paths such as invalid fields, high turnover, low fitness, and self-correlation.
4. Compare against CASE-Lingxi with explicit layer labels so factor-mining performance is not mistaken for executable strategy performance.
5. Provide schemas that allow a future private run to be verified without exposing private records.
