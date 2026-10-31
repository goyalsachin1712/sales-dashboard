# Peritus Inc. — Sales Performance Dashboard

An interactive sales-performance dashboard built for the Peritus assessment using **Python, Streamlit, pandas and Plotly**. It analyses transaction-line sales data from January 2024 to December 2025 and compares actual performance with monthly sales-representative targets where the available data supports a valid comparison.

> **Project status (01 November 2026):** The latest dashboard source is published to GitHub and deployed to Streamlit Community Cloud. Local technical validation and hosted functional QA have been completed. Final business insights and assessment preparation materials remain in progress.

- **Live dashboard:** https://peritus-sales-dashboard.streamlit.app/
- **Source repository:** https://github.com/goyalsachin1712/sales-dashboard

## Dashboard capabilities

- Eight executive KPIs: Net Sales, Gross Profit, Gross Margin, Orders, Units Sold, Unique Customers, Return Rate by Value and On-Time Delivery (Line Level).
- Global filters for date range, region, product category, customer segment, sales channel and sales representative.
- Dependent Sales Representative options based on the date range and other selection filters.
- Monthly sales trend with actuals and targets shown only for complete calendar months.
- Regional and product-category sales/profitability comparisons.
- Independent geographic drilldown from Region to State to City.
- Independent product drilldown from Category to Subcategory to Product.
- Region × Channel line-level delivery heatmap.
- Product-subcategory returns-versus-profitability analysis.
- Sales representative performance chart and full comparison table.
- Dynamic key performance observations, with descriptive wording when only one comparison group remains.
- Expandable filtered transaction-line data and export.

## Technology

- **Python:** application logic and calculations.
- **Streamlit:** interactive web application and hosting.
- **pandas:** workbook ingestion, filtering, grouping and data transformations.
- **Plotly:** interactive charts and visualisations.
- **openpyxl:** Excel workbook ingestion.

Exact package versions are maintained in `requirements.txt`.

## Project structure

```text
sales-dashboard/
├── app.py
├── charts.py
├── data.py
├── metrics.py
├── requirements.txt
├── README.md
├── AI_LOG.md
├── .gitignore
├── Peritus_Sales_Dashboard_Analysis_Tracker_v2.2.docx
├── data/
│   └── Sales_Dashboard_Candidate_Challenge.xlsx
└── tests/
    ├── check_data.py
    ├── validate_business_logic.py
    ├── validate_phase1_dataset.py
    ├── test_metrics.py
    ├── test_metrics_phase1.py
    └── additional manual validation scripts
```

### Main application files

- `app.py` — Streamlit page, global filters, KPI presentation, target comparisons, key observations, drilldown controls, tables and layout.
- `data.py` — loads and prepares sales and target data from the source workbook.
- `metrics.py` — centralises KPI, performance, return, discount and target calculations.
- `charts.py` — creates Plotly charts used by the dashboard.
- `requirements.txt` — pins Python package dependencies.
- `tests/` — manual validation scripts; this is not a formal pytest suite.
- `Peritus_Sales_Dashboard_Analysis_Tracker_v2.2.docx` — analysis, KPI definitions, findings, assumptions, limitations and QA register.
- `AI_LOG.md` — AI assistance and human review/validation record.

## Run locally

1. Install a Python version compatible with the packages in `requirements.txt`.
2. Open PowerShell in the project root.
3. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Start the dashboard:

   ```powershell
   streamlit run app.py
   ```

6. Open the local URL printed by Streamlit (normally `http://localhost:8501`).

## Run validation scripts

Run commands from the project root with the virtual environment activated:

```powershell
python tests/check_data.py
python tests/validate_business_logic.py
python tests/validate_phase1_dataset.py
python tests/test_metrics.py
python tests/test_metrics_phase1.py
```

The `tests/` directory contains 18 Python scripts. Sixteen earlier manual validation scripts were reported as successfully executed after the test-folder reorganisation. The two subsequently added scripts were also run; the five core commands above were rerun successfully during final repository preparation. These are manual validation utilities, not a formal pytest suite.

