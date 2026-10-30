import pandas as pd
import streamlit as st

from data import load_sales_data
from metrics import (
    calculate_kpis,
    calculate_target_attainment,
)
from charts import (
    monthly_sales_chart,
    regional_performance_chart,
    product_performance_chart,
    representative_performance_chart,
    regional_channel_delivery_chart,
    product_returns_profitability_chart,
)


st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("Sales Performance Dashboard")
st.caption(
    "Interactive analysis of sales, profitability, targets and "
    "operational performance | INR"
)


@st.cache_data
def get_data():
    return load_sales_data()


try:
    sales, targets = get_data()
except Exception as exc:
    st.error(f"Unable to load the dataset: {exc}")
    st.stop()



# ---------------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------------
st.sidebar.header("Dashboard Filters")

min_date = sales["Order_Date"].min().date()
max_date = sales["Order_Date"].max().date()

regions_options = sorted(sales["Region"].dropna().unique().tolist())
category_options = sorted(sales["Product_Category"].dropna().unique().tolist())
segment_options = sorted(sales["Segment"].dropna().unique().tolist())
channel_options = sorted(sales["Channel"].dropna().unique().tolist())

# Initialise date range state
if "filter_date_range" not in st.session_state:
    st.session_state["filter_date_range"] = (min_date, max_date)

st.sidebar.subheader("Selection Filters")


def reset_all_filters():
    """Reset the date range and all selection filters."""
    st.session_state["filter_date_range"] = (min_date, max_date)
    st.session_state["filter_region"] = regions_options.copy()
    st.session_state["filter_category"] = category_options.copy()
    st.session_state["filter_segment"] = segment_options.copy()
    st.session_state["filter_channel"] = channel_options.copy()
    st.session_state["filter_rep"] = []


st.sidebar.button(
    "Reset All Filters",
    use_container_width=True,
    on_click=reset_all_filters
)

# Date filter
date_range = st.sidebar.date_input(
    "Order date range",
    min_value=min_date,
    max_value=max_date,
    key="filter_date_range"
)

if not isinstance(date_range, (tuple, list)) or len(date_range) != 2:
    st.info("Select both a start date and an end date.")
    st.stop()

start_date, end_date = date_range

if start_date > end_date:
    st.error("The start date must not be after the end date.")
    st.stop()

# Initialise selection filter states
filter_defaults = {
    "filter_region": regions_options,
    "filter_category": category_options,
    "filter_segment": segment_options,
    "filter_channel": channel_options,
    "filter_rep": [],
}

for key, default_values in filter_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = default_values.copy()

regions = st.sidebar.multiselect(
    "Region",
    options=regions_options,
    key="filter_region",
)

categories = st.sidebar.multiselect(
    "Product category",
    options=category_options,
    key="filter_category",
)

segments = st.sidebar.multiselect(
    "Customer segment",
    options=segment_options,
    key="filter_segment",
)

channels = st.sidebar.multiselect(
    "Sales channel",
    options=channel_options,
    key="filter_channel",
)

# Representative choices remain dependent on the date and the four
# independent filters.
rep_option_mask = sales["Order_Date"].dt.date.between(start_date, end_date)

if regions:
    rep_option_mask &= sales["Region"].isin(regions)

if categories:
    rep_option_mask &= sales["Product_Category"].isin(categories)

if segments:
    rep_option_mask &= sales["Segment"].isin(segments)

if channels:
    rep_option_mask &= sales["Channel"].isin(channels)

rep_options = sorted(
    sales.loc[rep_option_mask, "Sales_Rep"].dropna().unique().tolist()
)

current_reps = st.session_state["filter_rep"]

if any(rep not in rep_options for rep in current_reps):
    st.session_state["filter_rep"] = []

reps = st.sidebar.multiselect(
    "Sales representative",
    options=rep_options,
    key="filter_rep",
)

st.sidebar.caption("Leave blank to include all matching representatives.")

