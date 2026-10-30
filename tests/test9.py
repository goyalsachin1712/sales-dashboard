import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from data import load_sales_data
from metrics import calculate_kpis

sales, targets = load_sales_data()

filtered = sales[
    (sales["Order_Date"] >= "2025-01-01") &
    (sales["Order_Date"] <= "2025-12-31")
]

print("Filtered rows:", len(filtered))
print(calculate_kpis(filtered))