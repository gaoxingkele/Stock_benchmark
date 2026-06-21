# Source Overview

## Registry row

```json
{
  "paper_id": "2021_tcts_wu",
  "title": "Temporally Correlated Task Scheduling for Sequence Learning",
  "authors": "Xueqing Wu et al.",
  "year": "2021",
  "venue": "ICML 2021",
  "pdf_url": "https://proceedings.mlr.press/v139/wu21e/wu21e.pdf",
  "code_url": "https://github.com/microsoft/qlib/tree/main/examples/benchmarks/TCTS",
  "task": "time series forecasting / alpha seeking",
  "tags": "expanded;CCF-A;multi-task;Qlib",
  "status": "candidate_expanded",
  "notes": "Paper URL verified from Qlib TCTS README and PMLR proceedings; Qlib provides runnable Alpha360 benchmark config."
}
```

## PDF status row

```json
{
  "paper_id": "2021_tcts_wu",
  "path": "C:\\aicoding\\Stock_benchmark\\papers\\raw\\2021_tcts_wu.pdf",
  "bytes": "900989",
  "valid_pdf_header": "True"
}
```

## Extracted text opening

```text
--- page 1 ---
Temporally Correlated Task Scheduling for Sequence Learning
Xueqing Wu 1 Lewen Wang 2 Yingce Xia 2 Weiqing Liu 2 Lijun Wu 2 Shufang Xie 2 Tao Qin 2 Tie-Yan Liu 2
Abstract
Sequence learning has attracted much research
attention from the machine learning community
in recent years. In many applications, a sequence
learning task is usually associated with multiple
temporally correlated auxiliary tasks, which are
different in terms of how much input information
to use or which future step to predict. For exam-
ple, (i) in simultaneous machine translation, one
can conduct translation under different latency
(i.e., how many input words to read/wait before
translation); (ii) in stock trend forecasting, one
can predict the price of a stock in different future
days (e.g., tomorrow, the day after tomorrow).
While it is clear that those temporally correlated
tasks can help each other, there is a very limited
exploration on how to better leverage multiple
```
