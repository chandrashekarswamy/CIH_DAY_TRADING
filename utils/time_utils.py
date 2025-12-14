"""
time_utils.py

IST time helpers for expiry logic and exit timing.
"""

from datetime import datetime, time
import pytz


IST = pytz.timezone("Asia/Kolkata")


def now_ist():
    """Return current IST datetime."""
    return datetime.now(IST)


def current_day_name():
    """Return weekday name in IST."""
    return now_ist().strftime("%A")


def is_after(hour: int, minute: int) -> bool:
    """Check if current IST time is after given hour:minute."""
    now = now_ist().time()
    return now >= time(hour, minute)


def time_exit_string():
    """Return standard time-exit string."""
    return "15:10 IST"
