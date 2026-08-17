import streamlit as st
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="Business Sales Performance Analytics",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("Business Sales Performance Analytics")
st.caption("Interactive analysis of business sales performance")

# --------------------------------------------------
# FIND EXCEL WORKBOOK
# --------------------------------------------------

excel_files = list(Path(".").glob("*.xlsx"))

if not excel_files:
    st.error("Excel workbook not found.")
    st.stop()


# Find the workbook containing the required sheets
FILE = None

required_sheets = {
    "Dashboard",
    "Top Products",
    "Country Analysis",
    "Monthly Trend"
}

for file in excel_files:
    try:
        sheets = set(pd.ExcelFile(file).sheet_names)

        if required_sheets.issubset(sheets):
            FILE = file
            break

    except Exception:
        continue


if FILE is None:
    st.error(
        "The required Business Sales Analysis workbook was not found."
    )
    st.stop()


# --------------------------------------------------
# LOAD EXCEL SHEETS
# --------------------------------------------------

try:
    dashboard = pd.read_excel(FILE, sheet_name="Dashboard")
    products = pd.read_excel(FILE, sheet_name="Top Products")
    countries = pd.read_excel(FILE, sheet_name="Country Analysis")
    monthly = pd.read_excel(FILE, sheet_name="Monthly Trend")

except Exception as e:
    st.error("Unable to read the Excel workbook.")
    st.write(e)
    st.stop()


# --------------------------------------------------
# CLEAN COLUMN NAMES
# --------------------------------------------------

for df in [dashboard, products, countries, monthly]:
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.replace("\n", " ", regex=False)
    )


# --------------------------------------------------
# CLEAN NUMERIC COLUMNS
# --------------------------------------------------

for df, columns in [
    (products, ["Revenue", "Quantity"]),
    (countries, ["Revenue", "Quantity", "Orders"]),
    (monthly, ["Revenue", "Quantity"])
]:

    for column in columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )


# --------------------------------------------------
# GET KPI VALUES FROM DASHBOARD SHEET
# --------------------------------------------------

try:

    kpi = dict(
        zip(
            dashboard["Metric"],
            dashboard["Value"]
        )
    )

    total_revenue = float(
        kpi.get("Total Revenue", 0)
    )

    total_quantity = int(
        kpi.get("Total Quantity", 0)
    )

    total_orders = int(
        kpi.get("Orders", 0)
    )

    total_customers = int(
        kpi.get("Customers", 0)
    )

    total_countries = int(
        kpi.get("Countries", 0)
    )

except Exception:

    total_revenue = 0
    total_quantity = 0
    total_orders = 0
    total_customers = 0
    total_countries = 0


# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

st.subheader("Key Performance Indicators")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Total Revenue",
    f"{total_revenue:,.2f}"
)

c2.metric(
    "Total Quantity",
    f"{total_quantity:,}"
)

c3.metric(
    "Orders",
    f"{total_orders:,}"
)

c4.metric(
    "Customers",
    f"{total_customers:,}"
)

c5.metric(
    "Countries",
    f"{total_countries:,}"
)


st.divider()


# --------------------------------------------------
# BUSINESS INSIGHTS
# --------------------------------------------------

st.subheader("Business Insights")

if not products.empty:

    top_product = products.loc[
        products["Revenue"].idxmax()
    ]

    top_product_name = top_product["Description"]
    top_product_revenue = top_product["Revenue"]

else:

    top_product_name = "N/A"
    top_product_revenue = 0


if not countries.empty:

    top_country = countries.loc[
        countries["Revenue"].idxmax()
    ]

    top_country_name = top_country["Country"]
    top_country_revenue = top_country["Revenue"]

else:

    top_country_name = "N/A"
    top_country_revenue = 0


if not monthly.empty:

    best_month = monthly.loc[
        monthly["Revenue"].idxmax()
    ]

    best_month_name = best_month["Month"]
    best_month_revenue = best_month["Revenue"]

else:

    best_month_name = "N/A"
    best_month_revenue = 0


average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)


i1, i2, i3, i4 = st.columns(4)

i1.metric(
    "Top Product Revenue",
    f"{top_product_revenue:,.2f}"
)

i2.metric(
    "Top Country Revenue",
    f"{top_country_revenue:,.2f}"
)

i3.metric(
    "Best Month Revenue",
    f"{best_month_revenue:,.2f}"
)

i4.metric(
    "Average Order Value",
    f"{average_order_value:,.2f}"
)


st.caption(
    f"Top product: {top_product_name} | "
    f"Top country: {top_country_name} | "
    f"Best month: {best_month_name}"
)


st.divider()


# --------------------------------------------------
# TOP PRODUCTS
# --------------------------------------------------

st.subheader("Top 10 Products by Revenue")

if not products.empty:

    top_products = (
        products
        .sort_values(
            "Revenue",
            ascending=False
        )
        .head(10)
        .copy()
    )

    chart_data = top_products.set_index(
        "Description"
    )["Revenue"]

    st.bar_chart(chart_data)

    st.dataframe(
        top_products,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No product data available.")


st.divider()


# --------------------------------------------------
# COUNTRY ANALYSIS
# --------------------------------------------------

st.subheader("Revenue by Country")

if not countries.empty:

    country_chart = (
        countries
        .sort_values(
            "Revenue",
            ascending=False
        )
        .head(10)
        .copy()
    )

    chart_data = country_chart.set_index(
        "Country"
    )["Revenue"]

    st.bar_chart(chart_data)

    st.dataframe(
        country_chart,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No country data available.")


st.divider()


# --------------------------------------------------
# MONTHLY TREND
# --------------------------------------------------

st.subheader("Monthly Revenue Trend")

if not monthly.empty:

    monthly_chart = monthly.copy()

    monthly_chart["Month"] = pd.to_datetime(
        monthly_chart["Month"],
        errors="coerce"
    )

    monthly_chart = monthly_chart.dropna(
        subset=["Month"]
    )

    monthly_chart = monthly_chart.sort_values(
        "Month"
    )

    st.line_chart(
        monthly_chart.set_index("Month")["Revenue"]
    )

    st.dataframe(
        monthly_chart,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No monthly data available.")


st.divider()


# --------------------------------------------------
# DATA EXPLORER
# --------------------------------------------------

st.subheader("Data Explorer")

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Dashboard",
        "Top Products",
        "Country Analysis",
        "Monthly Trend"
    ]
)

with tab1:
    st.dataframe(
        dashboard,
        use_container_width=True,
        hide_index=True
    )

with tab2:
    st.dataframe(
        products,
        use_container_width=True,
        hide_index=True
    )

with tab3:
    st.dataframe(
        countries,
        use_container_width=True,
        hide_index=True
    )

with tab4:
    st.dataframe(
        monthly,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# DOWNLOAD DATA
# --------------------------------------------------

st.divider()

st.subheader("Download Analysis")

csv_data = products.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Top Products CSV",
    data=csv_data,
    file_name="top_products.csv",
    mime="text/csv"
)

st.caption(
    "Source: Business Sales Analysis Excel workbook"
)
