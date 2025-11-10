from datetime import datetime
from typing import List, Tuple

def floor_to_5min(dt):
    # floor minutes to (m // 5) * 5
    m = (dt.minute // 5) * 5
    return dt.replace(minute=m, second=0, microsecond=0)

def to_5min(times, opens, highs, lows, closes):
    """
    Aggregate arrays of 1-min candles -> 5-min bars.
    Return times5, opens5, highs5, lows5, closes5 (ascending).
    """
    if not times:
        return [], [], [], []
    buckets = {}
    for i, t in enumerate(times):
        key = floor_to_5min(t)
        if key not in buckets:
            buckets[key] = {
                "open": opens[i],
                "high": highs[i],
                "low": lows[i],
                "close": closes[i]
            }
        else:
            b = buckets[key]
            b["high"] = max(b["high"], highs[i])
            b["low"] = max(b["low"], lows[i])
            b["close"] = closes[i]

    # sort by key time
    keys = sorted(buckets.keys())
    o = [buckets[k]["open"] for k in keys]
    h = [buckets[k]["high"] for k in keys]
    l = [buckets[k]["low"] for k in keys]
    c = [buckets[k]["close"] for k in keys]
    return keys, o, h, l, c
