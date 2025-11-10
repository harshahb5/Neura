import json
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.models import Trade, TradeChart
from datetime import datetime, timezone

def create_trade(db: Session, **kwargs) -> Trade:
    t = Trade(**kwargs)
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

def get_open_trades(db: Session) -> List[Trade]:
    return db.query(Trade).filter(Trade.status == "OPEN").all()

def get_recent_trades(db: Session, limit: int = 200) -> List[Trade]:
    return db.query(Trade).order_by(desc(Trade.opened_at)).limit(limit).all()

def get_trade(db: Session, trade_id: int) -> Optional[Trade]:
    return db.query(Trade).filter(Trade.id == trade_id).first()

def close_trade(db: Session, trade_id: int, exit_price: float, pnl_points: float, pnl_inr: float, note: str = ""):
    t = db.query(Trade).filter(Trade.id == trade_id).first()
    if not t or t.status != "OPEN":
        return None
    t.exit_price = exit_price
    t.status = "CLOSED"
    t.closed_at = datetime.now(timezone.utc)
    t.pnl_points = pnl_points
    t.pnl_inr = pnl_inr
    if note:
        t.note = ((t.note or "") + f"; {note}").strip("; ")
    db.commit()
    db.refresh(t)
    return t

def count_open(db: Session) -> int:
    return db.query(Trade).filter(Trade.status == "OPEN").count()

def save_trade_chart(db: Session, trade_id: int, chart_payload: dict):
    row = TradeChart(trade_id=trade_id, json_data=json.dumps(chart_payload))
    db.add(row)
    db.commit()
    return row

def get_trade_chart(db: Session, trade_id: int) -> Optional[TradeChart]:
    return db.query(TradeChart).filter(TradeChart.trade_id == trade_id).first()
