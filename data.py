
from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_DIR = Path(__file__).resolve().parent
DATA_FILE = PROJECT_DIR / "data" / "Sales_Dashboard_Candidate_Challenge.xlsx"


@st.cache_data
def load_sales_data():
    """Load the original sales and monthly target worksheets."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}\n"
            "Check that the Excel file is inside the data folder."
        )

    sales = pd.read_excel(DATA_FILE, sheet_name="Sales_Data")
    targets = pd.read_excel(DATA_FILE, sheet_name="Monthly_Targets")

    return sales, targets


def validate_data(sales, targets):
    """Return basic data-quality checks without modifying the data."""
    return {
        "sales_rows": len(sales),
        "sales_columns": list(sales.columns),
        "target_rows": len(targets),
        "target_columns": list(targets.columns),
        "sales_duplicate_rows": int(sales.duplicated().sum()),
        "target_duplicate_rows": int(targets.duplicated().sum()),
        "sales_missing_values": sales.isna().sum().to_dict(),
        "target_missing_values": targets.isna().sum().to_dict(),
    }
