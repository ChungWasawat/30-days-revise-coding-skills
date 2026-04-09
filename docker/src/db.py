# src/db.py
import psycopg2
from psycopg2 import sql
import os
import logging
import time
from dotenv import load_dotenv

load_dotenv()


def get_connection_with_retry(retries=5, wait=3):
    for attempt in range(1, retries + 1):
        try:
            conn = psycopg2.connect(
                host     = os.environ.get("POSTGRES_HOST"),
                port     = int(os.environ.get("HOST_PORT", 5432)),
                database = os.environ.get("POSTGRES_DB"),
                user     = os.environ.get("POSTGRES_USER"),
                password = os.environ.get("POSTGRES_PASSWORD")
            )
            logging.info(f"Connected on attempt {attempt}")
            return conn
        except psycopg2.OperationalError as e:
            logging.warning(f"Attempt {attempt}/{retries} failed: {e}")
            if attempt < retries:
                time.sleep(wait)
    raise RuntimeError("Could not connect to database after all retries")


def load_df_to_postgres(df, table, conn):
    cols = df[0]
    records = df[1:]

    data = [tuple(r) for r in records]

    query = sql.SQL("INSERT INTO {tbl} ({col}) VALUES ({vals})").format(   \
        tbl=sql.Identifier(table),                                     \
        col=sql.SQL(", ").join(map(sql.Identifier, cols)),             \
        vals=sql.SQL(", ").join([sql.Placeholder()] * len(cols))                                              \
    )
  
    #logging.info(f"col_str:\n {cols}")
    #logging.info(f"data:\n {data}")
    try: 
        with conn.cursor() as cur:
            cur.executemany(query, data)
            logging.info(cur.rowcount)
        conn.commit()
        logging.info(f"Loaded {len(records)} rows into {table}")
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"{error}")