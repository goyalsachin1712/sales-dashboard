
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "Sales_Dashboard_Candidate_Challenge.xlsx"
)

sales = pd.read_excel(DATA_FILE, sheet_name="Sales_Data")
targets = pd.read_excel(DATA_FILE, sheet_name="Monthly_Targets")

print("=" * 60)
print("BUSINESS LOGIC VALIDATION")
print("=" * 60)

# 1. Validate monthly target uniqueness
target_key = ["Month_Start", "Sales_Rep_ID"]
duplicate_targets = targets.duplicated(target_key).sum()

print(f"\nDuplicate monthly rep targets: {duplicate_targets}")

# 2. Validate sales representative coverage
sales_reps = set(sales["Sales_Rep_ID"])
target_reps = set(targets["Sales_Rep_ID"])

print(f"Sales reps in sales data: {len(sales_reps)}")
print(f"Sales reps in target data: {len(target_reps)}")
print(f"Reps missing targets: {sorted(sales_reps - target_reps)}")
print(f"Target-only reps: {sorted(target_reps - sales_reps)}")

# 3. Validate rep-region consistency
sales_rep_regions = sales[
    ["Sales_Rep_ID", "Region"]
].drop_duplicates()

target_rep_regions = targets[
    ["Sales_Rep_ID", "Region"]
].drop_duplicates()

print(
    "\nSales reps assigned to multiple regions:",
    int(
        (sales_rep_regions.groupby("Sales_Rep_ID")["Region"]
         .nunique() > 1).sum()
    ),
)

print(
    "Target rep-region mismatches:",
    len(
        sales_rep_regions.merge(
            target_rep_regions,
            on=["Sales_Rep_ID", "Region"],
            how="left",
            indicator=True,
        ).query("_merge == 'left_only'")
    ),
)

# 4. Validate financial calculations
profit_difference = (
    sales["Net_Sales_INR"]
    - sales["COGS_INR"]
    - sales["Gross_Profit_INR"]
).abs()

margin_difference = (
    sales["Gross_Profit_INR"] / sales["Net_Sales_INR"]
    - sales["Gross_Margin_Pct"]
).abs()

print("\nFinancial reconciliation:")
print(
    "Rows with profit difference > 0.02 INR:",
    int((profit_difference > 0.02).sum()),
)
print(
    "Rows with margin difference > 0.0001:",
    int((margin_difference > 0.0001).sum()),
)

# 5. Validate return flags and return amounts
return_flag = sales["Returned_Flag"].eq("Yes")
return_amount = sales["Return_Amount_INR"].gt(0)

print("\nReturn validation:")
print(
    "Returned rows with zero return amount:",
    int((return_flag & ~return_amount).sum()),
)
print(
    "Non-returned rows with positive return amount:",
    int((~return_flag & return_amount).sum()),
)

# 6. Validate date coverage
print("\nDate coverage:")
print("Sales:", sales["Month_Start"].min(), "to",
      sales["Month_Start"].max())
print("Targets:", targets["Month_Start"].min(), "to",
      targets["Month_Start"].max())
print("Sales months:", sales["Month_Start"].nunique())
print("Target months:", targets["Month_Start"].nunique())

print("\nValidation script completed.")