if reps:
    st.sidebar.caption(
        f"{len(reps)} selected · {len(rep_options)} matching representatives "
        f"(of {sales['Sales_Rep'].nunique()})"
    )
else:
    st.sidebar.caption(
        f"{len(rep_options)} matching representatives "
        f"(of {sales['Sales_Rep'].nunique()})"
    )


# ---------------------------------------------------------------------
# Apply filters
# ---------------------------------------------------------------------
filtered = sales[
    sales["Order_Date"].dt.date.between(start_date, end_date)
    & sales["Region"].isin(regions)
    & sales["Product_Category"].isin(categories)
    & sales["Segment"].isin(segments)
    & sales["Channel"].isin(channels)
    & (sales["Sales_Rep"].isin(reps) if reps else True)
].copy()

if filtered.empty:
    st.warning("No sales records match the selected filters.")
    st.stop()


# Active filter summary
active_filters = []
if len(regions) != len(regions_options):
    active_filters.append(f"Region: {', '.join(regions) if regions else 'None'}")
if len(categories) != len(category_options):
    active_filters.append(
        f"Category: {', '.join(categories) if categories else 'None'}"
    )
if len(segments) != len(segment_options):
    active_filters.append(
        f"Segment: {', '.join(segments) if segments else 'None'}"
    )
if len(channels) != len(channel_options):
    active_filters.append(
        f"Channel: {', '.join(channels) if channels else 'None'}"
    )
if reps:
    active_filters.append(f"Representative: {', '.join(reps)}")

st.caption(
    f"Showing {len(filtered):,} transaction lines from "
    f"{start_date:%d %b %Y} to {end_date:%d %b %Y}."
)
if active_filters:
    st.caption("Active filters — " + " | ".join(active_filters))


# ---------------------------------------------------------------------
# Executive KPI overview
# ---------------------------------------------------------------------
st.subheader("Executive Overview")
kpis = calculate_kpis(filtered)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Net Sales", f"₹{kpis['net_sales'] / 1e6:,.2f}M")
col2.metric("Gross Profit", f"₹{kpis['gross_profit'] / 1e6:,.2f}M")
col3.metric("Gross Margin", f"{kpis['gross_margin_pct']:.2f}%")
col4.metric("Orders", f"{kpis['orders']:,}")

col5, col6, col7, col8 = st.columns(4)
col5.metric("Units Sold", f"{kpis['units_sold']:,}")
col6.metric("Unique Customers", f"{kpis['customers']:,}")
col7.metric("Return Rate by Value", f"{kpis['return_rate_pct']:.2f}%")
col8.metric(
    "On-Time Delivery (Line Level)",
    f"{kpis['on_time_delivery_pct']:.2f}%",
)


# ---------------------------------------------------------------------
# Target comparison
# Targets are at Sales Rep x Month grain. Do not compare when filters
# narrow product category, segment or channel.
# ---------------------------------------------------------------------
target_comparable = (
    len(categories) == sales["Product_Category"].nunique()
    and len(segments) == sales["Segment"].nunique()
    and len(channels) == sales["Channel"].nunique()
)

if not target_comparable:
    st.info(
        "Target attainment is hidden when Product Category, Customer "
        "Segment or Sales Channel filters are narrowed. Targets are not "
        "defined at those levels."
    )
