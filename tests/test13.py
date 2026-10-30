import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from data import load_sales_data

# Load original workbook data
sales, targets = load_sales_data()

# Selected dashboard filters
region = "South"
start_date = pd.Timestamp("2024-01-01")
end_date = pd.Timestamp("2025-12-31")

# Ensure date columns are datetime
sales["Order_Date"] = pd.to_datetime(sales["Order_Date"])
sales["Month_Start"] = pd.to_datetime(sales["Month_Start"])
targets["Month_Start"] = pd.to_datetime(targets["Month_Start"])

# Filter actual sales
filtered_sales = sales[
    (sales["Region"] == region)
    & (sales["Order_Date"] >= start_date)
    & (sales["Order_Date"] <= end_date)
].copy()

# Filter monthly targets independently
filtered_targets = targets[
    (targets["Region"] == region)
    & (targets["Month_Start"] >= start_date)
    & (targets["Month_Start"] <= end_date)
].copy()

# Aggregate actual performance
actual_sales = filtered_sales["Net_Sales_INR"].sum()
actual_gp = filtered_sales["Gross_Profit_INR"].sum()
actual_units = filtered_sales["Units"].sum()

# Aggregate targets
sales_target = filtered_targets["Monthly_Sales_Target_INR"].sum()
gp_target = filtered_targets["Monthly_GP_Target_INR"].sum()
units_target = filtered_targets["Units_Target"].sum()

# Calculate attainment
print("\n--- SOUTH REGION TARGET VALIDATION ---")

print(f"Sales actual: ₹{actual_sales:,.2f}")
print(f"Sales target: ₹{sales_target:,.2f}")
print(f"Sales attainment: {actual_sales / sales_target * 100:.2f}%")

print(f"\nGross Profit actual: ₹{actual_gp:,.2f}")
print(f"Gross Profit target: ₹{gp_target:,.2f}")
print(f"Gross Profit attainment: {actual_gp / gp_target * 100:.2f}%")

print(f"\nUnits actual: {actual_units:,}")
print(f"Units target: {units_target:,}")
print(f"Units attainment: {actual_units / units_target * 100:.2f}%")

print("\n--- VALIDATION DETAILS ---")
print(f"Filtered sales rows: {len(filtered_sales):,}")
print(f"Filtered target rows: {len(filtered_targets):,}")
print(f"Distinct sales representatives: {filtered_sales['Sales_Rep'].nunique()}")
print(f"Distinct target representatives: {filtered_targets['Sales_Rep'].nunique()}")
print(f"Distinct target months: {filtered_targets['Month_Start'].nunique()}")