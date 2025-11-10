from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse, RedirectResponse
from app.core.config import settings
from app.db.base import SessionLocal
from app.db.crud import get_recent_trades, count_open, get_trade
from app.services.twelve_data import fetch_last_n_1min
from app.services.aggregate import to_5min
from app.trading.execution import try_close_by_levels


router = APIRouter()

@router.get("/trades")
def api_trades():
    with SessionLocal() as db:
        rows = get_recent_trades(db, limit=200)
        payload = [
            {
                "id": r.id,
                "symbol": r.symbol,
                "side": r.side,
                "qty": r.qty,
                "entry_price": r.entry_price,
                "sl": r.sl,
                "tp": r.tp,
                "opened_at": r.opened_at.isoformat() if r.opened_at else None,
                "status": r.status,
                "exit_price": r.exit_price,
                "closed_at": r.closed_at.isoformat() if r.closed_at else None,
                "pnl_points": r.pnl_points,
                "pnl_inr": r.pnl_inr,
                "note": r.note
            } for r in rows
        ]
    return JSONResponse(payload)

@router.post("/toggle")
def toggle_trading(enabled: bool = Form(...)):
    settings.TRADING_ENABLED = enabled
    return RedirectResponse("/", status_code=303)

@router.post("/close/{trade_id}")
def manual_close(trade_id: int):
    with SessionLocal() as db:
        t = get_trade(db, trade_id)
        if not t or t.status != "OPEN":
            return JSONResponse({"ok": False, "msg": "Trade not open"}, status_code=400)
        # close at last closed 5m price
        times, o, h, l, c = fetch_last_n_1min(settings.SYMBOL, n=50)
        t5, o5, h5, l5, c5 = to_5min(times, o, h, l, c)
        if len(c5) < 2:
            return JSONResponse({"ok": False, "msg": "Not enough 5m bars"}, status_code=400)
        last_closed = c5[-2]
        try_close_by_levels(db, t, current_price=last_closed)
    return JSONResponse({"ok": True})