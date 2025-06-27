# nano-sec-case-study

**TRB/USDT Spot-Perpetual Market Analysis for NanoSec**

---

## Overview

This repository contains the technical deliverables for the NanoSec Quantitative Researcher case study. The objective was to analyze high-frequency TRB/USDT Spot and Perpetual market data to:

✅ Detect rapid price movements  
✅ Quantify cross-market reactions within milliseconds  
✅ Evaluate market leadership in price discovery  
✅ Provide actionable signal logic for trading applications  

---

## Contents

- `spot_perp_analysis.py` → Full Python detection and analysis script  
- `market_summary.txt` → Leadership breakdown: Spot vs. Futures  
- `output.txt` → Full list of detected price events and reactions  
- `README.md` → Repository documentation  

---

## Key Findings

- 184 sudden spot price moves (±0.07% within 3ms)  
- 50 futures reactions within 5ms after spot moves  
- Spot market leads in 73.53% of observed events  
- Futures market leads in 26.47% of events  

These results indicate the TRB/USDT Spot market demonstrates stronger price discovery influence within the tested timeframe.

---

## How to Run the Analysis

1. Ensure you have Python 3.x and `pandas` installed  
2. Place the following files in the project directory:  
   - `spot.csv` (Spot order book data)  
   - `futures.csv` (Perpetual order book data)  
3. Run the analysis:

```bash
python spot_perp_analysis.py

