from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.db.base import SessionLocal
from app.db.crud import get_trade_chart

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/chart/{trade_id}", response_class=HTMLResponse)
def view_chart(request: Request, trade_id: int):
    with SessionLocal() as db:
        row = get_trade_chart(db, trade_id)
        if not row:
            return HTMLResponse("<p class='p-4'> No  chart available for this tarde yet. </p>")
        return templates.TemplateResponse("chart.html", {"request": request, "chart": row.json_data, "trade_id": trade_id})
    