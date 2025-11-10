from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from app.db.base import Base

def utcnow():
    return datetime.now(timezone.utc)

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), index=True)
    side = Column(String(4))  # BUY / SELL
    qty = Column(Float, default=1.0)
    entry_price = Column(Float)
    sl = Column(Float)
    tp = Column(Float)
    opened_at = Column(DateTime, default=utcnow)
    status = Column(String(12), default="OPEN")  # OPEN / CLOSED
    exit_price = Column(Float, nullable=True)
    closed_at = Column(DateTime, nullable=True)
    pnl_points = Column(Float, nullable=True)
    pnl_inr = Column(Float, nullable=True)
    note = Column(Text, default="")

class KV(Base):
    __tablename__ = "kv_state"
    id = Column(Integer, primary_key=True)
    k = Column(String(64), unique=True, index=True)
    v = Column(String(256))

class TradeChart(Base):
    __tablename__ = "trade_charts"
    id = Column(Integer, primary_key=True)
    trade_id = Column(Integer, index=True)
    json_data = Column(Text)
