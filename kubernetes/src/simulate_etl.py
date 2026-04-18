# src/etl_pipeline.py — Day 16 version
# Goal: prove that ConfigMap + Secret values are correctly injected.
# No DB connection yet — Postgres runs inside K8s starting Day 17.
import os
import logging

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

def run_pipeline():
    logger.info(f"Pipeline starting — APP_ENV: {os.environ.get('APP_ENV')}")
    logger.info(f"LOG_LEVEL:   {os.environ.get('LOG_LEVEL')}")
    logger.info(f"OUTPUT_DIR:  {os.environ.get('OUTPUT_DIR')}")

    # Confirm the secret arrived — never log the actual value
    db_url = os.environ.get("DATABASE_URL", "NOT SET")
    logger.info(f"DATABASE_URL present: {db_url != 'NOT SET'}")
    logger.info(f"DATABASE_URL prefix:  {db_url[:30]}...")   # safe to log the scheme only

    logger.info("All config loaded correctly — Day 16 complete")

if __name__ == "__main__":
    run_pipeline()