else:
    start_timestamp = pd.Timestamp(start_date)
    end_timestamp = pd.Timestamp(end_date)

    first_full_month = start_timestamp.to_period("M").to_timestamp()
    if start_date.day != 1:
        first_full_month += pd.offsets.MonthBegin(1)

    last_full_month = end_timestamp.to_period("M").to_timestamp()
    if end_date != end_timestamp.to_period("M").end_time.date():
        last_full_month -= pd.offsets.MonthBegin(1)

    if first_full_month > last_full_month:
        st.info(
            "No complete calendar months are included in the selected "
            "date range. Target attainment is hidden."
        )
    else:
        actual_full_months = filtered[
            filtered["Month_Start"].between(first_full_month, last_full_month)
        ].copy()

        targets_full_months = targets[
            targets["Month_Start"].between(first_full_month, last_full_month)
            & targets["Region"].isin(regions)
            & (targets["Sales_Rep"].isin(reps) if reps else True)
        ].copy()

        if actual_full_months.empty or targets_full_months.empty:
            st.info(
                "No matching sales and target records are available "
                "for the complete months selected."
            )
        else:
            attainment = calculate_target_attainment(
                actual_full_months,
                targets_full_months,
            )

            month_label = (
                f"{first_full_month:%b %Y}"
                if first_full_month == last_full_month
                else (
                    f"{first_full_month:%b %Y} – "
                    f"{last_full_month:%b %Y}"
                )
            )

            st.subheader(f"Target Attainment: {month_label}")
            t1, t2, t3 = st.columns(3)
            t1.metric(
                "Sales Target Attainment",
                f"{attainment['sales_attainment_pct']:.2f}%",
            )
            t2.metric(
                "Gross Profit Target Attainment",
                f"{attainment['profit_attainment_pct']:.2f}%",
            )
            t3.metric(
                "Units Target Attainment",
                f"{attainment['units_attainment_pct']:.2f}%",
            )


# ---------------------------------------------------------------------
# Dynamic business observations
# Signals are recalculated from the currently filtered data.
# They are descriptive, not causal explanations.
# ---------------------------------------------------------------------
st.subheader("What Stands Out")

insights = []

region_summary = (
    filtered.groupby("Region")
    .agg(
        sales=("Net_Sales_INR", "sum"),
        gp=("Gross_Profit_INR", "sum"),
    )
)
if not region_summary.empty:
    region_summary["margin"] = (
        region_summary["gp"]
        / region_summary["sales"].replace(0, float("nan"))
        * 100
    )

    if len(region_summary) >= 2:
        sales_leader = region_summary["sales"].idxmax()
        margin_watch = region_summary["margin"].idxmin()
        insights.append(
            f"**Sales leader:** {sales_leader} has the highest sales in this "
            f"selection (₹{region_summary.loc[sales_leader, 'sales'] / 1e6:,.2f}M)."
        )
        insights.append(
            f"**Margin watch:** {margin_watch} has the lowest gross margin "
            f"among selected regions ({region_summary.loc[margin_watch, 'margin']:.2f}%)."
        )
    else:
        selected_region = region_summary.index[0]
        insights.append(
            f"**Selected region:** {selected_region} generated "
            f"₹{region_summary.loc[selected_region, 'sales'] / 1e6:,.2f}M "
            f"in Net Sales at a gross margin of "
            f"{region_summary.loc[selected_region, 'margin']:.2f}%."
        )

if {"Region", "Channel", "On_Time_Delivery_Flag"}.issubset(filtered.columns):
    delivery_work = filtered.copy()
    delivery_work["_on_time"] = (
        delivery_work["On_Time_Delivery_Flag"]
        .astype(str).str.strip().str.lower()
        .isin(["yes", "y", "true", "1"])
    )
    region_delivery = delivery_work.groupby("Region")["_on_time"].mean().mul(100)
    if len(region_delivery) >= 2:
        weakest_region = region_delivery.idxmin()
        insights.append(
            f"**Delivery risk:** {weakest_region} has the lowest line-level "
            f"on-time delivery rate in the selected regions "
            f"({region_delivery.loc[weakest_region]:.2f}%). "
            "Use the Region × Channel heatmap to locate the weakest channel."
        )
    elif len(region_delivery) == 1:
        selected_region = region_delivery.index[0]
        insights.append(
            f"**Delivery performance:** {selected_region} has a line-level "
            f"on-time delivery rate of {region_delivery.iloc[0]:.2f}%."
        )

