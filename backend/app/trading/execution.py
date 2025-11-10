from app.core.config import settings
from app.db.crud import create_trade, close_trade

def simulate_order(db, side: str, price: float, qty: float = 1.0):
    sl = price - settings.SL_ABS if side == "BUY" else price + settings.SL_ABS
    tp = price + settings.TP_ABS if side == "BUY" else price - settings.TP_ABS
    return create_trade(
        db,
        symbol=settings.SYMBOL,
        side=side,
        qty=qty,
        entry_price=price,
        sl=sl,
        tp=tp
    )

def try_close_by_levels(db, trade, current_price: float):
    """
    Standard SL/TP management on last closed 5m price.
    """
    if trade.status != "OPEN":
        return False
    hit_tp = current_price >= trade.tp if trade.side == "BUY" else current_price <= trade.tp
    hit_sl = current_price <= trade.sl if trade.side == "BUY" else current_price >= trade.sl

    if not (hit_tp or hit_sl):
        return False

    exit_price = trade.tp if hit_tp else trade.sl
    diff = (exit_price - trade.entry_price) if trade.side == "BUY" else (trade.entry_price - exit_price)
    pnl_points = diff  # XAUUSD: 1 point = $1
    pnl_inr = pnl_points * settings.RUPEES_PER_POINT * trade.qty
    note = "TP hit" if hit_tp else "SL hit"
    close_trade(db, trade.id, exit_price=exit_price, pnl_points=pnl_points, pnl_inr=pnl_inr, note=note)
    return True

def close_at_price(db, trade, exit_price: float, note: str = "Exit on opposite crossover"):
    """
    Forced close at a specific price (e.g., next-bar open after opposite crossover).
    """
    if trade.status != "OPEN":
        return False
    diff = (exit_price - trade.entry_price) if trade.side == "BUY" else (trade.entry_price - exit_price)
    pnl_points = diff
    pnl_inr = pnl_points * settings.RUPEES_PER_POINT * trade.qty
    close_trade(db, trade.id, exit_price=exit_price, pnl_points=pnl_points, pnl_inr=pnl_inr, note=note)
    return True
