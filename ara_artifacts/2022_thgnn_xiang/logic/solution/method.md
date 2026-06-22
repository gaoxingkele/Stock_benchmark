# Method Summary

## Paper direction

- **Paper ID**: `2022_thgnn_xiang`
- **Title**: Temporal and Heterogeneous Graph Neural Network for Financial Time Series Prediction
- **Task bucket**: stock_trend_graph
- **Venue/status**: CIKM 2022
- **Source group**: paper_24_matrix

## Local representation

This ARA represents the paper through local benchmark evidence rather than an invented official-code implementation.

Local comparison status: ready_for_metric_level_comparison.

## Abstract or digest

The price movement prediction of stock market has been a classical yet challenging problem, with the attention of both economists and computer scientists. In recent years, graph neural network has significantly improved the prediction performance by employing deep learning on company relations. However, existing relation graphs are usually constructed by handcraft human labeling or na- ture language processing, which are suffering from heavy resource requirement and low accuracy. Besides, they cannot effectively re- sponse to the dynamic changes in relation graphs. Therefore, in this paper, we propose a temporal and heterogeneous graph neural network-based (THGNN) approach to learn the dynamic relations among price movements in financial time series. In particular, we first generate the company relation graph for each trading day according to their historic price. Then we leverage a transformer encoder to encode the price movement information into temporal representations. Afterward, w
