"""
constants.py

All fixed rules, thresholds, and configuration values
are defined here to keep the system deterministic
and extensible.
"""

# -------------------------
# General Trading Constants
# -------------------------

ENTRY_START_TIME = (9, 30)      # 09:30 IST
ENTRY_END_TIME   = (13, 30)     # 13:30 IST
TIME_EXIT_HOUR   = 15
TIME_EXIT_MINUTE = 10

VOLUME_RATIO_THRESHOLD = 1.2

# -------------------------
# ORB Constants
# -------------------------

ORB_WINDOW_START = (9, 15)
ORB_WINDOW_END   = (9, 30)

# -------------------------
# Delta Constants
# -------------------------

DELTA_NIFTY = 0.45
DELTA_BANKNIFTY = 0.55


# -------------------------
# Instruments
# -------------------------

WEEKLY_EXPIRY_SYMBOLS = ["NIFTY"]

SUPPORTED_SYMBOLS = [
    "NIFTY",
    "BANKNIFTY",
    "RELIANCE",
    "HDFCBANK",
    "ICICIBANK",
    "SBIN",
    "AXISBANK",
    "INFY",
    "LT",
    "BHARTIARTL",
    "TCS",
]

# -------------------------
# NIFTY Weekly Expiry Rules
# -------------------------

NIFTY_WEEKLY_EXPIRY_DAY = "Tuesday"

# Strike rounding
STRIKE_STEP = 50

STRIKE_OFFSET_BY_DAY = {
    "Monday":    50,
    "Tuesday":   100,
    "Wednesday": 100,
    "Thursday":  100,
    "Friday":    50
}
# -------------------------
# Delta-based Risk Model
# -------------------------

TARGET_MULTIPLIER = 0.9     # target = orb_range * delta * multiplier
SL_MULTIPLIER = 0.35        # sl = orb_range * delta * multiplier