## Data and KPI definitions

The source workbook contains:
- `Sales_Data`: 15,000 transaction lines.
- `Monthly_Targets`: 1,440 monthly target records at Sales Representative × Month grain.
- `Challenge_Brief` and `Data_Dictionary`: assessment context and field definitions.

Key calculation rules:

- **Net Sales:** sum of `Net_Sales_INR`; after discounts but before returns.
- **Gross Profit:** sum of `Gross_Profit_INR`.
- **Gross Margin:** total Gross Profit ÷ total Net Sales × 100; row-level margins are not averaged.
- **Orders:** distinct `Order_ID`, not transaction-line count.
- **Units Sold:** sum of `Units`.
- **Unique Customers:** distinct `Customer_ID`.
- **Return Rate by Value:** total `Return_Amount_INR` ÷ total Net Sales × 100.
- **On-Time Delivery:** share of transaction lines flagged on time; explicitly labelled line-level.
- **Weighted Discount:** weighted by list value (`List_Unit_Price_INR × Units`), not a simple average of row-level discount percentages.

### Target-comparison safeguards

Monthly targets are defined at Sales Representative × Month grain. Actuals and targets are aggregated independently at compatible dimensions; monthly targets are not joined directly to transaction lines. Target attainment is suppressed when product category, customer segment or sales channel filters are narrowed because targets are not supplied at those dimensions. Partial calendar months are not compared with full-month targets. In the monthly chart, actuals remain visible for partial months while target values are shown only for complete months.

## Full-dataset baseline

For January 2024–December 2025 with no filters:

| KPI | Baseline |
|---|---:|
| Net Sales | ₹7,600.68M |
| Gross Profit | ₹3,686.15M |
| Gross Margin | 48.50% |
| Orders | 11,777 |
| Units Sold | 68,662 |
| Unique Customers | 800 |
| Return Rate by Value | 3.11% |
| On-Time Delivery (Line Level) | 82.35% |
| Sales Target Attainment | 96.16% |
| Gross Profit Target Attainment | 96.25% |
| Units Target Attainment | 96.58% |

## Analytical limitations

- Net Sales is before returns; returns are reported separately.
- Campaign ROI cannot be calculated because campaign expenditure is not present.
- DSO cannot be calculated without invoice due dates and receivables balances.
- The supplied NPS field has not been validated for methodology and response population; its average must not be represented as official NPS.
- Descriptive comparisons do not establish causality.
- Two years of monthly data are insufficient to make strong claims about long-term seasonality.
- On-time delivery is measured at transaction-line level, not order level.

## QA and deployment status

- Local Python syntax, KPI, data-quality, target-grain and business-logic validations were run successfully.
- Global filters, combined-filter behaviour, target safeguards, geographic and product drilldowns, reset/empty states and transaction-data/export behaviour were tested locally.
- The dashboard was deployed to Streamlit Community Cloud from the GitHub `main` branch. The deployment log showed dependency processing, GitHub code retrieval and `Updated app!`.
- The project owner confirmed that hosted functional QA was completed.
- Visual inspection was performed, but not every plotted mark was independently recalculated.

See `AI_LOG.md` for the chronological AI-use and validation record. The analysis tracker contains detailed KPI definitions, candidate findings, assumptions, limitations and QA status.

## Assessment submission

Peritus requests:

1. **Working web application:** https://peritus-sales-dashboard.streamlit.app/
2. **Source code/repository:** https://github.com/goyalsachin1712/sales-dashboard
3. **Brief AI tools note:** `AI_LOG.md` contains the detailed record
4. **Three to five key business insights:** final selection, figure verification and recommendations remain in progress.

The repository includes the synthetic assessment workbook. The assessment brief describes the data as synthetically generated and safe for interview use; this README does not represent that statement as a separate public redistribution licence.
