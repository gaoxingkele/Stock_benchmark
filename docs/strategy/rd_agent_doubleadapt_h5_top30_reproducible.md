# RD-Agent-Quant / DoubleAdapt-family H5 Top30 Strategy Reproduction

本文档把当前项目中表现最好的 A 股策略固化为一份可迁移、可复现的策略说明。它可以复制到其他项目作为实现规范，但需要注意：这里的 `rd_agent_quant` 是本项目的可运行代理实现，核心机制路由到 DoubleAdapt-family proxy，不是官方 RD-Agent-Quant 或官方 DoubleAdapt 的完整版复现。

## 1. 策略定义

- 策略名：`RD-Agent-Quant / DoubleAdapt-family H5 Top30`
- 市场：A 股，当前实验使用 CSI300 成分股面板
- 信号周期：日频
- 预测目标：未来 5 个交易日收益，记为 H5 label
- 持仓方式：多头、等权、Top30
- 调仓频率：每日调仓
- 交易成本：单边 10 bps，按组合换手扣除
- 当前实现位置：
  - 预测模型：`scripts/run_paper_model_baseline.py`
  - 交易验证：`scripts/run_trade_validation.py`

## 2. 论文依托与当前边界

### 2.1 依托论文

当前策略标签来自 RD-Agent-Quant，但当前可运行机制实际依托 DoubleAdapt-family 的在线自适应思想。

1. DoubleAdapt
   - 论文：`DoubleAdapt: A Meta-learning Approach to Incremental Learning for Stock Trend Forecasting`
   - 作者：Lifan Zhao, Shuming Kong, Yanyan Shen
   - 发表：KDD 2023
   - 代码：`https://github.com/SJTU-DMTai/qlib`
   - 本策略使用的核心思想：对股票预测残差做在线自适应修正，以缓解分布漂移和个股层面的短期偏差。

2. RD-Agent-Quant
   - 论文：`R&D-Agent-Quant: A Multi-Agent Framework for Data-Centric Factors and Model Joint Optimization`
   - 作者：Yuante Li 等
   - 发表状态：2025 preprint
   - 代码：`https://github.com/microsoft/RD-Agent`
   - 本项目当前用途：作为候选论文方向和策略标签；尚未完整复现其多智能体因子生成、模型优化和实验流水线。

### 2.2 必须写清楚的边界

当前策略不是论文原版完整版：

- 不是官方 RD-Agent-Quant 全流程。
- 不是官方 DoubleAdapt 的 meta-learning data adapter + model adapter 完整实现。
- 当前是一个轻量代理：Ridge 基模型 + 20 日滚动特征 + 个股级在线残差 bias 修正。
- 当前结果可用于研究筛选和下一步实验优先级，不应直接等同于论文原始结果或实盘可交易收益。

## 3. 输入数据要求

每一行是一只股票在一个交易日的特征。最小字段如下：

```text
symbol,date,open,high,low,close,pre_close,volume,amount,change,pct_chg,
turnover_rate,volume_ratio,pe,pb,total_mv,circ_mv,factor
```

推荐额外字段：

```text
ts_code,industry
```

字段说明：

- `symbol`：证券代码，迁移到其他项目时可用 `ts_code` 或内部代码替代，但必须全局唯一。
- `date`：交易日期，格式建议 `YYYY-MM-DD`。
- `factor`：项目已有的基础因子字段；如果没有，可以先用一个稳定的技术/量价综合因子替代，或设为可解释的基础 alpha。
- `total_mv`：总市值，用于规模暴露检查和可选中性化。
- `industry`：行业分类，用于行业暴露检查和可选中性化。

数据排序要求：

```text
sort by symbol asc, date asc
```

缺失值处理：

- 用于训练的 20 日窗口内任一特征缺失，则跳过该样本。
- 标签所需的未来 `close[t+5]` 缺失，则跳过该样本。
- 不建议在未来窗口内做任何向前可见的数据填充。

## 4. 核心参数

