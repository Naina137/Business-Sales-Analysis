# Business Sales Performance Analytics

An interactive **Business Sales Performance Analytics Dashboard** built using **Python, Pandas, and Streamlit** to analyze business sales data and generate meaningful business insights.

## Live Demo

**Live Dashboard:**  
https://business-sales-analysis-gj2e5z4fwgfqmqlr5keivp.streamlit.app

**GitHub Repository:**  
https://github.com/Naina137/Business-Sales-Analysis

---

## Project Overview

Business Sales Performance Analytics is a data analytics project that transforms business sales data stored in an Excel workbook into an interactive and easy-to-understand dashboard.

The application processes sales data using Python and Pandas and presents important business metrics, product performance, country-wise revenue, and monthly sales trends through Streamlit.

The main purpose of this project is to understand sales performance and identify useful patterns that can support data-driven business decisions.

---

## Objectives

- Analyze overall business sales performance
- Calculate important business KPIs
- Identify top-performing products
- Analyze country-wise revenue
- Understand monthly revenue trends
- Generate meaningful business insights
- Provide an interactive data exploration interface
- Allow analyzed data to be downloaded

---

## Key Features

### Key Performance Indicators

The dashboard provides:

- Total Revenue
- Total Quantity
- Total Orders
- Total Customers
- Total Countries

### Business Insights

The dashboard identifies:

- Top Product by Revenue
- Top Country by Revenue
- Best Month by Revenue
- Average Order Value

### Product Revenue Analysis

The dashboard displays the **Top 10 Products by Revenue** using an interactive chart and detailed data table.

### Country Analysis

The dashboard compares the **Top 10 Countries by Revenue** and provides country-wise sales information.

### Monthly Revenue Trend

The dashboard visualizes revenue trends over time and identifies the best-performing month.

### Data Explorer

Users can explore the processed data through:

- Dashboard
- Top Products
- Country Analysis
- Monthly Trend

### Data Download

The dashboard includes a download option that allows users to export the Top Products analysis as a CSV file for further analysis.

---

## Dashboard Preview

### Main Dashboard

Provides an overview of overall business performance through key KPIs such as revenue, quantity, orders, customers, and countries.

![Business Sales Dashboard](dashboard.png)

### Revenue Analysis

Highlights the top-performing products based on revenue and provides a clear comparison of product-level sales performance.


![Revenue Analysis](revenue.png)

### Country Analysis

Presents country-wise revenue performance and highlights the countries contributing the most to overall sales.

![Country Analysis](country.png)

### Monthly Revenue Trend

Shows how revenue changes over time and helps identify the strongest-performing months and overall sales patterns.

![Monthly Revenue Trend](monthly.png)

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Pandas | Data processing and analysis |
| Streamlit | Interactive dashboard |
| Microsoft Excel | Data source |
| Git | Version control |
| GitHub | Project hosting |

---

## Data Source

The project uses an Excel workbook containing the following analysis sheets:

- **Dashboard**
- **Top Products**
- **Country Analysis**
- **Monthly Trend**

The workbook acts as the primary data source for the Streamlit application.

---

## Project Workflow

```text
Excel Sales Data
       ↓
Data Loading
       ↓
Data Cleaning
       ↓
Data Processing
       ↓
KPI Calculation
       ↓
Business Analysis
       ↓
Data Visualization
       ↓
Interactive Streamlit Dashboard
```

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
```

---

## How to Run Locally

Clone the repository:

```bash
git clone https://github.com/Naina137/Business-Sales-Analysis.git
```

Navigate to the project folder:

```bash
cd Business-Sales-Analysis
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

The dashboard will open automatically in your default browser.

If it does not open automatically, visit:

```text
http://localhost:8501
```

Make sure the Excel workbook is present in the project folder before running the application.

---

## Deployment

The application is deployed using **Streamlit Community Cloud**.

**Live Dashboard:**  
https://business-sales-analysis-gj2e5z4fwgfqmqlr5keivp.streamlit.app

---

## Future Improvements

- Interactive date filters
- Country and product filters
- Machine Learning-based sales forecasting
- Customer segmentation
- Product category analysis
- Advanced sales visualizations
- Predictive sales analytics
- Automated business reports

---

## Author

### Naina Kumari

**Computer Science & Engineering — Data Science**

Interested in Data Science, Data Analytics, Machine Learning, Business Intelligence, and building practical data-driven applications.

### Connect With Me

**GitHub:**  
https://github.com/Naina137

**LinkedIn:**  
https://www.linkedin.com/in/naina-kumari-06373132b

**Live Project:**  
https://business-sales-analysis-gj2e5z4fwgfqmqlr5keivp.streamlit.app

Feel free to explore the project, review the source code, or connect with me for collaboration and opportunities.

---

## Feedback & Collaboration

Suggestions and feedback are welcome.

If you have any ideas for improving this project, feel free to open an issue on GitHub or connect with me through LinkedIn.

---

## License

This project is created for educational and portfolio purposes.
