"""Validate Phase 1 metrics against the full Peritus assessment workbook."""

import sys
from pathlib import Path

# Add project root to Python import path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from pathlib import Path
import math
import pandas as pd

from metrics import (
    calculate_customer_concentration,
    calculate_customer_performance,
    calculate_discount_band_performance,
    calculate_target_attainment,
    calculate_target_performance_by_dimension,
    calculate_weighted_discount,
    calculate_year_over_year_performance,
    summarize_performance,
)

DATA_FILE = Path("data") / "Sales_Dashboard_Candidate_Challenge.xlsx"
if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Could not find {DATA_FILE}. Run this script from the project root."
    )

sales = pd.read_excel(DATA_FILE, sheet_name="Sales_Data")
targets = pd.read_excel(DATA_FILE, sheet_name="Monthly_Targets")

print("=" * 64)
print("PHASE 1 — FULL DATASET VALIDATION")
print("=" * 64)
print(f"Sales rows: {len(sales):,}")
print(f"Target rows: {len(targets):,}")

# 1. Weighted discount: compare function output with an independent calculation.
weighted_discount = calculate_weighted_discount(sales)
list_value = sales["List_Unit_Price_INR"] * sales["Units"]
independent_discount = (
    (list_value * sales["Discount_Pct"]).sum() / list_value.sum() * 100
)
assert math.isclose(weighted_discount, independent_discount, rel_tol=0, abs_tol=1e-10)
print(f"\n[PASS] Weighted discount: {weighted_discount:.4f}%")

# 2. Discount bands: all transaction lines should be represented exactly once.
discount_bands = calculate_discount_band_performance(sales)
assert int(discount_bands["Lines"].sum()) == len(sales)
assert math.isclose(
    discount_bands["Net_Sales_INR"].sum(), sales["Net_Sales_INR"].sum(),
    rel_tol=0, abs_tol=0.01
)
assert math.isclose(
    discount_bands["Gross_Profit_INR"].sum(), sales["Gross_Profit_INR"].sum(),
    rel_tol=0, abs_tol=0.01
)
print("\n[PASS] Discount-band reconciliation")
print(
    discount_bands[
        ["Discount_Band", "Lines", "Net_Sales_M", "Gross_Margin_Pct",
         "Weighted_Discount_Pct"]
    ].to_string(index=False, formatters={
        "Net_Sales_M": "{:,.2f}".format,
        "Gross_Margin_Pct": "{:.2f}%".format,
        "Weighted_Discount_Pct": "{:.2f}%".format,
    })
)

# 3. Customer performance: customer-level totals must reconcile to source sales.
customers = calculate_customer_performance(sales)
assert customers["Customer_ID"].nunique() == sales["Customer_ID"].nunique()
assert math.isclose(
    customers["Net_Sales_INR"].sum(), sales["Net_Sales_INR"].sum(),
    rel_tol=0, abs_tol=0.01
)
assert math.isclose(
    customers["Gross_Profit_INR"].sum(), sales["Gross_Profit_INR"].sum(),
    rel_tol=0, abs_tol=0.01
)
assert len(customers) == sales["Customer_ID"].nunique()
concentration = calculate_customer_concentration(customers)
assert concentration["Sales_Share_Pct"].is_monotonic_increasing
print(
    f"\n[PASS] Customer performance: {len(customers):,} customers; "
    f"customer sales reconcile to total sales"
)
print("\nCustomer concentration:")
print(concentration.to_string(index=False, formatters={
    "Net_Sales_INR": "{:,.2f}".format,
    "Sales_Share_Pct": "{:.2f}%".format,
}))

# 4. General dimension summary: regional and product hierarchy totals reconcile.
for dimension in ["Region", "State", "Product_Category", "Product_Subcategory"]:
    summary = summarize_performance(sales, dimension)
    assert math.isclose(
        summary["Net_Sales_INR"].sum(), sales["Net_Sales_INR"].sum(),
        rel_tol=0, abs_tol=0.01
    )
    assert math.isclose(
        summary["Gross_Profit_INR"].sum(), sales["Gross_Profit_INR"].sum(),
        rel_tol=0, abs_tol=0.01
    )
    print(f"[PASS] {dimension} summary reconciles ({len(summary)} groups)")

