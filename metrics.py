"""Reusable sales-dashboard metrics and aggregation functions.

All monetary inputs are expected in INR. Functions return monetary values in INR;
convert to ₹M only at the presentation layer.
"""
from __future__ import annotations

import pandas as pd


DISCOUNT_BANDS = ["0–5%", ">5–10%", ">10–15%", ">15–20%", ">20%"]
_DISCOUNT_EDGES = [0, 5, 10, 15, 20, float("inf")]


def parse_on_time_delivery(series: pd.Series) -> pd.Series:
    """Return True only for the source workbook's confirmed Yes flag."""
    return series.eq("Yes")


def _safe_pct(numerator: float, denominator: float) -> float:
    return float(numerator / denominator * 100) if denominator else float("nan")


def _require_columns(data: pd.DataFrame, columns: set[str], label: str) -> None:
    missing = columns.difference(data.columns)
    if missing:
        raise ValueError(
            f"{label} is missing required columns: {', '.join(sorted(missing))}"
        )


def calculate_kpis(sales: pd.DataFrame) -> dict:
    """Calculate summary KPIs from selected sales rows (legacy API retained)."""
    net_sales = sales["Net_Sales_INR"].sum()
    gross_profit = sales["Gross_Profit_INR"].sum()
    return_amount = sales["Return_Amount_INR"].sum()

    return {
        "net_sales": float(net_sales),
        "gross_profit": float(gross_profit),
        "gross_margin_pct": _safe_pct(gross_profit, net_sales) if net_sales else 0.0,
        "units_sold": int(sales["Units"].sum()),
        "orders": int(sales["Order_ID"].nunique()),
        "customers": int(sales["Customer_ID"].nunique()),
        "return_amount": float(return_amount),
        "return_rate_pct": _safe_pct(return_amount, net_sales) if net_sales else 0.0,
        "on_time_delivery_pct": (
            float(parse_on_time_delivery(sales["On_Time_Delivery_Flag"]).mean() * 100)
            if len(sales) else 0.0
        ),
    }


def calculate_weighted_discount(
    sales: pd.DataFrame,
    groupby: str | list[str] | None = None,
) -> pd.DataFrame | float:
    """Calculate weighted discount using list value (unit list price × units).

    With no groupby, returns one percentage. With groupby, returns a DataFrame
    containing the requested grouping columns and Weighted_Discount_Pct.
    """
    required = {"Discount_Pct", "List_Unit_Price_INR", "Units"}
    _require_columns(sales, required, "Sales data")

    work = sales.copy()
    work["_list_value"] = work["List_Unit_Price_INR"] * work["Units"]
    work["_discount_value"] = work["_list_value"] * work["Discount_Pct"]

    if groupby is None:
        denominator = work["_list_value"].sum()
        return (
            _safe_pct(work["_discount_value"].sum(), denominator)
            if denominator else float("nan")
        )

    group_cols = [groupby] if isinstance(groupby, str) else list(groupby)
    result = work.groupby(
        group_cols, dropna=False, as_index=False
    ).agg(
        _list_value=("_list_value", "sum"),
        _discount_value=("_discount_value", "sum"),
    )
    result["Weighted_Discount_Pct"] = (
        result["_discount_value"]
        / result["_list_value"].replace(0, float("nan")) * 100
    )
    return result.drop(columns=["_list_value", "_discount_value"])


def calculate_discount_band_performance(
    sales: pd.DataFrame,
    groupby: str | list[str] | None = None,
    min_lines: int = 1,
) -> pd.DataFrame:
    """Summarise sales and margin by discount band, optionally by dimensions.

    Discount_Pct is assumed to be stored as a fraction (e.g. 0.10 = 10%).
    Bands are (0, 5%], (5%, 10%], etc.; zero discount is included in 0–5%.
    """
    required = {
        "Discount_Pct", "List_Unit_Price_INR", "Units",
        "Net_Sales_INR", "Gross_Profit_INR",
    }
    _require_columns(sales, required, "Sales data")

    if min_lines < 1:
        raise ValueError("min_lines must be at least 1")

    group_cols = (
        [] if groupby is None
        else ([groupby] if isinstance(groupby, str) else list(groupby))
    )
    _require_columns(sales, set(group_cols), "Sales data")

    work = sales.copy()
    work["_discount_pct"] = (
        pd.to_numeric(work["Discount_Pct"], errors="coerce") * 100
    )
    work["Discount_Band"] = pd.cut(
        work["_discount_pct"],
        bins=_DISCOUNT_EDGES,
        labels=DISCOUNT_BANDS,
        include_lowest=True,
        right=True,
    )
    work["_list_value"] = work["List_Unit_Price_INR"] * work["Units"]
    work["_discount_value"] = work["_list_value"] * work["Discount_Pct"]

    keys = group_cols + ["Discount_Band"]
    result = work.groupby(
        keys, observed=True, dropna=False, as_index=False
    ).agg(
        Net_Sales_INR=("Net_Sales_INR", "sum"),
        Gross_Profit_INR=("Gross_Profit_INR", "sum"),
        Lines=("Net_Sales_INR", "size"),
        _list_value=("_list_value", "sum"),
        _discount_value=("_discount_value", "sum"),
    )

    result["Gross_Margin_Pct"] = (
        result["Gross_Profit_INR"]
        / result["Net_Sales_INR"].replace(0, float("nan")) * 100
    )
    result["Weighted_Discount_Pct"] = (
        result["_discount_value"]
        / result["_list_value"].replace(0, float("nan")) * 100
    )
    result["Net_Sales_M"] = result["Net_Sales_INR"] / 1_000_000
    result = result[result["Lines"] >= min_lines].copy()

    return result.drop(
        columns=["_list_value", "_discount_value"]
    ).reset_index(drop=True)


