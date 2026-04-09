import logging
from extract import fetch_all_posts
from transform import clean_posts
from db import get_connection_with_retry, load_df_to_postgres
from pathlib import Path

logging.basicConfig(level=logging.INFO)
data  = Path.cwd().parent / "data" / "users.csv"


def run():
    logging.info("Starting pipeline")

    # Extract
    raw = fetch_all_posts(data)
    logging.info(f"Extracted {len(raw)} records")

    # Transform
    df = clean_posts(raw)
    logging.info(f"Transformed — {len(df)} clean rows")

    # Load
    conn = get_connection_with_retry()
    load_df_to_postgres(df, "users", conn)
    conn.close()

    logging.info("Pipeline complete")

if __name__ == "__main__":
    run()