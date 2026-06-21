# Stock Benchmark Task Roadmap

Date: 2026-06-19

## Objective

Build a China A-share benchmark for stock/index trend prediction and alpha factor mining, covering recent CCF-A/B papers, strong journal candidates, and high-quality open-source repositories.

## Global Constraints

### Data

- Primary market: China A shares.
- Primary data provider: Tushare.
- First universe: CSI300.
- Later universes: CSI500, CSI1000, all A-share common stocks.

### LLM

- Preferred provider: DeepSeek, using the latest configured model version.
- Secondary provider: Doubao, using the latest configured model version.
- Do not call Gemini directly.
- Do not call Claude directly.
- Gemini and Claude can only be called through Cloubic.
- Cloubic is currently unavailable, so Gemini/Claude-dependent workflows are blocked.

### Evaluation

- Use a shared protocol before paper-specific variants.
- Start with Qlib-compatible daily-frequency ranking/alpha prediction.
- First metrics: IC, ICIR, RankIC, RankICIR, annualized return, information ratio, max drawdown, turnover.

## Task Tree

### 0. Preparation

- [x] Create `Stock_benchmark` directory structure.
- [x] Create paper registry.
- [x] Create repository candidate registry.
- [x] Create China A-share reproduction plan.
- [x] Check `.env` and `.env.cloubic` without exposing secrets.
- [x] Verify Tushare token.
- [x] Verify Gemini direct once, then disable direct Gemini by policy.
- [x] Diagnose Cloubic access failure.
- [x] Record LLM provider policy.
- [x] Create this task roadmap.

### 1. Source Collection

- [ ] Continue CCF-A/B and journal paper search.
- [ ] Verify venues for secondary candidates.
- [ ] Download PDFs into `papers/raw/`.
- [x] Download verified PDFs for TRA, DoubleAdapt, MASTER, TCTS, HIST, and AdaRNN.
- [ ] Retry or replace DDG-DA PDF source.
- [x] Verify TCTS paper URL.
- [ ] Extract text into `papers/extracted/`.
- [x] Extract text for TRA, DoubleAdapt, MASTER, TCTS, HIST, and AdaRNN.
- [ ] Fill BibTeX into `papers/metadata/references.bib`.
- [ ] Create one `paper_projects/*` directory per selected paper.
- [x] Create `paper_projects/2021_tra_lin`.
- [x] Create `paper_projects/2024_master_li`.
- [x] Create `paper_projects/2023_doubleadapt_zhao`.
- [x] Create `paper_projects/2021_tcts_wu`.
- [ ] Clone priority repositories into `external_repos/`.
- [x] Clone `microsoft/qlib`.
- [x] Clone `SJTU-DMTai/qlib`.

Priority repositories:

1. `microsoft/qlib`
2. `SJTU-DMTai/qlib`
3. `quantopian/alphalens`
4. `polakowo/vectorbt`
5. `gta0804/AlphaPROBE`
6. `thanhtrunghuynh93/estimate`

### 2. Tushare Data Pipeline

- [x] Implement `.env` loading helper.
- [x] Implement Tushare API wrapper.
- [x] Download sample trading calendar.
- [x] Download sample stock metadata.
- [ ] Download CSI300 constituents and weights.
- [x] Download sample CSI300 constituents and weights.
- [x] Download sample daily OHLCV.
- [x] Download sample adjustment factors.
- [x] Download sample daily basic data.
- [x] Download sample index daily data.
- [x] Build sample raw cache under `data/raw/tushare/sample/`.
- [x] Build processed panel under `data/processed/cn_a_share/`.
- [x] Build sample processed panel under `data/processed/cn_a_share/csi300_smoke/`.
- [x] Build sample Qlib-friendly per-symbol CSV files.
- [x] Implement by-date Tushare downloader for scalable CSI300 data collection.
- [x] Implement fragment-resumable by-date Tushare downloader for long windows.
- [x] Validate fragment downloader with two-day Tushare smoke and panel build.
- [x] Complete formal CSI300 2018-2024 fragment download.
- [x] Start formal CSI300 2018-2024 fragment download and record progress.
- [x] Build 300-symbol CSI300 by-date smoke panel.
- [x] Convert 300-symbol CSI300 by-date smoke panel to Qlib bin.
- [ ] Add tradability filters for suspension and limit-up/down when available.

