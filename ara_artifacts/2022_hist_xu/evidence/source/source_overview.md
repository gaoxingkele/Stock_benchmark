# Source Overview

## Registry row

```json
{
  "paper_id": "2022_hist_xu",
  "title": "HIST: A Graph-based Framework for Stock Trend Forecasting via Mining Concept-Oriented Shared Information",
  "authors": "Wentao Xu; Weiqing Liu; Lewen Wang; Yingce Xia; Jiang Bian; Jian Yin; Tie-Yan Liu",
  "year": "2022",
  "venue": "preprint/venue_unverified",
  "pdf_url": "https://arxiv.org/abs/2110.13716",
  "code_url": "https://github.com/microsoft/qlib",
  "task": "stock trend forecasting",
  "tags": "secondary;graph learning;concept-oriented shared information;Qlib",
  "status": "candidate_secondary",
  "notes": "Strongly relevant and included in Qlib, but CCF-A venue not verified in this pass."
}
```

## PDF status row

```json
{
  "paper_id": "2022_hist_xu",
  "path": "C:\\aicoding\\Stock_benchmark\\papers\\raw\\2022_hist_xu.pdf",
  "bytes": "1080885",
  "valid_pdf_header": "True"
}
```

## Extracted text opening

```text
--- page 1 ---
HIST: A Graph-based Framework for Stock Trend Forecasting
via Mining Concept-Oriented Shared Information
Wentao Xu1*, Weiqing Liu2, Lewen Wang2, Yingce Xia2, Jiang Bian2, Jian Yin1, Tie-Yan Liu2
1Sun Yat-sen University
2Microsoft Research
{xuwt6@mail2,issjyin@mail}.sysu.edu.cn
{weiqing.liu,lewen.wang,yingce.xia,jiang.bian,tyliu}@microsoft.com
ABSTRACT
Stock trend forecasting, which forecasts stock prices’ future trends,
plays an essential role in investment. The stocks in a market can
share information so that their stock prices are highly correlated.
Several methods were recently proposed to mine the shared infor-
mation through stock concepts (e.g., technology, Internet Retail)
extracted from the Web to improve the forecasting results. However,
previous work assumes the connections between stocks and con-
cepts are stationary, and neglects the dynamic relevance between
stocks and concepts, limiting the forecasting results. Moreover, ex-
isting methods overlook the invaluable shared information carried
by hidden concepts, which measure stocks’ commonness beyond
```
