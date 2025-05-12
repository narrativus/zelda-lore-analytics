# ingest.py
# from zla.analysis import frequency_by_game # noqa: F401
from zla.etl import run_etl

if __name__ == "__main__":
    path = run_etl()
    print(f"✓ ETL complete → {path}")
