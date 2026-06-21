# 2025 年度验证结果

交易协议固定为 CSI300、H5 score、Top30 等权多头、日频调仓、单边 10 bps 换手成本。训练/验证仍使用历史区间：

- Train: 2018-01-02 至 2021-12-31
- Valid: 2022-01-04 至 2022-12-30
- Test: 2025-01-02 至 2025-12-31
- Panel: `data/processed/cn_a_share/csi300_2018_2026_ytd/panel.csv`

## 结果汇总

| 方法 | 覆盖区间 | 变体 | 天数 | 累计净收益 | 年化收益 | Sharpe | MDD | 平均换手 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| RD-Agent-Quant / DoubleAdapt-family proxy | 2025-01-02 至 2025-12-31 | raw | 243 | 128.56% | 135.67% | 11.02 | -8.44% | 10.70% |
| RD-Agent-Quant / DoubleAdapt-family proxy | 2025-01-02 至 2025-12-31 | neutral | 243 | 101.96% | 107.29% | 9.95 | -9.58% | 11.34% |
| Proxy overlap | 2025-04-07 至 2025-12-31 | raw | 183 | 103.97% | 166.86% | 13.59 | -7.15% | 10.42% |
| Proxy overlap | 2025-04-07 至 2025-12-31 | neutral | 183 | 88.75% | 139.83% | 13.25 | -7.60% | 11.06% |
| Official DoubleAdapt core | 2025-04-07 至 2025-12-31 | raw | 183 | 19.48% | 27.78% | 3.76 | -8.80% | 34.55% |
| Official DoubleAdapt core | 2025-04-07 至 2025-12-31 | neutral | 183 | 28.09% | 40.62% | 5.63 | -7.00% | 34.46% |
| RDA-DoubleAdapt core fusion | 2025-04-07 至 2025-12-31 | raw | 183 | 99.45% | 158.75% | 13.83 | -6.37% | 13.41% |
| RDA-DoubleAdapt core fusion | 2025-04-07 至 2025-12-31 | neutral | 183 | 77.82% | 120.92% | 12.46 | -6.56% | 13.57% |

## 结论

1. 2025 全年验证支持当前最佳 proxy 的有效性：raw 扣 10 bps 后累计净收益 128.56%，neutral 仍有 101.96%，说明结果不是只来自单一年份或 2026 YTD。
2. 官方 DoubleAdapt core 在 2025 单独表现比 2023-2024 好，但仍远弱于 proxy，且换手约 34.5%，交易成本敏感性明显更高。
3. 2025 的融合版没有超过同覆盖区间 proxy。raw 累计净收益从 proxy 的 103.97% 降到 fusion 的 99.45%；neutral 从 88.75% 降到 77.82%。
4. 融合版虽然降低了回撤，raw MDD 从 -7.15% 收窄到 -6.37%，但收益损失更明显。因此 2025 验证不支持把 `0.75 proxy + 0.25 official core` 作为新最佳策略。
5. 当前可执行最佳策略仍应保持为 `RD-Agent-Quant / DoubleAdapt-family H5 Top30` proxy，而不是融合版。融合方向需要改为滚动学习权重、只在风险状态下启用 core 信号，或把 official core 作为风控/降回撤模块，而不是固定正权重 alpha。

## 复现命令

```powershell
python scripts\run_trade_validation.py --panel data\processed\cn_a_share\csi300_2018_2026_ytd\panel.csv --stock-basic data\raw\tushare\csi300_2025_2026\stock_basic.csv --model rd_agent_quant --horizon 5 --lookback 20 --topk 30 --cost-bps 10 --train-start 2018-01-02 --train-end 2021-12-31 --valid-start 2022-01-04 --valid-end 2022-12-30 --test-start 2025-01-02 --test-end 2025-12-31 --out-dir experiments\trade_validation_2025

python scripts\export_paper_proxy_scores.py --model rd_agent_quant --panel data\processed\cn_a_share\csi300_2018_2026_ytd\panel.csv --out experiments\official_scores\rd_agent_quant_proxy_2025_h5_scores.csv --horizon 5 --lookback 20 --train-start 2018-01-02 --train-end 2021-12-31 --valid-start 2022-01-04 --valid-end 2022-12-30 --test-start 2025-01-02 --test-end 2025-12-31

.venv-doubleadapt\Scripts\python.exe scripts\run_official_doubleadapt_core.py --panel data\processed\cn_a_share\csi300_2018_2026_ytd\panel.csv --train-start 2018-01-02 --train-end 2021-12-31 --valid-start 2022-01-04 --valid-end 2022-12-30 --test-start 2025-01-02 --test-end 2025-12-31 --max-train-tasks 12 --max-valid-tasks 4 --task-train-days 60 --task-test-days 20 --patience 2 --out experiments\official_scores\doubleadapt_official_core_2025_h5.csv

python scripts\blend_score_files.py --left experiments\official_scores\rd_agent_quant_proxy_2025_h5_scores.csv --right experiments\official_scores\doubleadapt_official_core_2025_h5.csv --out experiments\official_scores\rda_doubleadapt_core_fusion_2025_h5.csv --left-weight 0.75 --right-weight 0.25
```
