import requests
from datetime import datetime, timezone
from typing import List, Tuple
from app.core.config import settings

def fetch_last_n_1min(symbol: str, n: int = 300) -> Tuple[list, list, list, list, list]:
    """
    Returns: times, opens, highs, lows, closes (ascending)
    """
    params = {
        "symbol": symbol,
        "interval": "1min",
        "outputsize": str(n),
        "apikey": settings.TWELVE_DATA_API_KEY,
        "format": "JSON",
        "timezone": "UTC",
        "order": "desc"
    }
    r = requests.get(settings.TD_BASE, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    if "values" not in data:
        raise RuntimeError(f"Twelve Data bad response: {data}")
    vals = list(reversed(data["values"])) # chronological
    times = [datetime.fromisoformat(x["datetime"]).replace(tzinfo=timezone.utc) for x in vals]
    opens = [float(x["open"]) for x in vals]
    highs = [float(x["high"]) for x in vals]
    lows = [float(x["low"]) for x in vals]
    closes = [float(x["close"]) for x in vals]
    return times, opens, highs, lows, closes