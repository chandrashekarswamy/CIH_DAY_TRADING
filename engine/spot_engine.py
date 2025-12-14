"""
spot_engine.py

Evaluates spot-based ORB conditions and determines
whether a trade is valid along with spot-level
entry, SL, and target.
"""

from config.constants import VOLUME_RATIO_THRESHOLD


def evaluate_spot_trade(
    symbol: str,
    price: float,
    ema9: float,
    ema20: float,
    vwap: float,
    orb_high: float,
    orb_low: float,
    volume_ratio: float
) -> dict:
    """
    Evaluates spot conditions and returns a decision.

    Returns a dictionary with:
    - valid_trade (bool)
    - action (LONG / SHORT / NO TRADE)
    - entry
    - sl
    - target
    - reason
    """

    # Volume check
    if volume_ratio < VOLUME_RATIO_THRESHOLD:
        return {
            "valid_trade": False,
            "action": "NO TRADE",
            "reason": "Volume ratio below threshold"
        }

    # LONG conditions
    if ema9 > ema20 and price > vwap and price > orb_high:
        return {
            "valid_trade": True,
            "action": "LONG",
            "entry": price,
            "sl": orb_low,
            "target": price + (orb_high - orb_low),
            "reason": "ORB breakout + EMA + VWAP + Volume"
        }

    # SHORT conditions
    if ema9 < ema20 and price < vwap and price < orb_low:
        return {
            "valid_trade": True,
            "action": "SHORT",
            "entry": price,
            "sl": orb_high,
            "target": price - (orb_high - orb_low),
            "reason": "ORB breakdown + EMA + VWAP + Volume"
        }

    return {
        "valid_trade": False,
        "action": "NO TRADE",
        "reason": "Conditions not met"
    }
