"""
Tests for option_engine.py
"""

from engine.option_engine import build_option_trade


def test_nifty_long_option():
    result = build_option_trade(
        spot_price=26049,      # mandated
        action="LONG",
        ltp=112,
        orb_high=26020,
        orb_low=25940
    )

    print("NIFTY LONG OPTION:")
    for k, v in result.items():
        print(k, ":", v)


def test_nifty_short_option():
    result = build_option_trade(
        spot_price=26049,
        action="SHORT",
        ltp=108,
        orb_high=26020,
        orb_low=25940
    )

    print("NIFTY SHORT OPTION:")
    for k, v in result.items():
        print(k, ":", v)


if __name__ == "__main__":
    test_nifty_long_option()
    test_nifty_short_option()
