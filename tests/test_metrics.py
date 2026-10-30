
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from data import load_sales_data
from metrics import (
    calculate_kpis,
    calculate_monthly_performance,
    calculate_target_attainment,
)

sales, targets = load_sales_data()

kpis = calculate_kpis(sales)
monthly = calculate_monthly_performance(sales, targets)
attainment = calculate_target_attainment(sales, targets)

print("=" * 50)
print("KPI VALIDATION")
print("=" * 50)

for name, value in kpis.items():
    print(f"{name}: {value:,.2f}" if isinstance(value, float)
          else f"{name}: {value:,}")

print("\nTARGET ATTAINMENT")
for name, value in attainment.items():
    print(f"{name}: {value:,.2f}" if isinstance(value, float)
          else f"{name}: {value}")

print("\nMONTHLY PERFORMANCE")
print(monthly.head(3).to_string(index=False))
print("\nMonths:", len(monthly))

assert len(monthly) == 24
assert monthly["Month_Start"].is_monotonic_increasing
assert abs(
    kpis["gross_profit"]
    - sales["Gross_Profit_INR"].sum()
) < 0.01
assert abs(
    kpis["net_sales"]
    - sales["Net_Sales_INR"].sum()
) < 0.01

print("\nAll basic KPI checks passed.")
