# Small-Cap Parabolic Short High-Winrate Filters, 10Y Test

Created: 2026-07-22

Purpose: keep only filters whose 10-year Yahoo daily-bar backtest win rate was at least 70%.

Important: this is educational research, not a trade recommendation. The universe uses currently listed U.S. small-cap stocks, so survivorship bias is material. Yahoo daily bars do not confirm borrow availability, borrow fees, locates, halts, true intraday sequencing, slippage, or option liquidity.

## 10Y Version Summary

| filter | trades | win_rate_pct | avg_r | total_r | partial_hit_pct | stop_exit_pct | kept |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| profit_model | 179 | 59.78 | 0.077 | 13.797 | 24.02 | 25.70 | no |
| a_grade_profit_subset | 24 | 62.50 | 0.135 | 3.238 | 25.00 | 20.83 | no |
| relaxed_winrate_fade20 | 13 | 84.62 | 0.465 | 6.040 | 38.46 | 0.00 | yes |
| relaxed_winrate_fade15 | 54 | 66.67 | 0.215 | 11.594 | 24.07 | 11.11 | no |

## Filter Kept

Only `relaxed_winrate_fade20` stayed above 70% in the 10-year test.

Rules:

- Universe: U.S.-listed small-cap stocks.
- Market cap: below 2B USD.
- Price: at least 1 USD.
- Setup quality: B-grade or higher, score at least 55.
- Overextension: 1-day return at least 20%, or 3-day return at least 50%, or 5-day return at least 75%, or 10-day return at least 100%.
- Volume: volume ratio at least 3, unless the move is extreme enough to qualify by return.
- Fade condition: setup-day close must be at least 20% below setup-day high.
- Entry: short only if the next regular session trades at or below setup-day low minus 0.02 ATR.
- Initial stop: setup-day high plus 0.10 ATR.
- Risk filter: skip if entry-to-stop risk is above 35% of entry price.
- First cover: cover 50% of the position at +0.5R.
- Runner management: after first cover, move the remaining stop to breakeven.
- Time stop: exit remaining position after 3 trading days.

## Interpretation

`fade20` is now the cleanest high-winrate filter, but the sample is still small at 13 trades over 10 years. That means the win rate is promising, but not enough by itself to trust as an automated live strategy.

`fade15` remains more active and had higher total R than fade20, but its 10-year win rate fell below the 70% threshold. It may still be useful as a broader watchlist filter, while `fade20` can be used as the stricter execution filter.

## Practical Use

Recommended split:

- `fade15`: watchlist filter.
- `fade20`: execution-quality filter.
- manual/broker checks: required before any short sale or put option order.

## Source Outputs

- Main report: `smallcap_short_10y_backtest.md`
- Summary CSV: `smallcap_short_10y/version_comparison_summary.csv`
- Trade CSV: `smallcap_short_10y/version_comparison_trades.csv`
- Yearly CSV: `smallcap_short_10y/version_yearly_summary.csv`
- 70%+ filters CSV: `smallcap_short_10y/high_winrate_filters.csv`
