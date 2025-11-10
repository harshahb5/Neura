import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.base import init_db
from app.routes import api_trades, api_chart
from app.trading.worker import trader_loop

app = FastAPI(title="Neura — EMA 9/15 Auto Trader API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_trades.router, prefix="/api")
app.include_router(api_chart.router, prefix="/api")

@app.on_event("startup")
async def on_startup():
    init_db()
    asyncio.create_task(trader_loop())

@app.get("/healthz")
def health():
    return {
        "ok": True,
        "name": "neura-backend",
        "symbol": settings.SYMBOL,
        "poll_seconds": settings.POLL_SECONDS,
    }
