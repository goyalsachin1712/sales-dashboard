
import sys
from pathlib import Path

# Add project root to Python import path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

"""Small deterministic tests for Phase 1 metric helpers."""
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

sales = pd.DataFrame({
    "Order_ID": ["O1", "O2", "O3", "O4"],
    "Customer_ID": ["C1", "C1", "C2", "C3"],
    "Customer_Name": ["A", "A", "B", "C"],
    "Segment": ["Enterprise", "Enterprise", "SMB", "SMB"],
    "Industry": ["IT", "IT", "Retail", "Retail"],
    "Region": ["West", "West", "East", "East"],
    "Sales_Rep_ID": ["R1", "R1", "R2", "R2"],
    "Order_Date": pd.to_datetime([
        "2024-01-10", "2025-01-10",
        "2024-02-10", "2025-02-10"
    ]),
    "Net_Sales_INR": [90.0, 180.0, 80.0, 100.0],
    "Gross_Profit_INR": [30.0, 60.0, 20.0, 30.0],
    "Units": [1, 2, 1, 1],
    "Return_Amount_INR": [0.0, 9.0, 4.0, 0.0],
    "On_Time_Delivery_Flag": ["Yes", "No", "Yes", "Yes"],
    "Discount_Pct": [0.05, 0.10, 0.15, 0.25],
    "List_Unit_Price_INR": [100.0, 200.0, 100.0, 100.0],
})

# Weighted discount
weighted = calculate_weighted_discount(sales)
assert abs(weighted - (85 / 700 * 100)) < 1e-9

# Discount band performance
bands = calculate_discount_band_performance(sales)
assert bands["Lines"].sum() == 4
assert set(bands["Discount_Band"].astype(str)) == {
    "0–5%", ">5–10%", ">10–15%", ">20%"
}
assert "Weighted_Discount_Pct" in bands.columns

# Customer performance and concentration
customer = calculate_customer_performance(sales)
assert len(customer) == 3

concentration = calculate_customer_concentration(
    customer, top_n=(1, 2, 3)
)
assert abs(
    concentration.loc[0, "Sales_Share_Pct"]
    - (270 / 450 * 100)
) < 1e-9

# Dimension summary
region_summary = summarize_performance(sales, "Region")
assert set(region_summary["Region"]) == {"West", "East"}

west_gm = region_summary.loc[
    region_summary.Region == "West",
    "Gross_Margin_Pct"
].iloc[0]

assert abs(west_gm - (90 / 270 * 100)) < 1e-9

# Year-over-year performance
yoy = calculate_year_over_year_performance(sales)
assert list(yoy["Year"]) == [2024, 2025]

assert abs(
    yoy.loc[1, "Net_Sales_INR_YoY_Pct"]
    - (280 / 170 - 1) * 100
) < 1e-9

# Target performance by region and representative
targets = pd.DataFrame({
    "Region": ["West", "East"],
    "Sales_Rep_ID": ["R1", "R2"],
    "Monthly_Sales_Target_INR": [300.0, 200.0],
    "Monthly_GP_Target_INR": [100.0, 60.0],
    "Units_Target": [4, 3],
})

region_targets = calculate_target_performance_by_dimension(
    sales, targets, "Region"
)
assert len(region_targets) == 2

assert abs(
    region_targets.loc[
        region_targets.Region == "West",
        "Sales_Gap_M"
    ].iloc[0] - (-30 / 1_000_000)
) < 1e-12

rep_targets = calculate_target_performance_by_dimension(
    sales, targets, "Sales_Rep_ID"
)
assert len(rep_targets) == 2

attainment = calculate_target_attainment(sales, targets)
assert abs(attainment["sales_gap"] - (-50.0)) < 1e-9

print("Phase 1 metric tests passed.")