| 参数 | 当前值 | 含义 |
|---|---:|---|
| `lookback` | 20 | 每个样本使用过去 20 个交易日特征 |
| `horizon` | 5 | 预测未来 5 日收益 |
| `features` | 16 个字段 | open/high/low/close/pre_close/volume/amount/change/pct_chg/turnover_rate/volume_ratio/pe/pb/total_mv/circ_mv/factor |
| `base_model` | Ridge | 线性岭回归 |
| `ridge_alpha` | 10 | Ridge 正则强度 |
| `max_train_rows` | 250000 | 最大训练样本数 |
| `doubleadapt_alpha` | 0.15 | 在线 bias 平滑强度 |
| `max_history` | 20 | 每只股票保存最近残差数量 |
| `topk` | 30 | 每日选分数最高的 30 只股票 |
| `cost_bps` | 10 | 单边交易成本，按换手扣 |
| `rebalance` | daily | 每日调仓 |

## 5. 标签与特征

H5 标签定义：

```text
y(i,t) = close(i,t+5) / close(i,t) - 1
```

单个训练样本的特征是股票 `i` 在 `t-19` 到 `t` 的 20 日窗口，把 16 个日度字段展开成一个向量：

```text
x(i,t) = flatten(feature(i,t-19), ..., feature(i,t))
```

基模型是 Ridge：

```text
min_w sum((y - Xw)^2) + alpha * ||w||^2
```

得到基础预测：

```text
base_score(i,t) = X(i,t) * w
```

## 6. DoubleAdapt-style 在线修正

当前实现维护每只股票自己的残差 bias：

```text
error(i,t) = y(i,t) - base_score(i,t)
bias(i) = (1 - alpha) * bias(i) + alpha * mean(recent_errors(i))
score(i,t) = base_score(i,t) + bias(i)
```

实现细节：

- 每只股票保留最近 `max_history=20` 个残差。
- 每进入一个新交易日，先用已有残差队列更新该股票 bias。
- 当天的最终打分为 `base_score + symbol_bias`。
- 然后把当天样本的真实残差加入队列，供后续交易日使用。

注意：严格实盘中，`y(i,t)` 是未来 5 日收益，不能在当天知道。当前研究代码用的是离线面板上的代理更新，适合筛选方向；进入实盘模拟前必须改成只在标签成熟后更新残差，即 `t+5` 之后才允许使用 `y(i,t)`。

## 7. 可选行业/规模中性化

为了检查策略是否只是行业或市值暴露，当前交易验证同时输出两个版本：

1. `raw`
   - 直接使用 `score` 排名选股。

2. `industry_size_neutral`
   - 每个交易日横截面回归：

```text
score ~ log(total_mv) + industry_dummies
```

   - 使用残差 `neutral_score` 排名选股。

如果迁移到其他项目，至少要保留这个中性化对照。当前结果显示 neutral 版本收益下降，但仍显著为正，因此策略不完全依赖简单行业或规模暴露。

## 8. 组合构建与成本

每日流程：

1. 对当天可交易股票按 `score` 从高到低排序。
2. 选前 `Top30`。
3. 每只股票权重相同：

```text
w(i,t) = 1 / 30
```

4. 计算组合毛收益。当前研究实现用选中股票 H5 forward return 除以 5 近似日收益：

```text
gross_return(t) = mean(y(i,t) for selected i) / 5
```

5. 计算换手：

```text
turnover(t) = 0.5 * sum_i |w(i,t) - w(i,t-1)|
```

6. 扣成本：

```text
cost(t) = turnover(t) * 0.001
net_return(t) = gross_return(t) - cost(t)
```

其中 `0.001` 对应单边 10 bps。

## 9. 伪代码

```python
panel = load_panel()
panel = sort_by_symbol_date(panel)

train_rows = build_rolling_samples(panel, lookback=20, horizon=5, split="train")
test_rows = build_rolling_samples(panel, lookback=20, horizon=5, split="test")

X_train, y_train = flatten_20d_features(train_rows)
X_test, y_test = flatten_20d_features(test_rows)

ridge = fit_ridge(X_train, y_train, alpha=10)
base_pred = ridge.predict(X_test)

score = apply_symbol_online_bias(
    preds=base_pred,
    rows=test_rows,
    alpha=0.15,
    max_history=20,
)

for date in trading_dates:
    universe = rows_on_date(date)
    selected = topk(universe, key=score, k=30)
    weights = equal_weight(selected)
    turnover = 0.5 * abs_diff(weights, previous_weights).sum()
    gross = mean(label_h5(selected)) / 5
    net = gross - turnover * 0.001
    save_daily_result(date, net, turnover)
```

