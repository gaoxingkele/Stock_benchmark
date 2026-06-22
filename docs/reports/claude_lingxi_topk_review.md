# Claude CLI Review: Lingxi TopK Series

Date: 2026-06-22

Claude Code CLI was asked to review the Lingxi30/20/10/5 results against the two runner-up proxies, `qlib_alpha158` and `fintsb_ts`.

## Verdict

Claude's concise judgment:

- Use **Lingxi10** as the practical default.
- Use **Lingxi20** when capacity/diversification matters more.
- Do not use **Lingxi5** as the production default because the concentration risk and cost/capacity sensitivity are under-modeled.

## Reasoning

Claude's main points:

1. Top5 raises return, but it also raises tail and capacity risk. US Top10 is close to Top5 on Sharpe with lower drawdown; HK neutral Top5 is worse than Top10/Top20 on Sharpe; China is the only market where Top5 remains defensible, but the incremental risk is still meaningful.
2. The raw-to-neutral haircut is a useful robustness diagnostic. US and China remain robust; HK has a larger haircut, so its alpha is more style/beta sensitive.
3. `qlib_alpha158` is valuable because it is stable across K in US/HK. That suggests broad cross-sectional factor information that could be integrated into Lingxi as a stabilizing feature layer.
4. `fintsb_ts` contributes momentum/reversal information, especially in China, but its standalone drawdown profile is weak. It should be treated as a feature source, not as a replacement strategy.
5. The high Sharpe values require follow-up audit: point-in-time alignment, cost realism, and capacity/ADV haircuts.

## Actionable Takeaway

The practical ranking is:

1. **Lingxi10**: best return/risk/default deployment balance.
2. **Lingxi20**: safer capacity-oriented alternative.
3. **Lingxi5**: research/aggressive sleeve only, not default.
4. **Lingxi30**: conservative baseline, but leaves too much signal unused.

The two runner-up algorithms should be mined for features:

- Add Qlib/Alpha158-style cross-sectional factor primitives to improve breadth and HK/US robustness.
- Add FinTSB-style time-series state features as auxiliary signals, but gate them through Lingxi's residual/risk framework.
