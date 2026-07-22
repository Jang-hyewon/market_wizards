from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any

import pandas as pd

from backtest_smallcap_parabolic_short_2y import (
    Config,
    add_features,
    download_history,
    fetch_universe,
    is_setup,
    markdown_table,
    score_setup,
    simulate_trade,
    summarize_trades,
)


def evaluate_version(
    histories: dict[str, pd.DataFrame],
    cfg: Config,
    label: str,
    min_failed_from_high_pct: float | None = None,
) -> tuple[dict[str, Any], pd.DataFrame]:
    trades = []
    raw_setups = 0
    scored_setups = 0

    for symbol, frame in histories.items():
        if frame.empty:
            continue
        if len(frame) < 60:
            continue

        setup_mask = (
            (frame["Close"] >= cfg.min_price)
            & (frame["dollar_volume"] >= cfg.min_setup_dollar_volume)
            & frame["atr_14"].notna()
            & (frame["atr_14"] > 0)
            & (
                (frame["volume_ratio"] >= cfg.min_volume_ratio)
                | (
                    frame[["return_3d_pct", "return_5d_pct", "return_10d_pct"]].max(axis=1)
                    >= cfg.a_grade_return
                )
            )
            & (
                (frame["return_1d_pct"] >= 20)
                | (frame["return_3d_pct"] >= cfg.min_3d_return)
                | (frame["return_5d_pct"] >= cfg.min_5d_return)
                | (frame["return_10d_pct"] >= cfg.min_10d_return)
            )
        )

        next_allowed_i = 20
        setup_indices = [i for i in setup_mask[setup_mask].index.map(frame.index.get_loc) if 20 <= i < len(frame) - 1]
        for i in setup_indices:
            if i < next_allowed_i:
                continue
            row = frame.iloc[i]

            raw_setups += 1
            score, _ = score_setup(row, cfg)
            if score < cfg.min_score:
                continue
            if min_failed_from_high_pct is not None and row["failed_from_high_pct"] > min_failed_from_high_pct:
                continue

            scored_setups += 1
            trade = simulate_trade(symbol, frame, i, cfg)
            if trade:
                trades.append(trade)
                next_allowed_i = i + cfg.max_hold_days

    trades_frame = pd.DataFrame(trades)
    summary = summarize_trades(trades_frame)
    summary.update(
        {
            "version": label,
            "raw_setups": raw_setups,
            "scored_setups": scored_setups,
            "min_score": cfg.min_score,
            "trigger_atr_buffer": cfg.trigger_atr_buffer,
            "stop_atr_buffer": cfg.stop_atr_buffer,
            "max_risk_pct": cfg.max_entry_risk_pct,
            "hold_days": cfg.max_hold_days,
            "partial_r": cfg.partial_r,
            "fade_filter": min_failed_from_high_pct if min_failed_from_high_pct is not None else "",
        }
    )
    if not trades_frame.empty:
        trades_frame.insert(0, "version", label)
    return summary, trades_frame


def summarize_by_year(trades: pd.DataFrame) -> pd.DataFrame:
    if trades.empty:
        return pd.DataFrame()
    yearly = trades.copy()
    yearly["year"] = pd.to_datetime(yearly["entry_date"]).dt.year
    rows = []
    for (version, year), group in yearly.groupby(["version", "year"]):
        summary = summarize_trades(group)
        summary["version"] = version
        summary["year"] = int(year)
        rows.append(summary)
    return pd.DataFrame(rows).sort_values(["version", "year"])


def main() -> None:
    base = Config(period="10y", max_symbols=1600, chunk_size=80)
    universe = fetch_universe(base)
    universe["symbol"] = universe["symbol"].astype(str).str.strip()
    raw_histories = download_history(universe["symbol"].tolist(), base)
    histories = {
        symbol: add_features(raw)
        for symbol, raw in raw_histories.items()
        if not raw.empty
    }

    profit_cfg = base
    a_grade_cfg = replace(base, min_score=75)
    winrate_cfg = replace(
        base,
        min_score=55,
        trigger_atr_buffer=0.02,
        stop_atr_buffer=0.10,
        max_hold_days=3,
        partial_r=0.5,
        max_entry_risk_pct=35.0,
    )

    versions = [
        ("profit_model", profit_cfg, None),
        ("a_grade_profit_subset", a_grade_cfg, None),
        ("relaxed_winrate_fade20", winrate_cfg, -20.0),
        ("relaxed_winrate_fade15", winrate_cfg, -15.0),
    ]

    summaries = []
    trade_frames = []
    for label, cfg, fade_filter in versions:
        summary, trades = evaluate_version(histories, cfg, label, min_failed_from_high_pct=fade_filter)
        summaries.append(summary)
        if not trades.empty:
            trade_frames.append(trades)

    summary_frame = pd.DataFrame(summaries)
    trades_frame = pd.concat(trade_frames, ignore_index=True) if trade_frames else pd.DataFrame()
    yearly_frame = summarize_by_year(trades_frame)

    high_winrate = summary_frame[
        (summary_frame["trades"].fillna(0) > 0) & (summary_frame["win_rate_pct"].fillna(0) >= 70)
    ].copy()

    out_dir = Path("smallcap_short_10y")
    out_dir.mkdir(exist_ok=True)
    universe.to_csv(out_dir / "universe.csv", index=False)
    summary_frame.to_csv(out_dir / "version_comparison_summary.csv", index=False)
    trades_frame.to_csv(out_dir / "version_comparison_trades.csv", index=False)
    yearly_frame.to_csv(out_dir / "version_yearly_summary.csv", index=False)
    high_winrate.to_csv(out_dir / "high_winrate_filters.csv", index=False)

    report_cols = [
        "version",
        "trades",
        "win_rate_pct",
        "avg_r",
        "median_r",
        "total_r",
        "best_r",
        "worst_r",
        "partial_hit_pct",
        "stop_exit_pct",
        "raw_setups",
        "scored_setups",
        "min_score",
        "trigger_atr_buffer",
        "hold_days",
        "partial_r",
        "fade_filter",
    ]
    yearly_cols = [
        "version",
        "year",
        "trades",
        "win_rate_pct",
        "avg_r",
        "total_r",
        "partial_hit_pct",
        "stop_exit_pct",
    ]

    report = [
        "# Small-Cap Parabolic Short 10Y Backtest",
        "",
        "This expands the prior 2-year Yahoo daily-bar test to 10 years.",
        "",
        "Important limitations:",
        "",
        "- Universe is based on currently listed U.S. small-cap stocks, so survivorship bias is material.",
        "- Yahoo daily bars cannot verify borrow availability, borrow fees, locates, halts, or real intraday event order.",
        "- Results are in R units, not account return.",
        "- This is research output, not a trade recommendation.",
        "",
        "## Summary",
        "",
        markdown_table(summary_frame[report_cols]),
        "",
        "## Filters With Win Rate At Least 70%",
        "",
        markdown_table(high_winrate[report_cols] if not high_winrate.empty else high_winrate),
        "",
        "## Yearly Summary",
        "",
        markdown_table(yearly_frame[yearly_cols] if not yearly_frame.empty else yearly_frame),
        "",
    ]
    Path("smallcap_short_10y_backtest.md").write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report))


if __name__ == "__main__":
    main()
