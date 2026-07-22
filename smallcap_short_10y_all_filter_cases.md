# Small-Cap Parabolic Short 10Y All Filter Cases

Created: 2026-07-22

Purpose: summarize all four small-cap parabolic short filter cases tested over 10 years, including each filter's logic, result, and practical interpretation.

Important: this is educational research, not a trade recommendation. The backtest uses Yahoo daily bars and the current U.S.-listed small-cap universe. It does not confirm borrow availability, borrow fees, locates, halts, real intraday sequencing, slippage, commissions, forced buy-ins, or option liquidity. Because the universe is based on currently listed stocks, survivorship bias is material.

## Executive Summary

| case | trades | win_rate_pct | avg_r | total_r | partial_hit_pct | stop_exit_pct | role |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| profit_model | 179 | 59.78 | 0.077 | 13.801 | 24.02 | 25.70 | Broad profit-seeking baseline |
| a_grade_profit_subset | 24 | 62.50 | 0.135 | 3.239 | 25.00 | 20.83 | Higher-quality subset |
| relaxed_winrate_fade20 | 13 | 84.62 | 0.464 | 6.035 | 38.46 | 0.00 | Strict execution-quality filter |
| relaxed_winrate_fade15 | 54 | 66.67 | 0.215 | 11.594 | 24.07 | 11.11 | Broader watchlist filter |

Main conclusion:

- `relaxed_winrate_fade20` is the only filter above 70% win rate in the 10-year test.
- `relaxed_winrate_fade15` has more trades and higher total R, but its win rate falls below 70%.
- `profit_model` makes the most total R, but with a much lower win rate.
- `a_grade_profit_subset` improves quality versus the broad baseline, but not enough to reach 70% win rate.

## Shared Setup Logic

All four cases start from the same small-cap parabolic short idea:

- Find U.S.-listed small-cap stocks.
- Market cap below 2B USD.
- Price at least 1 USD.
- Abnormal price expansion:
  - 1-day return at least 20%, or
  - 3-day return at least 50%, or
  - 5-day return at least 75%, or
  - 10-day return at least 100%.
- Abnormal activity:
  - volume ratio at least 3, unless the price move is extreme enough to qualify by return.
- Entry is never automatic on the setup day.
- Short entry only happens if the next regular session trades below the setup-day low minus an ATR buffer.
- Skip trades where the distance from entry to stop is too wide.

## Case 1: profit_model

Purpose:

This is the broad baseline. It tries to capture more opportunities and maximize total R, accepting a lower win rate.

Rules:

- Minimum score: 55.
- Grade: B or higher.
- Entry: setup-day low minus 0.02 ATR.
- Stop: setup-day high plus 0.10 ATR.
- Max entry-to-stop risk: 35% of entry.
- Partial cover: 50% at +1R.
- Runner stop: breakeven after the first cover.
- Max hold: 5 trading days.

10-year result:

- Trades: 179.
- Win rate: 59.78%.
- Average R: +0.077R.
- Total R: +13.801R.
- Stop-out rate: 25.70%.

Interpretation:

This version produced the highest total R, but the win rate is below the user's 70% target. It is useful as a broad research baseline, but it is probably too noisy for direct automated execution.

Practical role:

- Use as a broad discovery model.
- Do not use as the final execution filter if the goal is high hit rate.

## Case 2: a_grade_profit_subset

Purpose:

This case keeps only the highest-scoring A-grade setups from the profit model.

Rules:

- Minimum score: 75.
- Grade: A only.
- Entry: setup-day low minus 0.02 ATR.
- Stop: setup-day high plus 0.10 ATR.
- Max entry-to-stop risk: 35% of entry.
- Partial cover: 50% at +1R.
- Runner stop: breakeven after the first cover.
- Max hold: 5 trading days.

10-year result:

- Trades: 24.
- Win rate: 62.50%.
- Average R: +0.135R.
- Total R: +3.239R.
- Stop-out rate: 20.83%.

Interpretation:

A-grade filtering improves selectivity, average R, and stop-out rate compared with the broad baseline, but it does not reach the 70% win-rate threshold in the 10-year test.

Practical role:

- Use as a priority flag.
- A-grade alone is not enough as a final execution rule.
- It can be combined with fade filters for stricter confirmation.

