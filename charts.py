import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def _to_millions(values):
    """Convert INR values to millions for chart axes and hover labels."""
    return values / 1_000_000


def _safe_ratio(numerator, denominator):
    """Return a percentage while avoiding division-by-zero errors."""
    denominator = denominator.replace(0, float("nan"))
    return numerator / denominator * 100


def monthly_sales_chart(monthly):
    """
    Plot monthly actual sales and, when supplied, monthly sales targets.

    Expected columns:
      - Month_Start
      - actual_sales
      - optional sales_target
    """
    fig = go.Figure()

    if monthly.empty:
        fig.update_layout(title="Monthly Sales Performance")
        return fig

    month_labels = pd.to_datetime(monthly["Month_Start"]).dt.strftime("%b %Y")
    actual_sales_m = _to_millions(monthly["actual_sales"])

    fig.add_trace(
        go.Scatter(
            x=month_labels,
            y=actual_sales_m,
            name="Actual Sales",
            mode="lines+markers",
            line=dict(width=3),
            hovertemplate=(
                "%{x}<br>"
                "Actual Sales: ₹%{y:,.2f}M"
                "<extra></extra>"
            ),
        )
    )

    if "sales_target" in monthly.columns:
        sales_target_m = _to_millions(monthly["sales_target"])
        fig.add_trace(
            go.Scatter(
                x=month_labels,
                y=sales_target_m,
                name="Sales Target",
                mode="lines+markers",
                line=dict(width=2, dash="dash"),
                hovertemplate=(
                    "%{x}<br>"
                    "Sales Target: ₹%{y:,.2f}M"
                    "<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        title="Monthly Sales Performance",
        xaxis_title="Month",
        yaxis_title="Sales (₹ Millions)",
        hovermode="x unified",
        legend_title="",
        margin=dict(l=20, r=20, t=60, b=20),
    )
    fig.update_xaxes(
        type="category",
        categoryorder="array",
        categoryarray=month_labels.tolist(),
    )
    fig.update_yaxes(rangemode="tozero", tickformat=",.0f")
    return fig


def regional_performance_chart(sales):
    """
    Compare regional sales and profitability.

    Bar height represents Net Sales. Hover details include Gross Profit,
    Gross Margin, transaction-line count and distinct orders.
    """
    required = {"Region", "Net_Sales_INR", "Gross_Profit_INR"}
    if sales.empty or not required.issubset(sales.columns):
        return go.Figure().update_layout(title="Regional Performance")

    regional = (
        sales.groupby("Region", as_index=False)
        .agg(
            Net_Sales_INR=("Net_Sales_INR", "sum"),
            Gross_Profit_INR=("Gross_Profit_INR", "sum"),
            Orders=("Order_ID", "nunique") if "Order_ID" in sales.columns
            else ("Net_Sales_INR", "size"),
        )
    )
    regional["Gross_Margin_Pct"] = _safe_ratio(
        regional["Gross_Profit_INR"], regional["Net_Sales_INR"]
    )
    regional = regional.sort_values("Net_Sales_INR", ascending=False)
    regional["Net_Sales_M"] = _to_millions(regional["Net_Sales_INR"])
    regional["Gross_Profit_M"] = _to_millions(regional["Gross_Profit_INR"])

    fig = px.bar(
        regional,
        x="Region",
        y="Net_Sales_M",
        color="Gross_Margin_Pct",
        color_continuous_scale="Blues",
        custom_data=[
            "Net_Sales_M",
            "Gross_Profit_M",
            "Gross_Margin_Pct",
            "Orders",
        ],
        title="Regional Sales and Profitability",
        labels={
            "Region": "Region",
            "Net_Sales_M": "Net Sales (₹ Millions)",
            "Gross_Margin_Pct": "Gross Margin (%)",
        },
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Net Sales: ₹%{customdata[0]:,.2f}M<br>"
            "Gross Profit: ₹%{customdata[1]:,.2f}M<br>"
            "Gross Margin: %{customdata[2]:.2f}%<br>"
            "Distinct orders: %{customdata[3]:,}"
            "<extra></extra>"
        )
    )
    fig.update_layout(
        yaxis_title="Net Sales (₹ Millions)",
        coloraxis_colorbar_title="Gross Margin (%)",
        margin=dict(l=20, r=20, t=60, b=20),
    )
    fig.update_yaxes(tickformat=",.0f", rangemode="tozero")
    return fig


def product_performance_chart(sales):
    """
    Compare product categories on sales and gross profit.

    Bar height represents Net Sales. Hover details show Gross Profit,
    Gross Margin, Units, return value and return rate by value.
    """
    required = {
        "Product_Category",
        "Net_Sales_INR",
        "Gross_Profit_INR",
        "Units",
    }
    if sales.empty or not required.issubset(sales.columns):
        return go.Figure().update_layout(title="Product Category Performance")

    aggregations = {
        "Net_Sales_INR": ("Net_Sales_INR", "sum"),
        "Gross_Profit_INR": ("Gross_Profit_INR", "sum"),
        "Units": ("Units", "sum"),
    }
    if "Return_Amount_INR" in sales.columns:
        aggregations["Return_Amount_INR"] = ("Return_Amount_INR", "sum")
    if "Order_ID" in sales.columns:
        aggregations["Orders"] = ("Order_ID", "nunique")

    products = sales.groupby("Product_Category", as_index=False).agg(**aggregations)
    products["Gross_Margin_Pct"] = _safe_ratio(
        products["Gross_Profit_INR"], products["Net_Sales_INR"]
    )
    if "Return_Amount_INR" in products.columns:
        products["Return_Rate_Pct"] = _safe_ratio(
            products["Return_Amount_INR"], products["Net_Sales_INR"]
        )
    else:
        products["Return_Rate_Pct"] = float("nan")

    products = products.sort_values("Net_Sales_INR", ascending=False)
    products["Net_Sales_M"] = _to_millions(products["Net_Sales_INR"])
    products["Gross_Profit_M"] = _to_millions(products["Gross_Profit_INR"])
    if "Return_Amount_INR" in products.columns:
        products["Return_Amount_M"] = _to_millions(products["Return_Amount_INR"])

    fig = px.bar(
        products,
        x="Product_Category",
        y="Net_Sales_M",
        color="Gross_Margin_Pct",
        color_continuous_scale="Teal",
        custom_data=[
            "Net_Sales_M",
            "Gross_Profit_M",
            "Gross_Margin_Pct",
            "Units",
            "Return_Amount_M" if "Return_Amount_M" in products.columns else "Net_Sales_M",
            "Return_Rate_Pct",
        ],
        title="Product Category Sales and Profitability",
        labels={
            "Product_Category": "Product Category",
            "Net_Sales_M": "Net Sales (₹ Millions)",
            "Gross_Margin_Pct": "Gross Margin (%)",
        },
    )
    return_label = (
        "Return Amount: ₹%{customdata[4]:,.2f}M<br>"
        if "Return_Amount_INR" in products.columns else ""
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Net Sales: ₹%{customdata[0]:,.2f}M<br>"
            "Gross Profit: ₹%{customdata[1]:,.2f}M<br>"
            "Gross Margin: %{customdata[2]:.2f}%<br>"
            "Units: %{customdata[3]:,.0f}<br>"
            + return_label
            + "Return Rate by Value: %{customdata[5]:.2f}%"
            "<extra></extra>"
        )
    )
    fig.update_layout(
        xaxis_title="Product Category",
        yaxis_title="Net Sales (₹ Millions)",
        coloraxis_colorbar_title="Gross Margin (%)",
        margin=dict(l=20, r=20, t=60, b=20),
    )
    fig.update_yaxes(tickformat=",.0f", rangemode="tozero")
    return fig