def summarize_performance(
    sales: pd.DataFrame,
    dimension: str | list[str],
) -> pd.DataFrame:
    """Reusable dimension summary for geography, product, customer and reps."""
    dims = [dimension] if isinstance(dimension, str) else list(dimension)
    required = set(dims) | {
        "Net_Sales_INR", "Gross_Profit_INR", "Order_ID", "Customer_ID",
        "Return_Amount_INR", "On_Time_Delivery_Flag",
    }
    _require_columns(sales, required, "Sales data")

    work = sales.copy()
    work["_on_time"] = parse_on_time_delivery(
        work["On_Time_Delivery_Flag"]
    )
    result = work.groupby(
        dims, dropna=False, as_index=False
    ).agg(
        Net_Sales_INR=("Net_Sales_INR", "sum"),
        Gross_Profit_INR=("Gross_Profit_INR", "sum"),
        Return_Amount_INR=("Return_Amount_INR", "sum"),
        Orders=("Order_ID", "nunique"),
        Customers=("Customer_ID", "nunique"),
        Lines=("Order_ID", "size"),
        On_Time_Lines=("_on_time", "sum"),
    )

    result["Gross_Margin_Pct"] = (
        result["Gross_Profit_INR"]
        / result["Net_Sales_INR"].replace(0, float("nan")) * 100
    )
    result["Return_Rate_Pct"] = (
        result["Return_Amount_INR"]
        / result["Net_Sales_INR"].replace(0, float("nan")) * 100
    )
    result["On_Time_Pct"] = (
        result["On_Time_Lines"]
        / result["Lines"].replace(0, float("nan")) * 100
    )
    result["Net_Sales_M"] = result["Net_Sales_INR"] / 1_000_000
    result["Gross_Profit_M"] = result["Gross_Profit_INR"] / 1_000_000

    return result.sort_values(
        "Net_Sales_INR", ascending=False
    ).reset_index(drop=True)


def calculate_customer_performance(sales: pd.DataFrame) -> pd.DataFrame:
    """Return one row per customer with segment, industry and performance."""
    dims = ["Customer_ID", "Customer_Name", "Segment", "Industry"]
    _require_columns(sales, set(dims), "Sales data")
    return summarize_performance(sales, dims)


def calculate_customer_concentration(
    customer_performance: pd.DataFrame,
    top_n: tuple[int, ...] = (1, 5, 10, 20, 40, 80),
) -> pd.DataFrame:
    """Calculate top-N customer sales concentration from customer-level rows."""
    _require_columns(
        customer_performance, {"Net_Sales_INR"}, "Customer performance"
    )
    total = customer_performance["Net_Sales_INR"].sum()
    rows = []
    ranked = customer_performance.nlargest(
        max(top_n, default=1), "Net_Sales_INR"
    )

    for n in top_n:
        actual_n = min(n, len(customer_performance))
        amount = ranked.head(actual_n)["Net_Sales_INR"].sum()
        rows.append({
            "Top_N": n,
            "Customers_Included": actual_n,
            "Net_Sales_INR": float(amount),
            "Sales_Share_Pct": (
                _safe_pct(amount, total) if total else float("nan")
            ),
        })

    return pd.DataFrame(rows)


