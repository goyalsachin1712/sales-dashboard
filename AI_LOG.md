# AI Usage Log — Peritus Inc. Sales Performance Dashboard

**Last updated:** 31 October 2026
**Project status:** Application implementation, local functional QA, code cleanup and execution of the 16 manual validation scripts are complete as reported. A previously deployed dashboard URL has been supplied by the project owner. The latest hosted build has not yet been independently verified; GitHub publication/review and hosted-app verification remain open tasks.

**Previously deployed dashboard URL:** https://peritus-sales-dashboard.streamlit.app/
**Verification note:** URL supplied by the project owner; current availability and whether it serves the latest local source version have not been independently confirmed.

## 1. Project overview

- **Assessment:** AI-assisted interactive sales dashboard.
- **Objective:** Build an explainable dashboard for sales, profitability, targets and operational performance.
- **Technology stack:** Python, Streamlit, pandas and Plotly.
- **Dataset:** `Sales_Dashboard_Candidate_Challenge.xlsx`.
- **Development environment:** VS Code / PowerShell with a Python virtual environment.
- **AI assistants used:** Claude and ChatGPT.

AI assistance supported planning, code scaffolding, troubleshooting, analytical reasoning, code review, validation design and documentation. AI-generated code and conclusions were not treated as correct until checked through local execution, independent calculations or visual inspection.

## 2. AI assistance and development record

### 29 October 2026 — Planning and environment setup

- Claude assisted with comparing dashboard development approaches and selecting a practical technology stack.
- Alternatives considered included Streamlit, React, static HTML/JavaScript and AI-assisted application builders.
- Streamlit, pandas and Plotly were selected to prioritise implementation speed, analytical transparency and explainability.
- ChatGPT assisted with project setup and troubleshooting an Excel-loading error caused by the missing `openpyxl` dependency.

### 29 October 2026 — Data loading and validation

- ChatGPT assisted with the initial Excel data loader and data-quality validation scripts.
- The workbook sheets, columns, data types, row counts, missing values, duplicates, representative coverage, region consistency, financial calculations, return flags and date coverage were inspected.
- Loaded 15,000 sales transaction lines and 1,440 monthly target records.
- The inspected source sheets had no exact duplicate rows or missing values in the validated fields.
- All 60 sales representatives were represented in both datasets; representative-region assignments were consistent.
- Financial calculations, return flags and 24-month coverage from January 2024 through December 2025 passed the implemented checks.

### 29 October 2026 — KPI calculation layer

- ChatGPT assisted with a centralised KPI calculation module and monthly actual-versus-target calculations.
- Distinct orders use unique `Order_ID` values, not transaction-line counts.
- Gross Margin is total Gross Profit divided by total Net Sales.
- Net Sales follows the dataset definition: after discounts but before returns.
- Sales transactions and monthly targets are kept at their respective grains to prevent target duplication.
- Validation confirmed 24 chronological monthly performance records and reconciled basic sales and gross profit totals.

### 29–30 October 2026 — Dashboard implementation and refinement

ChatGPT assisted with implementation review, debugging, filter logic, chart behaviour, calculation explanations and iterative refinements. Implemented components include:

- `app.py`: Streamlit page, filters, KPI display, observations, target comparison and table layout.
- `data.py`: source workbook loading and preparation.
- `metrics.py`: centralised KPI and target calculations.
- `charts.py`: Plotly visualisations.
- Sidebar filters for date range, region, product category, customer segment, sales channel and sales representative.
- Eight executive KPIs, target attainment, monthly sales trend, regional/product views, delivery heatmap, returns/profitability analysis, representative chart/table, customer-segment analysis and filtered transaction data.
- Independent geographic and product drilldowns, with local selections kept separate from global dashboard filters.

### 31 October 2026 — Code cleanup and final local regression

ChatGPT assisted with a final code-quality review and consolidation of repeated calculation logic. The project owner applied the changes and ran the checks locally.

