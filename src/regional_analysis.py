"""
Regional sales analysis module.
Provides functions to analyze sales performance by region.
"""

import os
import sys
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.data_loader import load_data
from src.kpi_calculator import calculate_kpis


def regional_analysis() -> pd.DataFrame:
    """
    Perform regional sales analysis.

    Computes aggregated metrics per region:
        - Total revenue, orders, visitors, customers
        - Average conversion rate, average order value
        - Revenue per visitor
        - Market share percentage

    Returns
    -------
    pd.DataFrame
        Regional summary DataFrame.
    """
    data_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "raw", "sales_data.csv"
    )
    df = load_data(data_path)
    df = calculate_kpis(df)

    regional = (
        df.groupby("region")
        .agg(
            revenue=("revenue", "sum"),
            orders=("orders", "sum"),
            visitors=("visitors", "sum"),
            customers=("customers", "sum"),
            conversion_rate=("conversion_rate", "mean"),
            average_order_value=("average_order_value", "mean"),
            revenue_per_visitor=("revenue_per_visitor", "mean"),
        )
        .reset_index()
    )

    # Round values
    regional["revenue"] = regional["revenue"].round(2)
    regional["conversion_rate"] = regional["conversion_rate"].round(4)
    regional["average_order_value"] = regional["average_order_value"].round(2)
    regional["revenue_per_visitor"] = regional["revenue_per_visitor"].round(2)

    # Market share
    total_revenue = regional["revenue"].sum()
    regional["market_share_pct"] = (
        (regional["revenue"] / total_revenue) * 100
    ).round(2)

    # Save output
    output_dir = os.path.join(
        os.path.dirname(__file__), "..", "data", "processed"
    )
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "regional_performance.csv")
    regional.to_csv(output_path, index=False)

    print(f"Regional performance generated -> {output_path}")
    return regional


def compare_regions(df: pd.DataFrame = None) -> pd.DataFrame:
    """
    Compare all regions side by side with key metrics.

    Returns
    -------
    pd.DataFrame
        Comparison DataFrame with rank by revenue.
    """
    if df is None:
        data_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "raw", "sales_data.csv"
        )
        df = load_data(data_path)
        df = calculate_kpis(df)

    comparison = (
        df.groupby("region")
        .agg(
            revenue=("revenue", "sum"),
            orders=("orders", "sum"),
            avg_conversion=("conversion_rate", "mean"),
            avg_aov=("average_order_value", "mean"),
            total_profit=("estimated_profit", "sum"),
        )
        .reset_index()
    )
    comparison["revenue"] = comparison["revenue"].round(2)
    comparison["total_profit"] = comparison["total_profit"].round(2)
    comparison["avg_conversion"] = (comparison["avg_conversion"] * 100).round(2)
    comparison["avg_aov"] = comparison["avg_aov"].round(2)
    comparison["rank"] = comparison["revenue"].rank(ascending=False).astype(int)

    return comparison.sort_values("rank")


if __name__ == "__main__":
    result = regional_analysis()
    print(result.to_string(index=False))
