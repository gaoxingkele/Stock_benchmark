# Method Summary

## Paper direction

- **Paper ID**: `2025_timefilter_hu`
- **Title**: TimeFilter: Patch-Specific Spatial-Temporal Graph Filtration for Time Series Forecasting
- **Task bucket**: time_series_graph_filter
- **Venue/status**: ICML 2025
- **Source group**: paper_24_matrix

## Local representation

This ARA represents the paper through local benchmark evidence rather than an invented official-code implementation.

Local comparison status: ready_for_metric_level_comparison.

## Abstract or digest

--- page 1 --- TimeFilter: Patch-Specific Spatial-Temporal Graph Filtration for Time Series Forecasting Yifan Hu 1 * Guibin Zhang 2 * Peiyuan Liu 1 * Disen Lan 3 Naiqi Li 1 Dawei Cheng 4 Tao Dai5 Shu-Tao Xia1 Shirui Pan 6 Abstract Time series forecasting methods generally fall into two main categories: Channel Independent (CI) and Channel Dependent (CD) strategies. While CI overlooks important covariate relation- ships, CD captures all dependencies without dis- tinction, introducing noise and reducing gener- alization. Recent advances in Channel Clus- tering (CC) aim to refine dependency model- ing by grouping channels with similar charac- teristics and applying tailored modeling tech- niques. However, coarse-grained clustering strug- gles to capture complex, time-varying interac- tions effectively. To address these challenges, we propose TimeFilter, a GNN-based framework for adaptive and fine-grained dependency mod- eling. After constructing the graph from the input sequence, TimeFilt
