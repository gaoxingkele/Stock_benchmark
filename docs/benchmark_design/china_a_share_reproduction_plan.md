# China A-Share Reproduction Plan

Date: 2026-06-18

Goal: reproduce and compare recent stock/index forecasting and alpha factor mining methods on China A-share data, using Tushare as the primary data source and Qlib-style alpha evaluation as the first shared protocol.

## API And Environment Check

Environment files checked:

- `Stock_benchmark/.env`
- `Stock_benchmark/.env.cloubic`

Security note: keys were checked by name/presence/length only. Secret values were not printed.

| Service | Env vars | Test result | Notes |
| --- | --- | --- | --- |
| Tushare | `TUSHARE_TOKEN` | OK | `trade_cal` request for SSE 2024-01-02 to 2024-01-05 returned 4 rows. |
| Gemini direct | `GEMINI_API_KEY`, `GEMINI_MODEL` | Disabled by policy | Key exists and was previously tested, but this project must not call Gemini directly. Use Gemini only through Cloubic after Cloubic becomes available. |
| OpenAI direct | `OPENAI_API_KEY` | Not configured | Variable exists but is empty in `.env`; use Cloubic bridge if available. |
| Claude direct | `ANTHROPIC_API_KEY` | Not configured | Variable exists but is empty in `.env`; use Cloubic bridge if available. |
| Cloubic bridge | `CLOUBIC_API_KEY`, `CLOUBIC_BASE_URL`, routed model vars | Not yet usable | With proxy variables disabled, HTTPS still fails during TLS handshake. HTTP reaches the host but returns a `403` page titled `Non-compliance ICP Filing`. The key is not being rejected by the API; requests are not reaching the API service. |

## Source Pool

### Tier 1: Core CCF-A / Mainline Models

| Method | Source | Code source | Reproduction target |
| --- | --- | --- | --- |
| TRA | KDD 2021 | `microsoft/qlib/examples/benchmarks/TRA` | Stock ranking / alpha score prediction |
| DoubleAdapt | KDD 2023 | `SJTU-DMTai/qlib` | Incremental stock trend forecasting under concept drift |
| MASTER | AAAI 2024 | `SJTU-DMTai/qlib` | Market-guided stock Transformer |
| TCTS | ICML 2021 via Qlib model zoo | `microsoft/qlib/examples/benchmarks/TCTS` | Transformer-style time-series alpha baseline |

### Tier 2: Expanded Stock-Specific Or CCF-A/B-Adjacent Candidates

| Method | Source | Code source | Reproduction target |
| --- | --- | --- | --- |
| HIST | Qlib / stock trend forecasting paper | `microsoft/qlib` | Concept-oriented graph baseline |
| AdaRNN | Adaptive time-series forecasting | `microsoft/qlib/examples/benchmarks/ADARNN` | Temporal covariate shift baseline |
| DDG-DA | Predictable concept drift adaptation | `microsoft/qlib` | Distribution generation for drift adaptation |
| THGNN | Financial time-series graph model | TBD | Dynamic heterogeneous graph baseline |
| ESTIMATE | WSDM 2023 candidate | `thanhtrunghuynh93/estimate` | Hypergraph/wavelet stock movement baseline |

### Tier 3: Alpha Mining And Research Automation

| Method/tool | Source | Code source | Reproduction target |
| --- | --- | --- | --- |
| AlphaForge | Formulaic alpha mining | TBD | Generate and combine formulaic alpha factors |
| AlphaPROBE | DAG-guided alpha mining | `gta0804/AlphaPROBE` | Retrieval and evolution of formulaic factors |
| R&D-Agent-Quant | Microsoft RD-Agent quant workflow | `microsoft/RD-Agent` | Automated factor mining/model optimization |
| Alphalens | Quantopian | `quantopian/alphalens` | Factor IC, returns, turnover, group analysis |
| vectorbt | vectorbt | `polakowo/vectorbt` | Fast vectorized factor and strategy sweeps |

## Data Plan: China A Shares

Primary source: Tushare.

Initial universe:

- CSI300 constituents for the first reproducible benchmark.
- Later expansion: CSI500, CSI1000, all A-share common stocks.

Core tables:

| Data | Tushare API | Purpose |
| --- | --- | --- |
| Trading calendar | `trade_cal` | Calendar alignment and open-day filtering |
| Stock metadata | `stock_basic` | Universe construction and listing status |
| Daily OHLCV | `daily` / `pro_bar` | Raw price-volume features |
| Adjust factors | `adj_factor` / `pro_bar` with adjustment | Forward/backward-adjusted prices |
| Daily basic | `daily_basic` | Turnover, market cap, PE/PB and liquidity controls |
| Index daily | `index_daily` | Index prediction and market state features |
| Index weights | `index_weight` | CSI300/CSI500/CSI1000 dynamic universe |
| Suspend data | `suspend_d` if available | Tradability filters |
| Limit prices | `stk_limit` if available | Limit-up/down tradability filters |

Storage layout:

