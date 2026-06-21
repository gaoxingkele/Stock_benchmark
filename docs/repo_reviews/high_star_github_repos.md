# High-Star GitHub Repositories for Quant Benchmarking

Search date: 2026-06-18

Stars are approximate values observed from GitHub pages during collection.

| Repo | Approx stars | Role in this benchmark | Initial action |
| --- | ---: | --- | --- |
| `microsoft/qlib` | 44.7k | Primary AI quant platform: data, models, alpha seeking, risk modeling, portfolio optimization, backtesting, TRA, HIST, many baselines. | Clone first into `external_repos/microsoft__qlib`. |
| `mementum/backtrader` | 22k | Mature event-driven backtesting engine; useful for strategy-level validation if Qlib is insufficient. | Optional infrastructure repo. |
| `quantopian/zipline` | 19.9k | Classic algorithmic trading backtester; useful for historical comparison, but maintenance risk should be checked. | Optional infrastructure repo. |
| `stefan-jansen/machine-learning-for-trading` | 19.2k | Broad ML-for-trading examples including alpha factor research and factor library material. | Reference implementation / notebooks. |
| `AI4Finance-Foundation/FinRL` | 15.5k | Financial reinforcement learning library; useful for trading/portfolio decision baselines rather than pure forecast models. | Later-stage RL baseline. |
| `microsoft/RD-Agent` | 13.5k | AI R&D automation; Qlib links it to quant factor mining and model optimization workflows. | Candidate for automated factor/model search experiments. |
| `polakowo/vectorbt` | 8k | Fast vectorized backtesting and large-scale parameter/factor sweeps. | Useful for factor_lab validation speed. |
| `quantopian/alphalens` | 4.3k | Factor tear sheets: returns, IC, turnover, group analysis. | Candidate dependency for factor evaluation. |
| `SJTU-DMTai/qlib` | 150 | Fork containing DoubleAdapt and MASTER re-experiment code. | Clone for CCF-A paper reproduction. |
| `gta0804/AlphaPROBE` | TBD | Recent alpha-mining code for DAG-guided factor evolution. | Verify repo maturity before cloning. |
| `thanhtrunghuynh93/estimate` | TBD | WSDM 2023 ESTIMATE implementation and data. | Secondary clone after core CCF-A work. |

## Pull Priority

1. `microsoft/qlib`
2. `SJTU-DMTai/qlib`
3. `quantopian/alphalens`
4. `polakowo/vectorbt`
5. `gta0804/AlphaPROBE`
6. `thanhtrunghuynh93/estimate`

## Notes

- Do not merge `microsoft/qlib` and `SJTU-DMTai/qlib` into one directory. Keep both under `external_repos/` because the fork carries paper-specific changes.
- Treat older infrastructure repos such as `zipline` and `backtrader` as optional until the benchmark protocol is stable.
- For alpha mining, `Alphalens` and `vectorbt` are more directly useful than full trading environments in the first pass.

