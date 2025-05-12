from pathlib import Path

import pandas as pd


def load_processed(
    path: str | Path = "data/processed/dialogue.parquet",
) -> pd.DataFrame:
    """Load the parquet produced by ETL."""
    return pd.read_parquet(path)
