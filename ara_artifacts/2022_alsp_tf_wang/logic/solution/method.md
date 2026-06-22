# Method Summary

## Paper direction

- **Paper ID**: `2022_alsp_tf_wang`
- **Title**: Adaptive Long-Short Pattern Transformer for Stock Investment Selection
- **Task bucket**: stock_investment_selection
- **Venue/status**: IJCAI 2022
- **Source group**: paper_24_matrix

## Local representation

This ARA represents the paper through local benchmark evidence rather than an invented official-code implementation.

Local comparison status: ready_for_metric_level_comparison.

## Abstract or digest

Stock investment selection is a hard issue in the Fintech ﬁeld due to non-stationary dynamics and complex market interdependencies. Existing stud- ies are mostly based on RNNs, which struggle to capture interactive information among ﬁne granular volatility patterns. Besides, they either treat stocks as isolated, or presuppose a ﬁxed graph structure heavily relying on prior domain knowledge. In this paper, we propose a novel Adaptive Long-Short Pattern Transformer (ALSP-TF) for stock ranking in terms of expected returns. Speciﬁcally, we over- come the limitations of canonical self-attention in- cluding context and position agnostic, with two ad- ditional capacities: (i) ﬁne-grained pattern distiller to contextualize queries and keys based on local- ized feature scales, and (ii) time-adaptive modula- tor to let the dependency modeling among pattern pairs sensitive to different time intervals. Attention heads in stacked layers gradually harvest short- and long-term transition traits, spon
