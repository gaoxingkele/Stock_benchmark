# Problem

Financial markets are non-stationary. A strategy that adapts aggressively to recent validation performance can overfit regime noise and degrade out of sample.

The practical question is not only:

> Which alpha model predicts returns?

The CASE-Lingxi question is:

> When should a strategy system adapt, and when should it refuse to adapt?

## Observed Failure Modes

The current repository contains evidence for several failure modes:

1. validation-only Sharpe selection fails out of sample;
2. universal dynamic routing does not consistently beat fixed/static sleeves;
3. frozen RL routing improves only a few scenarios and is not robust enough;
4. structured market tags are plausible but not yet tradable edge;
5. generic SOTA-inspired feature proxies usually do not beat Lingxi.

## Research Target

CASE-Lingxi separates:

1. alpha-layer score generation;
2. strategy-layer sleeve selection;
3. research-layer agentic hypothesis generation and audit.

The aim is to make the research layer more intelligent without letting it bypass the out-of-sample promotion gate.

