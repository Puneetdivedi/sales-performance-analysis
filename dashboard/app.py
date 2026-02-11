"""
Sales Performance Analysis Dashboard
Built with Streamlit for interactive data exploration.
"""

import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.data_loader import load_data
from src.kpi_calculator import calculate_kpis, summarize_kpis

# ── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .main { padding: 1rem 2rem; }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .metric-card h3 { margin: 0; font-size: 0.85rem; opacity: 0.9; }
    .metric-card h1 { margin: 0.3rem 0 0 0; font-size: 1.8rem; }
    .st-emotion-cache-1y4p8pa { padding-top: 2rem; }
    div[data-testid="stMetric"] {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Data Loading ────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    """Load and process sales data."""
    data_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "raw", "sales_data.csv"
    )
    df = load_data(data_path)
    df = calculate_kpis(df)
    return df


df = get_data()

# ── Sidebar Filters ─────────────────────────────────────────────────────────
st.sidebar.title("🔍 Filters")

# Date range filter
min_date = df["date"].min().date()
max_date = df["date"].max().date()
date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

# Region filter
regions = ["All"] + sorted(df["region"].unique().tolist())
selected_region = st.sidebar.selectbox("Region", regions)

# Product filter
products = ["All"] + sorted(df["product_name"].unique().tolist())
selected_product = st.sidebar.selectbox("Product", products)

# Apply filters
filtered = df.copy()
if len(date_range) == 2:
    filtered = filtered[
        (filtered["date"].dt.date >= date_range[0])
        & (filtered["date"].dt.date <= date_range[1])
    ]
if selected_region != "All":
    filtered = filtered[filtered["region"] == selected_region]
if selected_product != "All":
    filtered = filtered[filtered["product_name"] == selected_product]

# ── Header ──────────────────────────────────────────────────────────────────
st.title("📊 Sales Performance Dashboard")
st.markdown("Interactive analysis of sales data across regions and products.")
st.markdown("---")

# ── KPI Cards ───────────────────────────────────────────────────────────────
summary = summarize_kpis(filtered)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("💰 Total Revenue", f"${summary['total_revenue']:,.2f}")
with col2:
    st.metric("📦 Total Orders", f"{summary['total_orders']:,}")
with col3:
    st.metric("📈 Avg Conversion", f"{summary['avg_conversion_rate']:.2f}%")
with col4:
    st.metric("🛒 Avg Order Value", f"${summary['avg_order_value']:,.2f}")

st.markdown("---")

# ── Revenue Over Time ──────────────────────────────────────────────────────
st.subheader("📈 Revenue Trends")

monthly = filtered.copy()
monthly["month"] = monthly["date"].dt.to_period("M").astype(str)
monthly_agg = (
    monthly.groupby(["month", "region"])
    .agg(revenue=("revenue", "sum"), orders=("orders", "sum"))
    .reset_index()
)

fig_revenue = px.line(
    monthly_agg,
    x="month",
    y="revenue",
    color="region",
    title="Monthly Revenue by Region",
    labels={"month": "Month", "revenue": "Revenue ($)", "region": "Region"},
    markers=True,
)
fig_revenue.update_layout(
    hovermode="x unified",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(size=12),
)
st.plotly_chart(fig_revenue, use_container_width=True)

# ── Two-column layout: Regional & Product analysis ────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🌎 Regional Performance")
    regional = (
        filtered.groupby("region")
        .agg(
            revenue=("revenue", "sum"),
            orders=("orders", "sum"),
            avg_conversion=("conversion_rate", "mean"),
        )
        .reset_index()
    )
    regional["avg_conversion"] = (regional["avg_conversion"] * 100).round(2)

    fig_region = px.bar(
        regional,
        x="region",
        y="revenue",
        color="region",
        title="Revenue by Region",
        labels={"revenue": "Revenue ($)", "region": "Region"},
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig_region.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_region, use_container_width=True)

with col_right:
    st.subheader("📦 Top Products by Revenue")
    product_rev = (
        filtered.groupby("product_name")
        .agg(revenue=("revenue", "sum"), orders=("orders", "sum"))
        .reset_index()
        .sort_values("revenue", ascending=True)
        .tail(10)
    )

    fig_product = px.bar(
        product_rev,
        x="revenue",
        y="product_name",
        orientation="h",
        title="Top 10 Products",
        labels={"revenue": "Revenue ($)", "product_name": "Product"},
        color="revenue",
        color_continuous_scale="Viridis",
    )
    fig_product.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_product, use_container_width=True)

# ── Conversion Rate & Order Value Scatter ──────────────────────────────────
st.subheader("🔄 Conversion Rate vs Average Order Value")

scatter_data = (
    filtered.groupby(["region", "product_name"])
    .agg(
        conversion_rate=("conversion_rate", "mean"),
        avg_order_value=("average_order_value", "mean"),
        total_orders=("orders", "sum"),
    )
    .reset_index()
)

fig_scatter = px.scatter(
    scatter_data,
    x="conversion_rate",
    y="avg_order_value",
    size="total_orders",
    color="region",
    hover_name="product_name",
    title="Conversion Rate vs AOV (bubble size = order volume)",
    labels={
        "conversion_rate": "Conversion Rate",
        "avg_order_value": "Avg Order Value ($)",
    },
)
fig_scatter.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig_scatter, use_container_width=True)

# ── Monthly Orders Heatmap ──────────────────────────────────────────────────
st.subheader("🗓️ Orders Heatmap")

heatmap_data = filtered.copy()
heatmap_data["month_num"] = heatmap_data["date"].dt.month
heatmap_data["year"] = heatmap_data["date"].dt.year

heat_agg = (
    heatmap_data.groupby(["year", "month_num"])
    .agg(orders=("orders", "sum"))
    .reset_index()
)
heat_pivot = heat_agg.pivot(index="year", columns="month_num", values="orders").fillna(0)

month_names = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]
heat_pivot.columns = [month_names[m - 1] for m in heat_pivot.columns]

fig_heat = px.imshow(
    heat_pivot,
    labels=dict(x="Month", y="Year", color="Orders"),
    title="Order Volume by Month and Year",
    color_continuous_scale="YlOrRd",
    aspect="auto",
)
fig_heat.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig_heat, use_container_width=True)

# ── Data Table ──────────────────────────────────────────────────────────────
st.subheader("📋 Raw Data")
with st.expander("View filtered data table"):
    display_cols = [
        "date", "order_id", "product_name", "region",
        "visitors", "customers", "orders", "revenue",
        "conversion_rate", "average_order_value",
    ]
    st.dataframe(
        filtered[display_cols].sort_values("date", ascending=False),
        use_container_width=True,
        height=400,
    )

# ── Footer ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#888; font-size:0.85rem;'>"
    "Sales Performance Analysis Dashboard • Built with Streamlit & Plotly"
    "</div>",
    unsafe_allow_html=True,
)
