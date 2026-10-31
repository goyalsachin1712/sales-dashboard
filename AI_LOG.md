# AI Usage Log — Peritus Inc. Sales Performance Dashboard

**Last updated:** 01 November 2026  
**Project status:** Dashboard implementation, local validation, code cleanup, GitHub publication, Streamlit Community Cloud deployment and hosted functional QA are complete.

- **Live dashboard:** https://peritus-sales-dashboard.streamlit.app/
- **GitHub repository:** https://github.com/goyalsachin1712/sales-dashboard

## 1. Project overview

- **Assessment:** AI-assisted interactive sales dashboard.
- **Objective:** Build a web-based explainable dashboard for sales, profitability, targets and operational performance.
- **Technology stack:** Python, Streamlit, pandas and Plotly.
- **Dataset:** `Sales_Dashboard_Candidate_Challenge.xlsx`.
- **Development environment:** VS Code / PowerShell with a Python virtual environment.
- **AI assistants used:** Claude and ChatGPT.

AI assistance supported planning, code development, troubleshooting, analytical reasoning, code review, validation design and documentation. AI-generated code and conclusions were not treated as correct until checked through local execution, independent calculations or visual inspection.

## 2. AI assistance and development record

AI assistants supported the project in the following areas:

1. **Approach and technology selection:** Helped compare implementation options and select a practical stack for an interactive analytical dashboard.
2. **Project setup and data loading:** Guided project structure, environment setup, Excel ingestion and dependency troubleshooting.
3. **Data inspection and validation:** Assisted in creating checks for workbook structure, data types, missing values, duplicates, data consistency and date coverage.
4. **Code development:** Assisted with the development and refinement of the Streamlit application and its supporting data, metrics and chart modules.
5. **KPI and business logic:** Helped define and implement KPI calculations, target comparisons, aggregation logic and safeguards based on the source data's grain.
6. **Dashboard functionality and design:** Supported the implementation of filters, dependent selections, drilldowns, KPI cards, charts, tables and transaction export.
7. **Error handling and troubleshooting:** Helped investigate runtime errors, calculation discrepancies, filter behaviour, chart issues and deployment-related configuration.
8. **Testing and quality assurance:** Suggested test scenarios and edge cases; supported validation of calculations, filters, target safeguards, drilldowns, reset behaviour and exports.
9. **Code review and documentation:** Assisted with code cleanup, dependency review, README preparation, business-finding refinement and this AI usage log.

The project owner reviewed and applied relevant suggestions, ran the application and validation scripts, checked calculations and dashboard behaviour, and remains responsible for the final implementation and conclusions.

## 3. Important corrections and analytical safeguards

1. **Weighted discount:** Weighted discount uses list value (`List_Unit_Price_INR × Units`) as the weight, rather than a simple average of row-level discount percentages. An independent calculation matched.
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

The project contains **18 manual validation scripts**, which the project owner reports executed successfully. The scripts cover:

- Source data and business-logic validation.
- Core KPI and monthly performance calculations.
- Independent weighted discount calculation.
- Product category, customer segment and sales channel filters.
- Region and representative filtering, including combined filter scenarios.
- Full-year and partial-date selections.
- One-complete-month and no-complete-month date cases.
- Target aggregation and target-comparison safeguards.
- Representative-level calculations and transaction filtering.

Additional UI tests and independent calculations performed during dashboard QA included:

- Full-dataset baseline KPIs.
- Global filters individually and in combination, including dependent representative availability.
- Target aggregation and unsupported-dimension safeguards.
- Geographic drilldown: Region → State → City.
- Product drilldown: Category → Subcategory → Product.
- Independent local drilldown behaviour.
- Reset all filters, including date range and local drilldowns.
- Empty-selection behaviour and partial-month target chart behaviour.
- Dynamic insight wording for single-group selections.
- Representative filter caption clarity and full representative-table coverage.
- Customer-segment customer-count reconciliation.
- Transaction export for Meera Bose: 286 rows; all records contained the selected representative and expected columns.
- Final regression checks, including Python syntax compilation, reset, combined filters and representative selection/clearing.

**Validation scope:** The project owner inspected chart responsiveness and tooltip/table consistency, but not every plotted chart mark was independently recalculated. Local QA was followed by deployment and hosted functional QA. The project owner confirmed the hosted checks were completed.

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

The 18 validation scripts are organised in `tests/`, while the four runtime modules (`app.py`, `data.py`, `metrics.py`, `charts.py`) and the `data/` workbook directory remain in the project root. Test scripts resolve imports from the project root; the business-logic validation script locates the workbook in the root `data/` directory.

These scripts are manual validation utilities, not a formal `pytest` suite.

## 8. AI use and human responsibility

AI assistants were used for planning, code generation, troubleshooting, validation design, technical explanations, code review and documentation. The project owner ran the application and scripts locally, independently reconciled key calculations, inspected UI behaviour, reviewed the hosted application, and revised suggestions that conflicted with the dataset grain or available evidence.

No AI-generated result was accepted solely because it was suggested by a model. The project owner remains responsible for understanding and explaining the code, calculations, limitations, findings and design trade-offs.

## Deployment record

- **Hosting platform:** Streamlit Community Cloud
- **Public application:** https://peritus-sales-dashboard.streamlit.app/
- **Source repository:** https://github.com/goyalsachin1712/sales-dashboard
- **Status:** Source published, application deployed and hosted functional QA completed.

The hosted checks covered application loading, data availability, filters, drilldowns, KPI and trend views, target safeguards, delivery and profitability analyses, representative and customer views, transaction data and export.

## Repository and workbook note

The assessment workbook is included in the repository under `data/Sales_Dashboard_Candidate_Challenge.xlsx` so the project can be run with the supplied dataset.
The workbook was supplied for the assessment and described as synthetic data suitable for interview use. 

The repository includes the application source, dependency file, validation scripts, README, AI usage log and analysis tracker. Credentials, secrets, local virtual environments and cache files should not be committed.