def representative_performance_chart(sales):
    """
    Show the top 15 sales representatives by Net Sales.

    Gross Profit, Gross Margin, weighted Discount % and distinct orders
    are included in hover details. The chart is not a
    target-attainment ranking.
    """
    required = {
        "Sales_Rep",
        "Net_Sales_INR",
        "Gross_Profit_INR",
    }
    if sales.empty or not required.issubset(sales.columns):
        return go.Figure().update_layout(title="Representative Performance")

    reps = (
        sales.groupby("Sales_Rep", as_index=False)
        .agg(
            Net_Sales_INR=("Net_Sales_INR", "sum"),
            Gross_Profit_INR=("Gross_Profit_INR", "sum"),
            **({"Orders": ("Order_ID", "nunique")} if "Order_ID" in sales.columns else {}),
        )
    )
    reps["Gross_Margin_Pct"] = _safe_ratio(
        reps["Gross_Profit_INR"], reps["Net_Sales_INR"]
    )

    # Calculate weighted discount using list value as the weight, not a
    # simple average of row-level discount percentages.
    if {
        "Discount_Pct", "List_Unit_Price_INR", "Units"
    }.issubset(sales.columns):
        working = sales.copy()
        working["_List_Value"] = (
            working["List_Unit_Price_INR"] * working["Units"]
        )
        working["_Discounted_List_Value"] = (
            working["_List_Value"] * working["Discount_Pct"]
        )
        discount = (
            working.groupby("Sales_Rep")
            .agg(
                _List_Value=("_List_Value", "sum"),
                _Discounted_List_Value=("_Discounted_List_Value", "sum"),
            )
        )
        discount["Weighted_Discount_Pct"] = _safe_ratio(
            discount["_Discounted_List_Value"], discount["_List_Value"]
        )
        reps = reps.merge(
            discount[["Weighted_Discount_Pct"]],
            left_on="Sales_Rep",
            right_index=True,
            how="left",
        )

    reps = reps.nlargest(15, "Net_Sales_INR").sort_values("Net_Sales_INR")
    reps["Net_Sales_M"] = _to_millions(reps["Net_Sales_INR"])
    reps["Gross_Profit_M"] = _to_millions(reps["Gross_Profit_INR"])

    custom_fields = [
        "Gross_Profit_M",
        "Gross_Margin_Pct",
    ]
    if "Orders" in reps.columns:
        custom_fields.append("Orders")
    if "Weighted_Discount_Pct" in reps.columns:
        custom_fields.append("Weighted_Discount_Pct")

    fig = px.bar(
        reps,
        x="Net_Sales_M",
        y="Sales_Rep",
        orientation="h",
        color="Gross_Margin_Pct",
        color_continuous_scale="Teal",
        custom_data=["Net_Sales_M"] + custom_fields,
        labels={
            "Net_Sales_M": "Net Sales (₹ Millions)",
            "Sales_Rep": "Sales Representative",
            "Gross_Margin_Pct": "Gross Margin (%)",
        },
    )

    hover = (
        "<b>%{y}</b><br>"
        "Net Sales: ₹%{customdata[0]:,.2f}M<br>"
        "Gross Profit: ₹%{customdata[1]:,.2f}M<br>"
        "Gross Margin: %{customdata[2]:.2f}%<br>"
    )
    index = 3
    if "Orders" in reps.columns:
        hover += "Distinct orders: %{customdata[" + str(index) + "]:,}<br>"
        index += 1
    if "Weighted_Discount_Pct" in reps.columns:
        hover += "Weighted discount: %{customdata[" + str(index) + "]:.2f}%<br>"
    fig.update_traces(hovertemplate=hover + "<extra></extra>")
    fig.update_layout(
        xaxis_title="Net Sales (₹ Millions)",
        yaxis_title="Sales Representative",
        coloraxis_colorbar_title="Gross Margin (%)",
        margin=dict(l=20, r=20, t=60, b=20),
    )
    fig.update_xaxes(tickformat=",.0f", rangemode="tozero")
    return fig