def calculate_monthly_performance(
    sales: pd.DataFrame,
    targets: pd.DataFrame,
) -> pd.DataFrame:
    """Compare monthly actual sales and profit with monthly targets."""
    monthly_actuals = sales.groupby(
        "Month_Start", as_index=False
    ).agg(
        actual_sales=("Net_Sales_INR", "sum"),
        actual_gross_profit=("Gross_Profit_INR", "sum"),
        actual_units=("Units", "sum"),
    )
    monthly_targets = targets.groupby(
        "Month_Start", as_index=False
    ).agg(
        sales_target=("Monthly_Sales_Target_INR", "sum"),
        gross_profit_target=("Monthly_GP_Target_INR", "sum"),
        units_target=("Units_Target", "sum"),
    )
    monthly = monthly_actuals.merge(
        monthly_targets,
        on="Month_Start",
        how="outer",
        validate="one_to_one",
        indicator=True,
    )

    if not monthly["_merge"].eq("both").all():
        raise ValueError(
            "Sales and target data do not cover the same months."
        )

    monthly = monthly.drop(
        columns="_merge"
    ).sort_values("Month_Start")
    monthly["sales_attainment_pct"] = (
        monthly["actual_sales"]
        / monthly["sales_target"].replace(0, float("nan")) * 100
    )
    monthly["profit_attainment_pct"] = (
        monthly["actual_gross_profit"]
        / monthly["gross_profit_target"].replace(0, float("nan")) * 100
    )

    return monthly.reset_index(drop=True)


def calculate_year_over_year_performance(
    sales: pd.DataFrame,
    date_column: str = "Order_Date",
) -> pd.DataFrame:
    """Compare calendar-year sales, GP, units, orders and customers with prior year."""
    _require_columns(
        sales,
        {
            date_column, "Net_Sales_INR", "Gross_Profit_INR",
            "Units", "Order_ID", "Customer_ID",
        },
        "Sales data",
    )

    work = sales.copy()
    work[date_column] = pd.to_datetime(work[date_column])
    work["Year"] = work[date_column].dt.year
    annual = work.groupby(
        "Year", as_index=False
    ).agg(
        Net_Sales_INR=("Net_Sales_INR", "sum"),
        Gross_Profit_INR=("Gross_Profit_INR", "sum"),
        Units=("Units", "sum"),
        Orders=("Order_ID", "nunique"),
        Customers=("Customer_ID", "nunique"),
    )
    annual["Gross_Margin_Pct"] = (
        annual["Gross_Profit_INR"]
        / annual["Net_Sales_INR"].replace(0, float("nan")) * 100
    )

    # Only calculate YoY when adjacent years contain the same calendar months.
    month_sets = work.groupby("Year")[date_column].apply(
        lambda values: set(values.dt.month.unique())
    ).to_dict()
    comparable_years = {}

    for previous_year, current_year in zip(
        annual["Year"].tolist(), annual["Year"].tolist()[1:]
    ):
        comparable_years[current_year] = (
            current_year == previous_year + 1
            and month_sets.get(previous_year, set())
            == month_sets.get(current_year, set())
        )

    for metric in [
        "Net_Sales_INR", "Gross_Profit_INR", "Units", "Orders", "Customers"
    ]:
        annual[f"{metric}_YoY_Pct"] = annual[metric].pct_change() * 100
        for index in range(1, len(annual)):
            if not comparable_years.get(annual.loc[index, "Year"], False):
                annual.loc[index, f"{metric}_YoY_Pct"] = float("nan")

    annual["Gross_Margin_YoY_pp"] = annual["Gross_Margin_Pct"].diff()
    for index in range(1, len(annual)):
        if not comparable_years.get(annual.loc[index, "Year"], False):
            annual.loc[index, "Gross_Margin_YoY_pp"] = float("nan")

    return annual


def calculate_target_attainment(
    sales: pd.DataFrame,
    targets: pd.DataFrame,
) -> dict:
    """Calculate aggregate attainment; caller must supply matching complete months."""
    actual_sales = sales["Net_Sales_INR"].sum()
    actual_profit = sales["Gross_Profit_INR"].sum()
    actual_units = sales["Units"].sum()
    sales_target = targets["Monthly_Sales_Target_INR"].sum()
    profit_target = targets["Monthly_GP_Target_INR"].sum()
    units_target = targets["Units_Target"].sum()

    return {
        "sales_target": float(sales_target),
        "sales_gap": float(actual_sales - sales_target),
        "sales_attainment_pct": (
            _safe_pct(actual_sales, sales_target) if sales_target else None
        ),
        "gross_profit_target": float(profit_target),
        "gross_profit_gap": float(actual_profit - profit_target),
        "profit_attainment_pct": (
            _safe_pct(actual_profit, profit_target) if profit_target else None
        ),
        "units_target": int(units_target),
        "units_gap": int(actual_units - units_target),
        "units_attainment_pct": (
            _safe_pct(actual_units, units_target) if units_target else None
        ),
    }


