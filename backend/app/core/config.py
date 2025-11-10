import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load .env automatically
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

@dataclass
class Settings:
    SYMBOL: str = os.getenv("SYMBOL", "XAUUSD")
    FAST_EMA: int = int(os.getenv("FAST_EMA", "9"))
    SLOW_EMA: int = int(os.getenv("SLOW_EMA", "15"))

    SL_ABS: float = float(os.getenv("SL_ABS", "5"))
    TP_ABS: float = float(os.getenv("TP_ABS", "10"))
    NEAR_EMA_WINDOW: float = float(os.getenv("NEAR_EMA_WINDOW", "1.0"))

    RUPEES_PER_POINT: float = float(os.getenv("RUPEES_PER_POINT", "95"))

    TWELVE_DATA_API_KEY: str = os.getenv("TWELVE_DATA_API_KEY", "")
    TD_BASE: str = os.getenv("TD_BASE", "https://api.twelvedata.com/time_series")

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./local.db")
    POLL_SECONDS: int = int(os.getenv("POLL_SECONDS", "60"))
    TRADING_ENABLED: bool = os.getenv("TRADING_ENABLED", "true").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")

settings = Settings()
