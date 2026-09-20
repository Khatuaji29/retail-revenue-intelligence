# RETAILIQ — Revenue & Customer Intelligence

> **From raw retail transactions to business decisions.**

### 🔗 Explore the Project

🚀 **Live Dashboard:**  
https://retail-revenue-intelligence.streamlit.app/

💻 **GitHub Repository:**  
https://github.com/Khatuaji29/retail-revenue-intelligence

---

RetailIQ is a business-focused **e-commerce analytics dashboard** built
around the UCI Online Retail II dataset.

The project transforms more than **1 million raw transaction records**
into a decision-support product for understanding:

- revenue performance
- customer value and concentration
- new vs returning customer behaviour
- product performance
- returns and revenue leakage
- transaction anomalies
- business actions worth investigating

The goal was not to create another basic EDA notebook.

**The goal was to build something that looks and behaves like a real
business intelligence product.**

------------------------------------------------------------------------

## ✦ Why RetailIQ?

Raw transaction data tells you **what happened**.

RetailIQ tries to answer:

> **Why does it matter to the business, and what should we investigate
> next?**

The project follows a simple business-analysis flow:

``` text
RAW RETAIL DATA
      ↓
DATA QUALITY & CLEANING
      ↓
BUSINESS DEFINITIONS
      ↓
FEATURE ENGINEERING
      ↓
CUSTOMER INTELLIGENCE
      ↓
PRODUCT & REVENUE RISK
      ↓
INTERACTIVE DASHBOARD
      ↓
BUSINESS DECISIONS
```

------------------------------------------------------------------------

## ✦ Business Questions

RetailIQ was designed around practical management questions:

  -----------------------------------------------------------------------
  Business Question                   Analysis
  ----------------------------------- -----------------------------------
  How is revenue performing?          Revenue, orders, AOV and monthly
                                      trends

  What is driving growth?             Customer, order and AOV
                                      decomposition

  Who creates the most value?         RFM segmentation

  How concentrated is revenue?        Customer Pareto / concentration

  Are customers new or returning?     Customer-status analysis

  Which products matter?              Regular-product revenue analysis

  Where may revenue be leaking?       Returns and return-value analysis

  Which records need investigation?   Anomaly and transaction-risk
                                      analysis

  What should management investigate  Decision Center
  next?                               
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# ✦ Dashboard

RetailIQ is organised around four business views.

### 01 --- Executive Overview

A management-level view of:

-   Total Revenue
-   Orders
-   Customers
-   Average Order Value
-   Champion Revenue Share
-   Monthly revenue movement
-   Growth drivers
-   New vs returning customer revenue
-   Market performance

### 02 --- Customer Intelligence

Understand customer economics through:

-   RFM segmentation
-   Revenue by customer segment
-   Segment revenue share
-   Customer economics
-   Customer concentration
-   Pareto analysis
-   High-value customer exposure

### 03 --- Product & Revenue Risk

Identify:

-   Top-performing regular products
-   High-return products
-   Return exposure
-   Revenue leakage
-   Operational/product anomalies
-   Investigation candidates

### 04 --- Decision Center

The final layer translates analysis into business questions and actions.

Instead of stopping at:

> "This product has a high return rate."

RetailIQ asks:

> "Should we investigate product quality, fulfilment, product
> description, customer expectations or the underlying orders?"

------------------------------------------------------------------------

# ✦ Key Findings

The project produced several important business signals.

### Revenue

-   **£20.48M** valid sales revenue
-   **40,078** valid sales orders
-   **5,878** identifiable customers
-   **£510.92** average order value
-   **11.21M** units sold

### Customer concentration

Revenue is highly concentrated among a relatively small customer base:

  Customer Group     Revenue Share
  ---------------- ---------------
  Top 1%                    31.79%
  Top 5%                    51.95%
  Top 10%                   63.90%
  Top 20%                   77.23%

This creates an important business question around **high-value customer
retention and revenue exposure**.

### Customer segments

The RFM analysis identified:

  Segment                 Customers   Revenue
  --------------------- ----------- ---------
  Champions                   1,295   £12.53M
  Loyal Customers             1,357    £3.07M
  Potential Loyalists         1,453    £1.24M
  At Risk                       967     £373K
  Lost                          806     £159K

Champions represent about **22% of identifiable customers but
approximately 72% of identifiable customer revenue**.

### Growth decomposition

One of the strongest analytical ideas in the project was separating
revenue growth into:

``` text
Revenue
 ├── Customer growth
 ├── Order growth
 └── Average Order Value
```

For example, November 2011 showed:

-   Revenue: **+11.6%**
-   Orders: **+37.7%**
-   Customers: **+22.0%**
-   AOV: **-18.9%**

So the growth signal was primarily **volume-driven**, rather than simply
saying "revenue increased."

