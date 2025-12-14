# IH Trading Application (Phase-1)

## Overview
This project implements a rule-based ORB (Opening Range Breakout) trading system
with a Streamlit UI and Python backend.

Key design principles:
- Deterministic rules (no ML, no AI decisions)
- Spot-first logic
- Options logic ONLY for NIFTY (weekly expiry)
- Manual inputs, system-driven outputs
- Extensible architecture

---

## Instruments Supported
- NIFTY (weekly options – Tuesday expiry)
- BANKNIFTY (spot-only for now)
- Stocks (spot-only, monthly logic reserved)

---

## Trading Logic Summary

### ORB Window
09:15 – 09:30 (locked externally by user inputs)

### Entry Conditions (LONG)
- EMA9 > EMA20
- Price > VWAP
- Price > ORB High
- Volume Ratio ≥ 1.2

### Entry Conditions (SHORT)
- EMA9 < EMA20
- Price < VWAP
- Price < ORB Low
- Volume Ratio ≥ 1.2

### Entry Window
09:30 – 13:30 IST

---

## NIFTY Weekly Expiry Rules
Weekly expiry = Tuesday

| Day | Rule |
|----|-----|
| Monday | After 11:30 → Next week |
| Tuesday | Next week trade (caution) |
| Wednesday | Current week |
| Thursday | Trade allowed |
| Friday | Trade allowed |

---

## Strike Selection Rules
ATM = nearest 50

| Day | CE | PE |
|----|----|----|
| Mon | +50 | -50 |
| Tue | +100 | -100 |
| Wed | +100 | -100 |
| Thu | +100 | -100 |
| Fri | +50 | -50 |

---

## Exit Rules
- SL / Target based on delta projection
- Time exit on/before 15:10 IST

---

## Phase-1 Scope
✔ Spot logic
✔ NIFTY option logic
✔ Streamlit UI
❌ Automation
❌ Order placement
❌ Greeks calculation

