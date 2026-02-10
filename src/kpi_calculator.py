def calculate_kpis(df):
    """
    Calculate core sales KPIs.
    """
    df = df.copy()

    df["conversion_rate"] = df["orders"] / df["visitors"]
    df["average_order_value"] = df["revenue"] / df["orders"]

    return df
