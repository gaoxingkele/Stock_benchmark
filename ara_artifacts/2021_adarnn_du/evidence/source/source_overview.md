# Source Overview

## Registry row

```json
{
  "paper_id": "2021_adarnn_du",
  "title": "AdaRNN: Adaptive Learning and Forecasting of Time Series",
  "authors": "Yuntao Du; Jindong Wang; Wenjie Feng; Sinno Pan; Tao Qin; Renjun Xu; Chongjun Wang",
  "year": "2021",
  "venue": "venue_unverified",
  "pdf_url": "https://arxiv.org/abs/2108.04443",
  "code_url": "https://github.com/microsoft/qlib/tree/main/examples/benchmarks/ADARNN",
  "task": "time series forecasting / financial analysis",
  "tags": "expanded;domain adaptation;temporal covariate shift;Qlib",
  "status": "candidate_expanded",
  "notes": "General time-series model with financial analysis experiments; Qlib has runnable benchmark implementation."
}
```

## PDF status row

```json
{
  "paper_id": "2021_adarnn_du",
  "path": "C:\\aicoding\\Stock_benchmark\\papers\\raw\\2021_adarnn_du.pdf",
  "bytes": "1295311",
  "valid_pdf_header": "True"
}
```

## Extracted text opening

```text
--- page 1 ---
AdaRNN: Adaptive Learning and Forecasting for Time Series ∗
Yuntao Du1, Jindong Wang2, Wenjie Feng3, Sinno Pan4, Tao Qin2, Renjun Xu5, Chongjun Wang1
1Nanjing University, Nanjing, China 2Microsoft Research Asia, Beijing, China
3Institute of Data Science, National University of Singapore 4Nanyang Technological University 5Zhejiang University
dz1833005@smail.nju.edu.cn,jindong.wang@microsoft.com
ABSTRACT
Though time series forecasting has a wide range of real-world appli-
cations, it is a very challenging task. This is because the statistical
properties of a time series can vary with time, causing the distri-
bution to change temporally, which is known as the distribution
shift problem in the machine learning community. By far, it still
remains unexplored to model time series from the distribution-shift
perspective. In this paper, we formulate the Temporal Covariate
Shift (TCS) problem for the time series forecasting. We propose
Adaptive RNNs (AdaRNN) to tackle the TCS problem. AdaRNN is
sequentially composed of two modules. The first module is referred
to as Temporal Distribution Characterization, which aims to better
characterize the distribution information in a time series. The sec-
ond module is termed as Temporal Distribution Matching, which
```