def regional_channel_delivery_chart(sales):
    """
    Heatmap of line-level on-time delivery rate by Region and Channel.

    The percentage is calculated from On_Time_Delivery_Flag == 'Yes'.
    Hover details include the number of transaction lines in each cell.
    This is a line-level metric, not an order-level metric.
    """
    required = {"Region", "Channel", "On_Time_Delivery_Flag"}
    if sales.empty or not required.issubset(sales.columns):
        return go.Figure().update_layout(title="On-Time Delivery by Region and Channel")

    working = sales.copy()
    flag = working["On_Time_Delivery_Flag"].astype(str).str.strip().str.lower()
    working["_On_Time"] = flag.isin(["yes", "y", "true", "1"])

    summary = (
        working.groupby(["Region", "Channel"], as_index=False)
        .agg(
            On_Time_Rate=("_On_Time", "mean"),
            Transaction_Lines=("_On_Time", "size"),
        )
    )
    summary["On_Time_Rate_Pct"] = summary["On_Time_Rate"] * 100

    pivot_rate = summary.pivot(
        index="Region", columns="Channel", values="On_Time_Rate_Pct"
    )
    pivot_count = summary.pivot(
        index="Region", columns="Channel", values="Transaction_Lines"
    )

    fig = go.Figure(
        data=go.Heatmap(
            z=pivot_rate.values,
            x=pivot_rate.columns.tolist(),
            y=pivot_rate.index.tolist(),
            customdata=pivot_count.values,
            text=pivot_rate.values,
            texttemplate="%{text:.1f}%",
            textfont=dict(size=12, color="black"),
            colorscale="RdYlGn",
            zmin=0,
            zmax=100,
            colorbar=dict(title="On-Time (%)"),
            hovertemplate=(
                "<b>%{y} — %{x}</b><br>"
                "On-time delivery: %{z:.2f}%<br>"
                "Transaction lines: %{customdata:,}"
                "<extra></extra>"
            ),
        )
    )
    fig.update_layout(
        title="On-Time Delivery by Region and Channel",
        xaxis_title="Sales Channel",
        yaxis_title="Region",
        margin=dict(l=20, r=20, t=60, b=20),
    )
    return fig