```text
data/raw/tushare/
data/processed/cn_a_share/
data/features/alpha158/
data/features/alpha360/
data/labels/cn_a_share/
data/splits/cn_a_share/
```

## Shared Benchmark Protocol

Start with Qlib-compatible daily-frequency prediction.

Prediction task:

- Cross-sectional stock ranking.
- Label: next-period excess return or future return ranking.
- Horizon: start with 1 day and 5 days; expand to 10/20 days later.

Feature sets:

- `Alpha158`: first shared feature baseline.
- `Alpha360`: second shared feature baseline.
- Paper-specific features only after the shared baseline is reproduced.

Metrics:

- IC
- ICIR
- RankIC
- RankICIR
- Annualized return
- Information ratio
- Max drawdown
- Turnover
- Long-short return if implementation supports it

Splits:

- Train: 2010-01-01 to 2018-12-31
- Validation: 2019-01-01 to 2020-12-31
- Test: 2021-01-01 to latest available complete year

The split can be shifted if Tushare data availability or paper-specific requirements demand it.

## Implementation Phases

### Phase 0: Environment And Data Adapters

1. Add `.env` loading helper under `src/utils/`.
2. Add Tushare client wrapper under `src/data/`.
3. Add data download scripts under `scripts/`.
4. Store raw Tushare responses under `data/raw/tushare/`.
5. Convert daily data into Qlib-compatible binary format or a local parquet panel.

Exit criteria:

- Tushare calendar, CSI300 universe, daily OHLCV, adjusted close, and daily basic data can be downloaded and cached.
- A small CSI300 sample can be transformed into model-ready features and labels.

### Phase 1: Qlib Baseline Reproduction

Clone:

- `external_repos/microsoft__qlib`
- `external_repos/SJTU-DMTai__qlib`

Run initial models:

- LightGBM
- MLP
- LSTM
- Transformer
- TRA
- HIST
- TCTS

Exit criteria:

- One consistent China A-share dataset.
- One table comparing metrics across baseline models.
- Reproducible command/config for every run.

### Phase 2: Core Paper Reproduction

Priority order:

1. TRA
2. MASTER
3. DoubleAdapt
4. TCTS

For each paper:

- Create a project directory under `paper_projects/`.
- Save paper notes, repo analysis, config deltas, and reproduction plan.
- Run on the same China A-share dataset.
- Record original-paper assumptions that differ from our setup.

Exit criteria:

- Each core model has one successful training/evaluation run.
- Results are stored under `experiments/paper_runs/` and summarized under `docs/reports/`.

### Phase 3: Expanded Models

Add:

- AdaRNN
- DDG-DA
- THGNN
- ESTIMATE

Exit criteria:

- Expanded models either run in the shared protocol or have documented blockers.
- Any incompatible data assumptions are made explicit.

### Phase 4: Alpha Factor Mining

Start with factor evaluation infrastructure:

- Alphalens-compatible factor panel.
- vectorbt-based fast return simulation.
- Qlib factor analysis reports.

Then reproduce:

- AlphaPROBE
- AlphaForge if code or implementation details are sufficient
- R&D-Agent-Quant if Cloubic/OpenAI/Claude routing is fixed

Exit criteria:

- Formulaic factors can be generated, evaluated by IC/RankIC/turnover, and compared with model scores.

## LLM Usage Plan

Use LLMs for:

- PDF summarization and method extraction.
- Repo structure analysis.
- Config migration notes.
- Paper-specific implementation gap analysis.
- Academic discussion drafts.

Current status:

- Preferred direct providers: DeepSeek and Doubao.
- Gemini direct is disabled by project policy.
- Claude direct is disabled by project policy.
- Cloubic bridge is not yet usable. Retest without proxy still shows HTTPS TLS handshake failure; HTTP returns `403` with `Non-compliance ICP Filing`.
- Direct OpenAI and Anthropic keys are not configured.
- Gemini and Claude may only be used through Cloubic after the Cloubic API host is reachable.

Recommended next check:

1. Confirm whether `CLOUBIC_BASE_URL` points to the correct API host rather than a host blocked by ICP filing status.
2. Confirm whether Cloubic has an alternate API domain or IP endpoint for API access.
3. Confirm whether the base URL should include `/v1`.
4. Retest bridge routes after the host/scheme is corrected.

Provider policy:

1. Use DeepSeek first for paper summarization, repo analysis, and planning.
2. Use Doubao second if DeepSeek is unavailable or unsuitable.
3. Do not call Gemini directly, even though a direct key exists.
4. Do not call Claude directly.
5. Use Gemini and Claude only through Cloubic once Cloubic access is fixed.

## Immediate Next Steps

1. Clone `microsoft/qlib` and `SJTU-DMTai/qlib`.
2. Implement Tushare download and cache scripts.
3. Build CSI300 daily benchmark dataset.
4. Run LightGBM and one neural baseline to validate the full data-to-metrics loop.
5. Reproduce TRA first because it is CCF-A, stock-specific, and already integrated in Qlib.
