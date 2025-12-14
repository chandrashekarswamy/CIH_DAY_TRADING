"""
IH Trading APP – Phase 1 (UI FINAL)
"""

import streamlit as st
from datetime import datetime, timedelta
import pytz

from engine.spot_engine import evaluate_spot_trade
from engine.option_engine import (
    build_option_trade,
    determine_expiry,
    determine_strike,
)
from config.constants import SUPPORTED_SYMBOLS

# -------------------------
# Helpers
# -------------------------

IST = pytz.timezone("Asia/Kolkata")


def now_ist_str():
    return datetime.now(IST).strftime("%H:%M IST")


def expiry_date_str(expiry_label: str) -> str:
    today = datetime.now(IST).date()
    weekday = today.weekday()  # Monday = 0
    days_to_tuesday = (1 - weekday) % 7
    if "Next" in expiry_label:
        days_to_tuesday += 7
    expiry = today + timedelta(days=days_to_tuesday)
    return expiry.strftime("%d %b").upper()


def action_badge(action: str) -> str:
    color = "#00C853" if action == "LONG" else "#FF5252"
    return f"""
<span style="
    padding:2px 8px;
    border-radius:6px;
    background-color:{color};
    font-size:12px;
    font-weight:600;
    margin-left:6px;
">
{action}
</span>
"""


def reset_app():
    for k in list(st.session_state.keys()):
        del st.session_state[k]


# -------------------------
# Page
# -------------------------

st.set_page_config(page_title="IH Trading APP", layout="wide")
st.title("IH Trading APP")

# -------------------------
# Inputs
# -------------------------

c1, c2, c3, c4 = st.columns([1.3, 1, 1, 1])
with c1:
    symbol = st.selectbox("", SUPPORTED_SYMBOLS, index=SUPPORTED_SYMBOLS.index("NIFTY"))
with c2:
    ema9 = st.text_input("EMA9")
with c3:
    vwap = st.text_input("VWAP")
with c4:
    orb_low = st.text_input("ORB Low")

_, c5, c6, c7 = st.columns([1.3, 1, 1, 1])
with c5:
    ema20 = st.text_input("EMA20")
with c6:
    volume_ratio = st.text_input("Volume Ratio")
with c7:
    orb_high = st.text_input("ORB High")

st.divider()

b1, b2 = st.columns([1, 6])
with b1:
    eval_click = st.button("Evaluate")
with b2:
    if st.button("Reset"):
        reset_app()
        st.stop()

# -------------------------
# Evaluation
# -------------------------

if eval_click:
    try:
        sd = evaluate_spot_trade(
            symbol=symbol,
            price=float(ema9),
            ema9=float(ema9),
            ema20=float(ema20),
            vwap=float(vwap),
            orb_high=float(orb_high),
            orb_low=float(orb_low),
            volume_ratio=float(volume_ratio),
        )
        st.session_state["spot"] = sd
        st.session_state["orb"] = {
            "high": float(orb_high),
            "low": float(orb_low),
        }
    except ValueError:
        st.error("Invalid numeric inputs")
        st.stop()

# -------------------------
# Output
# -------------------------

if "spot" in st.session_state:
    sd = st.session_state["spot"]

    # ---- NO TRADE ----
    if not sd["valid_trade"]:
        st.warning(
            f"""
**NO TRADE**

Why?
• EMA alignment failed  
• ORB breakout/breakdown not confirmed  
• VWAP condition failed  
• Volume confirmation missing  

Report Time : {now_ist_str()}
"""
        )
        st.stop()

    # ---- NON-NIFTY ----
    if symbol != "NIFTY":
        entry, sl, tgt = sd["entry"], sd["sl"], sd["target"]
        t1 = round(entry + (tgt - entry) * 0.5, 2)

        st.markdown(
            f"""
**{symbol}** {action_badge(sd['action'])}
&nbsp;&nbsp;<span style="font-size:12px;">Report Time : {now_ist_str()}</span>
""",
            unsafe_allow_html=True,
        )

        st.code(
            f"""
ENTRY  : {entry}
SL     : {sl}
TARGET : T1 {t1} | T2 {tgt}
EXIT   : SL hit | T2 hit | Time exit on/before 15:10 IST
""",
            language="text",
        )
        st.stop()

    # ---- NIFTY OPTIONS ----
    expiry_lbl = determine_expiry()
    expiry = expiry_date_str(expiry_lbl)
    strike = determine_strike(sd["entry"], sd["action"])
    opt = "CE" if sd["action"] == "LONG" else "PE"
    color = "#00C853" if opt == "CE" else "#FF5252"

    st.markdown(
    f"""
<div style="
    display:flex;
    align-items:center;
    gap:10px;
    white-space:nowrap;
">
  <span style="font-size:16px;">
    Enter
  </span>

  <span style="font-size:16px; font-weight:600; color:{color};">
    NIFTY {expiry} {strike} {opt}
  </span>

  <span style="
    padding:2px 8px;
    border-radius:6px;
    background-color:{'#00C853' if sd['action']=='LONG' else '#FF5252'};
    font-size:12px;
    font-weight:600;
  ">
    {sd['action']}
  </span>

  <span style="font-size:12px; opacity:0.8;">
    Report Time : {now_ist_str()}
  </span>
</div>
""",
    unsafe_allow_html=True,
)


    ltp = st.text_input("")

    if st.button("Generate Trade Levels"):
        try:
            opt_trade = build_option_trade(
                spot_price=sd["entry"],
                action=sd["action"],
                ltp=float(ltp),
                orb_high=st.session_state["orb"]["high"],
                orb_low=st.session_state["orb"]["low"],
            )

            st.code(
                f"""
NIFTY {expiry} {strike} {opt}
Entry  : {opt_trade['entry'][0]} – {opt_trade['entry'][1]}
Target : {opt_trade['target']}
SL     : {opt_trade['sl']}
Exit   : Delta-based | Tight SL | Time exit on/before 15:10 IST
""",
                language="text",
            )
        except ValueError:
            st.error("Please enter valid Option LTP")
