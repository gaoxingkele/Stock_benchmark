# Problem Formulation

## Market And Portfolio Setting

Let \( \mathcal{U}_t \) be the tradable universe at date \(t\). For each asset \(i \in \mathcal{U}_t\), the system observes point-in-time features \(x_{i,t}\) and later evaluates an H-day forward return \(r_{i,t:t+H}\). The current experiments use \(H=5\).

A scoring model produces a cross-sectional score:

```text
s_{i,t}^{(m)} = f_m(x_{i,\le t})
```

where \(m\) indexes a sleeve such as Lingxi, PITNorm, or ReturnFloor-Gate.

For a TopK long-only sleeve, the selected portfolio is:

```text
P_t^{(m,K)} = top_k({s_{i,t}^{(m)} : i in U_t})
```

The portfolio is equal-weighted and rebalanced daily. Net return includes transaction cost:

```text
R_t^{(m)} = gross_return(P_t^{(m)}) - cost_bps * turnover_t^{(m)}
```

The benchmark uses single-side 10 bps cost.

## Sleeve-Level Routing

CASE-Lingxi evaluates routers at the sleeve level. Define a finite approved sleeve set:

```text
A = {lingxi, lingxi_pitnorm, lingxi_pitnorm_gate_return_floor}
```

A router policy chooses:

```text
a_t = pi(z_{\le t-lag}) in A
```

where \(z_{\le t-lag}\) is lagged market and sleeve context. The lag prevents lookahead.

The routed daily return is:

```text
R_t^{pi} = R_t^{(a_t)}
```

or a convex combination if the router is an ensemble. The current CASE-Lingxi production candidates are single-sleeve selectors.

## Static Production Menu

The static menu is a mapping:

```text
M: (market, topk, variant) -> sleeve
```

This menu is the baseline that every adaptive candidate must beat. It is deliberately simple because the empirical question is whether adaptation adds value beyond a robust scenario-specific default.

## Promotion Gate

For candidate \(c\) and static menu \(M\), define scenario set \(S\). Each scenario includes market, TopK, variant, horizon, and cost.

Candidate \(c\) can be promoted only if:

```text
WinRate_metric(c, M, S_oos) >= threshold
```

and no risk constraint is violated.

Current reported win rates use:

```text
WinRate_metric = count(metric(c, s) > metric(M, s)) / |S|
```

for annualized return, Sharpe, and MDD.

Promotion is not based on one metric alone. A drawdown-only improvement may become a research sleeve, but not a production replacement if return and Sharpe deteriorate broadly.

## Validation Echo Trap

Let \(V\) be a validation window and \(O\) be a later out-of-sample window. A validation-only selector chooses:

```text
a^* = argmax_a Sharpe_V(a)
```

The validation echo trap occurs when \(a^*\) fails to beat the static menu on \(O\). In the current evidence, this selector wins 2/16 in 2025, 0/16 in 2026 YTD, and 1/16 in the combined OOS window.

## Agentic Research Layer

An agentic research policy \(g\) does not output trades. It outputs candidate research objects:

```text
c_j = g(memory, literature, failed_paths, evidence)
```

A candidate can be:

1. a new sleeve;
2. a router;
3. a market tag schema;
4. an ablation;
5. an audit or failure hypothesis.

The production action is never \(g\)'s direct output. Production requires the promotion gate:

```text
production(c_j) = Promote(c_j, Evidence_oos)
```

This separation is the main safety and rigor mechanism in CASE-Lingxi.

