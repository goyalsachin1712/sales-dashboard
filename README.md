# Peritus Inc. — Sales Performance Dashboard

An interactive sales-performance dashboard developed for the Peritus Inc. assessment using **Python, Streamlit, pandas and Plotly**. It analyses transaction-line sales data from January 2024 to December 2025 and compares actual performance with monthly sales-representative targets wherever the available data supports a valid comparison.

**Project status (01 November 2026):** The dashboard is deployed on Streamlit Community Cloud, the source repository has been published to GitHub, and hosted functional QA has been completed.

- **Live dashboard:** https://peritus-sales-dashboard.streamlit.app/
- **GitHub repository:** https://github.com/goyalsachin1712/sales-dashboard

## Dashboard capabilities

The dashboard is designed for VP Sales and Regional Sales Leaders. It provides:

- **Executive KPIs:** Net Sales, Gross Profit, Gross Margin, Orders, Units Sold, Unique Customers, Return Rate by Value and On-Time Delivery (Line Level).
- **Global filters:** Date range, region, product category, customer segment, sales channel and sales representative.
- **Dependent representative filter:** Available Sales Representative options respond to the date range and other global selections.
- **Sales trend and target tracking:** Monthly actual sales against targets, with target comparisons restricted to complete calendar months.
- **Regional performance:** Sales and profitability analysis with geographic drilldown from Region to State to City.
- **Product performance:** Category sales and profitability with drilldown from Category to Subcategory to Product.
- **Delivery analysis:** Region × Channel heatmap using transaction-line delivery flags.
- **Returns and profitability:** Product-subcategory comparison of returns and profitability.
- **Discount analysis:** Discount-band performance and its observed relationship with gross margin.
- **Sales representative performance:** Top-15 representative chart and a full comparison table.
- **Customer segment analysis:** Performance comparison across Enterprise, Mid-Market and SMB segments.
- **Transaction detail:** Expandable filtered transaction-line data and export.

Drilldown selectors for geographic and product analysis are local to their respective sections; they do not change the global dashboard filters or unrelated analysis sections.

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
├── Peritus_Sales_Dashboard_Analysis_Tracker_v2.2.docx
├── data/
│   └── Sales_Dashboard_Candidate_Challenge.xlsx
└── tests/
    ├── check_data.py
    ├── validate_business_logic.py
    ├── test_metrics.py
    ├── test_metrics_phase1.py
    ├── validate_phase1_dataset.py
    └── additional manual validation scripts
```

The application is split into four modules:

- `app.py` — Streamlit application layout, filters and dashboard orchestration.
- `data.py` — source workbook loading.
- `metrics.py` — KPI and target-performance calculations.
- `charts.py` — Plotly chart construction.

The `tests/` directory contains **18 manual validation scripts**. These are validation utilities rather than a formal `pytest` test suite. The project also includes an analysis tracker documenting KPI definitions, analytical decisions, limitations and QA evidence.

## Run locally

1. Install a Python version compatible with the packages pinned in `requirements.txt`.
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
python tests/test_metrics_phase1.py
python tests/validate_phase1_dataset.py
python tests/test13.py
python tests/test14.py
```

The project contains 18 scripts in `tests/`. They can be run individually in the same way, for example `python tests/test2.py`.

These scripts provide data checks, metric validation, business-logic checks and scenario-based/manual regression coverage. They should not be described as a formal automated `pytest` suite.

## Data and KPI definitions

The supplied workbook contains:

- `Sales_Data`: 15,000 transaction lines.
- `Monthly_Targets`: 1,440 monthly target records at Sales Representative × Month grain.
- `Challenge_Brief` and `Data_Dictionary`: assessment context and field definitions.

The two main data sources have different grains:

- **Sales data:** transaction-line grain. An order can contain multiple lines.
- **Monthly targets:** Sales Representative × Month grain.

Key calculation rules:

- **Net Sales:** sum of `Net_Sales_INR`; after discounts but before returns.
- **Gross Profit:** sum of `Gross_Profit_INR`.
- **Gross Margin:** total Gross Profit ÷ total Net Sales × 100; row-level margins are not averaged.
- **Orders:** distinct `Order_ID`, not transaction-line count.
- **Units:** sum of `Units`.
- **Customers:** distinct `Customer_ID`.
- **Return Rate by Value:** total `Return_Amount_INR` ÷ total Net Sales × 100.
- **On-Time Delivery:** share of transaction lines flagged on time; the KPI and related views are explicitly labelled line-level.
- **Weighted Discount:** weighted by list value (`List_Unit_Price_INR × Units`), not a simple average of row-level discount percentages.

### Target-comparison safeguards

Monthly targets are defined at Sales Representative × Month grain. Actuals and targets are aggregated independently at compatible dimensions; targets are not joined directly to transaction lines, which would risk duplicating target values.

Target comparisons are supported at the appropriate month, region and sales-representative levels. Target attainment is suppressed when product category, customer segment or sales channel filters are narrowed because targets are not supplied at those dimensions. Partial calendar months are not compared with full-month targets. In the monthly chart, actuals remain visible for partial months while target values are shown only for complete months.

## Full-dataset baseline

The following baseline covers January 2024–December 2025 with no filters:

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

## Business findings and areas for investigation

