import streamlit as st
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="Business Sales Performance Analytics",
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

required_sheets = {
    "Dashboard",
    "Top Products",
    "Country Analysis",
    "Monthly Trend"
}

FILE = None

for file in excel_files:
    try:
        workbook = pd.ExcelFile(file)
        sheets = set(workbook.sheet_names)

        if required_sheets.issubset(sheets):
            FILE = file
            break

    except Exception:
        pass

if FILE is None:
    st.error("Required Business Sales Analysis workbook was not found.")
    st.stop()

# --------------------------------------------------
# LOAD EXCEL SHEETS
# --------------------------------------------------

@st.cache_data
def load_data(file_path):

    dashboard = pd.read_excel(
        file_path,
        sheet_name="Dashboard"
    )

    products = pd.read_excel(
        file_path,
        sheet_name="Top Products"
    )

    countries = pd.read_excel(
        file_path,
        sheet_name="Country Analysis"
    )

    monthly = pd.read_excel(
        file_path,
        sheet_name="Monthly Trend"
    )

    return dashboard, products, countries, monthly


try:
    dashboard, products, countries, monthly = load_data(FILE)

except Exception as e:
    st.error("Unable to read the Excel workbook.")
    st.write(str(e))
    st.stop()

# --------------------------------------------------
# CLEAN COLUMN NAMES
# --------------------------------------------------

def clean_columns(df):

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.replace("\n", " ", regex=False)
    )

    return df


dashboard = clean_columns(dashboard)
products = clean_columns(products)
countries = clean_columns(countries)
monthly = clean_columns(monthly)

# --------------------------------------------------
# CLEAN DATA
# --------------------------------------------------

for column in ["Revenue", "Quantity"]:
    if column in products.columns:
        products[column] = pd.to_numeric(
            products[column],
            errors="coerce"
        )

for column in ["Revenue", "Quantity", "Orders"]:
    if column in countries.columns:
        countries[column] = pd.to_numeric(
            countries[column],
            errors="coerce"
        )

for column in ["Revenue", "Quantity"]:
    if column in monthly.columns:
        monthly[column] = pd.to_numeric(
            monthly[column],
            errors="coerce"
        )

# --------------------------------------------------
# GET KPI VALUES FROM DASHBOARD SHEET
# --------------------------------------------------

dashboard = dashboard.dropna(
    subset=["Metric"]
)

dashboard["Metric"] = (
    dashboard["Metric"]
    .astype(str)
    .str.strip()
)

dashboard["Value"] = pd.to_numeric(
    dashboard["Value"],
    errors="coerce"
)


def get_kpi(metric_name):
    row = dashboard[
        dashboard["Metric"].str.lower()
        == metric_name.lower()
    ]

    if not row.empty:
        return row.iloc[0]["Value"]

    return 0


total_revenue = get_kpi("Total Revenue")
total_quantity = get_kpi("Total Quantity")
total_orders = get_kpi("Orders")
total_customers = get_kpi("Customers")
total_countries = get_kpi("Countries")

# --------------------------------------------------
# KEY PERFORMANCE INDICATORS
# --------------------------------------------------

st.subheader("Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Revenue",
    f"{total_revenue:,.2f}"
)

col2.metric(
    "Total Quantity",
    f"{total_quantity:,.0f}"
)

col3.metric(
    "Orders",
    f"{total_orders:,.0f}"
)

col4.metric(
    "Customers",
    f"{total_customers:,.0f}"
)

col5.metric(
    "Countries",
    f"{total_countries:,.0f}"
)

st.divider()

# --------------------------------------------------
# BUSINESS INSIGHTS
# --------------------------------------------------

st.subheader("Business Insights")

# Top Product

if (
    not products.empty
    and "Revenue" in products.columns
    and "Description" in products.columns
):

    products_valid = products.dropna(
        subset=["Revenue"]
    )

    if not products_valid.empty:

        top_product = products_valid.loc[
            products_valid["Revenue"].idxmax()
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

else:
    top_product_name = "N/A"
    top_product_revenue = 0


# Top Country

if (
    not countries.empty
    and "Revenue" in countries.columns
    and "Country" in countries.columns
):

    countries_valid = countries.dropna(
        subset=["Revenue"]
    )

    if not countries_valid.empty:

        top_country = countries_valid.loc[
            countries_valid["Revenue"].idxmax()
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

else:
    top_country_name = "N/A"
    top_country_revenue = 0


# Best Month

if (
    not monthly.empty
    and "Revenue" in monthly.columns
    and "Month" in monthly.columns
):

    monthly_valid = monthly.dropna(
        subset=["Revenue"]
    ).copy()

    monthly_valid["Month"] = pd.to_datetime(
        monthly_valid["Month"],
        errors="coerce"
    )

    monthly_valid = monthly_valid.dropna(
        subset=["Month"]
    )

    if not monthly_valid.empty:

        best_month = monthly_valid.loc[
            monthly_valid["Revenue"].idxmax()
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

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)

# --------------------------------------------------
# INSIGHT METRICS
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

if (
    not products.empty
    and "Description" in products.columns
    and "Revenue" in products.columns
):

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

st.subheader("Top Countries by Revenue")

if (
    not countries.empty
    and "Country" in countries.columns
    and "Revenue" in countries.columns
):

    top_countries = (
        countries
        .sort_values(
            "Revenue",
            ascending=False
        )
        .head(10)
        .copy()
    )

    country_chart = top_countries.set_index(
        "Country"
    )["Revenue"]

    st.bar_chart(country_chart)

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

if (
    not monthly.empty
    and "Month" in monthly.columns
    and "Revenue" in monthly.columns
):

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
