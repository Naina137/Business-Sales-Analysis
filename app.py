import streamlit as st
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIG
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
# FIND EXCEL FILE
# --------------------------------------------------

excel_files = list(Path(".").glob("*.xlsx"))

if not excel_files:
    st.error("Excel workbook not found.")
    st.stop()

FILE = excel_files[0]

# --------------------------------------------------
# LOAD EXCEL
# --------------------------------------------------

try:

    dashboard_raw = pd.read_excel(
        FILE,
        sheet_name="Dashboard",
        header=None
    )

    products = pd.read_excel(
        FILE,
        sheet_name="Top Products"
    )

    countries = pd.read_excel(
        FILE,
        sheet_name="Country Analysis"
    )

    monthly = pd.read_excel(
        FILE,
        sheet_name="Monthly Trend"
    )

except Exception as e:

    st.error("Unable to read the Excel workbook.")
    st.write(str(e))
    st.stop()

# --------------------------------------------------
# CLEAN COLUMN NAMES
# --------------------------------------------------

products.columns = (
    products.columns
    .astype(str)
    .str.strip()
)

countries.columns = (
    countries.columns
    .astype(str)
    .str.strip()
)

monthly.columns = (
    monthly.columns
    .astype(str)
    .str.strip()
)

# --------------------------------------------------
# CLEAN NUMERIC DATA
# --------------------------------------------------

for col in ["Revenue", "Quantity"]:

    if col in products.columns:
        products[col] = pd.to_numeric(
            products[col],
            errors="coerce"
        )

for col in ["Revenue", "Quantity", "Orders"]:

    if col in countries.columns:
        countries[col] = pd.to_numeric(
            countries[col],
            errors="coerce"
        )

for col in ["Revenue", "Quantity"]:

    if col in monthly.columns:
        monthly[col] = pd.to_numeric(
            monthly[col],
            errors="coerce"
        )

# --------------------------------------------------
# READ KPI VALUES FROM DASHBOARD
# --------------------------------------------------

kpis = {}

for i in range(len(dashboard_raw)):

    row = dashboard_raw.iloc[i].astype(str).str.strip().tolist()

    for j in range(len(row) - 1):

        metric = row[j]

        value = row[j + 1]

        if metric in [
            "Total Revenue",
            "Total Quantity",
            "Orders",
            "Customers",
            "Countries"
        ]:

            try:
                kpis[metric] = float(value)
            except:
                pass

# --------------------------------------------------
# KPI VALUES
# --------------------------------------------------

total_revenue = kpis.get(
    "Total Revenue",
    0
)

total_quantity = kpis.get(
    "Total Quantity",
    0
)

total_orders = kpis.get(
    "Orders",
    0
)

total_customers = kpis.get(
    "Customers",
    0
)

total_countries = kpis.get(
    "Countries",
    0
)

# --------------------------------------------------
# KEY PERFORMANCE INDICATORS
# --------------------------------------------------

st.subheader("Key Performance Indicators")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Total Revenue",
    f"{total_revenue:,.2f}"
)

c2.metric(
    "Total Quantity",
    f"{total_quantity:,.0f}"
)

c3.metric(
    "Orders",
    f"{total_orders:,.0f}"
)

c4.metric(
    "Customers",
    f"{total_customers:,.0f}"
)

c5.metric(
    "Countries",
    f"{total_countries:,.0f}"
)

st.divider()

# --------------------------------------------------
# BUSINESS INSIGHTS
# --------------------------------------------------

st.subheader("Business Insights")

# Top Product
if not products.empty:

    top_product = products.loc[
        products["Revenue"].idxmax()
    ]

    top_product_name = str(
        top_product["Description"]
    )

    top_product_revenue = float(
        top_product["Revenue"]
    )

else:

    top_product_name = "N/A"
    top_product_revenue = 0


# Top Country
if not countries.empty:

    top_country = countries.loc[
        countries["Revenue"].idxmax()
    ]

    top_country_name = str(
        top_country["Country"]
    )

    top_country_revenue = float(
        top_country["Revenue"]
    )

else:

    top_country_name = "N/A"
    top_country_revenue = 0


# Best Month
if not monthly.empty:

    monthly["Month"] = pd.to_datetime(
        monthly["Month"],
        errors="coerce"
    )

    valid_months = monthly.dropna(
        subset=["Month"]
    )

    if not valid_months.empty:

        best_month = valid_months.loc[
            valid_months["Revenue"].idxmax()
        ]

        best_month_name = best_month[
            "Month"
        ].strftime("%B %Y")

        best_month_revenue = float(
            best_month["Revenue"]
        )

    else:

        best_month_name = "N/A"
        best_month_revenue = 0

else:

    best_month_name = "N/A"
    best_month_revenue = 0


# Average Order Value
if total_orders > 0:

    average_order_value = (
        total_revenue / total_orders
    )

else:

    average_order_value = 0

# --------------------------------------------------
# INSIGHT CARDS
# --------------------------------------------------

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
    )

    st.bar_chart(
        top_products.set_index(
            "Description"
        )["Revenue"]
    )

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

st.subheader("Top 10 Countries by Revenue")

if not countries.empty:

    top_countries = (
        countries
        .sort_values(
            "Revenue",
            ascending=False
        )
        .head(10)
    )

    st.bar_chart(
        top_countries.set_index(
            "Country"
        )["Revenue"]
    )

    st.dataframe(
        top_countries,
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

    monthly_chart = monthly.dropna(
        subset=["Month"]
    ).sort_values("Month")

    st.line_chart(
        monthly_chart.set_index(
            "Month"
        )["Revenue"]
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

tab1, tab2, tab3 = st.tabs(
    [
        "Top Products",
        "Country Analysis",
        "Monthly Trend"
    ]
)

with tab1:

    st.dataframe(
        products,
        use_container_width=True,
        hide_index=True
    )

with tab2:

    st.dataframe(
        countries,
        use_container_width=True,
        hide_index=True
    )

with tab3:

    st.dataframe(
        monthly,
        use_container_width=True,
        hide_index=True
    )

# --------------------------------------------------
# DOWNLOAD
# --------------------------------------------------

st.divider()

st.subheader("Download Analysis")

csv_file = products.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "Download Top Products CSV",
    csv_file,
    "top_products.csv",
    "text/csv"
)

st.caption(
    "Source: Business Sales Analysis Excel workbook"
)
