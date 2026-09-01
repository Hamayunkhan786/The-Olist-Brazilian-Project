import os

import pandas as pd
import psycopg2
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

PG_CONN_PARAMS = {
    "dbname": os.getenv("PGDATABASE", "ecommerce_source"),
    "user": os.getenv("PGUSER", "postgres"),
    "password": os.getenv("PGPASSWORD", "change_me"),
    "host": os.getenv("PGHOST", "localhost"),
    "port": os.getenv("PGPORT", "5432"),
}

SNOWFLAKE_CONN = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER", "your_user"),
    password=os.getenv("SNOWFLAKE_PASSWORD", "change_me"),
    account=os.getenv("SNOWFLAKE_ACCOUNT", "your_account"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
    database=os.getenv("SNOWFLAKE_DATABASE", "ECOMMERCE_DW"),
    schema=os.getenv("SNOWFLAKE_SCHEMA", "RAW"),
)


def main():
    print("Connecting to PostgreSQL...")
    pg_conn = psycopg2.connect(**PG_CONN_PARAMS)
    query = "SELECT * FROM source.orders;"
    df = pd.read_sql(query, pg_conn)
    pg_conn.close()

    print(f"Fetched {len(df)} rows from source.orders")

    if df.empty:
        raise ValueError("No rows returned from source.orders")

    df.columns = [str(col).upper() for col in df.columns]

    print("Loading data into Snowflake RAW.ORDERS...")
    success, nchunks, nrows, _ = write_pandas(
        conn=SNOWFLAKE_CONN,
        df=df,
        table_name="ORDERS",
        database="ECOMMERCE_DW",
        schema="RAW",
        overwrite=True,
        auto_create_table=True,
        quote_identifiers=True,
    )

    print(f"SUCCESS: wrote {nrows} rows into RAW.ORDERS")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}")
        raise
    finally:
        SNOWFLAKE_CONN.close()
        print("Snowflake connection closed.")