## 10. 本项目复现实验命令

### 10.1 2023-2024 主验证

```powershell
python scripts\run_trade_validation.py `
  --panel data\processed\cn_a_share\csi300\panel.csv `
  --stock-basic data\raw\tushare\csi300\stock_basic.csv `
  --model rd_agent_quant `
  --horizon 5 `
  --topk 30 `
  --cost-bps 10 `
  --train-start 2018-01-02 `
  --train-end 2022-12-30 `
  --valid-start 2022-01-04 `
  --valid-end 2022-12-30 `
  --test-start 2023-01-03 `
  --test-end 2024-12-31 `
  --out-dir experiments\trade_validation
```

如果本地面板路径不同，只需要替换 `--panel` 和 `--stock-basic`。

### 10.2 2026 YTD 验证

```powershell
python scripts\run_trade_validation.py `
  --panel data\processed\cn_a_share\csi300_2018_2026_ytd\panel.csv `
  --stock-basic data\raw\tushare\csi300_2025_2026\stock_basic.csv `
  --model rd_agent_quant `
  --horizon 5 `
  --topk 30 `
  --cost-bps 10 `
  --train-start 2018-01-02 `
  --train-end 2023-12-29 `
  --valid-start 2024-01-02 `
  --valid-end 2024-12-31 `
  --test-start 2026-01-01 `
  --test-end 2026-06-18 `
  --out-dir experiments\trade_validation_2026_ytd
```

## 11. 当前可复现结果

### 11.1 2023-2024

| Variant | Net Ann. Return | Sharpe | MDD | Cum Return | Avg Turnover | Yearly |
|---|---:|---:|---:|---:|---:|---|
| raw | 43.90% | 3.05 | -13.68% | 99.74% | 10.91% | 2023: 38.22%; 2024: 49.95% |
| industry_size_neutral | 32.77% | 2.42 | -19.27% | 71.39% | 11.23% | 2023: 23.18%; 2024: 43.33% |

### 11.2 2026 YTD

测试窗口中有效 H5 标签日期为 2026-01-05 至 2026-06-11，共 104 个交易日。

| Variant | Cum Net Return | Annualized Return | Sharpe | MDD | Benchmark Cum Return | Avg Turnover |
|---|---:|---:|---:|---:|---:|---:|
| raw | 62.67% | 225.10% | 16.34 | -6.91% | -2.33% | 11.09% |
| industry_size_neutral | 44.57% | 144.28% | 14.68 | -4.94% | -2.33% | 15.29% |

2026 是半年度样本，年化收益会被明显放大。判断价值时优先看累计收益、最大回撤、换手、相对基准和 raw/neutral 一致性。

## 12. 迁移到其他项目的检查清单

1. 确认 `date` 没有未来数据泄漏。
2. 确认 `close[t+5]` 的标签只用于训练和离线评估，实盘模拟必须等标签成熟后才能更新 residual bias。
3. 确认股票池当天真实可交易，剔除停牌、涨跌停无法成交、ST、极低成交额股票。
4. 确认价格使用前复权或一致的复权口径，不能训练一套、回测另一套。
5. 保留 raw 和 industry/size neutral 两个版本。
6. 做成本敏感性：5 bps、10 bps、20 bps。
7. 做组合敏感性：Top10、Top30、Top50。
8. 做调仓敏感性：日频、每 2 日、周频。
9. 做 walk-forward retraining，不要只固定一次训练集。
10. 输出逐日持仓、换手、行业权重、规模暴露和成交额容量。

## 13. 交易解释

当前结果对交易有研究指导意义，但还不能直接作为实盘策略。

有意义的部分：

- 在 2023-2024 和 2026 YTD 两段样本上，Top30 多头组合扣 10 bps 后仍显著为正。
- raw 与行业/规模中性化版本都为正，说明结果不只是单一行业或大/小市值暴露。
- 平均日换手约 11% 到 15%，在日频策略里不是极端不可控。
- 对照的 Master、TCTS、HIST、TRA 代理模式在同一交易口径下表现较差，因此下一步资源应集中在 DoubleAdapt-family。

