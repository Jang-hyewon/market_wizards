from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, time
from pathlib import Path
from statistics import mean, median
from urllib.parse import quote
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


NY = ZoneInfo("America/New_York")
OUT_DIR = Path("jason_lance_60d")


@dataclass
class Bar:
    ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


def fetch_yahoo_chart(symbol: str, range_: str = "60d", interval: str = "5m") -> list[Bar]:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{quote(symbol)}?range={range_}&interval={interval}"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=30) as response:
        payload = json.load(response)

    result = payload.get("chart", {}).get("result")
    if not result:
        return []
    result = result[0]
    timestamps = result.get("timestamp") or []
    quote_data = result.get("indicators", {}).get("quote", [{}])[0]
    rows = []
    for i, stamp in enumerate(timestamps):
        try:
            o = quote_data["open"][i]
            h = quote_data["high"][i]
            l = quote_data["low"][i]
            c = quote_data["close"][i]
            v = quote_data.get("volume", [0] * len(timestamps))[i] or 0
        except (KeyError, IndexError):
            continue
        if o is None or h is None or l is None or c is None:
            continue
        rows.append(
            Bar(
                ts=datetime.fromtimestamp(stamp, tz=ZoneInfo("UTC")).astimezone(NY),
                open=float(o),
                high=float(h),
                low=float(l),
                close=float(c),
                volume=float(v),
            )
        )
    return rows


def group_by_day(bars: list[Bar]) -> dict[str, list[Bar]]:
    grouped: dict[str, list[Bar]] = defaultdict(list)
    for bar in bars:
        grouped[str(bar.ts.date())].append(bar)
    return dict(sorted(grouped.items()))


def ema(values: list[float], period: int) -> list[float]:
    if not values:
        return []
    alpha = 2 / (period + 1)
    out = [values[0]]
    for value in values[1:]:
        out.append(alpha * value + (1 - alpha) * out[-1])
    return out


def rolling_atr(bars: list[Bar], period: int = 14) -> list[float]:
    trs = []
    prev_close = None
    for bar in bars:
        if prev_close is None:
            tr = bar.high - bar.low
        else:
            tr = max(bar.high - bar.low, abs(bar.high - prev_close), abs(bar.low - prev_close))
        trs.append(tr)
        prev_close = bar.close

    atr = []
    for i in range(len(trs)):
        window = trs[max(0, i - period + 1) : i + 1]
        atr.append(mean(window))
    return atr


def day_vwap(day: list[Bar]) -> list[float]:
    total_pv = 0.0
    total_v = 0.0
    out = []
    for bar in day:
        typical = (bar.high + bar.low + bar.close) / 3
        vol = max(bar.volume, 1.0)
        total_pv += typical * vol
        total_v += vol
        out.append(total_pv / total_v)
    return out


def summarize(trades: list[dict]) -> dict:
    if not trades:
        return {
            "trades": 0,
            "win_rate_pct": "",
            "avg_r": "",
            "median_r": "",
            "total_r": "",
            "best_r": "",
            "worst_r": "",
        }
    pnl = [float(t["pnl_r"]) for t in trades]
    wins = [x for x in pnl if x > 0]
    return {
        "trades": len(trades),
        "win_rate_pct": round(100 * len(wins) / len(pnl), 2),
        "avg_r": round(mean(pnl), 3),
        "median_r": round(median(pnl), 3),
        "total_r": round(sum(pnl), 3),
        "best_r": round(max(pnl), 3),
        "worst_r": round(min(pnl), 3),
    }


