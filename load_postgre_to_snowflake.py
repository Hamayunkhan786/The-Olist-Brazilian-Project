import os
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import pandas as pd
import psycopg2

# 1. PostgreSQL Connection Configuration
pg_conn_params = {
    "dbname": "ecommerce_source",
    "user": "postgres",
    "password": "REDACTED",
    "host": "localhost",
    "port": "5432"
}

# 2. Snowflake Connection Configuration
snowflake_conn = snowflake.connector.connect(
    user='HAMAYUNKHAN',
    password='03287568610aA@',
    account='dqvneja-gp96469',
    warehouse='COMPUTE_WH',
    database='ECOMMERCE_DW',
    schema='RAW'
)

try:
    print("Connecting to PostgreSQL...")
    pg_conn = psycopg2.connect(**pg_conn_params)
    
    print("Fetching data from PostgreSQL source.customers table...")
    query = "SELECT customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state FROM source.customers;"
    df_customers = pd.read_sql(query, pg_conn)
    
    pg_conn.close()
    print(f"Fetched {len(df_customers)} rows from PostgreSQL.")

    # IMPORTANT: Snowflake ke liye column names ko uppercase karna zaroori hai
    df_customers.columns = [col.upper() for col in df_customers.columns]

    print("Loading data into Snowflake table POSTGRES_CUSTOMERS...")
    # 3. DataFrame ko Snowflake table mein load karna
    success, nchunks, nrows, _ = write_pandas(
        conn=snowflake_conn,
        df=df_customers,
        table_name='POSTGRES_CUSTOMERS',
        database='ECOMMERCE_DW',
        schema='RAW'
    )
    
    print(f"Successfully loaded {nrows} rows into Snowflake table POSTGRES_CUSTOMERS!")

except Exception as e:
    print(f"Error during data ingestion: {e}")

finally:
    snowflake_conn.close()
    print("Snowflake connection closed.")