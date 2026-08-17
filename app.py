import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(
    page_title="Business Sales Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("Business Sales Performance Analytics")
st.write("Interactive Business Sales Dashboard")

# Excel file
FILE = "Task1_Business_Sales_Analysis-16 (1).xlsx"


@st.cache_data
def load_excel():
    excel = pd.ExcelFile(FILE)
    sheets = excel.sheet_names

    data_sheet = None

    # Automatically find the sheet containing sales data
    for sheet in sheets:
        temp = pd.read_excel(FILE, sheet_name=sheet)
        temp.columns = temp.columns.astype(str).str.strip()

        if "Quantity" in temp.columns:
            data_sheet = sheet
            break

    return excel, sheets, data_sheet


try:
    excel, sheets, data_sheet = load_excel()

    # Sidebar
    st.sidebar.header("Workbook")
    st.sidebar.write("Available Sheets:")

    for sheet in sheets:
        st.sidebar.write("• " + sheet)

    # Sales data found
    if data_sheet:

        df = pd.read_excel(FILE, sheet_name=data_sheet)
        df.columns = df.columns.astype(str).str.strip()

        # Create Revenue
        if "Revenue" not in df.columns:

            if "Quantity" in df.columns and "UnitPrice" in df.columns:
                df["Revenue"] = (
                    pd.to_numeric(
                        df["Quantity"], errors="coerce"
                    ).fillna(0)
                    *
                    pd.to_numeric(
                        df["UnitPrice"], errors="coerce"
                    ).fillna(0)
                )

            elif "Quantity" in df.columns and "Price" in df.columns:
                df["Revenue"] = (
                    pd.to_numeric(
                        df["Quantity"], errors="coerce"
                    ).fillna(0)
                    *
                    pd.to_numeric(
                        df["Price"], errors="coerce"
                    ).fillna(0)
                )

        # Convert date
        if "InvoiceDate" in df.columns:
            df["InvoiceDate"] = pd.to_datetime(
                df["InvoiceDate"],
                errors="coerce"
            )

        # Key Performance Indicators
        st.subheader("Key Performance Indicators")

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

        total_orders = (
            df["InvoiceNo"].nunique()
            if "InvoiceNo" in df.columns
            else len(df)
        )

        if "Customer ID" in df.columns:
            total_customers = df["Customer ID"].nunique()
        elif "CustomerID" in df.columns:
            total_customers = df["CustomerID"].nunique()
        else:
            total_customers = 0

        total_countries = (
            df["Country"].nunique()
            if "Country" in df.columns
            else 0
        )

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

        # Top Products
        if "Description" in df.columns and "Revenue" in df.columns:

            st.subheader("Top 10 Products by Revenue")

            top_products = (
                df.groupby("Description")["Revenue"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
            )

            st.bar_chart(top_products)

        # Country Analysis
        if "Country" in df.columns and "Revenue" in df.columns:

            st.subheader("Top 10 Countries by Revenue")

            country_revenue = (
                df.groupby("Country")["Revenue"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
            )

            st.bar_chart(country_revenue)

        # Monthly Trend
        if "InvoiceDate" in df.columns and "Revenue" in df.columns:

            st.subheader("Monthly Revenue Trend")

            monthly = (
                df.dropna(subset=["InvoiceDate"])
                .set_index("InvoiceDate")["Revenue"]
                .resample("ME")
                .sum()
            )

            st.line_chart(monthly)

        # Data Preview
        st.subheader("Sales Data Preview")

        st.dataframe(
            df.head(100),
            use_container_width=True
        )

    else:

        st.warning(
            "No raw sales-data sheet containing 'Quantity' was found."
        )

        st.info(
            "The workbook contains dashboard or analysis sheets, "
            "but the original transaction data sheet is missing."
        )

        if "Dashboard" in sheets:

            dashboard = pd.read_excel(
                FILE,
                sheet_name="Dashboard"
            )

            dashboard.columns = (
                dashboard.columns
                .astype(str)
                .str.strip()
            )

            st.subheader("Dashboard")

            st.dataframe(
                dashboard,
                use_container_width=True
            )

except FileNotFoundError:

    st.error("Excel file not found.")

    st.write(
        "Make sure the Excel file is uploaded to the GitHub repository "
        "with exactly this name:"
    )

    st.code(FILE)

except Exception as e:

    st.error("Something went wrong.")
    st.exception(e)
