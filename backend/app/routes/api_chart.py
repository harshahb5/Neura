from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.db.base import SessionLocal
from app.db.crud import get_trade_chart

router = APIRouter()

@router.get("/chart/{trade_id}")
def get_chart(trade_id: int):
    with SessionLocal() as db:
        row = get_trade_chart(db, trade_id)
        if not row:
            return JSONResponse({"error": "Chart not found"}, status_code=404)
        return JSONResponse(content=row.json_data)
    