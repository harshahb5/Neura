from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.config import settings

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("dashboard.html",{
        "request": request,
        "app_name": "Neura",
        "symbol": settings.SYMBOL,
        "rupees_per_point": settings.RUPEES_PER_POINT,
        "sl": settings.SL_ABS,
        "tp": settings.TP_ABS,
        "near": settings.NEAR_EMA_WINDOW
    })