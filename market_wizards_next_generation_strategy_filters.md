# Market Wizards: The Next Generation Strategy Filters

Created: 2026-07-25

Purpose: summarize the four trader styles selected from *Unknown Market Wizards / Market Wizards: The Next Generation* research and translate them into practical strategy-filter ideas.

Important: this is an educational research memo, not investment advice. The filters below are simplified interpretations for systematic research. The actual traders use discretion, experience, risk control, and market context that cannot be fully captured by simple rules.

## Selected Traders

We excluded:

- Pure small-cap short specialists.
- Pure option-selling specialists.

The remaining four research candidates:

| trader | market | core style | systematic fit |
| --- | --- | --- | --- |
| Jason Berry | Futures | Intraday futures trading around volatility, momentum, timing, and tight risk | High |
| Lance Breitstein | Equities | Catalyst-driven momentum, relative strength, tape reading, and intraday reaction | Medium-high |
| Kelvin Chiu | Commodities / macro | Fundamental commodity themes combined with price confirmation and risk control | Medium |
| Rick Bandazian Jr. | Event-driven equities | Merger arbitrage and deal-risk/event-driven positioning | Medium |

## 1. Jason Berry

### Plain-English Summary

Jason's style is closest to short-term futures trading. He looks for liquid futures markets where price is already moving, then waits for a clean intraday setup with defined risk. The main idea is not to predict a huge move, but to repeatedly take trades where the market gives a favorable short-term opportunity and losses can be kept small.

### Strategy DNA

- Liquid futures only.
- Intraday focus.
- Directional momentum or reversal setups.
- Time-of-day awareness.
- Small predefined losses.
- Fast trade management.
- Avoid forcing trades when conditions are unclear.

### Filter Ideas

Candidate markets:

- ES: S&P 500 futures.
- NQ: Nasdaq futures.
- CL: crude oil futures.
- ZB / ZN: Treasury futures.

Core filters:

- Market is liquid during regular active session.
- Volatility is above a minimum threshold.
- Price shows clear directional pressure or failed breakout.
- Entry is near a defined level, not in the middle of noise.
- Stop is close enough to keep risk controlled.
- Trade is skipped if spread, volatility, or signal quality is poor.

Backtest version already explored:

- 5-minute Yahoo futures data.
- ES and NQ performed best in the initial 60-day test.
- Later version added partial profit, breakeven move, and runner exit.

### Possible Automation

Best fit for automation among the four.

Required data:

- Real-time futures data.
- Minute bars or tick data.
- Broker API.
- Session calendar.
- Volatility filter.
- Stop/target/OCO order support.

## 2. Lance Breitstein

### Plain-English Summary

Lance's style is equity trading based on catalysts and market reaction. The key is not simply "good news means buy" or "bad news means short." The important part is how the stock reacts compared with expectations, volume, the overall market, and similar stocks. Strong stocks that hold up after good catalysts can become long candidates. Weak stocks that fail after excitement can become short candidates.

### Strategy DNA

- Catalyst first.
- Relative strength or relative weakness.
- Volume expansion.
- Intraday tape and reaction.
- Focus on stocks where other traders are paying attention.
- Cut quickly when the expected reaction does not appear.

### Strategy Filter

Candidate stocks:

- Liquid U.S. equities.
- Usually active large-cap or mid-cap names for cleaner execution.
- Smaller names can be used only when liquidity is acceptable.

Core long filters:

- Fresh catalyst: earnings, guidance, analyst action, product news, sector news.
- Gap or strong early move.
- Relative strength versus market and sector.
- Volume above normal.
- Holds VWAP or key opening range.
- Pullbacks are bought instead of collapsing.

Core short filters:

- Bad reaction after good news.
- Good news fails to hold.
- Stock loses VWAP.
- Breaks opening range low.
- Weak versus market and peers.
- Volume confirms selling pressure.

Backtest version already explored:

- Yahoo 60-day equity test on liquid large-cap names.
- First pass was weak overall, but TSLA and META showed better behavior in limited tests.
- Lance's style likely needs better catalyst/news tagging and intraday data than simple price filters.

### Possible Automation

Partially automatable.

Required data:

- Real-time prices.
- Intraday VWAP and opening range.
- Sector/peer relative strength.
- News/catalyst feed.
- Earnings calendar.
- Analyst/news classification.
- Manual review layer is strongly recommended.

## 3. Kelvin Chiu

### Plain-English Summary

Kelvin's style is more macro and commodity-oriented. The basic idea is to understand a fundamental pressure in a market, such as supply/demand imbalance, inventory stress, weather impact, policy change, or macro flow, and then wait for price to confirm that the thesis is starting to work.

