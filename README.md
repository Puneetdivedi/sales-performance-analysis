# Sales Performance Analysis

A data analysis project for tracking and visualizing sales performance across regions and products.

## Project Structure

```
sales-performance-analysis/
├── dashboard/
│   └── app.py                  # Streamlit interactive dashboard
├── data/
│   ├── raw/
│   │   └── sales_data.csv      # Raw sales data
│   └── processed/              # Generated analysis outputs
├── scripts/
│   └── generate_data.py        # Sample data generator
├── src/
│   ├── __init__.py
│   ├── data_loader.py          # Data loading & cleaning
│   ├── kpi_calculator.py       # KPI calculations
│   ├── time_analysis.py        # Monthly trend analysis
│   ├── regional_analysis.py    # Regional performance analysis
│   └── product_analysis.py     # Product performance analysis
├── notebooks/                  # Jupyter notebooks (exploration)
├── insights.md                 # Key findings
├── requirements.txt            # Python dependencies
└── README.md
```

## Setup

```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage

### Run the Dashboard
```bash
streamlit run dashboard/app.py
```

### Run Analysis Scripts
```bash
# Monthly trend analysis
python src/time_analysis.py

# Regional performance analysis
python src/regional_analysis.py

# Product performance analysis
python src/product_analysis.py
```

### Generate Sample Data
```bash
python scripts/generate_data.py
```

## Data Columns

| Column         | Description                          |
|----------------|--------------------------------------|
| `date`         | Transaction date                     |
| `order_id`     | Unique order identifier              |
| `product_id`   | Product code                         |
| `product_name` | Product display name                 |
| `region`       | Sales region (North/South/East/West) |
| `visitors`     | Number of site visitors              |
| `customers`    | Number of paying customers           |
| `orders`       | Number of orders placed              |
| `revenue`      | Total revenue in USD                 |

## KPIs Calculated

- **Conversion Rate** — Orders / Visitors
- **Average Order Value** — Revenue / Orders
- **Revenue per Visitor** — Revenue / Visitors
- **Customer Acquisition Cost Proxy** — Visitors / Customers
- **Revenue Growth %** — Month-over-month revenue change

## Tech Stack

- **Python** — Core data processing
- **Pandas** — Data manipulation
- **Streamlit** — Interactive dashboard
- **Plotly** — Interactive charts
- **Matplotlib / Seaborn** — Static visualizations
