from typing import List

def ema(series: List[float], period: int) -> List[float]:
    if not series:
        return []
    alpha = 2 / (period + 1)
    out = []
    prev = series[0]
    out.append(prev)
    for x in series[1:]:
        prev = (x - prev) * alpha + prev
        out.append(prev)
    return out
