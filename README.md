# Peritus Inc. — Sales Performance Dashboard

An interactive sales-performance dashboard developed for the Peritus assessment using **Python, Streamlit, pandas and Plotly**. It analyses transaction-line sales data from January 2024 to December 2025 and compares actual performance with monthly sales-representative targets wherever the available data supports a valid comparison.

> **Project status (31 October 2026):** The dashboard has a previously deployed Streamlit-hosted URL. The latest local code and QA updates are complete, but it has not yet been confirmed that this URL serves the latest source version. GitHub publication and hosted-environment verification remain open tasks.

**Previously deployed dashboard URL:** https://peritus-sales-dashboard.streamlit.app/
**Deployment status:** URL supplied by the project owner; current live availability and deployed-code version not independently verified.

## Dashboard capabilities

- Eight executive KPIs: Net Sales, Gross Profit, Gross Margin, Orders, Units Sold, Unique Customers, Return Rate by Value and On-Time Delivery (Line Level).
- Interactive filters for date range, region, product category, customer segment, sales channel and sales representative.
- Dependent Sales Representative options based on the date range and the other selection filters.
- Monthly sales trend with actuals and targets shown only for complete calendar months.
- Regional sales and profitability analysis, with geographic drilldown from Region to State to City.
- Product-category sales and profitability analysis, with drilldown from Category to Subcategory to Product.
- Region × Channel line-level delivery heatmap.
- Product-subcategory returns-versus-profitability analysis.
- Discount-band and profitability analysis.
- Sales representative performance chart and full comparison table.
- Customer segment performance comparison.
- Expandable filtered transaction-line data and export.

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
    └── 16 manual validation scripts
```

The four application modules remain in the project root. The `tests/` directory contains manual validation scripts; it is not a formal pytest suite. Test scripts were adjusted to resolve imports from the project root, and the business-logic validation script was adjusted to locate the workbook in the root `data/` directory.

> Confirm the final repository file list before publication. The tracker filename and test-folder contents shown above should match the committed project.

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
python tests/test13.py
python tests/test14.py
```

The remaining scripts can be run in the same way, for example `python tests/test2.py`. All 16 scripts in the current `tests/` folder were reported as executing successfully after the folder move and import/workbook-path adjustments.

These are manual validation utilities, not a formal automated pytest suite.

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

## Evidence-backed business patterns

The following are descriptive findings from the supplied dataset. They are not causal conclusions.

1. **Growth with stable margin:** 2025 Net Sales were ₹4,043.97M versus ₹3,556.70M in 2024 (+13.70%); Gross Profit increased 13.90%, while Gross Margin moved from 48.45% to 48.54% (+0.09 percentage points). Growth was accompanied by broadly stable aggregate margin; the underlying drivers are not established.
2. **November 2025 monthly exception:** November 2025 sales were 4.92% lower year over year, and Gross Margin was 46.96% versus 48.48% in November 2024. This warrants investigation but does not establish a cause or a recurring seasonal pattern.
3. **Regional delivery gap:** East line-level on-time delivery was 73.81%, compared with South 83.25%, West 84.29% and North 84.51%. East Partner delivery was 65.93%. This is a diagnostic signal for fulfilment investigation, not proof of operational cause.
4. **Product-category economics:** Hardware represented 46.28% of sales but 23.92% of Gross Profit, with 25.07% Gross Margin. Software represented 41.68% of Gross Profit with 75.93% Gross Margin; Services Gross Margin was 61.57%. A mix shift should not be assumed feasible without demand, capacity and cost-to-serve analysis.
5. **Discount/margin association:** Gross Margin was 48.55% in the 0–5% discount band, 47.40% in the >15–20% band and 45.24% above 20%. The >20% band represented only 1.63% of sales. This is an association, not evidence that discounts caused lower margins.

## Analytical limitations

- Net Sales is before returns; returns are reported separately.
- Campaign ROI cannot be calculated because campaign expenditure is not present.
- DSO cannot be calculated without invoice due dates and receivables balances.
- The supplied NPS field has not been validated for methodology and response population; its average must not be represented as official NPS.
- Descriptive comparisons do not establish causality.
- Two years of monthly data are insufficient to make strong claims about long-term seasonality.
- On-time delivery is a transaction-line-level measure. The source data includes 814 orders with mixed line-level delivery flags; an order-level measure would require a separately stated definition.

## QA status

Local validation covered source data and business logic, baseline KPIs, weighted discount, multiple filter combinations, representative selections, date-range edge cases, target aggregation and safeguards, reset behavior, empty selections, drilldowns and transaction export. All 16 manual validation scripts were reported as executing successfully after being moved into `tests/`. Syntax, calculation and regression checks also passed.

Chart responsiveness and tooltip/table consistency were visually inspected, but not every plotted mark was independently recalculated. The project owner supplied a previously deployed URL; the live application and whether it contains the latest code have not yet been independently verified. See `AI_LOG.md` and the analysis tracker for the recorded validation scope.

## Deployment and hosted verification

**Previously deployed dashboard URL:** https://peritus-sales-dashboard.streamlit.app/

**Hosting platform:** Streamlit-hosted deployment (exact deployment configuration and current build version to be confirmed).

The URL above was supplied by the project owner as the last deployed dashboard link. It is recorded here as the available deployment endpoint, not as proof that the current hosted build is live, healthy or up to date. Complete the following post-deployment checks after publishing/redeploying the final source version and before treating the project as submission-ready:

- [ ] POST-DEPLOYMENT: Open the supplied public URL in a fresh browser session and confirm the app loads.
- [ ] POST-DEPLOYMENT: Verify the workbook is available to the hosted app and data loads correctly.
- [ ] POST-DEPLOYMENT: Retest global filters and dependent Sales Representative options.
- [ ] POST-DEPLOYMENT: Retest geographic and product drilldowns.
- [ ] POST-DEPLOYMENT: Verify KPI cards, monthly trends and target safeguards.
- [ ] POST-DEPLOYMENT: Verify delivery, returns/profitability, discount and customer-segment views.
- [ ] POST-DEPLOYMENT: Verify the representative chart and full representative table.
- [ ] POST-DEPLOYMENT: Verify transaction data and export functionality.
- [ ] POST-DEPLOYMENT: Check deployment logs for errors, missing dependencies and file-path issues.
- [ ] POST-DEPLOYMENT: Record the verified public URL and hosting details in this README and the analysis tracker.
- [ ] POST-DEPLOYMENT: Capture final screenshots for the assessment submission.

Do not use the local Streamlit URL as a public submission link.

## Repository and submission checks

- [ ] Review `.gitignore`; exclude virtual environments, caches, secrets and local-only files.
- [ ] Confirm permission to redistribute the supplied assessment workbook before committing it to a public repository.
- [ ] Review the final repository contents and confirm all required source and documentation files are present.
- [ ] Publish the source repository and record its URL.
- [ ] Prepare the concise assessment submission note and walkthrough.

## Assessment deliverables

- Application source code and project files.
- Previously deployed dashboard URL: https://peritus-sales-dashboard.streamlit.app/ (retest and confirm latest build before submission).
- `AI_LOG.md` describing AI assistance and human validation.
- Three to five evidence-backed business insights with caveats.
- Analysis tracker documenting KPI definitions, decisions, limitations and QA evidence.