- Replaced deprecated Streamlit `use_container_width` arguments; a source search returned no remaining matches in the reviewed application modules.
- Centralised on-time delivery parsing in `parse_on_time_delivery()` and reused it across the KPI, summary and chart calculations.
- Centralised weighted discount calculation in `calculate_weighted_discount()` and reused it across the application and chart code.
- Reviewed candidate unused functions against the tests and validation scripts; no functions were removed because they remained referenced.
- Reviewed dependencies and pinned `openpyxl==3.1.5`.
- Parsed all 25 Python files successfully.
- Re-ran the four core validation commands; all passed:
  - `python tests\test_metrics_phase1.py`
  - `python tests\test_metrics.py`
  - `python tests\validate_business_logic.py`
  - `python tests\check_data.py`
- Reconciled the full-dataset KPI baseline against the established results.
- Confirmed the Streamlit app started locally.
- The project owner inspected the dashboard and confirmed the representative table includes all 60 representatives, the customer-segment totals reconcile to 800 customers, and the geographic/product drilldowns, filter combinations, reset behaviour and transaction export passed the recorded UI checks.

## 3. Important corrections and analytical safeguards

1. **Weighted discount:** Corrected the source column reference to `List_Unit_Price_INR`. Weighted discount uses list value (`List_Unit_Price_INR × Units`) as the weight. An independent calculation matched.
2. **Target grain:** Monthly targets are at Sales Representative × Month grain. Actuals and targets are aggregated separately; monthly targets are not joined directly to transaction-line data.
3. **Target dimensionality:** Target attainment is hidden when product category, customer segment or sales channel filters are narrowed because targets are not supplied at those dimensions.
4. **Complete months:** Full-month targets are compared only with actuals for calendar months fully contained in the selected date range. Partial-month actuals remain visible without a target value.
5. **Dynamic observations:** Single-region and single-product/subcategory selections use descriptive wording rather than unsupported “leader”, “lowest” or “weakest” comparisons.
6. **Representative filter:** Options depend on date and the other selection filters. Blank selection means all matching representatives. The caption distinguishes selected representatives from matching representatives.
7. **Reset behaviour:** Reset restores the date range, global filters and local drilldown selections.
8. **Delivery metric:** On-time delivery is labelled as a transaction-line-level metric, not an order-level rate.
9. **Monetary display:** Monetary values use ₹M (millions) consistently.
10. **Independent target aggregation:** Regional and representative target comparisons use independently aggregated actuals and targets at compatible grain; regional target comparisons are shown only at Region level.

## 4. Independent validation and functional QA

The project owner reports that all 16 validation scripts in the reorganised `tests/` folder executed successfully after path adjustments.

The scripts cover:
- Source data and business-logic validation.
- Core KPI and monthly performance calculations.
- Independent weighted discount calculation.
- Region + product category filtering.
- Product category, customer segment and sales channel filters.
- Representative KPI calculations.
- Multiple combined filters.
- Full-year and partial-date selections.
- One-complete-month and no-complete-month date cases.
- South region target attainment.
- Meera Bose representative calculation.

Additional UI tests and independent calculations performed during dashboard QA included:
- Full-dataset baseline KPIs.
- Region, category, segment and channel selections, individually and in combination.
- Representative selection and dependent representative availability.
- Target aggregation and target-comparison safeguards.
- Geographic drilldown: Region → State → City.
- Product drilldown: Category → Subcategory → Product.
- Independent local drilldown behaviour.
- Reset all filters, including date range and local drilldowns.
- Empty-selection behaviour.
- Partial-month target chart behaviour.
- Dynamic insight wording for single-group selections.
- Representative filter caption clarity.
- Customer-segment customer-count reconciliation.
- Transaction export for Meera Bose: 286 rows; all records contained the selected representative and expected columns.
- Final regression: Python syntax compilation, reset, combined filters, and representative selection/clearing.

