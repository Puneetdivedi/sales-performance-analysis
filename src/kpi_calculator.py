import pandas as pd


def calculate_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate core sales KPIs from raw sales data.

    Adds the following columns:
        - conversion_rate: orders / visitors
        - average_order_value: revenue / orders
        - customer_acquisition_cost_proxy: visitors / customers
        - revenue_per_visitor: revenue / visitors

    Parameters
    ----------
    df : pd.DataFrame
        Raw sales DataFrame with columns: visitors, orders, revenue, customers.

    Returns
    -------
    pd.DataFrame
        DataFrame with additional KPI columns.
    """
    df = df.copy()

    # Core KPIs
    df["conversion_rate"] = (df["orders"] / df["visitors"]).round(4)
    df["average_order_value"] = (df["revenue"] / df["orders"]).round(2)

    # Extra KPIs
    df["revenue_per_visitor"] = (df["revenue"] / df["visitors"]).round(2)
    df["customer_acquisition_cost_proxy"] = (
        df["visitors"] / df["customers"]
    ).round(2)

    return df


def summarize_kpis(df: pd.DataFrame) -> dict:
    """
    Return a summary dictionary of KPIs across the entire dataset.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with KPI columns already calculated.

    Returns
    -------
    dict
        Summary statistics for key metrics.
    """
    return {
        "total_revenue": round(df["revenue"].sum(), 2),
        "total_orders": int(df["orders"].sum()),
        "total_visitors": int(df["visitors"].sum()),
        "total_customers": int(df["customers"].sum()),
        "avg_conversion_rate": round(df["conversion_rate"].mean() * 100, 2),
        "avg_order_value": round(df["average_order_value"].mean(), 2),
        "avg_revenue_per_visitor": round(df["revenue_per_visitor"].mean(), 2),
    }
