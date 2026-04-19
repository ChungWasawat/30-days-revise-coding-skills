# src/etl_pipeline.py — Day 17 version, now with real DB
import os
import logging
import pandas as pd
from sqlalchemy import create_engine, text

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format="%(levelname)s %(asctime)s %(message)s"
)
logger = logging.getLogger(__name__)

def get_engine():
    return create_engine(
        os.environ["DATABASE_URL"],
        pool_size=2,
        pool_pre_ping=True,
    )

def setup_schema(engine):
    """Idempotent schema creation — safe to run on every pipeline execution."""
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS customers (
                id SERIAL PRIMARY KEY,
                name TEXT,
                tenure_months INT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """))
    logger.info("Created customers table")
    
def run_pipeline():
    logger.info(f"Pipeline starting — APP_ENV: {os.environ.get('APP_ENV')}")
    engine = get_engine()

    setup_schema(engine)

    # Simulate extracted data
    df = pd.DataFrame([
        {"name": "Alice", "tenure_months": 3},
        {"name": "Bob",   "tenure_months": 18},
        {"name": "Carol", "tenure_months": 1},
    ])

    # Transform
    df["churn_risk"] = df["tenure_months"].apply(lambda x: "high" if x < 6 else "low")
    data = df.to_dict(orient="records")

    try: 
        with engine.begin() as conn:
            # Create table if it doesn't exist yet
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS churn_scores (
                    name TEXT,
                    tenure_months INT,
                    churn_risk TEXT
                )
            """))

            # Now safe to truncate — table always exists at this point
            conn.execute(text("TRUNCATE TABLE churn_scores"))

            stmt = text("""
                INSERT INTO churn_scores (name, tenure_months, churn_risk)
                VALUES (:name, :tenure_months, :churn_risk)
            """)
            conn.execute(stmt, data)
            logger.info(f"Wrote {len(df)} rows to churn_scores")

            count = conn.execute(text("SELECT COUNT(*) FROM churn_scores")).scalar()
            logger.info(f"Verification: {count} rows in table")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise


if __name__ == "__main__":
    run_pipeline()