def product_returns_profitability_chart(sales):
    """
    Compare product subcategories by gross margin and return rate by value.

    Each bubble represents a Product_Subcategory. Bubble size represents
    Net Sales. Return rate = Return_Amount_INR / Net_Sales_INR * 100.
    Hover details include sales, gross profit, return amount and distinct products.
    """
    required = {
        "Product_Subcategory",
        "Net_Sales_INR",
        "Gross_Profit_INR",
        "Return_Amount_INR",
    }
    if sales.empty or not required.issubset(sales.columns):
        return go.Figure().update_layout(title="Product Returns vs Profitability")

    aggregations = {
        "Net_Sales_INR": ("Net_Sales_INR", "sum"),
        "Gross_Profit_INR": ("Gross_Profit_INR", "sum"),
        "Return_Amount_INR": ("Return_Amount_INR", "sum"),
    }
    if "Product" in sales.columns:
        aggregations["Products"] = ("Product", "nunique")

    summary = (
        sales.groupby("Product_Subcategory", as_index=False)
        .agg(**aggregations)
    )
    summary["Gross_Margin_Pct"] = _safe_ratio(
        summary["Gross_Profit_INR"], summary["Net_Sales_INR"]
    )
    summary["Return_Rate_Pct"] = _safe_ratio(
        summary["Return_Amount_INR"], summary["Net_Sales_INR"]
    )
    summary["Net_Sales_M"] = _to_millions(summary["Net_Sales_INR"])
    summary["Gross_Profit_M"] = _to_millions(summary["Gross_Profit_INR"])
    summary["Return_Amount_M"] = _to_millions(summary["Return_Amount_INR"])

    fig = px.scatter(
        summary,
        x="Gross_Margin_Pct",
        y="Return_Rate_Pct",
        size="Net_Sales_INR",
        color="Product_Subcategory",
        size_max=55,
        hover_name="Product_Subcategory",
        custom_data=[
            "Net_Sales_M",
            "Gross_Profit_M",
            "Return_Amount_M",
        ] + (["Products"] if "Products" in summary.columns else []),
        title="Product Subcategory Returns vs Profitability",
        labels={
            "Gross_Margin_Pct": "Gross Margin (%)",
            "Return_Rate_Pct": "Return Rate by Value (%)",
            "Net_Sales_INR": "Net Sales (INR; bubble size)",
        },
    )
    hover = (
        "<b>%{hovertext}</b><br>"
        "Gross Margin: %{x:.2f}%<br>"
        "Return Rate by Value: %{y:.2f}%<br>"
        "Net Sales: ₹%{customdata[0]:,.2f}M<br>"
        "Gross Profit: ₹%{customdata[1]:,.2f}M<br>"
        "Return Amount: ₹%{customdata[2]:,.2f}M<br>"
    )
    if "Products" in summary.columns:
        hover += "Distinct products: %{customdata[3]:,}<br>"
    fig.update_traces(hovertemplate=hover + "<extra></extra>")
    overall_margin = (
        sales["Gross_Profit_INR"].sum() / sales["Net_Sales_INR"].sum() * 100
        if sales["Net_Sales_INR"].sum() else 0
    )
    overall_return_rate = (
        sales["Return_Amount_INR"].sum() / sales["Net_Sales_INR"].sum() * 100
        if sales["Net_Sales_INR"].sum() else 0
    )
    fig.add_vline(
        x=overall_margin,
        line_dash="dash",
        line_color="gray",
        annotation_text=f"Overall GM {overall_margin:.1f}%",
        annotation_position="top",
    )
    fig.add_hline(
        y=overall_return_rate,
        line_dash="dash",
        line_color="gray",
        annotation_text=f"Overall return {overall_return_rate:.1f}%",
        annotation_position="top left",
    )
    fig.update_layout(
        xaxis_title="Gross Margin (%)",
        yaxis_title="Return Rate by Value (%)",
        legend_title="Subcategory",
        margin=dict(l=20, r=20, t=60, b=20),
    )
    return fig
