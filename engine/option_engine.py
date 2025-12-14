"""
option_engine.py

Handles NIFTY weekly option selection and
delta-based SL / Target computation.
"""

from config.constants import (
    STRIKE_STEP,
    STRIKE_OFFSET_BY_DAY,
    DELTA_NIFTY,
    TARGET_MULTIPLIER,
    SL_MULTIPLIER,
)
from utils.time_utils import current_day_name, is_after


def nearest_strike(price: float) -> int:
    """
    Round spot price to nearest 50 strike.
    """
    return int(round(price / STRIKE_STEP) * STRIKE_STEP)


def determine_expiry() -> str:
    """
    Determine whether to use current or next week expiry
    based on NIFTY Tuesday expiry rules.
    """
    day = current_day_name()

    if day == "Monday" and is_after(11, 30):
        return "Next Week"

    if day == "Tuesday":
        return "Next Week (Caution)"

    if day == "Wednesday":
        return "Current Week"

    return "Current Week"


def determine_strike(spot_price: float, action: str) -> int:
    """
    Determine CE/PE strike based on weekday rules.
    """
    day = current_day_name()
    atm = nearest_strike(spot_price)
    offset = STRIKE_OFFSET_BY_DAY.get(day, 100)

    if action == "LONG":
        return atm + offset
    elif action == "SHORT":
        return atm - offset
    else:
        raise ValueError("Action must be LONG or SHORT")


def compute_option_levels(
    ltp: float,
    orb_high: float,
    orb_low: float
) -> dict:
    """
    Compute delta-based target & SL for options.
    """
    orb_range = orb_high - orb_low

    target_points = orb_range * DELTA_NIFTY * TARGET_MULTIPLIER
    sl_points = orb_range * DELTA_NIFTY * SL_MULTIPLIER

    return {
        "entry_range": (round(ltp - 2, 2), round(ltp + 2, 2)),
        "target": round(ltp + target_points, 2),
        "sl": round(ltp - sl_points, 2),
        "time_exit": "on/before 15:10 IST",
    }


def build_option_trade(
    spot_price: float,
    action: str,
    ltp: float,
    orb_high: float,
    orb_low: float
) -> dict:
    """
    Build full NIFTY option trade structure.
    """
    expiry = determine_expiry()
    strike = determine_strike(spot_price, action)
    option_type = "CE" if action == "LONG" else "PE"

    levels = compute_option_levels(ltp, orb_high, orb_low)

    return {
        "instrument": f"NIFTY {strike} {option_type}",
        "expiry": expiry,
        "entry": levels["entry_range"],
        "target": levels["target"],
        "sl": levels["sl"],
        "time_exit": levels["time_exit"],
    }
