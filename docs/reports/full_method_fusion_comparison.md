# 完整版方法与融合加强版对比状态

本报告把当前最佳可运行 proxy、两篇参考论文的完整版方法，以及拟定的完整版融合加强方法，放到同一个交易协议下比较：CSI300、H5 score、Top30 等权多头、日频调仓、单边 10 bps 换手成本。

## 当前可执行结果

| 方法 | 实现口径 | 2023-2024 累计净收益 | 2023-2024 年化收益 | Sharpe | MDD | 2026 YTD 累计净收益 | 状态 |
|---|---|---:|---:|---:|---:|---:|---|
| RD-Agent-Quant / DoubleAdapt-family H5 Top30 | 本地 proxy：Ridge + 个股残差自适应 | 99.74% | 43.90% | 3.05 | -13.68% | 62.67% | 已完成 |
| Official DoubleAdapt | SJTU-DMTai qlib incremental 官方实现 | pending | pending | pending | pending | pending | 运行环境阻塞 |
| Official RD-Agent-Quant | Microsoft RD-Agent(Q) 因子-模型协同优化 | pending | pending | pending | pending | pending | 仓库/环境/LLM 编排阻塞 |
| RDA-DoubleAdapt full fusion | RD-Agent(Q) 因子/模型 + DoubleAdapt 官方在线适配 | pending | pending | pending | pending | pending | 等待两个完整版上游输出 |

## 运行环境审计

- Python: `Python 3.14.4`
- DoubleAdapt 仓库：`fbd067c`，路径 `external_repos/SJTU-DMTai__qlib`
- RD-Agent 仓库：`not_cloned`，路径 `external_repos/microsoft__RD-Agent`
- `torch` 可用：`False`
- `qlib` 可用：`False`
- `higher` 可用：`False`
- `mlflow` 可用：`False`
- `jinja2` 可用：`False`

官方 DoubleAdapt 需要 fork 版 Qlib 运行时，并要求 `torch==1.9.0` 和 `higher==0.2.1`。当前机器只暴露 Python 3.14，且 PyTorch/Qlib 运行栈未安装。因此现在不能诚实地报告官方 DoubleAdapt 完整版结果。

官方 RD-Agent-Quant 需要 Microsoft RD-Agent 应用栈、Qlib quant 场景配置、LLM API 凭据，以及因子/模型迭代运行。本地 RD-Agent 克隆当前不完整，因此还没有官方 RD-Agent(Q) score 输出。

## 标准 Score 接口

每个完整版方法进入统一交易对比前，必须先导出一个 CSV：

```text
date,symbol,score
2023-01-03,SH600000,-0.00123
```

可以额外提供 `label`，但推荐让 `scripts/run_score_trade_validation.py` 从本地 panel 统一拼接 H5 标签，确保每个方法使用相同标签和成本协议。

## 复现实验命令

回测官方 DoubleAdapt score 文件：

```powershell
python scripts\run_score_trade_validation.py `
  --scores experiments\official_scores\doubleadapt_official_h5.csv `
  --panel data\processed\cn_a_share\csi300_2018_2024\panel.csv `
  --stock-basic data\raw\tushare\csi300_2018_2024\stock_basic.csv `
  --method doubleadapt_official `
  --horizon 5 --topk 30 --cost-bps 10
```

回测 RD-Agent(Q) score 文件：

```powershell
python scripts\run_score_trade_validation.py `
  --scores experiments\official_scores\rd_agent_quant_official_h5.csv `
  --panel data\processed\cn_a_share\csi300_2018_2024\panel.csv `
  --stock-basic data\raw\tushare\csi300_2018_2024\stock_basic.csv `
  --method rd_agent_quant_official `
  --horizon 5 --topk 30 --cost-bps 10
```

回测完整版融合 score 文件：

```powershell
python scripts\run_score_trade_validation.py `
  --scores experiments\official_scores\rda_doubleadapt_full_h5.csv `
  --panel data\processed\cn_a_share\csi300_2018_2024\panel.csv `
  --stock-basic data\raw\tushare\csi300_2018_2024\stock_basic.csv `
  --method rda_doubleadapt_full `
  --horizon 5 --topk 30 --cost-bps 10
```

## 完整版融合定义

融合加强版不应是几个 proxy 输出的简单平均。真正的完整版定义是：

1. 在相同 CSI300 train/valid 切分上运行 RD-Agent(Q) 因子-模型协同优化。
2. 导出 RD-Agent(Q) 的日频 H5 股票 score。
3. 把这些 score 或 RD-Agent 选出的模型 embedding 接入 DoubleAdapt 官方 online adapter。
4. 导出适配后的 H5 score：`rda_doubleadapt_full_h5.csv`。
5. 用同一成本模型验证 raw 和行业/规模中性化 Top30 组合。

## 判定规则

在至少一个官方方法产出可比 score 文件之前，当前 proxy 仍是研究基线。融合方法只有在 raw 和 neutral 两个版本上都能扣 10 bps 后超过当前 proxy，且没有显著抬高回撤或换手时，才算真正通过。