不能直接交易的原因：

- 当前是代理模型，不是官方完整版。
- 当前回测收益用 H5 forward return / 5 近似日收益，还不是逐笔成交撮合。
- 当前没有完整处理停牌、涨跌停、成交量容量、滑点、冲击成本和真实订单成交。
- 当前在线 bias 更新在研究代码中依赖离线标签，需要改成标签成熟后再更新，才能接近真实交易。

结论：它足够支持进入下一阶段交易级验证，不足以支持直接实盘。

## 14. 是否需要做原依托方法的完整版对比

需要。原因很直接：当前最佳结果来自代理机制，而不是论文官方完整机制。如果不做完整版，很难判断收益来自：

- DoubleAdapt 的核心在线自适应思想；
- 当前 Ridge + 手工特征的实现偶然性；
- H5 标签和 Top30 组合口径；
- 或者某种未识别的数据/回测偏差。

建议先做 DoubleAdapt 官方完整版，再做 RD-Agent-Quant 完整版。优先级如下：

1. 官方 DoubleAdapt 完整版
   - 优先级最高。
   - 因为当前收益最可能来自 DoubleAdapt-style adaptation。
   - 目标是在同一 A 股数据、同一 H5、同一 Top30、同一成本下比较 proxy vs official。

2. RD-Agent-Quant 完整版
   - 第二优先级。
   - 用于验证多智能体因子生成和模型优化是否能在 A 股数据上带来额外增益。
   - 如果工程成本高，可以先做其生成因子/模型输出的离线接入版本。

3. 融合方法完整版
   - 在 DoubleAdapt 官方版和 RD-Agent-Quant 可用输出之后再做。
   - 否则会出现两个代理叠加，结果很难解释。

## 15. 融合新方法设计

建议的新方法名：`RDA-DoubleAdapt`。

核心思想：

```text
RD-Agent-Quant 负责发现和优化因子/模型，
DoubleAdapt 负责对模型输出做在线分布漂移自适应。
```

完整流程：

1. RD-Agent-Quant 生成候选因子和候选模型。
2. 用统一 A 股训练集评估候选因子，过滤低 IC、高换手、高相关冗余因子。
3. 训练基础预测模型，输出 H5 score。
4. 在 score 层接入 DoubleAdapt online adapter。
5. 输出 raw score 和 industry/size neutral score。
6. 用同一交易验证器跑 Top30、Top50、成本敏感性和 walk-forward。

最低实验矩阵：

| 组别 | 目的 |
|---|---|
| Ridge base only | 检查没有自适应时的基础收益 |
| Ridge + proxy DoubleAdapt | 当前最佳策略，作为基线 |
| Official DoubleAdapt | 验证论文原方法是否优于代理 |
| RD-Agent factors + Ridge | 验证 agent 因子是否有增益 |
| RD-Agent factors + proxy DoubleAdapt | 验证低成本融合 |
| RD-Agent factors + Official DoubleAdapt | 最终候选完整版 |
| 每组 raw + neutral | 排除行业/规模暴露解释 |

进入纸面交易前的验收线：

- 2023、2024、2026 YTD 均为正收益。
- 10 bps 成本后年化 Sharpe 大于 1.5。
- 最大回撤低于 20%。
- neutral 版本仍显著为正。
- Top10/Top30/Top50 不应只在单一 k 上有效。
- 20 bps 成本下不应完全失效。
- 改成标签成熟后再更新 residual bias，结果仍保持主要结论。

## 16. 下一步 goal

下一步目标应定义为：

```text
在同一 CSI300 A 股数据、同一 H5 标签、同一 Top30/成本交易口径下，
完成 DoubleAdapt 官方完整版、当前 proxy 版本、RD-Agent 因子接入版本、
以及 RDA-DoubleAdapt 融合版本的可比实验，并判断当前最佳策略是否仍成立。
```

交付物：

1. 官方 DoubleAdapt 复现实验脚本。
2. RD-Agent 因子输出接入脚本。
3. 统一交易验证报告。
4. proxy vs official vs fusion 的 ablation 表。
5. 实盘前风险清单：泄漏、成交、容量、滑点、涨跌停、停牌。

