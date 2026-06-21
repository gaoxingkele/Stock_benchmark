# Risk-Gated AgentAdapt 动态融合实验

## 方法目标

Risk-Gated AgentAdapt 用 `RD-Agent-Quant / DoubleAdapt-family` proxy 作为主 alpha，用 official DoubleAdapt core 作为分布漂移/风险状态适配信号。它不做固定权重平均，而是在每个交易日从候选 adapter 权重 `{0, 0.1, 0.25, 0.4}` 中选择一个权重。

门控只使用滞后信息：H5 标签下，日期 `t` 的门控最多只使用 `t-5` 以前已经可观察的历史结果，避免同日未来收益泄漏。选择标准是过去窗口内候选组合的风险调整净收益，包含波动、回撤和换手成本惩罚。

实现文件：

- `scripts/run_risk_gated_agentadapt.py`
- `scripts/run_score_sensitivity_grid.py`

## 主协议

- 标的：CSI300 A 股 panel
- 标签：H5 forward return
- 组合：Top30 等权多头
- 调仓：日频
- 成本：单边 10 bps
- 训练/验证：2018-2021 train，2022 valid
- 测试：2023-2024、2025、2026 YTD

由于 official DoubleAdapt core 需要在线适配窗口，公平比较使用和 core/fusion 相同的 overlap 区间。

## Top30 / 10bps 结果

| 区间 | 方法 | 变体 | 天数 | 累计净收益 | 年化收益 | Sharpe | MDD | 平均换手 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 2023-2024 overlap | Proxy | raw | 419 | 37.23% | 20.97% | 1.47 | -13.68% | 10.98% |
| 2023-2024 overlap | Static fusion | raw | 419 | 50.45% | 27.85% | 2.00 | -10.92% | 13.21% |
| 2023-2024 overlap | Risk-Gated | raw | 419 | 49.07% | 27.14% | 2.07 | -10.76% | 14.89% |
| 2023-2024 overlap | Proxy | neutral | 419 | 31.08% | 17.68% | 1.28 | -19.27% | 11.25% |
| 2023-2024 overlap | Static fusion | neutral | 419 | 32.76% | 18.58% | 1.39 | -17.54% | 13.40% |
| 2023-2024 overlap | Risk-Gated | neutral | 419 | 29.51% | 16.83% | 1.34 | -17.18% | 15.64% |
| 2025 overlap | Proxy | raw | 183 | 103.97% | 166.86% | 13.59 | -7.15% | 10.42% |
| 2025 overlap | Static fusion | raw | 183 | 99.45% | 158.75% | 13.83 | -6.37% | 13.41% |
| 2025 overlap | Risk-Gated | raw | 183 | 97.16% | 154.67% | 13.07 | -7.16% | 12.02% |
| 2025 overlap | Proxy | neutral | 183 | 88.75% | 139.83% | 13.25 | -7.60% | 11.06% |
| 2025 overlap | Static fusion | neutral | 183 | 77.82% | 120.92% | 12.46 | -6.56% | 13.57% |
| 2025 overlap | Risk-Gated | neutral | 183 | 82.08% | 128.24% | 12.67 | -6.55% | 13.28% |
| 2026 YTD overlap | Proxy | raw | 44 | 38.65% | 549.91% | 35.41 | -4.25% | 9.47% |
| 2026 YTD overlap | Static fusion | raw | 44 | 38.83% | 554.79% | 35.52 | -4.15% | 15.08% |
| 2026 YTD overlap | Risk-Gated | raw | 44 | 39.13% | 562.83% | 35.73 | -4.37% | 9.77% |
| 2026 YTD overlap | Proxy | neutral | 44 | 20.04% | 184.60% | 18.72 | -2.82% | 16.44% |
| 2026 YTD overlap | Static fusion | neutral | 44 | 21.43% | 204.02% | 20.24 | -2.15% | 23.71% |
| 2026 YTD overlap | Risk-Gated | neutral | 44 | 20.34% | 188.77% | 19.14 | -2.66% | 16.82% |

## 敏感性网格