### Strategy DNA

- Commodity and macro themes.
- Fundamental supply/demand view.
- Patience before entry.
- Price confirmation.
- Risk control when the thesis is wrong.
- Avoid trading only from opinion.

### Strategy Filter

Candidate markets:

- Crude oil.
- Natural gas.
- Agricultural commodities.
- Metals.
- Commodity-linked ETFs or futures.

Core filters:

- Fundamental theme exists.
- Market is near an important price level.
- Trend or breakout confirms the thesis.
- Volatility is acceptable for the account size.
- Stop can be placed at a logical invalidation point.
- Position size is adjusted to contract volatility.

Example systematic translation:

- Identify commodity trend regime.
- Confirm with moving average slope or breakout.
- Require volatility-adjusted stop.
- Enter only when price confirms thesis direction.
- Exit when trend fails or risk limit is hit.

### Possible Automation

Medium fit.

Required data:

- Futures or ETF price data.
- Commitment of Traders data if used.
- Inventory reports.
- Calendar of commodity reports.
- Macro/event calendar.
- Volatility-adjusted sizing.

## 4. Rick Bandazian Jr.

### Plain-English Summary

Rick's style is event-driven, especially merger arbitrage. Instead of betting mainly on chart patterns, the trade depends on whether a corporate event will complete as expected. If a company is being acquired, the stock may trade below the deal price. The trader studies whether the deal will close, how long it may take, and what the downside is if it breaks.

### Strategy DNA

- Event-driven equity trading.
- Deal spread analysis.
- Probability and downside estimation.
- Legal/regulatory risk.
- Time-to-close matters.
- Position sizing depends on deal risk.

### Strategy Filter

Candidate stocks:

- Announced mergers.
- Tender offers.
- Acquisition targets.
- Special situations with clear event terms.

Core filters:

- Confirmed announced deal.
- Clear deal price.
- Current price below deal price.
- Spread is large enough to compensate for risk.
- Expected close date is known or estimable.
- Regulatory risk is acceptable.
- Financing risk is acceptable.
- Downside if deal breaks is estimated.

Example metrics:

- Deal spread percentage.
- Annualized spread.
- Time to expected close.
- Break price downside.
- Risk-adjusted expected value.

### Possible Automation

Medium fit for screening, lower fit for full automation.

Required data:

- M&A announcement feed.
- SEC filings.
- Deal terms.
- Current price.
- Expected close date.
- Regulatory status.
- Financing status.
- Manual legal/news review.

## Comparison

| trader | best use | weakest point | best next step |
| --- | --- | --- | --- |
| Jason Berry | Intraday futures system | Needs good intraday data | Improve ES/NQ test with better data and realistic execution |
| Lance Breitstein | Catalyst equity scanner | Needs news classification and discretionary context | Add catalyst/news feed and VWAP/opening range filters |
| Kelvin Chiu | Macro/commodity swing filter | Fundamental data is harder to automate | Build commodity regime dashboard |
| Rick Bandazian Jr. | Event-driven deal scanner | Legal/deal risk is hard to automate | Build merger spread watchlist, not auto-execution |

## Recommended Research Order

1. Jason Berry
   - Most systematic.
   - Futures are liquid.
   - Clear risk and execution logic.

2. Lance Breitstein
   - Good candidate for scanners.
   - Needs better catalyst data.
   - Useful for both long and short equity setups.

3. Small-cap parabolic short adaptation
   - Not one of the four remaining traders, but related to the user's preferred short strategy.
   - Already tested with 2-year and 10-year filters.

4. Kelvin Chiu
   - Build after futures/stock filters because it needs fundamental commodity data.

5. Rick Bandazian Jr.
   - Best as a watchlist and research dashboard, not direct automated trading.

## Current Project Status

Completed research files:

- `smallcap_short_10y_all_filter_cases.md`
- `smallcap_short_10y_backtest.md`
- `smallcap_short_high_winrate_filters_10y.md`
- `compare_smallcap_short_versions_10y.py`

Current best-developed strategy:

- Small-cap parabolic short filter.
- 10-year test completed.
- `fade15` works better as a watchlist.
- `fade20` is stricter and had the highest win rate, but sample size is small.

Next recommended implementation:

- Add fundamental filters to the small-cap short model:
  - net income loss,
  - operating cash flow loss,
  - low cash runway,
  - dilution filings,
  - going-concern language,
  - recent S-1/S-3/424B/ATM/warrant filings.