**Validation scope:** The project owner inspected chart responsiveness and tooltip/table consistency, but not every plotted chart mark was independently recalculated. Local QA does not establish hosted-environment reliability. A previously deployed URL is available, but hosted verification of the current code version remains pending.

## 5. Baseline KPI reconciliation

Full dataset, January 2024–December 2025:

| KPI | Result |
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

## 6. Analytical limitations

- Net Sales is after discounts but before returns; returns are reported separately.
- On-time delivery of 82.35% is line-level. 814 orders contain mixed line-level delivery flags. An order-level measure requires a separately stated definition.
- Campaign ROI is not calculable because campaign expenditure is unavailable.
- DSO is not calculable without invoice due dates and receivables balances.
- The supplied NPS field's methodology and response population have not been validated; its average is not presented as official NPS.
- Descriptive comparisons do not establish causality.
- Two years of monthly data are insufficient for strong claims about long-term seasonality.

## 7. Test-folder organisation

The 16 validation scripts were moved into `tests/`, while the four runtime modules (`app.py`, `data.py`, `metrics.py`, `charts.py`) and the `data/` workbook directory remain in the project root. Test scripts were adjusted to resolve imports from the project root; the business-logic validation script was adjusted to locate the workbook in the root `data/` directory. The project owner reports that all scripts ran successfully after these changes.

These scripts are manual validation utilities, not a formal pytest suite.

## 8. AI use and human responsibility

AI assistants were used for planning, code generation, troubleshooting, validation design, technical explanations, code review and documentation. The project owner ran the application and scripts locally, independently reconciled key calculations, inspected UI behaviour, and revised suggestions that conflicted with the dataset grain or available evidence.

No AI-generated result was accepted solely because it was suggested by a model. The project owner remains responsible for understanding and explaining the code, calculations, limitations, findings and design trade-offs.

## 9. Deployment record and remaining work

The project owner supplied the following previously deployed dashboard URL: https://peritus-sales-dashboard.streamlit.app/. This confirms the existence of a deployment endpoint in the project record, but does not by itself establish current uptime, successful loading, or that the latest local code is deployed. The hosted version must be checked after the final source is published/redeployed.

### Before final redeployment / publication

- [ ] Review final repository contents and `.gitignore`.
- [ ] Confirm that the workbook is permitted to be included in the assessment repository.
- [ ] Review the final repository contents and `.gitignore`; exclude virtual environments, caches, secrets and local-only files.
- [ ] Confirm that the workbook is permitted to be included in the assessment repository.
- [ ] Publish the final source code to GitHub and record the repository URL.
- [ ] Confirm deployment configuration, dependency installation and workbook path.
- [ ] Redeploy the latest reviewed source to the existing Streamlit URL, if that is the intended production endpoint.

### After deployment — required before submission

- [ ] Confirm and record the hosting platform and public application URL (currently supplied URL: https://peritus-sales-dashboard.streamlit.app/).
- [ ] Open the public URL in a fresh browser session and confirm the app loads.
- [ ] Verify workbook loading and baseline KPI values in the hosted environment.
- [ ] Retest global filters and dependent Sales Representative options.
- [ ] Retest geographic and product drilldowns and their independent behaviour.
- [ ] Verify KPI cards, monthly trends and target-comparison safeguards.
- [ ] Verify delivery, returns/profitability, discount and customer-segment views.
- [ ] Verify the representative chart and full representative table.
- [ ] Verify transaction data and export functionality.
- [ ] Inspect hosted logs for errors, missing dependencies and path issues.
- [ ] Capture final hosted screenshots for assessment evidence.
- [ ] Update README, this log and the analysis tracker with verified deployment details and any fixes made.
- [ ] Update the analysis tracker and final submission note with hosted-QA evidence.

### Final assessment preparation

- [ ] Finalise three to five business insights and their caveats.
- [ ] Prepare the concise assessment submission note.
- [ ] Prepare the walkthrough covering data grain, KPI logic, target safeguards, design decisions, limitations and AI use.