网格：TopK `{20, 30, 50}` × 单边成本 `{5, 10, 20}` bps，raw/neutral 共 18 个组合。

| 区间 | Risk-Gated 相对 Proxy 胜出组合 | raw 平均累计收益差 | neutral 平均累计收益差 | 结论 |
|---|---:|---:|---:|---|
| 2023-2024 overlap | 11 / 18 | +8.12 pct | -1.85 pct | raw 稳定改善，neutral 不稳定 |
| 2025 overlap | 0 / 18 | -9.33 pct | -4.44 pct | 全网格输给 proxy |
| 2026 YTD overlap | 15 / 18 | +0.88 pct | -0.04 pct | raw 小幅改善，样本短 |

## 门控行为

| 区间 | adapter weight 分布 |
|---|---|
| 2023-2024 overlap | 0.0: 67 天；0.1: 62 天；0.25: 36 天；0.4: 254 天 |
| 2025 overlap | 0.0: 98 天；0.1: 10 天；0.25: 27 天；0.4: 48 天 |
| 2026 YTD overlap | 0.0: 39 天；0.25: 5 天 |

2023-2024 中门控较多选择高 adapter 权重，因此接近 static fusion 的 raw 改善；2025 中门控虽然减少了 adapter 使用，但仍未避免收益退化；2026 YTD 中门控大部分时间关闭 adapter，仅少量启用，带来很小的 raw 增益。

## 结论

1. Risk-Gated AgentAdapt 作为学术机制成立：它把 alpha discovery 和 distribution adaptation 放进了一个无未来泄漏的在线门控框架，并能输出可交易 score。
2. 当前实现没有达到“新最佳策略”标准。关键证据是 2025 overlap 的 TopK/成本敏感性网格中 18/18 全部输给 proxy。
3. DoubleAdapt core 更适合被研究为风险状态模块，而不是固定正权重 alpha。它在 2023-2024 和 2026 YTD 可改善 raw 或回撤，但 2025 会拖累收益。
4. 当前生产/交易候选仍应保留 `RD-Agent-Quant / DoubleAdapt-family H5 Top30` proxy。Risk-Gated AgentAdapt 应作为论文候选方向继续迭代。

## 下一步研究方向

- 用 validation 年份学习门控参数，而不是手工候选权重。
- 门控目标从收益最大化改为“回撤/波动状态下的保护性启用”。
- 加入显式行业/规模暴露约束，让 neutral 版本不退化。
- 引入 rolling walk-forward calibration，避免 2025 这种 regime 下误启用 adapter。
- 把 official core 输出拆成 alpha 与风险控制两条通道，而不是单一 score 融合。

## 复现命令

```powershell
python scripts\run_risk_gated_agentadapt.py --proxy experiments\official_scores\rd_agent_quant_proxy_h5_scores.csv --adapter experiments\official_scores\doubleadapt_official_core_h5.csv --out experiments\official_scores\risk_gated_agentadapt_h5.csv --diagnostics-out experiments\risk_gated_agentadapt\risk_gated_agentadapt_diagnostics.csv --horizon 5 --topk 30 --cost-bps 10

python scripts\run_score_trade_validation.py --scores experiments\official_scores\risk_gated_agentadapt_h5.csv --panel data\processed\cn_a_share\csi300_2018_2024\panel.csv --stock-basic data\raw\tushare\csi300_2018_2024\stock_basic.csv --method risk_gated_agentadapt --horizon 5 --topk 30 --cost-bps 10 --test-start 2023-01-03 --test-end 2024-12-31 --out-dir experiments\risk_gated_agentadapt

python scripts\run_score_sensitivity_grid.py --scores experiments\official_scores\risk_gated_agentadapt_h5.csv --panel data\processed\cn_a_share\csi300_2018_2024\panel.csv --stock-basic data\raw\tushare\csi300_2018_2024\stock_basic.csv --method risk_gated_2023_2024 --test-start 2023-04-04 --test-end 2024-12-31 --out experiments\risk_gated_agentadapt\risk_gated_2023_2024_sensitivity.csv
```
