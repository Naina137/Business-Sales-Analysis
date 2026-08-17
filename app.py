import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Business Sales Performance Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("Business Sales Performance Analytics")
st.caption("Interactive analysis of business sales performance")

# Find Excel file
excel_files = list(Path(".").glob("*.xlsx"))

if not excel_files:
    st.error("Excel workbook not found.")
    st.stop()

FILE = excel_files[0]

# Load sheets
try:
    dashboard = pd.read_excel(FILE, sheet_name="Dashboard", header=None)
    products = pd.read_excel(FILE, sheet_name="Top Products")
    countries = pd.read_excel(FILE, sheet_name="Country Analysis")
    monthly = pd.read_excel(FILE, sheet_name="Monthly Trend")

except Exception as e:
    st.error("Unable to read the Excel workbook.")
    st.write(str(e))
    st.stop()

# Clean column names
products.columns = products.columns.astype(str).str.strip()
countries.columns = countries.columns.astype(str).str.strip()
monthly.columns = monthly.columns.astype(str).str.strip()

# Convert numeric columns
for col in ["Revenue", "Quantity"]:
    if col in products.columns:
        products[col] = pd.to_numeric(products[col], errors="coerce")

for col in ["Revenue", "Quantity", "Orders"]:
    if col in countries.columns:
        countries[col] = pd.to_numeric(countries[col], errors="coerce")

if "Revenue" in monthly.columns:
    monthly["Revenue"] = pd.to_numeric(
        monthly["Revenue"],
        errors="coerce"
    )

if "Quantity" in monthly.columns:
    monthly["Quantity"] = pd.to_numeric(
        monthly["Quantity"],
        errors="coerce"
    )

# -----------------------------------------
# KPI VALUES FROM DASHBOARD SHEET
# -----------------------------------------

kpis = {
    "Total Revenue": 0,
    "Total Quantity": 0,
    "Orders": 0,
    "Customers": 0,
    "Countries": 0
}

for i in range(len(dashboard)):
    row = dashboard.iloc[i].tolist()

    for j in range(len(row) - 1):
        metric = str(row[j]).strip()

        if metric in kpis:
            value = pd.to_numeric(
                row[j + 1],
                errors="coerce"
            )

            if pd.notna(value):
                kpis[metric] = float(value)

total_revenue = kpis["Total Revenue"]
total_quantity = kpis["Total Quantity"]
total_orders = kpis["Orders"]
total_customers = kpis["Customers"]
total_countries = kpis["Countries"]

# -----------------------------------------
# KPI SECTION
# -----------------------------------------

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

# -----------------------------------------
# BUSINESS INSIGHTS
# -----------------------------------------

st.subheader("Business Insights")

# Top product
if (
    not products.empty
    and "Revenue" in products.columns
    and "Description" in products.columns
):

    products_valid = products.dropna(subset=["Revenue"])

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

# Top country
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

# Best month
best_month_name = "N/A"
best_month_revenue = 0

if (
    not monthly.empty
    and "Month" in monthly.columns
    and "Revenue" in monthly.columns
):

    monthly["Month"] = pd.to_datetime(
        monthly["Month"],
        errors="coerce"
    )

    valid_months = monthly.dropna(
        subset=["Month", "Revenue"]
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

# -----------------------------------------
# TOP PRODUCTS
# -----------------------------------------

st.subheader("Top 10 Products by Revenue")

if (
    not products.empty
    and "Revenue" in products.columns
    and "Description" in products.columns
):

    top_products = (
        products
        .dropna(subset=["Revenue"])
        .sort_values("Revenue", ascending=False)
        .head(10)
    )

    if not top_products.empty:

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
    st.info("Product information is not available.")

st.divider()

# -----------------------------------------
# COUNTRY ANALYSIS
# -----------------------------------------

st.subheader("Top 10 Countries by Revenue")

if (
    not countries.empty
    and "Revenue" in countries.columns
    and "Country" in countries.columns
):

    top_countries = (
        countries
        .dropna(subset=["Revenue"])
        .sort_values("Revenue", ascending=False)
        .head(10)
    )

    if not top_countries.empty:

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
    st.info("Country information is not available.")

st.divider()

# -----------------------------------------
# MONTHLY TREND
# -----------------------------------------

st.subheader("Monthly Revenue Trend")

if (
    not monthly.empty
    and "Month" in monthly.columns
    and "Revenue" in monthly.columns
):

    monthly_chart = (
        monthly
        .dropna(subset=["Month", "Revenue"])
        .sort_values("Month")
    )

    if not monthly_chart.empty:

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
    st.info("Monthly sales information is not available.")

st.divider()

# -----------------------------------------
# DATA EXPLORER
# -----------------------------------------

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