### Product / return risk

Several products showed unusually high return behaviour.

One extreme example had a **100% return rate from only one order**.

That is treated as an **anomaly to investigate**, not as evidence that
the product normally has a 100% return rate.

This distinction is important in real business analytics.

------------------------------------------------------------------------

# ✦ Data Journey

## 1. Raw Data

The UCI Online Retail II workbook contains two yearly sheets:

-   `Year 2009-2010`
-   `Year 2010-2011`

Combined raw dataset:

-   **1,067,371 rows**
-   **8 original columns**
-   **53,628 unique invoices**
-   **5,305 unique products**
-   **5,942 unique customers**
-   **43 countries**

Original fields:

``` text
Invoice
StockCode
Description
Quantity
InvoiceDate
Price
Customer ID
Country
```

------------------------------------------------------------------------

## 2. Data Cleaning

The cleaning process was deliberately conservative.

We:

-   combined the two yearly sheets
-   standardized column names and text fields
-   removed exact duplicate records
-   preserved missing customer IDs
-   preserved negative quantities as business signals
-   identified cancellation-style transactions
-   identified zero-price records
-   identified negative-price accounting adjustments
-   protected normal revenue calculations from invalid records

### Important principle

**We did not blindly delete suspicious data.**

For example:

``` text
Negative Quantity
        ↓
Potential return/cancellation
        ↓
Keep + Flag
        ↓
Analyse separately
```

This makes the project more realistic than simply dropping every unusual
row.

------------------------------------------------------------------------

# ✦ Business Features Created

The analytical dataset adds business-friendly fields such as:

``` text
is_cancelled
is_negative_quantity
is_zero_price
is_invalid_price

revenue
sales_revenue
return_value

year
month
month_name
year_month
quarter

day_of_week
day_name
hour
is_weekend

is_return
is_sales

order_id

product_type
is_regular_product
```

These fields allow the dashboard to work with business concepts instead
of repeatedly rebuilding the same logic.

------------------------------------------------------------------------

# ✦ Customer Intelligence

Customer analysis uses an RFM framework:

### Recency

How recently did the customer purchase?

### Frequency

How often did the customer purchase?

### Monetary

How much revenue did the customer generate?

These dimensions are combined into project-defined RFM segments:

``` text
Champions
Loyal Customers
Potential Loyalists
At Risk
Lost
```

The thresholds are analytical rules created for this project and should
be validated before being used as an operational CRM policy.

------------------------------------------------------------------------

# ✦ Product Classification

The raw data contains more than normal merchandise.

Some records represent:

-   postage
-   manual/service transactions
-   operational items
-   accounting adjustments

If these are mixed with normal products, product rankings can become
misleading.

RetailIQ therefore separates:

``` text
Regular Product
Operational / Service
Adjustment
```

Product-performance views focus on **Regular Products**.

------------------------------------------------------------------------

# ✦ Revenue & Return Logic

The project separates normal sales from reversals and operational
records.

Conceptually:

``` text
Valid Sales
    ↓
Quantity > 0
Price > 0
Valid transaction
    ↓
Sales Revenue
```

Returns are handled separately:

``` text
Quantity < 0
    ↓
Return Transaction
    ↓
Return Value
    ↓
Revenue Risk / Leakage Analysis
```

Negative-price accounting adjustments are not treated as normal product
sales.

------------------------------------------------------------------------

# ✦ Business Recommendations

RetailIQ does not pretend that correlation proves causation.

Instead, the dashboard identifies areas that deserve business
investigation.

### 01 --- Protect high-value customers

A large percentage of identifiable revenue comes from Champions.

**Question to investigate:**\
Are high-value customers showing signs of reduced recency or frequency?

### 02 --- Investigate high-return products

Products with elevated return rates should be reviewed.

Possible investigation areas:

-   product quality
-   fulfilment
-   product descriptions
-   customer expectations
-   order-level anomalies

### 03 --- Understand basket compression

When orders grow faster than revenue, AOV can fall.

**Question to investigate:**\
Is the business acquiring more low-value orders, or has product mix
changed?

### 04 --- Validate international signals

Some markets show high AOV but relatively small customer bases.

These are **directional signals**, not automatic market-investment
decisions.

### 05 --- Investigate anomalies before acting

A 100% return rate from one order is very different from a 100% return
rate across hundreds of orders.

RetailIQ keeps anomaly investigation separate from normal product
benchmarking.

------------------------------------------------------------------------

# ✦ Technology

The project is intentionally Python-first.

### Core stack

-   **Python**
-   **Pandas**
-   **NumPy**
-   **Plotly**
-   **Streamlit**
-   **OpenPyXL**

### Interface

