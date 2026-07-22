# Small-Cap Parabolic Short 10Y Backtest

This expands the prior 2-year Yahoo daily-bar test to 10 years.

Important limitations:

- Universe is based on currently listed U.S. small-cap stocks, so survivorship bias is material.
- Yahoo daily bars cannot verify borrow availability, borrow fees, locates, halts, or real intraday event order.
- Results are in R units, not account return.
- This is research output, not a trade recommendation.

## Summary

| version | trades | win_rate_pct | avg_r | median_r | total_r | best_r | worst_r | partial_hit_pct | stop_exit_pct | raw_setups | scored_setups | min_score | trigger_atr_buffer | hold_days | partial_r | fade_filter |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| profit_model | 179 | 59.78 | 0.08 | 0.18 | 13.80 | 1.92 | -1.00 | 24.02 | 25.70 | 5226 | 2004 | 55 | 0.02 | 5 | 1.00 |  |
| a_grade_profit_subset | 24 | 62.50 | 0.14 | 0.23 | 3.24 | 1.39 | -1.00 | 25.00 | 20.83 | 5317 | 569 | 75 | 0.02 | 5 | 1.00 |  |
| relaxed_winrate_fade20 | 13 | 84.62 | 0.46 | 0.40 | 6.04 | 1.35 | -0.08 | 38.46 | 0.00 | 5330 | 664 | 55 | 0.02 | 3 | 0.50 | -20.0 |
| relaxed_winrate_fade15 | 54 | 66.67 | 0.21 | 0.28 | 11.59 | 1.35 | -1.00 | 24.07 | 11.11 | 5314 | 884 | 55 | 0.02 | 3 | 0.50 | -15.0 |

## Filters With Win Rate At Least 70%

| version | trades | win_rate_pct | avg_r | median_r | total_r | best_r | worst_r | partial_hit_pct | stop_exit_pct | raw_setups | scored_setups | min_score | trigger_atr_buffer | hold_days | partial_r | fade_filter |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| relaxed_winrate_fade20 | 13 | 84.62 | 0.46 | 0.40 | 6.04 | 1.35 | -0.08 | 38.46 | 0.00 | 5330 | 664 | 55 | 0.02 | 3 | 0.50 | -20.0 |

## Yearly Summary

| version | year | trades | win_rate_pct | avg_r | total_r | partial_hit_pct | stop_exit_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| a_grade_profit_subset | 2017 | 2 | 50.00 | -0.25 | -0.50 | 50.00 | 50.00 |
| a_grade_profit_subset | 2018 | 2 | 0.00 | -0.51 | -1.02 | 0.00 | 50.00 |
| a_grade_profit_subset | 2019 | 1 | 100.00 | 0.41 | 0.41 | 0.00 | 0.00 |
| a_grade_profit_subset | 2020 | 3 | 66.67 | 0.16 | 0.49 | 0.00 | 0.00 |
| a_grade_profit_subset | 2021 | 1 | 0.00 | -1.00 | -1.00 | 0.00 | 100.00 |
| a_grade_profit_subset | 2023 | 5 | 80.00 | 0.48 | 2.39 | 40.00 | 0.00 |
| a_grade_profit_subset | 2024 | 2 | 100.00 | 0.60 | 1.20 | 50.00 | 0.00 |
| a_grade_profit_subset | 2025 | 5 | 60.00 | 0.00 | 0.01 | 20.00 | 20.00 |
| a_grade_profit_subset | 2026 | 3 | 66.67 | 0.42 | 1.26 | 33.33 | 33.33 |
| profit_model | 2016 | 1 | 100.00 | 0.24 | 0.24 | 0.00 | 0.00 |
| profit_model | 2017 | 5 | 60.00 | 0.23 | 1.18 | 40.00 | 20.00 |
| profit_model | 2018 | 9 | 55.56 | 0.14 | 1.27 | 44.44 | 33.33 |
| profit_model | 2019 | 8 | 50.00 | -0.14 | -1.14 | 0.00 | 25.00 |
| profit_model | 2020 | 28 | 67.86 | 0.12 | 3.38 | 32.14 | 28.57 |
| profit_model | 2021 | 15 | 66.67 | 0.04 | 0.64 | 0.00 | 20.00 |
| profit_model | 2022 | 9 | 66.67 | 0.16 | 1.44 | 22.22 | 22.22 |
| profit_model | 2023 | 16 | 56.25 | 0.03 | 0.40 | 18.75 | 25.00 |
| profit_model | 2024 | 21 | 71.43 | 0.18 | 3.71 | 38.10 | 28.57 |
| profit_model | 2025 | 44 | 54.55 | 0.04 | 1.55 | 22.73 | 27.27 |
| profit_model | 2026 | 23 | 47.83 | 0.05 | 1.14 | 21.74 | 21.74 |
| relaxed_winrate_fade15 | 2016 | 1 | 100.00 | 0.39 | 0.39 | 0.00 | 0.00 |
| relaxed_winrate_fade15 | 2017 | 1 | 100.00 | 0.01 | 0.01 | 0.00 | 0.00 |
| relaxed_winrate_fade15 | 2018 | 5 | 60.00 | 0.26 | 1.30 | 40.00 | 20.00 |
| relaxed_winrate_fade15 | 2019 | 4 | 25.00 | -0.18 | -0.73 | 0.00 | 25.00 |
| relaxed_winrate_fade15 | 2020 | 7 | 57.14 | 0.10 | 0.67 | 14.29 | 14.29 |
| relaxed_winrate_fade15 | 2021 | 6 | 50.00 | -0.15 | -0.91 | 0.00 | 16.67 |
| relaxed_winrate_fade15 | 2022 | 3 | 66.67 | 0.33 | 0.99 | 33.33 | 0.00 |
| relaxed_winrate_fade15 | 2023 | 2 | 100.00 | 0.19 | 0.37 | 0.00 | 0.00 |
| relaxed_winrate_fade15 | 2024 | 7 | 57.14 | 0.12 | 0.86 | 28.57 | 28.57 |
| relaxed_winrate_fade15 | 2025 | 11 | 81.82 | 0.46 | 5.07 | 45.45 | 0.00 |
| relaxed_winrate_fade15 | 2026 | 7 | 85.71 | 0.51 | 3.56 | 28.57 | 0.00 |
| relaxed_winrate_fade20 | 2017 | 1 | 100.00 | 0.01 | 0.01 | 0.00 | 0.00 |
| relaxed_winrate_fade20 | 2018 | 2 | 100.00 | 0.97 | 1.93 | 100.00 | 0.00 |
| relaxed_winrate_fade20 | 2019 | 1 | 100.00 | 0.40 | 0.40 | 0.00 | 0.00 |
| relaxed_winrate_fade20 | 2020 | 2 | 50.00 | 0.35 | 0.70 | 0.00 | 0.00 |
| relaxed_winrate_fade20 | 2021 | 1 | 100.00 | 0.05 | 0.05 | 0.00 | 0.00 |
| relaxed_winrate_fade20 | 2022 | 1 | 100.00 | 0.26 | 0.26 | 0.00 | 0.00 |
| relaxed_winrate_fade20 | 2024 | 3 | 66.67 | 0.40 | 1.19 | 33.33 | 0.00 |
| relaxed_winrate_fade20 | 2025 | 2 | 100.00 | 0.75 | 1.50 | 100.00 | 0.00 |