if {
    "Product_Subcategory", "Net_Sales_INR", "Gross_Profit_INR",
    "Return_Amount_INR"
}.issubset(filtered.columns):
    subcategory = (
        filtered.groupby("Product_Subcategory")
        .agg(
            sales=("Net_Sales_INR", "sum"),
            gp=("Gross_Profit_INR", "sum"),
            returns=("Return_Amount_INR", "sum"),
        )
    )
    subcategory["margin"] = (
        subcategory["gp"] / subcategory["sales"].replace(0, float("nan")) * 100
    )
    subcategory["return_rate"] = (
        subcategory["returns"] / subcategory["sales"].replace(0, float("nan")) * 100
    )
    material = subcategory[
        subcategory["sales"] >= filtered["Net_Sales_INR"].sum() * 0.02
    ]
    if len(material) >= 2:
        high_return = material["return_rate"].idxmax()
        low_margin = material["margin"].idxmin()
        insights.append(
            f"**Returns exposure:** {high_return} has the highest return rate "
            f"by value among subcategories representing at least 2% of "
            f"selected sales ({material.loc[high_return, 'return_rate']:.2f}%)."
        )
        insights.append(
            f"**Profitability watch:** {low_margin} has the lowest gross "
            f"margin among those material subcategories "
            f"({material.loc[low_margin, 'margin']:.2f}%)."
        )
    elif len(material) == 1:
        selected_subcategory = material.index[0]
        insights.append(
            f"**Selected subcategory:** {selected_subcategory} represents at "
            f"least 2% of selected sales, with a return rate of "
            f"{material.loc[selected_subcategory, 'return_rate']:.2f}% "
            f"and gross margin of {material.loc[selected_subcategory, 'margin']:.2f}%."
        )

for insight in insights:
    st.markdown(f"- {insight}")

st.caption(
    "**Observations are recalculated for the current selection. They identify "
    "areas for investigation and do not establish causation."
)


# ---------------------------------------------------------------------
# Monthly sales trend
# ---------------------------------------------------------------------
st.subheader("Monthly Performance")

monthly_actuals = (
    filtered.groupby("Month_Start", as_index=False)
    .agg(
        actual_sales=("Net_Sales_INR", "sum"),
        actual_gross_profit=("Gross_Profit_INR", "sum"),
        actual_units=("Units", "sum"),
    )
    .sort_values("Month_Start")
)

monthly_chart_data = monthly_actuals.copy()

# A target is comparable only for a calendar month fully contained in
# the selected date range. Partial months retain actual sales but no target.
month_starts = pd.to_datetime(monthly_actuals["Month_Start"])
month_ends = month_starts + pd.offsets.MonthEnd(0)
complete_month_mask = (
    (month_starts.dt.date >= start_date)
    & (month_ends.dt.date <= end_date)
)
complete_months = monthly_actuals.loc[
    complete_month_mask, "Month_Start"
]

if target_comparable and not complete_months.empty:
    monthly_targets = (
        targets[
            targets["Month_Start"].isin(complete_months)
            & targets["Region"].isin(regions)
            & (targets["Sales_Rep"].isin(reps) if reps else True)
        ]
        .groupby("Month_Start", as_index=False)
        .agg(sales_target=("Monthly_Sales_Target_INR", "sum"))
    )

    monthly_chart_data = monthly_actuals.merge(
        monthly_targets,
        on="Month_Start",
        how="left",
        validate="one_to_one",
    )

st.plotly_chart(
    monthly_sales_chart(monthly_chart_data),
    use_container_width=True,
)


# ---------------------------------------------------------------------
# Regional and product performance
# ---------------------------------------------------------------------
st.subheader("Regional and Product Performance")

left, right = st.columns(2)
with left:
    st.plotly_chart(
        regional_performance_chart(filtered),
        use_container_width=True,
    )
with right:
    st.plotly_chart(
        product_performance_chart(filtered),
        use_container_width=True,
    )


# ---------------------------------------------------------------------
# Operational delivery analysis
# ---------------------------------------------------------------------
st.subheader("Operational Performance")
st.plotly_chart(
    regional_channel_delivery_chart(filtered),
    use_container_width=True,
)
st.caption(
    "Delivery heatmap uses transaction-line-level On_Time_Delivery_Flag. "
    "It is not an order-level on-time delivery measure."
)


