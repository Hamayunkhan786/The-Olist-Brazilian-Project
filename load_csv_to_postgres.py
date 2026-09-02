import os
import pandas as pd
from sqlalchemy import create_engine

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "change_me")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "ecommerce_source")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

csv_file_path = "olist_customers_dataset.csv" 

try:
    print("CSV file read ho rahi hai...")
    df = pd.read_csv(csv_file_path)
    print(f"Total rows read: {len(df)}")

    print("PostgreSQL ke 'source.customers' table mein data write ho raha hai...")
    df.to_sql(
        name='customers',
        con=engine,
        schema='source',
        if_exists='replace',
        index=False
    )
    print("Data PostgreSQL 'source.customers' mein successfully load ho gaya!")

except Exception as e:
    print(f"Error aaya: {e}")