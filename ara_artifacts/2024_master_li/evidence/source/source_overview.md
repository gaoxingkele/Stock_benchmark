# Source Overview

## Registry row

```json
{
  "paper_id": "2024_master_li",
  "title": "MASTER: Market-Guided Stock Transformer for Stock Price Forecasting",
  "authors": "Tong Li; Zhaoyang Liu; Yanyan Shen; Xue Wang; Haokun Chen; Sen Huang",
  "year": "2024",
  "venue": "AAAI 2024",
  "pdf_url": "https://arxiv.org/abs/2312.15235",
  "code_url": "https://github.com/SJTU-DMTai/qlib",
  "task": "stock price/ranking forecasting",
  "tags": "CCF-A;stock transformer;market-guided gating;cross-time stock correlation",
  "status": "candidate_verified",
  "notes": "Core CCF-A candidate. Repository page states this fork includes MASTER for re-experiment."
}
```

## PDF status row

```json
{
  "paper_id": "2024_master_li",
  "path": "C:\\aicoding\\Stock_benchmark\\papers\\raw\\2024_master_li.pdf",
  "bytes": "451322",
  "valid_pdf_header": "True"
}
```

## Extracted text opening

```text
--- page 1 ---
MASTER: Market-Guided Stock Transformer for Stock Price Forecasting
Tong Li1*, Zhaoyang Liu2, Yanyan Shen1†, Xue Wang2, Haokun Chen2, Sen Huang2
1 Shanghai Jiao Tong University,2 Alibaba Group
{2017lt, shenyy}@sjtu.edu.cn, {jingmu.lzy, xue.w, hankel.chk, huangsen.huang}@alibaba-inc.com
Abstract
Stock price forecasting has remained an extremely challeng-
ing problem for many decades due to the high volatility of the
stock market. Recent efforts have been devoted to modeling
complex stock correlations toward joint stock price forecast-
ing. Existing works share a common neural architecture that
learns temporal patterns from individual stock series and then
mixes up temporal representations to establish stock correla-
tions. However, they only consider time-aligned stock cor-
relations stemming from all the input stock features, which
suffer from two limitations. First, stock correlations often oc-
cur momentarily and in a cross-time manner. Second, the fea-
ture effectiveness is dynamic with market variation, which af-
fects both the stock sequential patterns and their correlations.
To address the limitations, this paper introduces MASTER, a
```