### 3. Shared Benchmark Protocol

- [x] Define benchmark config schema.
- [x] Define CSI300 smoke universe config.
- [x] Define CSI300 smoke train/test split.
- [x] Implement reusable forward-return label generation.
- [x] Generate CSI300 smoke H1 and H5 label files.
- [x] Generate formal CSI300 2018-2024 H1 and H5 label files.
- [x] Validate CSI300 smoke universe, split, and label counts.
- [x] Define formal long-history CSI300 train/valid/test split.
- [x] Implement Alpha158-compatible feature generation.
- [x] Implement Alpha360-compatible feature generation.
- [ ] Validate native Qlib Alpha158/Alpha360 handlers after Qlib runtime is available.
- [x] Implement basic metric summary aggregation.
- [ ] Implement advanced cross-run metric aggregation and reporting.
- [x] Implement smoke experiment result table format.

### 4. Baseline Run

- [x] Clone and inspect `microsoft/qlib`.
- [x] Convert China A-share data to Qlib-compatible format.
- [x] Convert CSI300 smoke CSV to Qlib bin format.
- [x] Run LightGBM smoke baseline on processed panel.
- [x] Run 300-symbol CSI300 by-date factor smoke baseline.
- [x] Run 300-symbol CSI300 by-date LightGBM smoke baseline.
- [x] Run config-driven 300-symbol CSI300 by-date LightGBM smoke baseline.
- [x] Run formal CSI300 2018-2024 LightGBM H1/H5 baseline without Qlib runtime.
- [x] Run formal CSI300 2018-2024 Qlib DataHandler direct LightGBM H1 baseline.
- [x] Materialize China A-share H1/H5 paper-inspired proxy runs for all 24 target papers.
- [x] Run CSI300 H5 Top30 trading validation for selected top paper directions and proxy controls with 10 bps cost, turnover, drawdown, yearly stability, and industry/size-neutral checks.
- [x] Generate and evaluate industry/size-neutralized basic factors.
- [x] Summarize first runnable smoke results.
- [ ] Run formal Qlib LightGBM workflow.
- [x] Prepare CSI300 smoke Qlib LightGBM workflow config.
- [x] Validate Qlib smoke workflow file prerequisites.
- [x] Prepare formal CSI300 2018-2024 Qlib LightGBM workflow config.
- [x] Add NumPy-only first-run paper-model baseline script for blocked Qlib/PyTorch runtime.
- [ ] Run MLP.
- [ ] Run LSTM or GRU.
- [ ] Run Transformer.
- [x] Confirm smoke data-to-metrics loop.
- [x] Compile downloaded papers into ARA artifacts and validate each independently.

### 5. Core Paper Reproduction

Priority order:

1. TRA
2. MASTER
3. DoubleAdapt
4. TCTS

Per paper:

- [x] Create project directory from `_template`.
- [x] Download paper PDF.
- [x] Write paper notes.
- [x] Analyze official/community repo.
- [x] Document reproduction assumptions.
- [x] Create China A-share smoke config.
- [x] Create China A-share formal config.
- [x] Run first formal paper-inspired experiment.
- [x] Record first formal paper-inspired results.
- [x] Write first-run reproduction summary.
- [ ] Run official/fork implementation after PyTorch/Qlib runtime is available.
- [ ] Write official reproduction summary.

Current note status:

- [x] TRA paper notes drafted.
- [x] MASTER paper notes drafted.
- [x] DoubleAdapt paper notes drafted.
- [x] TCTS paper notes drafted after source verification.

