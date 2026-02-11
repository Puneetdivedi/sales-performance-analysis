"""
Main analysis runner — generates a quick regional summary.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.data_loader import load_data
from src.kpi_calculator import calculate_kpis


def main():
    data_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "raw", "sales_data.csv"
    )
    df = load_data(data_path)
    df = calculate_kpis(df)

    region_summary = (
        df.groupby("region")
        .agg(
            total_revenue=("revenue", "sum"),
            total_orders=("orders", "sum"),
            avg_conversion_rate=("conversion_rate", "mean"),
            avg_aov=("average_order_value", "mean"),
        )
        .reset_index()
    )

    print("\nRegional Sales Performance:\n")
    print(region_summary)

    output_dir = os.path.join(
        os.path.dirname(__file__), "..", "data", "processed"
    )
    os.makedirs(output_dir, exist_ok=True)
    region_summary.to_csv(
        os.path.join(output_dir, "region_performance_summary.csv"), index=False
    )


if __name__ == "__main__":
    main()
