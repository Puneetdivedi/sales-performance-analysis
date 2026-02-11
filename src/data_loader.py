import pandas as pd
import os


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load sales data from CSV and perform basic cleaning.

    Parameters
    ----------
    file_path : str
        Path to the CSV file containing sales data.

    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame with parsed dates and no missing values.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found: {file_path}")

    df = pd.read_csv(file_path)

    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"])

    # Drop rows with any missing values
    df = df.dropna()

    # Ensure numeric columns are the right type
    numeric_cols = ["visitors", "customers", "orders", "revenue"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop any rows that became NaN after coercion
    df = df.dropna()

    # Sort by date
    df = df.sort_values("date").reset_index(drop=True)

    return df


def load_processed_data(file_path: str) -> pd.DataFrame:
    """
    Load a processed CSV file (e.g., monthly trends).

    Parameters
    ----------
    file_path : str
        Path to the processed CSV file.

    Returns
    -------
    pd.DataFrame
        The loaded DataFrame.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Processed data not found: {file_path}")

    df = pd.read_csv(file_path)
    return df