# 5. YoY: only comparable full calendar years should produce growth.
yoy = calculate_year_over_year_performance(sales)
assert yoy["Year"].tolist() == [2024, 2025]
assert yoy.loc[1, "Net_Sales_INR_YoY_Pct"] == yoy.loc[1, "Net_Sales_INR_YoY_Pct"]
assert yoy.loc[0, "Net_Sales_INR_YoY_Pct"] != yoy.loc[0, "Net_Sales_INR_YoY_Pct"]
print("\n[PASS] Year-over-year comparison")
print(yoy[[
    "Year", "Net_Sales_INR", "Net_Sales_INR_YoY_Pct",
    "Gross_Profit_INR", "Gross_Profit_INR_YoY_Pct",
    "Gross_Margin_Pct", "Gross_Margin_YoY_pp",
]].to_string(index=False, formatters={
    "Net_Sales_INR": "{:,.2f}".format,
    "Net_Sales_INR_YoY_Pct": "{:.2f}%".format,
    "Gross_Profit_INR": "{:,.2f}".format,
    "Gross_Profit_INR_YoY_Pct": "{:.2f}%".format,
    "Gross_Margin_Pct": "{:.2f}%".format,
    "Gross_Margin_YoY_pp": "{:.2f} pp".format,
}))

# 6. Region target performance: both actuals and targets must reconcile independently.
region_targets = calculate_target_performance_by_dimension(
    sales, targets, "Region"
)
assert math.isclose(
    region_targets["Actual_Sales_INR"].sum(), sales["Net_Sales_INR"].sum(),
    rel_tol=0, abs_tol=0.01
)
assert math.isclose(
    region_targets["Sales_Target_INR"].sum(),
    targets["Monthly_Sales_Target_INR"].sum(),
    rel_tol=0, abs_tol=0.01
)
print("\n[PASS] Regional target performance")
print(region_targets[[
    "Region", "Actual_Sales_M", "Sales_Target_M",
    "Sales_Gap_M", "Sales_Attainment_Pct",
]].to_string(index=False, formatters={
    "Actual_Sales_M": "₹{:,.2f}".format,
    "Sales_Target_M": "₹{:,.2f}".format,
    "Sales_Gap_M": "₹{:,.2f}".format,
    "Sales_Attainment_Pct": "{:.2f}%".format,
}))

# 7. Representative target performance: same reconciliation at rep grain.
rep_targets = calculate_target_performance_by_dimension(
    sales, targets, "Sales_Rep_ID"
)
assert rep_targets["Sales_Rep_ID"].nunique() == targets["Sales_Rep_ID"].nunique()
assert math.isclose(
    rep_targets["Actual_Sales_INR"].sum(), sales["Net_Sales_INR"].sum(),
    rel_tol=0, abs_tol=0.01
)
assert math.isclose(
    rep_targets["Sales_Target_INR"].sum(),
    targets["Monthly_Sales_Target_INR"].sum(),
    rel_tol=0, abs_tol=0.01
)
print(
    f"\n[PASS] Representative target performance: "
    f"{len(rep_targets)} representatives; actuals and targets reconcile"
)

# 8. Overall target attainment should reconcile with regional and rep outputs.
overall = calculate_target_attainment(sales, targets)
assert math.isclose(
    overall["sales_target"], region_targets["Sales_Target_INR"].sum(),
    rel_tol=0, abs_tol=0.01
)
assert math.isclose(
    overall["sales_target"], rep_targets["Sales_Target_INR"].sum(),
    rel_tol=0, abs_tol=0.01
)
print("\n[PASS] Overall target totals reconcile across region and rep summaries")
print(f"Sales attainment: {overall['sales_attainment_pct']:.2f}%")
print(f"Sales gap: ₹{overall['sales_gap'] / 1_000_000:,.2f}M")

print("\n" + "=" * 64)
print("ALL PHASE 1 FULL-DATASET CHECKS PASSED")
print("=" * 64)
