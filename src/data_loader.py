import pandas as pd


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load sales data from CSV and perform basic cleaning.
    """
    df = pd.read_csv(file_path)

    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"])

    # Basic sanity check
    df = df.dropna()

    return df