def calculate_target_performance_by_dimension(
    sales: pd.DataFrame,
    targets: pd.DataFrame,
    dimension: str,
) -> pd.DataFrame:
    """Compare actuals and targets by Region or Sales_Rep_ID without fan-out.

    Input sales and targets must already be restricted to the same complete
    months and compatible region/representative selections.
    """
    if dimension not in {"Region", "Sales_Rep_ID"}:
        raise ValueError(
            "Target comparisons are supported only for Region or Sales_Rep_ID."
        )

    actual_required = {
        dimension, "Net_Sales_INR", "Gross_Profit_INR", "Units"
    }
    target_required = {
        dimension, "Monthly_Sales_Target_INR",
        "Monthly_GP_Target_INR", "Units_Target",
    }
    _require_columns(sales, actual_required, "Sales data")
    _require_columns(targets, target_required, "Target data")

    actual = sales.groupby(
        dimension, as_index=False
    ).agg(
        Actual_Sales_INR=("Net_Sales_INR", "sum"),
        Actual_GP_INR=("Gross_Profit_INR", "sum"),
        Actual_Units=("Units", "sum"),
    )
    target = targets.groupby(
        dimension, as_index=False
    ).agg(
        Sales_Target_INR=("Monthly_Sales_Target_INR", "sum"),
        GP_Target_INR=("Monthly_GP_Target_INR", "sum"),
        Units_Target=("Units_Target", "sum"),
    )

    result = actual.merge(
        target, on=dimension, how="outer", validate="one_to_one"
    )
    numeric = [column for column in result.columns if column != dimension]
    result[numeric] = result[numeric].fillna(0)

    result["Sales_Gap_INR"] = (
        result["Actual_Sales_INR"] - result["Sales_Target_INR"]
    )
    result["GP_Gap_INR"] = (
        result["Actual_GP_INR"] - result["GP_Target_INR"]
    )
    result["Units_Gap"] = (
        result["Actual_Units"] - result["Units_Target"]
    )
    result["Sales_Attainment_Pct"] = (
        result["Actual_Sales_INR"]
        / result["Sales_Target_INR"].replace(0, float("nan")) * 100
    )
    result["GP_Attainment_Pct"] = (
        result["Actual_GP_INR"]
        / result["GP_Target_INR"].replace(0, float("nan")) * 100
    )
    result["Units_Attainment_Pct"] = (
        result["Actual_Units"]
        / result["Units_Target"].replace(0, float("nan")) * 100
    )
    result["Actual_Sales_M"] = result["Actual_Sales_INR"] / 1_000_000
    result["Sales_Target_M"] = result["Sales_Target_INR"] / 1_000_000
    result["Sales_Gap_M"] = result["Sales_Gap_INR"] / 1_000_000

    return result.sort_values(
        "Actual_Sales_INR", ascending=False
    ).reset_index(drop=True)


def calculate_product_performance(
    sales: pd.DataFrame,
    dimension: str,
) -> pd.DataFrame:
    """Summarise product performance at category, subcategory or product grain."""
    allowed = {"Product_Category", "Product_Subcategory", "Product"}
    if dimension not in allowed:
        raise ValueError(
            f"Product performance dimension must be one of {sorted(allowed)}"
        )

    required = {
        dimension, "Net_Sales_INR", "Gross_Profit_INR",
        "Return_Amount_INR", "Units", "Order_ID",
    }
    _require_columns(sales, required, "Sales data")

    result = sales.groupby(
        dimension, dropna=False, as_index=False
    ).agg(
        Net_Sales_INR=("Net_Sales_INR", "sum"),
        Gross_Profit_INR=("Gross_Profit_INR", "sum"),
        Return_Amount_INR=("Return_Amount_INR", "sum"),
        Units=("Units", "sum"),
        Orders=("Order_ID", "nunique"),
        Lines=("Order_ID", "size"),
    )
    result["Gross_Margin_Pct"] = (
        result["Gross_Profit_INR"]
        / result["Net_Sales_INR"].replace(0, float("nan")) * 100
    )
    result["Return_Rate_Pct"] = (
        result["Return_Amount_INR"]
        / result["Net_Sales_INR"].replace(0, float("nan")) * 100
    )
    result["Net_Sales_M"] = result["Net_Sales_INR"] / 1_000_000
    result["Gross_Profit_M"] = result["Gross_Profit_INR"] / 1_000_000
    result["Return_Amount_M"] = result["Return_Amount_INR"] / 1_000_000

    return result.sort_values(
        "Net_Sales_INR", ascending=False
    ).reset_index(drop=True)