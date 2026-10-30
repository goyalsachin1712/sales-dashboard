
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from data import load_sales_data, validate_data

sales, targets = load_sales_data()
report = validate_data(sales, targets)

print("DATA VALIDATION REPORT")
print("=" * 40)

for key, value in report.items():
    print(f"\n{key}:")
    print(value)

print("\nSALES SAMPLE")
print(sales.head(5).to_string(index=False))

print("\nTARGET SAMPLE")
print(targets.head(5).to_string(index=False))

print("\nSALES DATA TYPES")
print(sales.dtypes)

print("\nTARGET DATA TYPES")
print(targets.dtypes)
