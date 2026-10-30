
import pandas as pd


def calculate_kpis(sales: pd.DataFrame) -> dict:
    """Calculate summary KPIs from the selected sales rows."""

    net_sales = sales["Net_Sales_INR"].sum()
    gross_profit = sales["Gross_Profit_INR"].sum()
    total_units = sales["Units"].sum()

    return {
        "net_sales": float(net_sales),
        "gross_profit": float(gross_profit),
        "gross_margin_pct": (
            float(gross_profit / net_sales * 100)
            if net_sales else 0.0
        ),
        "units_sold": int(total_units),
        "orders": int(sales["Order_ID"].nunique()),
        "customers": int(sales["Customer_ID"].nunique()),
        "return_amount": float(sales["Return_Amount_INR"].sum()),
        "return_rate_pct": (
            float(
                sales["Return_Amount_INR"].sum()
                / net_sales * 100
            )
            if net_sales else 0.0
        ),
        "on_time_delivery_pct": (
            float(
                sales["On_Time_Delivery_Flag"].eq("Yes").mean()
                * 100
            )
            if len(sales) else 0.0
        ),
    }


def calculate_monthly_performance(
    sales: pd.DataFrame,
    targets: pd.DataFrame,
) -> pd.DataFrame:
    """Compare monthly actual sales and profit with monthly targets."""

    monthly_actuals = (
        sales.groupby("Month_Start", as_index=False)
        .agg(
            actual_sales=("Net_Sales_INR", "sum"),
            actual_gross_profit=("Gross_Profit_INR", "sum"),
            actual_units=("Units", "sum"),
        )
    )

    monthly_targets = (
        targets.groupby("Month_Start", as_index=False)
        .agg(
            sales_target=("Monthly_Sales_Target_INR", "sum"),
            gross_profit_target=("Monthly_GP_Target_INR", "sum"),
            units_target=("Units_Target", "sum"),
        )
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

    monthly = monthly.drop(columns="_merge").sort_values("Month_Start")

    monthly["sales_attainment_pct"] = (
        monthly["actual_sales"]
        / monthly["sales_target"].replace(0, float("nan"))
        * 100
    )

    monthly["profit_attainment_pct"] = (
        monthly["actual_gross_profit"]
        / monthly["gross_profit_target"].replace(0, float("nan"))
        * 100
    )

    return monthly.reset_index(drop=True)


def calculate_target_attainment(
    sales: pd.DataFrame,
    targets: pd.DataFrame,
) -> dict:
    """Calculate overall target attainment without duplicating targets."""

    actual_sales = sales["Net_Sales_INR"].sum()
    actual_profit = sales["Gross_Profit_INR"].sum()
    actual_units = sales["Units"].sum()

    sales_target = targets["Monthly_Sales_Target_INR"].sum()
    profit_target = targets["Monthly_GP_Target_INR"].sum()
    units_target = targets["Units_Target"].sum()

    return {
        "sales_target": float(sales_target),
        "sales_attainment_pct": (
            float(actual_sales / sales_target * 100)
            if sales_target else None
        ),
        "gross_profit_target": float(profit_target),
        "profit_attainment_pct": (
            float(actual_profit / profit_target * 100)
            if profit_target else None
        ),
        "units_target": int(units_target),
        "units_attainment_pct": (
            float(actual_units / units_target * 100)
            if units_target else None
        ),
    }
