# Concepts

## Alpha discovery agent

An agentic loop that proposes alpha expressions, submits or simulates them, reads feedback, diagnoses failures, and changes the next search direction.

## Self-evolution memory

The persistent record of what worked, what failed, and what rules should affect future candidate generation. In the WQ-style skill, this is represented by skill-file updates and local alpha databases. In ARA, it is represented by evidence tables and the exploration trace.

## Sanitized WQ evidence

Aggregate statistics derived from WorldQuant BRAIN interactions. It must exclude raw alpha identifiers, account-linked records, private expressions, cookies, credentials, and raw PnL time series.

## Public proxy factor run

A local factor-mining experiment that uses public or repository-controlled data to approximate the research loop without depending on WorldQuant BRAIN.

## Cross-framework comparison

A comparison between factor-mining agents and strategy-evolution systems using layer-aware metrics:

1. generation efficiency;
2. failure-memory quality;
3. novelty and self-correlation control;
4. OOS proxy performance;
5. reproducibility and auditability.