def simulate_intraday(
    symbol: str,
    strategy: str,
    day: list[Bar],
    entry_i: int,
    direction: str,
    entry: float,
    stop: float,
    target_r: float,
    max_exit_time: time,
    setup: str,
) -> dict | None:
    if direction == "long":
        risk = entry - stop
    else:
        risk = stop - entry
    if risk <= 0 or risk / entry > 0.02:
        return None

    target = entry + target_r * risk if direction == "long" else entry - target_r * risk
    partial_hit = False
    runner_stop = stop
    exit_price = day[-1].close
    exit_reason = "time"
    exit_ts = day[-1].ts
    first_half_r = None

    for bar in day[entry_i:]:
        if bar.ts.time() > max_exit_time:
            exit_price = bar.close
            exit_reason = "time"
            exit_ts = bar.ts
            break

        if direction == "long":
            if bar.low <= runner_stop:
                exit_price = runner_stop
                exit_reason = "breakeven" if partial_hit else "stop"
                exit_ts = bar.ts
                break
            if not partial_hit and bar.high >= target:
                partial_hit = True
                first_half_r = target_r
                runner_stop = entry
        else:
            if bar.high >= runner_stop:
                exit_price = runner_stop
                exit_reason = "breakeven" if partial_hit else "stop"
                exit_ts = bar.ts
                break
            if not partial_hit and bar.low <= target:
                partial_hit = True
                first_half_r = target_r
                runner_stop = entry

    if direction == "long":
        runner_r = (exit_price - entry) / risk
    else:
        runner_r = (entry - exit_price) / risk
    pnl_r = 0.5 * first_half_r + 0.5 * runner_r if partial_hit else runner_r

    return {
        "strategy": strategy,
        "symbol": symbol,
        "date": str(day[entry_i].ts.date()),
        "entry_time": day[entry_i].ts.strftime("%H:%M"),
        "exit_time": exit_ts.strftime("%H:%M"),
        "direction": direction,
        "setup": setup,
        "entry": round(entry, 4),
        "stop": round(stop, 4),
        "risk_pct": round(100 * risk / entry, 3),
        "target_r": target_r,
        "partial_hit": partial_hit,
        "exit_reason": exit_reason,
        "pnl_r": round(pnl_r, 3),
    }


def backtest_jason() -> list[dict]:
    symbols = ["ES=F", "NQ=F", "CL=F", "ZB=F", "ZN=F"]
    trades = []
    for symbol in symbols:
        bars = fetch_yahoo_chart(symbol)
        all_atr = rolling_atr(bars)
        atr_by_ts = {bar.ts: all_atr[i] for i, bar in enumerate(bars)}
        for _, day in group_by_day(bars).items():
            active = [b for b in day if time(9, 30) <= b.ts.time() <= time(15, 55)]
            if len(active) < 50:
                continue
            closes = [b.close for b in active]
            ema9 = ema(closes, 9)
            ema21 = ema(closes, 21)
            opening = active[:6]
            or_high = max(b.high for b in opening)
            or_low = min(b.low for b in opening)
            day_open = active[0].open
            traded = False
            for i in range(7, len(active)):
                if traded or active[i].ts.time() > time(14, 45):
                    break
                bar = active[i]
                atr = atr_by_ts.get(bar.ts, 0)
                if atr <= 0:
                    continue
                trend_up = ema9[i] > ema21[i] and bar.close > day_open
                trend_down = ema9[i] < ema21[i] and bar.close < day_open
                if bar.close > or_high and trend_up:
                    entry = bar.close
                    stop = max(or_high - 0.7 * atr, entry - 1.5 * atr)
                    trade = simulate_intraday(symbol, "Jason Berry", active, i, "long", entry, stop, 1.0, time(15, 45), "OR breakout + EMA trend")
                    if trade:
                        trades.append(trade)
                        traded = True
                elif bar.close < or_low and trend_down:
                    entry = bar.close
                    stop = min(or_low + 0.7 * atr, entry + 1.5 * atr)
                    trade = simulate_intraday(symbol, "Jason Berry", active, i, "short", entry, stop, 1.0, time(15, 45), "OR breakdown + EMA trend")
                    if trade:
                        trades.append(trade)
                        traded = True
    return trades


def first_30m_volume_by_day(days: dict[str, list[Bar]]) -> dict[str, float]:
    out = {}
    for date, day in days.items():
        regular = [b for b in day if time(9, 30) <= b.ts.time() <= time(10, 0)]
        out[date] = sum(b.volume for b in regular)
    return out


def median_previous(values: list[float], i: int, lookback: int = 20) -> float:
    start = max(0, i - lookback)
    prev = [v for v in values[start:i] if v > 0]
    return median(prev) if prev else 0


