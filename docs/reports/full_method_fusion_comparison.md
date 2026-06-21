# 完整版方法与融合加强版对比状态

交易协议固定为 CSI300、H5 score、Top30 等权多头、日频调仓、单边 10 bps 换手成本。官方 DoubleAdapt core 已在本地跑通；RD-Agent 官方应用栈仍未跑通，因此当前融合版是“RD-Agent-Quant proxy score + 官方 DoubleAdapt core score”的可执行融合。由于官方 DoubleAdapt core 从 2023-04-04 起才有在线适配输出，公平比较同时列出 419 天重叠区间。

## 交易结果

| 方法 | 实现路径 | 天数 | 累计净收益 | 年化收益 | Sharpe | MDD | 平均换手 | 状态 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 当前最佳 RD-Agent-Quant / DoubleAdapt-family | 本地 proxy：Ridge + 个股残差自适应 | 479 | 99.74% | 43.90% | 3.05 | -13.68% | 10.91% | 2023-2024 全区间基线 |
| 当前最佳 proxy 重叠区间 | 同一 proxy，限制到 2023-04-04 至 2024-12-31 | 419 | 37.23% | 20.97% | 1.47 | -13.68% | 10.98% | 用于和官方 core 公平比较 |
| Official DoubleAdapt core | SJTU-DMTai Qlib incremental DoubleAdapt 核心训练循环 | 419 | 2.00% | 1.20% | 0.11 | -25.88% | 25.11% | 已跑通，但单独表现弱 |
| RDA-DoubleAdapt core fusion | 0.75 proxy daily z-score + 0.25 official DoubleAdapt core daily z-score | 419 | 50.45% | 27.85% | 2.00 | -10.92% | 13.21% | 已跑通，raw 超过重叠 proxy |

- 2026 YTD 当前最佳 proxy raw 累计净收益：62.67%，年化：225.10%，Sharpe：16.34。
- Official DoubleAdapt core neutral：累计 -6.37%，年化 -3.88%，Sharpe -0.39。
- Fusion neutral：累计 32.76%，年化 18.58%，Sharpe 1.39。

## 结论

1. 官方 DoubleAdapt core 单独不适合直接作为当前 A 股 Top30 交易策略：raw 年化只有 1.20%，Sharpe 0.11，neutral 为负，且平均换手约 25%，明显弱于现有最佳 proxy。
2. 融合版有增益，但增益主要发生在 2024 年，2023 年重叠段仍为负。419 天重叠区间 raw 从 proxy 的 37.23% 累计净收益提升到 50.45%，Sharpe 从 1.47 提升到 2.00，MDD 从 -13.68% 收窄到 -10.92%。
3. neutral 融合提升很小：累计净收益从 31.08% 到 32.76%，Sharpe 从 1.28 到 1.39，说明新增信号仍含有行业/规模或市场状态暴露，不能直接认定为稳健 alpha。
4. 现阶段不能声称“完整版融合加强版全面通过”。可以把 fusion 作为下一轮候选，但需要在 2026 YTD、滚动权重、不同 TopK/成本和行业规模中性约束下继续验证。

## 环境审计

- Python: `Python 3.14.4`
- DoubleAdapt 专用环境: `.venv-doubleadapt`，Python 3.9，torch/higher/mlflow/qlib 依赖已补齐到可运行官方 core。
- DoubleAdapt fork: `fbd067c` at `external_repos/SJTU-DMTai__qlib`。
- RD-Agent repo: `not_cloned` at `external_repos/microsoft__RD-Agent`。
- 当前默认 Python 可见依赖: torch=False, qlib=False, higher=False, mlflow=False。

## 复现命令

导出当前最佳 proxy 逐股 score：

```powershell
python scripts\export_paper_proxy_scores.py --model rd_agent_quant --panel data\processed\cn_a_share\csi300_2018_2024\panel.csv --out experiments\official_scores\rd_agent_quant_proxy_h5_scores.csv --horizon 5 --lookback 20
```

运行官方 DoubleAdapt core：

```powershell
.venv-doubleadapt\Scripts\python.exe scripts\run_official_doubleadapt_core.py --out experiments\official_scores\doubleadapt_official_core_h5.csv --max-train-tasks 12 --max-valid-tasks 4 --task-train-days 60 --task-test-days 20 --patience 2
```

生成融合 score 并回测：

```powershell
python scripts\blend_score_files.py --left experiments\official_scores\rd_agent_quant_proxy_h5_scores.csv --right experiments\official_scores\doubleadapt_official_core_h5.csv --out experiments\official_scores\rda_doubleadapt_core_fusion_h5.csv --left-weight 0.75 --right-weight 0.25
python scripts\run_score_trade_validation.py --scores experiments\official_scores\rda_doubleadapt_core_fusion_h5.csv --panel data\processed\cn_a_share\csi300_2018_2024\panel.csv --stock-basic data\raw\tushare\csi300_2018_2024\stock_basic.csv --method rda_doubleadapt_core_fusion --horizon 5 --topk 30 --cost-bps 10 --test-start 2023-01-03 --test-end 2024-12-31
```
