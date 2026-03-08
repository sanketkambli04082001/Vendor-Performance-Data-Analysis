# 🏪 Vendor Performance Data Analysis

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?logo=sqlite)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green?logo=pandas)
![PowerBI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow?logo=powerbi)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

An end-to-end data analytics project analyzing vendor performance for a liquor store chain. The project covers the full analytics pipeline — from raw CSV ingestion into a SQLite database, SQL-based transformation, exploratory data analysis with statistical testing, all the way to an interactive Power BI business dashboard.

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Dataset](#-dataset)
- [Screenshots](#-screenshots)
- [Project Structure](#-project-structure)
- [Pipeline Architecture](#-pipeline-architecture)
- [Tech Stack](#-tech-stack)
- [Data Ingestion](#-data-ingestion)
- [Vendor Summary Creation](#-vendor-summary-creation)
- [Exploratory Data Analysis](#-exploratory-data-analysis)
- [Statistical Analysis](#-statistical-analysis)
- [Power BI Dashboard](#-power-bi-dashboard)
- [Key Business Insights](#-key-business-insights)
- [How to Run](#-how-to-run)
- [Output Files](#-output-files)
- [Author](#-author)

---

## 📌 Project Overview

This project analyzes vendor-level performance across **purchase behavior, sales contribution, profit margins, and stock turnover** for a liquor store inventory dataset. The goal is to identify top-performing and low-performing vendors and brands to support data-driven procurement and pricing decisions.

**Core Questions Answered:**
- Which vendors contribute the most to total purchases?
- Which brands generate the highest sales revenue?
- What is the profit margin distribution across vendors?
- Are there statistically significant differences in profit margins between top and low-performing vendors?
- Which vendors have low stock turnover indicating slow-moving inventory?

---

## 📦 Dataset

The dataset represents real-world inventory, purchase, and sales data for a liquor store chain.

📥 **Download the raw dataset here:**
👉 [Vendor Performance Raw Dataset (Google Drive)](https://drive.google.com/file/d/1wFeWgNlsyqhLpKhBUosyEkBu7wFuEo_4/view?usp=sharing)

After downloading, extract and place all CSV files inside the `data/` folder in the project directory.

**The dataset contains 6 CSV files:**

| File | Description |
|------|-------------|
| `begin_inventory.csv` | Opening stock levels per store and product |
| `end_inventory.csv` | Closing stock levels per store and product |
| `purchases.csv` | Purchase transactions by vendor and brand |
| `purchase_prices.csv` | Reference prices per brand and volume |
| `sales.csv` | Sales transactions by brand and store |
| `vendor_invoice.csv` | Freight and invoice data per vendor |

> ⚠️ Raw data files are not included in this repository due to size. Please download from the link above.

---

## 📸 Screenshots

### Power BI Dashboard
<img width="1316" height="738" alt="image" src="https://github.com/user-attachments/assets/da68d0fd-cffa-4488-8571-8ef76c3b12a9" />


### Purchase Contribution % (EDA)
<!-- PASTE Donut_Chart.png here using Ctrl+V in GitHub editor -->
<img width="982" height="654" alt="image" src="https://github.com/user-attachments/assets/d0be0bcc-585f-4a2e-8ca9-60fb6ac4db14" />

---

## 🗂️ Project Structure

```
Vendor-Performance-Data-Analysis/
│
├── data/                               # ← Place downloaded CSV files here
│
├── logs/
│   ├── injestion.log                   # Ingestion pipeline execution log
│   └── get_vendor_summary.log          # Vendor summary pipeline log
│
├── injestion_db.py                     # Loads raw CSVs into SQLite database
├── get_vendor_summary.py               # Transforms and cleans vendor data via SQL + Pandas
│
├── Expolatory_Data_Analysis.ipynb      # Full EDA notebook with visualizations
├── vendor_performance_analysis.ipynb   # Statistical analysis notebook
│
├── Vendor_Performance_Analytics.pbix   # Power BI dashboard
│
├── requirement.txt                     # Python dependencies
├── .gitignore                          # Files excluded from version control
└── README.md                           # Project documentation
```

---

## 🔄 Pipeline Architecture

```
📂 Raw CSV Files (6 files)
         │
         ▼
 injestion_db.py
 (Loads CSVs → SQLite via SQLAlchemy)
         │
         ▼
 inventory.db (SQLite Database)
 Tables: begin_inventory, end_inventory,
         purchases, purchase_prices,
         sales, vendor_invoice
         │
         ▼
 get_vendor_summary.py
 (3 SQL CTEs + LEFT JOINs + Pandas Cleaning + Feature Engineering)
         │
         ▼
 vendor_sales_summary (10,514 rows × 18 columns)
         │
         ├──▶ Jupyter Notebooks (EDA + Statistical Analysis)
         │
         └──▶ Power BI Dashboard (Interactive Visuals)
```

---

## 🛠️ Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.x | Core programming language |
| Pandas | 3.0.1 | Data manipulation and cleaning |
| SQLite3 | Built-in | Local database storage |
| SQLAlchemy | 2.0.47 | Database ORM for data ingestion |
| SciPy | 1.17.1 | Statistical analysis (T-Test, Confidence Intervals) |
| Matplotlib | 3.10.8 | Data visualization |
| Seaborn | 0.13.2 | Advanced statistical visualizations |
| Jupyter Notebook | Latest | Interactive analysis environment |
| Power BI Desktop | Latest | Interactive business dashboard |
| Git | Latest | Version control |

---

## 📥 Data Ingestion — `injestion_db.py`

Loads all 6 raw CSV files from the `data/` folder into a local SQLite database (`inventory.db`) using SQLAlchemy.

**What it does:**
- Iterates over all `.csv` files in the `data/` folder
- Loads each file into a corresponding SQLite table using `df.to_sql()`
- Logs each step with timestamps

**Execution log summary:**
```
injesting begin_inventory.csv   ✅
injesting end_inventory.csv     ✅
injesting purchases.csv         ✅
injesting purchase_prices.csv   ✅
injesting sales.csv             ✅
injesting vendor_invoice.csv    ✅
-----------Injestion Complete-----------
Time taken for injestion: 4.55 mins
```

---

## 🔧 Vendor Summary Creation — `get_vendor_summary.py`

Builds the core analytical table `vendor_sales_summary` using **3 SQL CTEs with LEFT JOINs** and then cleans and engineers features using Pandas.

### SQL Query Structure

```sql
WITH
  FreightSummary AS (
    SELECT VendorNumber, SUM(Freight) AS FreightCost
    FROM vendor_invoice
    GROUP BY VendorNumber
  ),
  PurchaseSummary AS (
    SELECT p.VendorNumber, p.VendorName, p.Brand, p.Description,
           p.PurchasePrice, pp.Volume, pp.Price AS ActualPrice,
           SUM(p.Quantity) AS TotalPurchaseQuantity,
           SUM(p.Dollars)  AS TotalPurchaseDollars
    FROM purchases p
    JOIN purchase_prices pp ON p.Brand = pp.Brand
    WHERE p.PurchasePrice > 0
    GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description,
             p.PurchasePrice, pp.Price, pp.Volume
  ),
  SalesSummary AS (
    SELECT VendorNo, Brand,
           SUM(SalesDollars)   AS TotalSalesDollar,
           SUM(SalesPrice)     AS TotalSalesPrice,
           SUM(SalesQuantity)  AS TotalSalesQuantity,
           SUM(ExciseTax)      AS TotalExciseTax
    FROM sales
    GROUP BY VendorNo, Brand
  )
SELECT ps.*, ss.*, fs.*
FROM   PurchaseSummary ps
  LEFT JOIN SalesSummary   ss ON ps.VendorNumber = ss.VendorNo AND ps.Brand = ss.Brand
  LEFT JOIN FreightSummary fs ON ps.VendorNumber = fs.VendorNumber
ORDER BY TotalPurchaseDollars DESC
```

### Pandas Cleaning Steps

```python
df['Volume']      = df['Volume'].astype('float64')   # Fix dtype
df                = df.fillna(0)                      # Fill NULLs with 0
df['VendorName']  = df['VendorName'].str.strip()      # Remove whitespace
df['Description'] = df['Description'].str.strip()
```

### Engineered Features

| Feature | Formula | Business Meaning |
|---------|---------|-----------------|
| `GrossProfit` | `TotalSalesDollar - TotalPurchaseDollars` | Raw profit per vendor-brand |
| `ProfitMargin` | `(GrossProfit / TotalSalesDollar) × 100` | % profit on every dollar sold |
| `StockTurnover` | `TotalSalesQuantity / TotalPurchaseQuantity` | How efficiently inventory converts to sales |
| `SalesToPurchaseRatio` | `TotalSalesDollar / TotalPurchaseDollars` | Revenue generated per dollar purchased |

**Final output:** `vendor_sales_summary` — **10,514 rows × 18 columns, 0 nulls**

---

## 📊 Exploratory Data Analysis

### Summary Statistics Insights

**Negative & Zero Values:**
- Some vendors have `GrossProfit = 0` and `ProfitMargin = 0` due to no recorded sales
- Vendors with no matching sales records after LEFT JOIN are filled with 0 — these represent purchased but unsold inventory

**Outliers Detected:**
- Extreme high values in `TotalSalesDollar` and `TotalPurchaseDollars` for top vendors (DIAGEO, MARTIGNETTI)
- `PurchasePrice` outliers exist for premium spirits with very high unit costs

### Visualizations Produced

| Chart | Purpose |
|-------|---------|
| Histograms | Distribution of ProfitMargin and Volume |
| Boxplots | Outlier detection across all numeric columns |
| Correlation Heatmap | Relationship strength between all numeric features |
| Pareto Chart | Top vendors driving 80% of total purchases |
| Bar Charts | Top 10 vendors and brands by total sales |
| Scatter Plot | Sales vs Profit Margin by vendor tier |
| Bulk Pricing Chart | Unit price vs purchase quantity quartiles |

### Correlation Insights

- **Strong positive** correlation between `TotalPurchaseDollars` and `TotalSalesDollar` (r ≈ 0.97)
- **Moderate** correlation between `FreightCost` and `TotalPurchaseDollars`
- **Weak** correlation between `ProfitMargin` and `Volume` — bulk purchases do not guarantee higher margins
- `StockTurnover` and `SalesToPurchaseRatio` are highly correlated with each other

### Bulk Purchasing Analysis

Used `pd.qcut()` to segment vendors into **4 purchase quantity quartiles:**
- Q1 (lowest) vendors pay significantly higher unit prices
- Q4 (highest) vendors receive notably lower unit prices — confirming bulk discount behavior
- Mid-tier vendors (Q2/Q3) show inconsistent pricing suggesting negotiation-based pricing models

---

## 📐 Statistical Analysis

### Confidence Intervals

Computed **95% Confidence Intervals** for `ProfitMargin` across vendor performance tiers:

| Vendor Tier | Mean Profit Margin | Confidence Interval |
|-------------|-------------------|-------------------|
| Top Vendors | 31.18% | 30.74% – 31.61% (Narrow) |
| Low Vendors | 41.57% | 40.50% – 42.64% (Wide) |

### Hypothesis Testing — Welch's Two-Sample T-Test

```
H₀ (Null):        No significant difference in profit margins between
                  top and low-performing vendors

H₁ (Alternative): There IS a significant difference in profit margins
                  between top and low-performing vendors

Segmentation:
  Top vendors  = vendors with TotalSalesDollars ≥ 75th percentile
  Low vendors  = vendors with TotalSalesDollars ≤ 25th percentile

Method: scipy.stats.ttest_ind(top_vendors, low_vendors, equal_var=False)
Significance level: α = 0.05
```

**Result: p-value < 0.05 → Reject H₀**

✅ Top-performing vendors (by sales volume) generate **statistically significantly higher profit margins** than low-performing vendors.

---

## 📈 Power BI Dashboard

### Dashboard Visuals

| Visual | Type | Insight |
|--------|------|---------|
| Total Sales | KPI Card | $441.41M |
| Total Purchase | KPI Card | $307.34M |
| Gross Profit | KPI Card | $134.07M |
| Profit Margin | KPI Card | 38.72% |
| Unsold Capital | KPI Card | $2.71M |
| Purchase Contribution % | Donut Chart | Top 10 vendors = 65.7% of all purchases |
| Top Vendors by Sales | Horizontal Bar | DIAGEO NORTH AMERICA leads at $68M |
| Top Brands by Sales | Horizontal Bar | Jack Daniels No 7 leads at $8M |
| Low Performing Vendors | Bar Chart | Stock Turnover ratio below 0.77 |
| Low Performing Brands | Scatter Plot | Avg Profit Margin vs Total Sales by TargetBrand |

### DAX Tables & Measures

**1. BrandPerformance Table**
```dax
BrandPerformance =
    SUMMARIZE(
        vendor_sales_summary,
        vendor_sales_summary[Description],
        "TotalSales", SUM(vendor_sales_summary[TotalSalesDollar]),
        "AvgProfitMargin", AVERAGE(vendor_sales_summary[ProfitMargin])
    )
```

**2. TargetBrand Column**
```dax
TargetBrand =
    IF(
        [TotalSales] <= PERCENTILEX.INC(BrandPerformance, BrandPerformance[TotalSales], 0.15)
        && [AvgProfitMargin] >= PERCENTILEX.INC(BrandPerformance, BrandPerformance[AvgProfitMargin], 0.85),
        "Yes", "No"
    )
```

**3. LowTurnoverVendor Table**
```dax
LowTurnoverVendor =
    VAR FilteredData =
        FILTER(vendor_sales_summary, vendor_sales_summary[StockTurnover] < 1)
    RETURN
        SUMMARIZE(
            FilteredData,
            vendor_sales_summary[VendorName],
            "AvgStockTurnOver", AVERAGE(vendor_sales_summary[StockTurnover])
        )
```

**4. PurchaseContribution Table**
```dax
PurchaseContribution =
    SUMMARIZE(
        vendor_sales_summary,
        vendor_sales_summary[VendorName],
        "TotalPurchaseDollars", SUM(vendor_sales_summary[TotalPurchaseDollars])
    )
```

**5. PurchaseContribution% Column**
```dax
PurchaseContribution% =
    PurchaseContribution[TotalPurchaseDollars] /
    SUM(PurchaseContribution[TotalPurchaseDollars]) * 100
```

---

## 💡 Key Business Insights

1. 🏆 **DIAGEO NORTH AMERICA INC** is the dominant vendor — **16.3% of total purchases** and **$68M in sales**
2. 📊 **Top 10 vendors** control **65.7%** of all purchase spending — indicating heavy vendor concentration
3. 🥃 **Jack Daniels No 7 Black** is the top-selling brand at **$8.0M in total sales**
4. ⚠️ **Low-performing vendors** have a Stock Turnover ratio **below 0.77** — inventory is not converting to sales efficiently
5. 📦 **Bulk purchasing vendors** receive significantly lower unit prices — reinforcing the value of volume-based procurement
6. 📐 **Statistical testing confirms** top vendors generate significantly higher profit margins (p < 0.05)
7. 🎯 **TargetBrand flag** identifies brands with low sales but high margins — potential pricing or marketing opportunities worth exploring

---

## ⚙️ How to Run

**1. Clone the repository:**
```bash
git clone https://github.com/sanketkambli04082001/Vendor-Performance-Data-Analysis.git
cd Vendor-Performance-Data-Analysis
```

**2. Install dependencies:**
```bash
pip install -r requirement.txt
```

**3. Download the raw dataset:**

👉 [Download Raw Dataset (Google Drive)](https://drive.google.com/file/d/1wFeWgNlsyqhLpKhBUosyEkBu7wFuEo_4/view?usp=sharing)

Create a `data/` folder in the project directory and place all 6 CSV files inside it.

**4. Run the ingestion pipeline:**
```bash
python injestion_db.py
```

**5. Run the vendor summary pipeline:**
```bash
python get_vendor_summary.py
```

**6. Open Jupyter Notebook for EDA:**
```bash
jupyter notebook
```
Open `Expolatory_Data_Analysis.ipynb` and run all cells.

**7. View the Power BI Dashboard:**

Open `Vendor_Performance_Analytics.pbix` in Power BI Desktop.

---

## 📁 Output Files

> Output files are not stored in this repository. Download them directly from the links below.

| File | Description | Download |
|------|-------------|----------|
| `vendor_sales_summary.csv` | Final cleaned and feature-engineered dataset (10,514 rows × 18 columns) | [Download from Google Drive](https://drive.google.com/file/d/1RmloWNAbMKjL73sa14V0nMIwJRgwx-Ck/view?usp=sharing) |
| `Vendor_Performance_Analytics.pbix` | Interactive Power BI dashboard | Available in repository |
| `logs/injestion.log` | Timestamped ingestion pipeline execution log | Available in repository |
| `logs/get_vendor_summary.log` | Timestamped vendor summary pipeline execution log | Available in repository |

---

## 👨‍💻 Author

**Sanket Kambli**
Data Analyst | Python • SQL • Power BI • Data Visualization

🔗 [GitHub](https://github.com/sanketkambli04082001) | [LinkedIn](https://linkedin.com/in/sanket-kambli-6bb012223)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

⭐ If you found this project useful, please consider giving it a star!