-   Streamlit
-   Custom CSS
-   Interactive Plotly visualisations
-   Responsive business dashboard
-   Dark green / emerald visual identity

### Important architecture decision

This version focuses on a **Python-first analytics workflow**.

SQL / SQLite / SQLAlchemy were intentionally kept outside this project
so the project remains focused on retail analytics and business
decision-making.

A future project can demonstrate the database/SQL layer separately.

------------------------------------------------------------------------

# ✦ Project Structure

``` text
retail_revenue_intelligence/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── cleaning.py
│   ├── profile.py
│   ├── investigate.py
│   ├── feature_engineering.py
│   ├── analysis.py
│   ├── business_analysis.py
│   └── decision_analysis.py
│
├── dashboard/
│   ├── app.py
│   └── style.css
│
├── docs/
│   └── Business_Project_Documentation.docx
│
├── requirements.txt
├── README.md
└── .gitignore
```

------------------------------------------------------------------------

# ✦ Run Locally

Clone the repository:

``` bash
git clone YOUR_REPOSITORY_URL
cd retail_revenue_intelligence
```

Create a virtual environment:

``` bash
python -m venv .venv
```

Activate it on Windows:

``` bash
.venv\Scripts\activate
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

Run the dashboard:

``` bash
streamlit run dashboard/app.py
```

------------------------------------------------------------------------

# ✦ Data Notes

The project uses the **UCI Online Retail II** dataset.

The analytical workflow produces:

``` text
Raw Excel
    ↓
Combined Transactions
    ↓
Cleaned Transactions
    ↓
Analytical Dataset
    ↓
RetailIQ Dashboard
```

The source data contains historical transaction records and should
therefore be interpreted as historical observational data.

------------------------------------------------------------------------

# ✦ Important Analytical Caveats

RetailIQ is a decision-support project, not a causal experimentation
platform.

Keep these points in mind:

-   Customer ID is missing for a portion of transactions.
-   December 2011 is a partial month ending on 9 December.
-   Small customer counts can make country-level AOV signals unstable.
-   RFM thresholds are project-defined.
-   Bulk/wholesale-like transactions can distort simple basket metrics.
-   Operational and adjustment records should not be treated as regular
    products.
-   Extremely high return rates with very small order counts require
    investigation.
-   Historical observational data cannot by itself prove that one
    business action caused another outcome.

------------------------------------------------------------------------

# ✦ What Makes This Project Different?

This project was built around a simple principle:

> **Don't stop at "What happened?" --- move toward "What does it mean
> for the business?"**

Instead of producing:

``` text
EDA
↓
Charts
↓
Done
```

RetailIQ follows:

``` text
Business Problem
      ↓
Data Quality
      ↓
Business Definitions
      ↓
Feature Engineering
      ↓
Analysis
      ↓
Risk Identification
      ↓
Decision Support
```

That makes the project useful as both a **portfolio project** and an
example of how a Data Analyst can approach a real business problem.

------------------------------------------------------------------------

# ✦ Skills Demonstrated

This project demonstrates experience with:

### Data Analysis

-   Data cleaning
-   Data profiling
-   Exploratory analysis
-   Feature engineering
-   Aggregation
-   Trend analysis
-   Customer analysis
-   Product analysis

### Business Analytics

-   Revenue analysis
-   AOV analysis
-   Customer concentration
-   RFM segmentation
-   New vs returning customers
-   Return analysis
-   Revenue leakage
-   Anomaly investigation
-   Decision-oriented recommendations

### Data Visualisation

-   Interactive dashboards
-   KPI design
-   Trend charts
-   Segment analysis
-   Pareto analysis
-   Risk visualisation
-   Business storytelling

### Product Thinking

-   User-focused dashboard design
-   Clear information hierarchy
-   Decision Center
-   Business-first metrics
-   Data-quality caveats

------------------------------------------------------------------------

# ✦ Future Improvements

Possible next versions could include:

-   cohort retention analysis
-   customer lifetime value modelling
-   more advanced product-mix analysis
-   automated data-quality monitoring
-   forecasting
-   experiment/A-B testing when suitable experimental data becomes
    available
-   SQL/database-backed architecture
-   automated refresh pipelines

These are intentionally future enhancements rather than artificially
added features.

------------------------------------------------------------------------

# ✦ Project Documentation

For the complete business explanation of the project, see:

**`docs/Business_Project_Documentation.docx`**

That document explains the project from raw data to final business
decisions in a simple, non-technical format.

------------------------------------------------------------------------

# ✦ Author

**SXS Analytics Lab**

Built as a portfolio project demonstrating practical **Data Analytics +
Business Intelligence + Dashboard Design**.

------------------------------------------------------------------------

## Final Thought

RetailIQ is designed around one idea:

> **Good analytics does not end with a chart. It helps someone make a
> better business decision.**
