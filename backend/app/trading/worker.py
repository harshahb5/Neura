import asyncio
from app.core.config import settings
from app.db.base import SessionLocal
from app.db.crud import get_open_trades, count_open, save_trade_chart
from app.services.twelve_data import fetch_last_n_1min
from app.services.aggregate import to_5min
from app.trading.logic import crossover_and_retest_5m, detect_crossover_direction_5m
from app.trading.execution import simulate_order, try_close_by_levels, close_at_price

async def trader_loop():
    while True:
        try:
            # 1) Pull 1-min → aggregate to 5-min
            times, opens, highs, lows, closes = fetch_last_n_1min(settings.SYMBOL, n=300)

            # If the API returns nothing, market is likely closed
            if not times or not closes:
                print("[neura-worker] ⏸️ Market Closed or No Data — Skipping this cycle.")
                await asyncio.sleep(settings.POLL_SECONDS)
                continue

            # Aggregate to 5-min candles
            times5, o5, h5, l5, c5 = to_5min(times, opens, highs, lows, closes)

            # If aggregation failed or incomplete
            if len(c5) < 2:
                print("[neura-worker] ⚠️ Not enough 5m candles — waiting for next data.")
                await asyncio.sleep(settings.POLL_SECONDS)
                continue

            last_closed_price = c5[-2]   # last closed 5m bar
            next_bar_open     = o5[-1]   # current forming bar's open (next bar after last closed)

            # 2) Manage existing trade(s)
            with SessionLocal() as db:
                open_trades = get_open_trades(db)

                # 2a) SL/TP check first (priority)
                for t in list(open_trades):
                    try_close_by_levels(db, t, current_price=last_closed_price)

                # refresh open list after possible SL/TP closures
                open_trades = get_open_trades(db)

                # 2b) Opposite-crossover exit (if still open)
                if open_trades:
                    t = open_trades[0]  # one trade per symbol policy
                    recent_cross = detect_crossover_direction_5m(c5)
                    if recent_cross:
                        # If a BUY is open and a SELL crossover appears (confirmed on last closed bar) → exit at next bar open.
                        is_opposite = (t.side == "BUY" and recent_cross == "SELL") or (t.side == "SELL" and recent_cross == "BUY")
                        if is_opposite:
                            close_at_price(db, t, exit_price=next_bar_open, note="Opposite crossover → exit at next 5m open")

                # 3) If no open trade, look for a new entry (crossover + retest on last closed)
                if settings.TRADING_ENABLED and count_open(db) == 0:
                    signal, details = crossover_and_retest_5m(times5, o5, h5, l5, c5)
                    if signal in ("BUY", "SELL"):
                        simulate_order(db, signal, price=last_closed_price, qty=1.0)

                # 4) Snapshot chart for any newly closed trades lacking a chart
                from app.db.models import Trade, TradeChart
                recent = db.query(Trade).order_by(Trade.opened_at.desc()).limit(10).all()
                for t in recent:
                    if t.status == "CLOSED":
                        has_chart = db.query(TradeChart).filter(TradeChart.trade_id == t.id).first()
                        if not has_chart:
                            tail = -50 if len(c5) >= 50 else 0
                            chart_payload = {
                                "times": [x.isoformat() for x in times5[tail:]],
                                "opens": o5[tail:], "highs": h5[tail:], "lows": l5[tail:], "closes": c5[tail:],
                                "ema9": __ema(c5, 9)[tail:], "ema15": __ema(c5, 15)[tail:],
                                "entry": t.entry_price, "exit": t.exit_price,
                                "sl": t.sl, "tp": t.tp, "side": t.side
                            }
                            save_trade_chart(db, t.id, chart_payload)
                db.commit()

        except Exception as e:
            print("[neura-worker] error:", e)

        await asyncio.sleep(settings.POLL_SECONDS)

# local EMA helper for snapshot
def __ema(series, period):
    if not series:
        return []
    alpha = 2 / (period + 1)
    out = []
    prev = series[0]
    out.append(prev)
    for x in series[1:]:
        prev = (x - prev) * alpha + prev
        out.append(prev)
    return out
