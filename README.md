# Peritus Inc. — Sales Performance Dashboard

An interactive sales-performance dashboard built for the Peritus assessment using **Python, Streamlit, pandas and Plotly**. It analyses transaction-line sales data from January 2024 to December 2025 and compares actual performance with monthly sales-representative targets where the available data supports a valid comparison.

> **Project status (30 October 2026):** Local functional QA and all 16 validation scripts have been run successfully after the test-folder reorganisation. GitHub publication, public deployment and hosted-link verification remain pending.

## Dashboard capabilities

- Eight executive KPIs: Net Sales, Gross Profit, Gross Margin, Orders, Units Sold, Unique Customers, Return Rate by Value and On-Time Delivery (Line Level).
- Interactive filters for date range, region, product category, customer segment, sales channel and sales representative.
- Dependent Sales Representative options based on the date range and the other four selection filters.
- Monthly sales trend with actuals and targets shown only for complete calendar months.
- Regional and product-category sales/profitability comparisons.
- Region × Channel line-level delivery heatmap.
- Product-subcategory returns-versus-profitability analysis.
- Sales representative performance chart and full comparison table.
- Expandable filtered transaction-line data.

## Technology

- Python
- Streamlit
- pandas
- Plotly
- openpyxl for Excel workbook ingestion

Exact package requirements are maintained in `requirements.txt`.

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
├── Peritus_Sales_Dashboard_Analysis_Tracker_v2.docx
├── data/
│   └── Sales_Dashboard_Candidate_Challenge.xlsx
└── tests/
    ├── validate_business_logic.py
    ├── check_data.py
    ├── test.py
    ├── test_metrics.py
    ├── test2.py
    ├── test3.py
    ├── test4.py
    ├── test5.py
    ├── test6.py
    ├── test8.py
    ├── test9.py
    ├── test10.py
    ├── test11.py
    ├── test12.py
    ├── test13.py
    └── test14.py
```

The four application modules remain in the project root. The `tests/` directory contains manual validation scripts; it is not a formal pytest test suite. Test scripts add the project root to the Python import path so they can be run from the project root after reorganisation.

## Run locally

1. Install Python compatible with the packages pinned in `requirements.txt`.
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

Run commands from the project root with the virtual environment activated. Examples:

```powershell
python tests/check_data.py
python tests/validate_business_logic.py
python tests/test_metrics.py
python tests/test13.py
python tests/test14.py
```

The remaining scripts can be run in the same way, for example `python tests/test2.py`. All 16 scripts in the current `tests/` folder were reported as executing successfully after the folder move and import/workbook-path adjustments.

## Data and KPI definitions

The source workbook contains:
- `Sales_Data`: 15,000 transaction lines.
- `Monthly_Targets`: 1,440 monthly target records at Sales Representative × Month grain.
- `Challenge_Brief` and `Data_Dictionary`: assessment context and field definitions.

Key calculation rules:
- **Net Sales:** sum of `Net_Sales_INR`; after discounts but before returns.
- **Gross Profit:** sum of `Gross_Profit_INR`.
- **Gross Margin:** total Gross Profit ÷ total Net Sales × 100; do not average row-level margins.
- **Orders:** distinct `Order_ID`, not transaction-line count.
- **Return Rate by Value:** total `Return_Amount_INR` ÷ total Net Sales × 100.
- **On-Time Delivery:** share of transaction lines flagged on time; explicitly labelled line-level.
- **Weighted Discount:** weighted by list value (`List_Unit_Price_INR × Units`), not a simple average of row-level discount percentages.

### Target-comparison safeguards

Monthly targets are defined at Sales Representative × Month grain. Actuals and targets are aggregated independently at compatible dimensions; targets are not joined directly to transaction lines. Target attainment is suppressed when product category, customer segment or sales channel filters are narrowed because targets are not supplied at those dimensions. Partial calendar months are not compared with full-month targets. In the monthly chart, actuals remain visible for partial months while target values are shown only for complete months.

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

## QA status

Local functional testing and independent calculations covered baseline KPIs, weighted discount, multiple filter combinations, representative selections, date-range edge cases, target aggregation and safeguards, reset behavior, empty selections and transaction export. All 16 validation scripts were run successfully after being moved into `tests/`. Dashboard chart responsiveness was visually inspected, but not every plotted mark was independently recalculated. Hosted deployment has not yet been tested. See `AI_LOG.md` and the analysis tracker for details.

## Deployment

Deployment instructions and the public application URL will be added after the hosted app is published and tested. Do not treat the local Streamlit URL as a public submission link.

## Assessment deliverables

- Application source code and project files.
- Hosted dashboard link (pending deployment).
- `AI_LOG.md` describing AI assistance and human validation.
- Three to five evidence-backed business insights, with caveats, recorded in the analysis tracker and final submission notes.
