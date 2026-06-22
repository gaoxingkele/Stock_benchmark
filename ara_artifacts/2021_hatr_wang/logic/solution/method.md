# Method Summary

## Paper direction

- **Paper ID**: `2021_hatr_wang`
- **Title**: Hierarchical Adaptive Temporal-Relational Modeling for Stock Trend Prediction
- **Task bucket**: stock_trend_temporal_relational
- **Venue/status**: IJCAI 2021
- **Source group**: paper_24_matrix

## Local representation

This ARA represents the paper through local benchmark evidence rather than an invented official-code implementation.

Local comparison status: ready_for_metric_level_comparison.

## Abstract or digest

Stock trend prediction is a challenging task due to the non-stationary dynamics and complex mar- ket dependencies. Existing methods usually regard each stock as isolated for prediction, or simply de- tect their correlations based on a ﬁxed predeﬁned graph structure. Genuinely, stock associations stem from diverse aspects, the underlying relation sig- nals should be implicit in comprehensive graphs. On the other hand, the RNN network is mainly used to model stock historical data, while is hard to capture ﬁne-granular volatility patterns implied in different time spans. In this paper, we propose a novel Hierarchical Adaptive Temporal-Relational Network (HATR) to characterize and predict stock evolutions. By stacking dilated causal convolutions and gating paths, short- and long-term transition features are gradually grasped from multi-scale lo- cal compositions of stock trading sequences. Par- ticularly, a dual attention mechanism with Hawkes process and target-speciﬁc query is proposed t
