from typing import Tuple, Optional
from app.indicators.ema import ema
from app.core.config import settings

def detect_crossover_direction_5m(closes5) -> Optional[str]:
    """
    Check if the last CLOSED bar (-2) produced a crossover vs the previous closed (-3).
    Returns: "BUY" (bullish cross), "SELL" (bearish cross), or None.
    """
    if len(closes5) < max(settings.FAST_EMA, settings.SLOW_EMA) + 3:
        return None
    f = ema(closes5, settings.FAST_EMA)
    s = ema(closes5, settings.SLOW_EMA)
    f_prev, f_curr = f[-3], f[-2]
    s_prev, s_curr = s[-3], s[-2]
    if f_prev < s_prev and f_curr > s_curr:
        return "BUY"
    if f_prev > s_prev and f_curr < s_curr:
        return "SELL"
    return None

def crossover_and_retest_5m(times5, opens5, highs5, lows5, closes5) -> Tuple[Optional[str], dict]:
    """
    Strategy on 5-minute bars using CLOSED candles.
    Entry only when:
      - Crossover between -3 and -2 (prev_closed → last_closed)
      - Retest on last_closed (-2): wick touches fast EMA, close back across, near ≤ window
    Returns: ("BUY"/"SELL"/None, details)
    """
    if len(closes5) < max(settings.FAST_EMA, settings.SLOW_EMA) + 3:
        return None, {"reason": "not_enough_bars"}

    f = ema(closes5, settings.FAST_EMA)
    s = ema(closes5, settings.SLOW_EMA)

    f_prev, f_curr = f[-3], f[-2]
    s_prev, s_curr = s[-3], s[-2]

    # Step 1: crossover direction at last closed bar
    pending = 0
    if f_prev < s_prev and f_curr > s_curr:
        pending = 1  # BUY side
    elif f_prev > s_prev and f_curr < s_curr:
        pending = -1 # SELL side
    else:
        return None, {"reason": "no_crossover"}

    # Step 2: retest on last closed bar (-2)
    last_close = closes5[-2]
    last_high = highs5[-2]
    last_low  = lows5[-2]
    fast_last = f_curr
    dist = abs(last_close - fast_last)
    is_near = dist <= settings.NEAR_EMA_WINDOW

    if pending == 1:
        if last_low <= fast_last and last_close >= fast_last and is_near:
            return "BUY", {"fast_last": fast_last, "last_close": last_close, "dist": dist}
    else:
        if last_high >= fast_last and last_close <= fast_last and is_near:
            return "SELL", {"fast_last": fast_last, "last_close": last_close, "dist": dist}

    return None, {"reason": "retest_not_confirmed", "dist": dist}