# ---------------------------------------------------------------------
# Product returns and profitability
# ---------------------------------------------------------------------
st.subheader("Product Returns and Profitability")
st.plotly_chart(
    product_returns_profitability_chart(filtered),
    use_container_width=True,
)
st.caption(
    "Return rate by value is Return Amount divided by Net Sales. "
    "Bubble size represents Net Sales; investigate high-return, "
    "low-margin subcategories rather than assuming returns caused "
    "the margin outcome."
)


# ---------------------------------------------------------------------
# Representative performance
# ---------------------------------------------------------------------
st.subheader("Sales Representative Performance")

st.markdown("**Top 15 Sales Representatives by Net Sales**")

st.plotly_chart(
    representative_performance_chart(filtered),
    use_container_width=True,
)

# Full representative comparison table: includes all selected reps,
# not only the top 15 shown in the chart.
st.markdown("**All Sales Representatives – Performance Details**")
rep_table = (
    filtered.groupby("Sales_Rep", as_index=False)
    .agg(
        Net_Sales_INR=("Net_Sales_INR", "sum"),
        Gross_Profit_INR=("Gross_Profit_INR", "sum"),
        Orders=("Order_ID", "nunique"),
    )
)
rep_table["Gross_Margin_Pct"] = (
    rep_table["Gross_Profit_INR"]
    / rep_table["Net_Sales_INR"].replace(0, float("nan"))
    * 100
)

if {
    "Discount_Pct", "List_Unit_Price_INR", "Units"
}.issubset(filtered.columns):
    discount_work = filtered.copy()
    discount_work["_list_value"] = (
        discount_work["List_Unit_Price_INR"] * discount_work["Units"]
    )
    discount_work["_discount_value"] = (
        discount_work["_list_value"] * discount_work["Discount_Pct"]
    )
    discount_table = (
        discount_work.groupby("Sales_Rep")
        .agg(
            list_value=("_list_value", "sum"),
            discount_value=("_discount_value", "sum"),
        )
    )
    discount_table["Weighted_Discount_Pct"] = (
        discount_table["discount_value"]
        / discount_table["list_value"].replace(0, float("nan"))
        * 100
    )
    rep_table = rep_table.merge(
        discount_table[["Weighted_Discount_Pct"]],
        left_on="Sales_Rep",
        right_index=True,
        how="left",
    )

rep_table = rep_table.sort_values("Net_Sales_INR", ascending=False)
rep_display = rep_table.rename(
    columns={
        "Sales_Rep": "Sales Representative",
        "Gross_Margin_Pct": "Gross Margin (%)",
        "Weighted_Discount_Pct": "Weighted Discount (%)",
        "Orders": "Distinct Orders",
    }
).copy()
rep_display["Net Sales (₹M)"] = rep_display["Net_Sales_INR"] / 1_000_000
rep_display["Gross Profit (₹M)"] = rep_display["Gross_Profit_INR"] / 1_000_000
display_columns = [
    "Sales Representative",
    "Net Sales (₹M)",
    "Gross Profit (₹M)",
    "Gross Margin (%)",
]
if "Weighted Discount (%)" in rep_display.columns:
    display_columns.append("Weighted Discount (%)")
display_columns += ["Distinct Orders"]

st.dataframe(
    rep_display[display_columns].style.format(
        {
            "Net Sales (₹M)": "{:,.2f}",
            "Gross Profit (₹M)": "{:,.2f}",
            "Gross Margin (%)": "{:.2f}%",
            "Weighted Discount (%)": "{:.2f}%",
            "Distinct Orders": "{:,.0f}",
        },
        na_rep="—",
    ),
    use_container_width=True,
    hide_index=True,
)


# ---------------------------------------------------------------------
# Detail table
# ---------------------------------------------------------------------
with st.expander("View filtered transaction data"):
    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
    )

st.caption(
    "Net Sales is reported before returns, consistent with the dataset "
    "definition. Targets are compared only at their supported "
    "representative-month aggregation level and for complete months."
)