def backtest_lance() -> list[dict]:
    symbols = ["NVDA", "TSLA", "AMD", "META", "AAPL", "MSFT", "AMZN", "GOOGL", "AVGO", "NFLX", "PLTR"]
    spy_days = group_by_day(fetch_yahoo_chart("SPY"))
    spy_open_close = {}
    for date, day in spy_days.items():
        regular = [b for b in day if time(9, 30) <= b.ts.time() <= time(15, 55)]
        if regular:
            spy_open_close[date] = (regular[0].open, regular[-1].close)

    trades = []
    for symbol in symbols:
        bars = fetch_yahoo_chart(symbol)
        days = group_by_day(bars)
        dates = list(days.keys())
        vol30 = first_30m_volume_by_day(days)
        vol_series = [vol30.get(d, 0) for d in dates]
        previous_close = None

        for di, date in enumerate(dates):
            day = [b for b in days[date] if time(9, 30) <= b.ts.time() <= time(15, 55)]
            if len(day) < 50:
                continue
            if previous_close is None:
                previous_close = day[-1].close
                continue
            gap_pct = 100 * (day[0].open / previous_close - 1)
            first_vol = vol30.get(date, 0)
            base_vol = median_previous(vol_series, di)
            if abs(gap_pct) < 1.2 and (base_vol <= 0 or first_vol < 1.5 * base_vol):
                previous_close = day[-1].close
                continue

            vwap = day_vwap(day)
            opening = day[:6]
            or_high = max(b.high for b in opening)
            or_low = min(b.low for b in opening)
            spy_pair = spy_open_close.get(date)
            spy_ret = 0.0 if not spy_pair else 100 * (spy_pair[1] / spy_pair[0] - 1)
            traded = False
            for i in range(7, len(day)):
                if traded or day[i].ts.time() > time(14, 45):
                    break
                bar = day[i]
                stock_ret = 100 * (bar.close / day[0].open - 1)
                rel = stock_ret - spy_ret
                atr_proxy = max(or_high - or_low, 0.003 * bar.close)
                if gap_pct > 0 and bar.close > or_high and bar.close > vwap[i] and rel > 0.5:
                    entry = bar.close
                    stop = min(vwap[i], entry - 0.6 * atr_proxy)
                    trade = simulate_intraday(symbol, "Lance Breitstein", day, i, "long", entry, stop, 1.0, time(15, 45), "gap/catalyst proxy + VWAP + relative strength")
                    if trade:
                        trades.append(trade)
                        traded = True
                elif gap_pct < 0 and bar.close < or_low and bar.close < vwap[i] and rel < -0.5:
                    entry = bar.close
                    stop = max(vwap[i], entry + 0.6 * atr_proxy)
                    trade = simulate_intraday(symbol, "Lance Breitstein", day, i, "short", entry, stop, 1.0, time(15, 45), "gap/catalyst proxy + VWAP + relative weakness")
                    if trade:
                        trades.append(trade)
                        traded = True
            previous_close = day[-1].close
    return trades


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict]) -> str:
    if not rows:
        return "_No rows._"
    cols = list(rows[0].keys())
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(c, "")) for c in cols) + " |")
    return "\n".join(lines)


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    jason_trades = backtest_jason()
    lance_trades = backtest_lance()
    all_trades = jason_trades + lance_trades

    write_csv(OUT_DIR / "jason_trades.csv", jason_trades)
    write_csv(OUT_DIR / "lance_trades.csv", lance_trades)
    write_csv(OUT_DIR / "all_trades.csv", all_trades)

    summary_rows = []
    for name, trades in [("Jason Berry", jason_trades), ("Lance Breitstein", lance_trades)]:
        row = {"strategy": name, **summarize(trades)}
        summary_rows.append(row)
    write_csv(OUT_DIR / "summary.csv", summary_rows)

    by_symbol = []
    for strategy, trades in [("Jason Berry", jason_trades), ("Lance Breitstein", lance_trades)]:
        symbols = sorted(set(t["symbol"] for t in trades))
        for symbol in symbols:
            st = [t for t in trades if t["symbol"] == symbol]
            by_symbol.append({"strategy": strategy, "symbol": symbol, **summarize(st)})
    write_csv(OUT_DIR / "summary_by_symbol.csv", by_symbol)

    report = [
        "# Jason Berry / Lance Breitstein 60D Mini Backtest",
        "",
        "Data: Yahoo chart API, recent 60 days, 5-minute bars.",
        "",
        "Important limitations:",
        "",
        "- This is a simplified systematic approximation, not an exact recreation of the traders' discretionary process.",
        "- Lance's strategy especially needs true catalyst/news tagging, which is not included here.",
        "- Yahoo intraday data limits the test to recent history and does not model slippage, commissions, order queue, or broker restrictions.",
        "",
        "## Strategy Summary",
        "",
        markdown_table(summary_rows),
        "",
        "## Summary By Symbol",
        "",
        markdown_table(by_symbol),
        "",
        "## Recent Trades",
        "",
        markdown_table(all_trades[:80]),
        "",
    ]
    Path("jason_lance_60d_backtest.md").write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report))


if __name__ == "__main__":
    main()
