import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from data import load_sales_data

df, targets = load_sales_data()

filtered = df[
    (df["Sales_Rep"] == "Meera Bose")
].copy()

print("Rows:", len(filtered))
print("Net Sales:", filtered["Net_Sales_INR"].sum() / 1_000_000)
print("Gross Profit:", filtered["Gross_Profit_INR"].sum() / 1_000_000)
print(
    "Gross Margin:",
    filtered["Gross_Profit_INR"].sum()
    / filtered["Net_Sales_INR"].sum() * 100
)
print("Orders:", filtered["Order_ID"].nunique())

list_value = (
    filtered["List_Unit_Price_INR"] * filtered["Units"]
).sum()

weighted_discount = (
    (
        filtered["List_Unit_Price_INR"]
        * filtered["Units"]
        * filtered["Discount_Pct"]
    ).sum() / list_value
) * 100

print("Weighted Discount:", weighted_discount)