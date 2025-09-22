# Data Science Portfolio

This repository contains interactive Dash applications for financial analysis:

## Apps

- **DCF Model** ([dcf/app_dcf.py](dcf/app_dcf.py)): Discounted Cash Flow dashboard to visualize valuation based on cash flow and growth assumptions.
- **Portfolio Optimization** ([portfolio/app_portfolio.py](portfolio/app_portfolio.py)): Efficient Frontier dashboard to explore risk-return tradeoffs.
- **Scenario Analysis** ([scenario/app_scenario.py](scenario/app_scenario.py)): Scenario & sensitivity analysis for key financial drivers.
- **PMMS Dashboard** ([pmms/app_pmms.py](pmms/app_pmms.py)): Visualizes historical weekly mortgage rates from Freddie Mac.

## Structure

```
dcf/
    app_dcf.py
    requirements.txt
pmms/
    app_pmms.py
    historicalweeklydata.xlsx
    requirements.txt
portfolio/
    app_portfolio.py
    requirements.txt
scenario/
    app_scenario.py
    requirements.txt
requirements.txt
Procfile
README.md
```

## Setup

1. **Install dependencies**  
   Use the root [requirements.txt](requirements.txt) or app-specific files:
   ```sh
   pip install -r requirements.txt
   ```

2. **Run an app locally**  
   Example for DCF:
   ```sh
   python dcf/app_dcf.py
   ```
   Replace with the desired app path.

3. **Deployment**  
   The [Procfile](Procfile) is set up for deployment with Gunicorn:
   ```
   web: gunicorn app:server
   ```
   Make sure your entry-point app exposes `server`.

## Notes

- For the PMMS dashboard, ensure [historicalweeklydata.xlsx](pmms/historicalweeklydata.xlsx) is present in the `pmms` folder.
- All apps use Dash and Plotly for interactive visualization.

---
Document basic DataScience learnings
