# Business Sales Performance Analytics

An interactive sales analytics dashboard built with Python and Streamlit to analyze business sales performance, identify revenue trends, and generate meaningful business insights from Excel data.

## Live Demo

[View Live Dashboard](https://business-sales-analysis-gj2e5z4fwgfqmqlr5keivp.streamlit.app)

## GitHub Repository

[View Source Code](https://github.com/Naina137/Business-Sales-Analysis)

---

## Project Overview

Business Sales Performance Analytics is an interactive data analysis project that transforms business sales data into meaningful visual insights.

The application uses an Excel workbook as the data source and processes the data using Python and Pandas. The results are presented through an interactive Streamlit dashboard covering overall performance, product revenue, country-wise sales, and monthly trends.

The project focuses on making business sales data easier to explore, understand, and use for data-driven decision making.

---

## Dashboard

The main dashboard provides a quick overview of the overall business performance through key performance indicators and business insights.

![Business Sales Dashboard](dashboard.png)

### Key Performance Indicators

- Total Revenue
- Total Quantity
- Total Orders
- Total Customers
- Total Countries

The dashboard also highlights the top-performing product, top-performing country, best-performing month, and average order value.

---

## Product Revenue Analysis

The product analysis identifies the top products based on revenue generation and provides a detailed comparison of product performance.

![Product Revenue Analysis](revenue.png)

### Analysis Includes

- Top 10 products by revenue
- Product-wise revenue comparison
- Product quantity information
- Revenue contribution of individual products

---

## Country Analysis

The country analysis provides a geographical view of business performance by comparing revenue across different countries.

![Country Revenue Analysis](country.png)

### Analysis Includes

- Top 10 countries by revenue
- Country-wise revenue comparison
- Quantity sold by country
- Number of orders by country

---

## Monthly Sales Trend

The monthly trend analysis shows how revenue changes over time and helps identify high-performing and low-performing periods.

![Monthly Revenue Trend](monthly.png)

### Analysis Includes

- Monthly revenue trend
- Monthly quantity trend
- Best-performing month
- Revenue patterns over time

---

## Key Features

- Interactive sales performance dashboard
- KPI-based business overview
- Top 10 product analysis
- Country-wise revenue analysis
- Monthly sales trend analysis
- Business performance insights
- Average Order Value calculation
- Interactive data explorer
- Detailed analysis tables
- CSV download for product analysis
- Excel-based data processing

---

## Dataset

The project uses an Excel workbook containing four analytical sheets:

| Sheet | Description |
|---|---|
| Dashboard | Overall business KPIs and performance summary |
| Top Products | Product-wise revenue and quantity analysis |
| Country Analysis | Country-wise revenue, quantity, and order analysis |
| Monthly Trend | Monthly revenue and quantity trends |

---

## Technologies Used

- Python
- Pandas
- Streamlit
- OpenPyXL
- Microsoft Excel
- GitHub
- Streamlit Community Cloud

---

## Project Structure

```text
Business-Sales-Analysis/
│
├── app.py
├── requirements.txt
├── README.md
├── dashboard.png
├── revenue.png
├── country.png
├── monthly.png
└── Task1_Business_Sales_Analysis-16 (1).xlsx


How to Run Locally
Step 1: Clone the Repository
git clone https://github.com/Naina137/Business-Sales-Analysis.git
Step 2: Navigate to the Project Folder
cd Business-Sales-Analysis
Step 3: Install Dependencies
pip install -r requirements.txt
Step 4: Run the Streamlit Application
streamlit run app.py
The application will open automatically in your default browser.
If it does not open automatically, visit:
http://localhost:8501
Make sure the Excel workbook is present in the project folder before running the application.
Deployment
The application is deployed using Streamlit Community Cloud.
Live Dashboard:
https://business-sales-analysis-gj2e5z4fwgfqmqlr5keivp.streamlit.app⁠
Future Improvements
Interactive date and country filters
Sales forecasting using Machine Learning
Customer segmentation
Product category analysis
Advanced sales visualizations
Automated business reports
Predictive sales analytics
Author
Naina Kumari
Computer Science & Engineering — Data Science
Interested in Data Science, Data Analytics, Machine Learning, and building practical data-driven applications.
Connect With Me
GitHub⁠
LinkedIn⁠
Feel free to explore the project, review the source code, or connect with me for collaboration and opportunities.
License
This project is created for educational and portfolio purposes.
