import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Business Sales Performance Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("Business Sales Performance Analytics")
st.write("Interactive Business Sales Dashboard")

# --------------------------------------------------
# FIND EXCEL FILE
# --------------------------------------------------

excel_files = list(Path(".").glob("*.xlsx"))

if not excel_files:
    st.error("Excel file not found in the repository.")
    st.stop()

FILE = excel_files[0]


# --------------------------------------------------
# LOAD EXCEL DATA
# --------------------------------------------------

def load_excel():
    excel = pd.ExcelFile(FILE)
    sheets = excel.sheet_names

    # Read the first sheet
    df = pd.read_excel(FILE, sheet_name=sheets[0])

    # Clean column names
    df.columns = df.columns.astype(str).str.strip()

    return df


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

try:
    df = load_excel()

except Exception as e:
    st.error("Unable to load the Excel file.")
    st.write(e)
    st.stop()


# --------------------------------------------------
# CLEAN DATA
# --------------------------------------------------

# Create Revenue if required columns exist
if "Revenue" not in df.columns:

    if "Quantity" in df.columns and "UnitPrice" in df.columns:
        df["Revenue"] = df["Quantity"] * df["UnitPrice"]

    elif "Quantity" in df.columns and "Unit Price" in df.columns:
        df["Revenue"] = df["Quantity"] * df["Unit Price"]


# Convert date column
if "InvoiceDate" in df.columns:
    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"],
        errors="coerce"
    )


# --------------------------------------------------
# KEY PERFORMANCE INDICATORS
# --------------------------------------------------

total_revenue = (
    df["Revenue"].sum()
    if "Revenue" in df.columns
    else 0
)

total_quantity = (
    df["Quantity"].sum()
    if "Quantity" in df.columns
    else 0
)

if "InvoiceNo" in df.columns:
    total_orders = df["InvoiceNo"].nunique()
else:
    total_orders = len(df)


if "Customer ID" in df.columns:
    total_customers = df["Customer ID"].nunique()

elif "CustomerID" in df.columns:
    total_customers = df["CustomerID"].nunique()

else:
    total_customers = 0


if "Country" in df.columns:
    total_countries = df["Country"].nunique()

else:
    total_countries = 0


# --------------------------------------------------
# KPI DISPLAY
# --------------------------------------------------

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
# TOP PRODUCTS
# --------------------------------------------------

st.subheader("Top 10 Products by Revenue")

if "Description" in df.columns and "Revenue" in df.columns:

    top_products = (
        df.groupby("Description")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(top_products)

else:
    st.info("Product information is not available.")


# --------------------------------------------------
# COUNTRY ANALYSIS
# --------------------------------------------------

if "Country" in df.columns and "Revenue" in df.columns:

    st.subheader("Revenue by Country")

    country_revenue = (
        df.groupby("Country")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(country_revenue)


# --------------------------------------------------
# MONTHLY REVENUE TREND
# --------------------------------------------------

if "InvoiceDate" in df.columns and "Revenue" in df.columns:

    st.subheader("Monthly Revenue Trend")

    monthly_revenue = (
        df.dropna(subset=["InvoiceDate"])
        .set_index("InvoiceDate")["Revenue"]
        .resample("ME")
        .sum()
    )

    st.line_chart(monthly_revenue)


# --------------------------------------------------
# DATA PREVIEW
# --------------------------------------------------

st.subheader("Sales Data Preview")

st.dataframe(
    df.head(100),
    use_container_width=True
)
