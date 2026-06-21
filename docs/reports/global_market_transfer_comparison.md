# 美股、港股、主流加密货币跨市场验证

## 数据与协议

数据由 `scripts/download_yahoo_market_panel.py` 通过 Yahoo Finance Chart API 下载，并转换成项目统一 `panel.csv` 格式。

| 市场 | Universe | 样本 | 数据区间 | 测试区间 | 组合 |
|---|---|---:|---|---|---|
| US large cap | 40 只美股大盘股 | 85,080 行 | 2018-01-01 至 2026-06-21 | 2023-01-03 至 2025-12-31 | Top30 |
| HK large cap | 39 只港股大盘股 | 78,853 行 | 2018-01-01 至 2026-06-21 | 2023-01-03 至 2025-12-31 | Top30 |
| Crypto major | 20 个主流加密货币 | 55,629 行 | 2018-01-01 至 2026-06-21 | 2023-01-03 至 2025-12-31 | Top10 |

统一训练/验证/测试协议：

- Train: 2018-01-02 至 2021-12-31
- Valid: 2022-01-03 至 2022-12-30
- Test: 2023-01-03 至 2025-12-31
- Label: H5 forward return
- 调仓: 日频
- 成本: 单边 10 bps

## 与原论文方法代理的对应关系

| 本地方法名 | 论文/方法族 | 本地代理口径 |
|---|---|---|
| `rd_agent_quant`, `diffsformer`, `doubleadapt`, `doubleensemble` | RD-Agent-Quant / DoubleAdapt-family | Ridge 主模型 + 个股残差在线自适应 |
| `master`, `alphaprobe` | MASTER / market-guided transformer family | Ridge + market context representation |
| `hist` | HIST graph/concept family | market shared state + stock residual representation |
| `tra` | TRA temporal routing family | volatility regime buckets |
| `tcts` | TCTS multi-horizon family | H1/H3/H5 多预测头加权集成 |

这些不是官方完整实现，而是项目内可迁移的 paper-inspired proxy；官方 DoubleAdapt core 已在 A 股部分单独跑过，跨市场这里先比较可批量复用的原方法代理。

## 主结果

| 市场 | 最优方法 | 变体 | 年化收益 | Sharpe | MDD | 累计净收益 | 平均换手 |
|---|---|---|---:|---:|---:|---:|---:|
| US large cap | DoubleAdapt-family proxy | raw | 32.61% | 5.24 | -14.86% | 132.15% | 6.41% |
| US large cap | DoubleAdapt-family proxy | neutral | 31.26% | 5.17 | -14.49% | 125.20% | 7.04% |
| HK large cap | DoubleAdapt-family proxy | raw | 22.59% | 2.17 | -18.58% | 81.15% | 3.27% |
| HK large cap | DoubleAdapt-family proxy | neutral | 17.53% | 1.75 | -20.75% | 60.20% | 4.35% |
| Crypto major | DoubleAdapt-family proxy | raw | 108.61% | 3.73 | -41.94% | 2333.94% | 12.65% |
| Crypto major | DoubleAdapt-family proxy | neutral | 72.57% | 2.56 | -45.06% | 968.48% | 18.69% |

## 方法横向对比

### US Large Cap

| 方法族 | raw 年化 | raw Sharpe | raw MDD | neutral 年化 | neutral Sharpe |
|---|---:|---:|---:|---:|---:|
| DoubleAdapt-family | 32.61% | 5.24 | -14.86% | 31.26% | 5.17 |
| HIST | 25.86% | 4.34 | -14.27% | 26.92% | 4.60 |
| MASTER / AlphaProbe | 25.38% | 4.23 | -14.90% | 24.83% | 4.22 |
| TRA | 24.91% | 4.15 | -15.32% | 23.72% | 4.00 |
| TCTS | 22.43% | 3.68 | -15.21% | 22.36% | 3.76 |

### HK Large Cap

| 方法族 | raw 年化 | raw Sharpe | raw MDD | neutral 年化 | neutral Sharpe |
|---|---:|---:|---:|---:|---:|
| DoubleAdapt-family | 22.59% | 2.17 | -18.58% | 17.53% | 1.75 |
| TRA | 8.53% | 0.79 | -29.44% | 10.69% | 1.02 |
| HIST | 9.74% | 0.93 | -28.38% | 9.11% | 0.90 |
| MASTER / AlphaProbe | 9.51% | 0.90 | -27.86% | 9.83% | 0.97 |
| TCTS | 7.88% | 0.72 | -30.07% | 8.98% | 0.87 |

### Crypto Major

| 方法族 | raw 年化 | raw Sharpe | raw MDD | neutral 年化 | neutral Sharpe |
|---|---:|---:|---:|---:|---:|
| DoubleAdapt-family | 108.61% | 3.73 | -41.94% | 72.57% | 2.56 |
| TRA | 61.62% | 2.31 | -47.09% | 48.13% | 1.85 |
| TCTS | 52.47% | 1.89 | -50.35% | 42.76% | 1.64 |
| HIST | 33.01% | 1.31 | -53.38% | 54.85% | 2.02 |
| MASTER / AlphaProbe | 36.70% | 1.39 | -55.81% | 51.10% | 1.92 |

## 解释

1. DoubleAdapt-family proxy 在三个市场都排第一，说明“基础预测 + 个体残差在线自适应”的迁移性强于纯 market-context 或 volatility bucket 代理。
2. 美股结果最稳定，neutral 后几乎不退化，说明大盘股 universe 的行业/规模暴露对结果影响较小。
3. 港股结果仍为正，但明显弱于美股，2023 年为负、2024-2025 修复，说明该市场 regime 切换更强。
4. Crypto raw 收益高但 MDD 极大，neutral 后收益大幅下降，说明结果有很强资产类别/市值/趋势暴露，不能直接等同于稳健 alpha。
5. 和 A 股结论一致：DoubleAdapt-family 在跨市场上仍是最强候选，但应继续用 Regime-Gated 思路控制回撤和暴露。

## 局限

- Yahoo Finance 数据没有复权基本面和完整退市样本，存在 survivorship bias。
- 美股/港股 universe 是大盘股静态池，不是指数成分历史动态池。
- Crypto 7×24 交易与股票交易日不同，当前仍按日频 H5 协议验证。
- 这里比较的是 paper-inspired proxy，不是所有论文官方完整代码。

## 复现命令

```powershell
python scripts\download_yahoo_market_panel.py --universe us_large_cap --start 2018-01-01 --end 2026-06-21 --out-dir data\processed\global_markets\us_large_cap_2018_2026 --sleep 0.6 --retries 4

python scripts\download_yahoo_market_panel.py --universe hk_large_cap --start 2018-01-01 --end 2026-06-21 --out-dir data\processed\global_markets\hk_large_cap_2018_2026 --sleep 0.6 --retries 4

python scripts\download_yahoo_market_panel.py --universe crypto_major --start 2018-01-01 --end 2026-06-21 --out-dir data\processed\global_markets\crypto_major_2018_2026 --sleep 0.6 --retries 4

python scripts\run_trade_validation.py --panel data\processed\global_markets\us_large_cap_2018_2026\panel.csv --stock-basic data\processed\global_markets\us_large_cap_2018_2026\stock_basic.csv --horizon 5 --lookback 20 --topk 30 --cost-bps 10 --train-start 2018-01-02 --train-end 2021-12-31 --valid-start 2022-01-03 --valid-end 2022-12-30 --test-start 2023-01-03 --test-end 2025-12-31 --out-dir experiments\global_markets\us_large_cap_2018_2026
```