### 6. Expanded Models

- [ ] HIST
- [ ] AdaRNN
- [ ] DDG-DA
- [ ] THGNN
- [ ] ESTIMATE

For each:

- [ ] Verify venue/source.
- [ ] Verify code availability.
- [ ] Decide whether it fits shared protocol.
- [ ] Run or document blocker.

### 7. Alpha Factor Mining

- [x] Build smoke factor panel format.
- [x] Add factor IC/RankIC validation.
- [x] Add smoke turnover and decay validation.
- [ ] Evaluate Alphalens integration.
- [ ] Evaluate vectorbt integration.
- [ ] Reproduce AlphaPROBE if repo is mature enough.
- [ ] Reproduce AlphaForge if implementation details are sufficient.
- [ ] Revisit R&D-Agent-Quant after LLM routing is stable.

Current factor status:

- [x] Generate 15 basic price-volume/valuation factors.
- [x] Evaluate basic factors with IC/RankIC on 300-symbol CSI300 by-date smoke data.
- [x] Add industry/size neutralization.
- [x] Add factor turnover and decay reports.

### 8. Reports

- [ ] Write paper-by-paper method summaries.
- [ ] Write repo review summaries.
- [ ] Write benchmark protocol report.
- [ ] Write baseline result report.
- [ ] Write core model comparison.
- [ ] Write China A-share findings and limitations.
- [x] Create 24-paper target matrix for original-vs-China experiment tracking.
- [x] Normalize original-paper metric rows for all 24 target papers.
- [x] Build 24-paper original-vs-China comparison matrix with all target papers ready for metric-level comparison.
- [x] Generate trading-guidance conclusion report from the 24-paper comparison.
- [x] Generate acquisition queue for the 18 target papers without comparable local evidence.
- [x] Download and extract 15 additional target-paper PDFs from the 18-paper queue.
- [x] Add target-24 PDF source table and downloader script.
- [ ] Resolve command-line PDF download failures for CI-STHPAN and DeepTrader; MDGNN is now downloaded from arXiv.
- [x] Transcribe remaining original-paper tables for all currently extracted target papers with detected table mentions.
- [ ] Handle DoubleEnsemble and DiffsFormer table extraction separately because standard `Table N` text was not detected.
- [x] Normalize original-paper experiment tables for the remaining target papers using local text or browser-readable PDF evidence.
- [ ] Run or bind China A-share comparison runs for the remaining 18 target papers.

## Current Blockers

- Cloubic API host is not reachable from command line. HTTPS fails at TLS handshake; HTTP returns `403 Non-compliance ICP Filing`.
- Direct Gemini/Claude calls are disallowed by project policy.
- Some expanded paper venues still need verification.
- Native Qlib/PyTorch workflow execution still needs a stable runtime path for official/fork model reproduction.
- AAAI/OJS command-line PDF downloads currently fail for CI-STHPAN, MDGNN, and DeepTrader with remote TLS/connection close errors, although the paper pages are reachable in browser-style access.

## Next Execution Goals

The first execution goal has been completed: both Qlib repositories were cloned, the Tushare data pipeline was built, CSI300 smoke/formal datasets were prepared, and first baselines were run.

Next work should prioritize:

1. Run the formal native Qlib LightGBM workflow once the runtime is stable.
2. Validate native Qlib Alpha158/Alpha360 handlers against the generated formal dataset.
3. Implement advanced cross-run metric aggregation and reporting.
4. Fill `papers/metadata/references.bib` for the downloaded paper corpus.
5. Expand official/fork reproduction beyond first NumPy-only paper-inspired runs.
6. Use `papers/metadata/paper_target_24.csv`, `papers/metadata/original_experiment_results.csv`, and `experiments/summary/paper_24_comparison_matrix.csv` as the control tables for the 24-paper original-vs-China comparison objective.
