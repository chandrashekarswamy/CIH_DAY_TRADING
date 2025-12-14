"""
Test cases for spot_engine.py
Covers LONG, SHORT, NO TRADE scenarios
"""

from engine.spot_engine import evaluate_spot_trade


def test_nifty_long():
    result = evaluate_spot_trade(
        symbol="NIFTY",
        price=26049,
        ema9=26030,
        ema20=25990,
        vwap=26000,
        orb_high=26020,
        orb_low=25940,
        volume_ratio=1.35
    )
    print("NIFTY LONG:", result)


def test_nifty_no_trade_volume():
    result = evaluate_spot_trade(
        symbol="NIFTY",
        price=26049,
        ema9=26030,
        ema20=25990,
        vwap=26000,
        orb_high=26020,
        orb_low=25940,
        volume_ratio=0.8
    )
    print("NIFTY NO TRADE (VOLUME):", result)


def test_banknifty_short():
    result = evaluate_spot_trade(
        symbol="BANKNIFTY",
        price=59890,
        ema9=59800,
        ema20=59950,
        vwap=59920,
        orb_high=60000,
        orb_low=59850,
        volume_ratio=1.4
    )
    print("BANKNIFTY SHORT:", result)


if __name__ == "__main__":
    test_nifty_long()
    test_nifty_no_trade_volume()
    test_banknifty_short()
