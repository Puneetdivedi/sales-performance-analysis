import os
import sys

# Add project root to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.data_loader import load_data
from src.kpi_calculator import calculate_kpis, calculate_growth_rate


def monthly_analysis():
    """
    Perform monthly sales trend analysis grouped by region.

    Generates a CSV with monthly aggregates including:
        - Total revenue and orders per region per month
        - Average conversion rate and average order value
        - Month-over-month revenue growth percentage
    """
    data_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "raw", "sales_data.csv"
    )
    df = load_data(data_path)
    df = calculate_kpis(df)

    # Extract month period
    df["month"] = df["date"].dt.to_period("M").astype(str)

    # Aggregate by month and region
    monthly = (
        df.groupby(["month", "region"])
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

    # Round aggregated values
    monthly["revenue"] = monthly["revenue"].round(2)
    monthly["conversion_rate"] = monthly["conversion_rate"].round(4)
    monthly["average_order_value"] = monthly["average_order_value"].round(2)
    monthly["revenue_per_visitor"] = monthly["revenue_per_visitor"].round(2)

    # Calculate month-over-month revenue growth
    monthly["revenue_growth_pct"] = (
        monthly.groupby("region")["revenue"].pct_change() * 100
    ).round(2)

    # Save output
    output_dir = os.path.join(
        os.path.dirname(__file__), "..", "data", "processed"
    )
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "monthly_sales_trends.csv")
    monthly.to_csv(output_path, index=False)

    print(f"Monthly sales trends generated -> {output_path}")
    print(f"  Rows: {len(monthly)}")
    print(f"  Date range: {monthly['month'].min()} to {monthly['month'].max()}")
    print(f"  Regions: {monthly['region'].nunique()}")

    return monthly


def quarterly_analysis() -> pd.DataFrame:
    """
    Perform quarterly sales trend analysis.

    Returns
    -------
    pd.DataFrame
        Quarterly aggregated sales data with growth rates.
    """
    data_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "raw", "sales_data.csv"
    )
    df = load_data(data_path)
    df = calculate_kpis(df)

    df["quarter"] = df["date"].dt.to_period("Q").astype(str)

    quarterly = (
        df.groupby(["quarter", "region"])
        .agg(
            revenue=("revenue", "sum"),
            orders=("orders", "sum"),
            visitors=("visitors", "sum"),
            estimated_profit=("estimated_profit", "sum"),
        )
        .reset_index()
    )

    quarterly["revenue"] = quarterly["revenue"].round(2)
    quarterly["estimated_profit"] = quarterly["estimated_profit"].round(2)
    quarterly["revenue_growth_pct"] = calculate_growth_rate(
        quarterly.groupby("region")["revenue"].transform(lambda x: x)
    )

    output_dir = os.path.join(
        os.path.dirname(__file__), "..", "data", "processed"
    )
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "quarterly_sales_trends.csv")
    quarterly.to_csv(output_path, index=False)

    print(f"Quarterly sales trends generated -> {output_path}")
    return quarterly


def get_best_worst_months(df: pd.DataFrame = None) -> dict:
    """
    Identify the best and worst performing months by revenue.

    Returns
    -------
    dict
        Dictionary with 'best_month' and 'worst_month' info.
    """
    if df is None:
        data_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "raw", "sales_data.csv"
        )
        df = load_data(data_path)

    df["month"] = df["date"].dt.to_period("M").astype(str)
    monthly_rev = df.groupby("month")["revenue"].sum()

    return {
        "best_month": monthly_rev.idxmax(),
        "best_revenue": round(monthly_rev.max(), 2),
        "worst_month": monthly_rev.idxmin(),
        "worst_revenue": round(monthly_rev.min(), 2),
    }


if __name__ == "__main__":
    monthly_analysis()