## Case 3: relaxed_winrate_fade20

Purpose:

This is the strict high-winrate execution filter. It requires the stock to have already failed meaningfully from the setup-day high before considering a next-day breakdown short.

Rules:

- Minimum score: 55.
- Grade: B or higher.
- Fade condition: setup-day close must be at least 20% below setup-day high.
- Entry: setup-day low minus 0.02 ATR.
- Stop: setup-day high plus 0.10 ATR.
- Max entry-to-stop risk: 35% of entry.
- Partial cover: 50% at +0.5R.
- Runner stop: breakeven after the first cover.
- Max hold: 3 trading days.

10-year result:

- Trades: 13.
- Win rate: 84.62%.
- Average R: +0.464R.
- Total R: +6.035R.
- Stop-out rate: 0.00%.

Interpretation:

This is the cleanest high-winrate filter in the 10-year test. The logic is stricter: the stock must already show a major intraday failure from the high, and profit is taken faster at +0.5R.

The main weakness is sample size. Only 13 trades over 10 years is promising but thin. It should be treated as an execution-quality gate, not as enough evidence for fully autonomous live trading.

Practical role:

- Best candidate for the final execution filter.
- Use only after borrow, fee, news, filing, halt, spread, and liquidity checks pass.
- Better suited to manual approval or paper trading before live automation.

## Case 4: relaxed_winrate_fade15

Purpose:

This is the broader win-rate model. It catches more setups than fade20 by allowing a smaller failure from the high.

Rules:

- Minimum score: 55.
- Grade: B or higher.
- Fade condition: setup-day close must be at least 15% below setup-day high.
- Entry: setup-day low minus 0.02 ATR.
- Stop: setup-day high plus 0.10 ATR.
- Max entry-to-stop risk: 35% of entry.
- Partial cover: 50% at +0.5R.
- Runner stop: breakeven after the first cover.
- Max hold: 3 trading days.

10-year result:

- Trades: 54.
- Win rate: 66.67%.
- Average R: +0.215R.
- Total R: +11.594R.
- Stop-out rate: 11.11%.

Interpretation:

This case gives a better trade count and higher total R than fade20, but the win rate is below 70% over 10 years. It is still a useful filter because it captures a wider set of weakening parabolic names.

Practical role:

- Best as a watchlist filter.
- Use it to find candidates worth monitoring.
- Require fade20, intraday VWAP loss, opening range breakdown, borrow availability, and manual review before execution.

## Recommended Workflow

Use the filters in layers:

1. `profit_model`: broad research universe.
2. `fade15`: active watchlist filter.
3. `fade20`: execution-quality filter.
4. Broker/manual checks: final gate before any order.

The practical workflow should be:

- Scan with `fade15`.
- Promote to execution candidate only if `fade20` also passes.
- Create a trade ticket with entry, stop, partial cover, runner stop, time stop, and position size.
- Confirm borrow availability and borrow fee.
- Check SSR, halt risk, filings, news quality, and option availability.
- Require manual approval before live order placement.

## Automation Notes

For short-sale automation, Yahoo data is not enough. The system needs:

- Broker API access.
- Real-time or near-real-time market data.
- Borrow availability.
- Borrow fee.
- Locate status.
- Short sale restriction status.
- Halt status.
- Bid, ask, spread, and preferably market depth.
- Bracket or OCO order support.
- Position sizing by fixed R.
- Max daily loss control.
- Full order, fill, cancel, and error logs.

For put-option automation, the system also needs:

- Option chain data.
- Expiration dates.
- Strike list.
- Bid, ask, mid, and spread.
- Option volume.
- Open interest.
- Implied volatility.
- Greeks.
- Liquidity rules.
- Premium risk limit.
- Exit rules based on both underlying price and option price.

## Source Files

- Main 10Y report: `smallcap_short_10y_backtest.md`
- Summary CSV: `smallcap_short_10y/version_comparison_summary.csv`
- Trade CSV: `smallcap_short_10y/version_comparison_trades.csv`
- Yearly CSV: `smallcap_short_10y/version_yearly_summary.csv`
- 10Y script: `compare_smallcap_short_versions_10y.py`
