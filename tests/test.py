
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from data import load_sales_data

sales, targets = load_sales_data()

# Calculate weighted discount independently
sales["_list_value"] = (
    sales["List_Unit_Price_INR"] * sales["Units"]
)

sales["_discount_value"] = (
    sales["_list_value"] * sales["Discount_Pct"]
)

validation = (
    sales.groupby("Sales_Rep")
    .agg(
        List_Value=("_list_value", "sum"),
        Discount_Value=("_discount_value", "sum")
    )
)

validation["Expected_Weighted_Discount"] = (
    validation["Discount_Value"]
    / validation["List_Value"]
    * 100
)

print("\nOverall weighted discount:")
print(
    sales["_discount_value"].sum()
    / sales["_list_value"].sum()
    * 100
)

print("\nRepresentative-level validation:")
print(
    validation["Expected_Weighted_Discount"]
    .sort_values(ascending=False)
    .round(2)
)
