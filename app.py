import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Business Sales Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Business Sales Performance Analytics")
st.write("Interactive sales dashboard")

# Excel file
FILE = "Task1_Business_Sales_Analysis-16 (1).xlsx"

@st.cache_data
def load_data():
    df = pd.read_excel(FILE)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Create Revenue if it doesn't already exist
    if "Revenue" not in df.columns:
        df["Revenue"] = df["Quantity"] * df["UnitPrice"]

    # Convert date
    if "InvoiceDate" in df.columns:
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

    return df


try:
    df = load_data()

    # ---------- KPIs ----------
    total_revenue = df["Revenue"].sum()
    total_quantity = df["Quantity"].sum()
    total_orders = df["InvoiceNo"].nunique() if "InvoiceNo" in df.columns else len(df)

    if "Customer ID" in df.columns:
        total_customers = df["Customer ID"].nunique()
    elif "CustomerID" in df.columns:
        total_customers = df["CustomerID"].nunique()
    else:
        total_customers = 0

    total_countries = df["Country"].nunique() if "Country" in df.columns else 0

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Total Revenue", f"{total_revenue:,.2f}")
    c2.metric("Total Quantity", f"{total_quantity:,.0f}")
    c3.metric("Orders", f"{total_orders:,}")
    c4.metric("Customers", f"{total_customers:,}")
    c5.metric("Countries", f"{total_countries:,}")

    st.divider()

    # ---------- TOP PRODUCTS ----------
    st.subheader("🏆 Top 10 Products by Revenue")

    if "Description" in df.columns:
        top_products = (
            df.groupby("Description")["Revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        st.bar_chart(top_products)

    # ---------- COUNTRY ANALYSIS ----------
    if "Country" in df.columns:
        st.subheader("🌍 Revenue by Country")

        country_revenue = (
            df.groupby("Country")["Revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        st.bar_chart(country_revenue)

    # ---------- MONTHLY TREND ----------
    if "InvoiceDate" in df.columns:
        st.subheader("📈 Monthly Revenue Trend")

        monthly = (
            df.dropna(subset=["InvoiceDate"])
            .set_index("InvoiceDate")["Revenue"]
            .resample("ME")
            .sum()
        )

        st.line_chart(monthly)

    # ---------- DATA PREVIEW ----------
    st.subheader("📋 Sales Data Preview")
    st.dataframe(df.head(100), use_container_width=True)

except Exception as e:
    st.error("Unable to load the Excel file.")
    st.write("Error:", e)
