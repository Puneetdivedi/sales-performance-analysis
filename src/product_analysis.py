"""
Product performance analysis module.
Provides functions to analyze sales performance by product.
"""

import os
import sys
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.data_loader import load_data
from src.kpi_calculator import calculate_kpis


def product_analysis() -> pd.DataFrame:
    """
    Perform product-level sales analysis.

    Computes aggregated metrics per product:
        - Total revenue and orders
        - Average order value
        - Revenue share percentage
        - Ranking by revenue

    Returns
    -------
    pd.DataFrame
        Product summary DataFrame sorted by revenue descending.
    """
    data_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "raw", "sales_data.csv"
    )
    df = load_data(data_path)
    df = calculate_kpis(df)

    product = (
        df.groupby(["product_id", "product_name"])
        .agg(
            revenue=("revenue", "sum"),
            orders=("orders", "sum"),
            avg_order_value=("average_order_value", "mean"),
            total_transactions=("order_id", "count"),
        )
        .reset_index()
    )

    # Round values
    product["revenue"] = product["revenue"].round(2)
    product["avg_order_value"] = product["avg_order_value"].round(2)

    # Revenue share
    total_revenue = product["revenue"].sum()
    product["revenue_share_pct"] = (
        (product["revenue"] / total_revenue) * 100
    ).round(2)

    # Rank by revenue
    product = product.sort_values("revenue", ascending=False).reset_index(drop=True)
    product["rank"] = product.index + 1

    # Save output
    output_dir = os.path.join(
        os.path.dirname(__file__), "..", "data", "processed"
    )
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "product_performance.csv")
    product.to_csv(output_path, index=False)

    print(f"Product performance generated -> {output_path}")
    return product


if __name__ == "__main__":
    result = product_analysis()
    print(result.to_string(index=False))
