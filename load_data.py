import pandas as pd
from sqlalchemy import create_engine, text, event
import os

PG_URI = os.getenv("PG_URI", "postgresql://postgres:change_me@localhost:5432/ecommerce_source")
engine = create_engine(PG_URI)

conn = engine.raw_connection()
cursor = conn.cursor()
cursor.execute("DROP SCHEMA IF EXISTS source CASCADE;")
cursor.execute("CREATE SCHEMA source;")
conn.commit()
conn.close()

with engine.begin() as conn:
    pass

data_dir = "data"
csv_files = {
    'olist_customers_dataset.csv': 'customers',
    'olist_orders_dataset.csv': 'orders',
    'olist_order_items_dataset.csv': 'order_items',
    'olist_order_payments_dataset.csv': 'order_payments',
    'olist_sellers_dataset.csv': 'sellers',
    'olist_geolocation_dataset.csv': 'geolocation',
}

if os.path.exists(os.path.join(data_dir, 'olist_products_dataset.csv')):
    csv_files['olist_products_dataset.csv'] = 'products'

print("Loading CSV files into PostgreSQL...")
for csv_file, table_name in csv_files.items():
    file_path = os.path.join(data_dir, csv_file)
    if os.path.exists(file_path):
        print(f"Loading {csv_file} into {table_name}...")
        df = pd.read_csv(file_path)
        df.to_sql(table_name, engine, schema='source', if_exists='replace', index=False)
        print(f"✓ Loaded {len(df)} rows into source.{table_name}")
    else:
        print(f"✗ File not found: {file_path}")

print("\nData loading complete!")