The findings below are descriptive observations from the supplied dataset. They identify areas for management attention; they do not establish causality or prove what operational action will produce a particular result.

1. **Revenue growth was accompanied by broadly stable gross margin.** 2025 Net Sales were ₹4,043.97M compared with ₹3,556.70M in 2024, an increase of 13.70%. Gross Profit increased by 13.90%, while Gross Margin moved from 48.45% to 48.54% (+0.09 percentage points). This indicates that aggregate margin was broadly maintained during the year-on-year growth period. A useful next step would be to examine growth contributions by region, category and representative, then test whether the growth is concentrated in a small number of areas.

2. **November 2025 is a month-level performance exception worth investigating.** Net Sales were 4.92% lower than November 2024, while Gross Margin was 46.96% compared with 48.48% in November 2024. This combination suggests that both revenue and margin merit a closer review for that month. The dataset alone does not identify whether the difference reflects product mix, discounting, customer mix, timing or another factor; nor does one comparison establish a recurring seasonal pattern.

3. **The East region has a material delivery-performance gap in the supplied line-level data.** East recorded 73.81% on-time delivery, compared with South at 83.25%, West at 84.29% and North at 84.51%. Within East, the Partner channel recorded 65.93%. This makes East—and particularly East Partner—a sensible starting point for an operational diagnostic. Before drawing conclusions about teams or suppliers, validate the underlying order and line records and investigate the relevant fulfilment processes.

4. **Sales contribution and gross-margin contribution differ substantially by product category.** Hardware generated 46.28% of Net Sales but 23.92% of Gross Profit, with a 25.07% Gross Margin. Software generated 41.68% of Gross Profit and had a 75.93% Gross Margin; Services had a 61.57% Gross Margin. This points to materially different category economics. It does not, by itself, justify shifting sales toward a higher-margin category: demand, addressable market, delivery capacity, cost-to-serve and strategic role would also need to be assessed.

5. **Higher discount bands show lower observed gross margins, but the relationship is not proof of discount impact.** Gross Margin was 48.55% in the 0–5% discount band, 47.40% in the >15–20% band and 45.24% above 20%. The >20% band represented only 1.63% of sales, so it is a relatively small part of the overall sales base. The pattern supports reviewing high-discount transactions and their commercial rationale, while controlling for product and customer mix before changing discount policy.

## Analytical limitations and interpretation

- Net Sales is measured after discounts but before returns; returns are reported separately.
- Campaign ROI cannot be calculated because campaign expenditure is not present.
- Days Sales Outstanding (DSO) cannot be calculated without invoice due dates and receivables balances.
- The supplied NPS field has not been validated for methodology and response population; its average must not be represented as official NPS.
- Descriptive comparisons do not establish causality.
- Two years of monthly data are insufficient to make strong claims about long-term seasonality.
- On-time delivery is a transaction-line-level measure. The source data includes 814 orders with mixed line-level delivery flags; an order-level measure would require a separately stated definition.
- Targets are not available at product, customer, segment or channel grain. Target attainment must not be inferred for those dimensions.
- The dataset does not include campaign spend or sufficient receivables information for the related commercial/finance metrics noted above.

## Quality assurance

Local validation covered:

- Source data structure and business logic.
- Baseline KPI calculations and weighted discount.
- Global filter combinations and dependent representative selections.
- Date-range edge cases and partial-month handling.
- Target aggregation, target safeguards and unsupported-dimension suppression.
- Reset behavior and empty-result states.
- Geographic and product drilldowns, including their independent behavior.
- Representative chart and full representative table.
- Transaction-line data and export behavior.

All **18 manual validation scripts** were reported as executing successfully. Syntax, calculation and regression checks also passed. The hosted application was subsequently deployed and hosted functional QA was completed by the project owner.

Chart responsiveness and tooltip/table consistency were visually inspected; not every plotted mark was independently recalculated. See `AI_LOG.md` and the analysis tracker for the recorded validation scope and evidence.

## Deployment

- **Platform:** Streamlit Community Cloud
- **Live dashboard:** https://peritus-sales-dashboard.streamlit.app/
- **Source repository:** https://github.com/goyalsachin1712/sales-dashboard

The application has been deployed and the hosted functional QA has been completed. The checks covered application loading, data availability, filters, drilldowns, KPI and trend views, target safeguards, delivery and profitability analyses, representative and customer views, transaction data and export.

For a later code change, push the updated source to the connected GitHub branch and confirm that Streamlit Community Cloud has completed the redeployment. Re-run the relevant hosted checks after each material change.

## Repository and workbook note

The assessment workbook is included in the repository under `data/Sales_Dashboard_Candidate_Challenge.xlsx` so the project can be run with the supplied dataset.

The workbook was supplied for the assessment and described as synthetic data suitable for interview use. 

The repository also includes `.gitignore`, the application source, dependency file, validation scripts, README, AI usage log and analysis tracker. Do not commit credentials, secrets, local virtual environments or cache files.

## Assessment deliverables

- Application source code and project files in the GitHub repository.
- Deployed dashboard: https://peritus-sales-dashboard.streamlit.app/
- `AI_LOG.md` describing AI assistance and human validation.
- Three to five evidence-backed business findings with appropriate caveats.
- Analysis tracker documenting KPI definitions, analytical decisions, limitations and QA evidence.
