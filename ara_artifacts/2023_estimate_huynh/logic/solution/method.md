# Method Summary

## Paper direction

- **Paper ID**: `2023_estimate_huynh`
- **Title**: Efficient Integration of Multi-Order Dynamics and Internal Dynamics in Stock Movement Prediction
- **Task bucket**: stock_movement_hypergraph
- **Venue/status**: WSDM 2023
- **Source group**: paper_24_matrix

## Local representation

This ARA represents the paper through local benchmark evidence rather than an invented official-code implementation.

Local comparison status: ready_for_metric_level_comparison.

## Abstract or digest

Advances in deep neural network (DNN) architectures have en- abled new prediction techniques for stock market data. Unlike other multivariate time-series data, stock markets show two unique characteristics: (i) multi-order dynamics, as stock prices are affected by strong non-pairwise correlations (e.g., within the same industry); and (ii) internal dynamics, as each individual stock shows some par- ticular behaviour. Recent DNN-based methods capture multi-order dynamics using hypergraphs, but rely on the Fourier basis in the convolution, which is both inefficient and ineffective. In addition, they largely ignore internal dynamics by adopting the same model for each stock, which implies a severe information loss. In this paper, we propose a framework for stock movement pre- diction to overcome the above issues. Specifically, the framework includes temporal generative filters that implement a memory- based mechanism onto an LSTM network in an attempt to learn individual patterns per stock
