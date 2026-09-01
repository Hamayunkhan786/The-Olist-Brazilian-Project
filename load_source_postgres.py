import os
import pandas as pd
from sqlalchemy import create_engine

# 1. PostgreSQL Connection
PG_URI = os.getenv(
    "PG_URI",
    "postgresql://postgres:change_me@localhost:5432/ecommerce_source",
)
engine = create_engine(PG_URI)

# 2. Data folder ka path jahan CSVs mojood hain
data_folder = r"D:\olist-data-platform\data"

# 3. Project blueprint ke mutabiq tables ki mapping[cite: 1]
postgres_files = {
    "olist_customers_dataset.csv": "customers",
    "olist_orders_dataset.csv": "orders",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "payments",
    "olist_sellers_dataset.csv": "sellers",
    "olist_geolocation_dataset.csv": "geolocation"
}

# 4. Loop ke zariye load karna
for file_name, table_name in postgres_files.items():
    file_path = os.path.join(data_folder, file_name)
    
    if os.path.exists(file_path):
        print(f"Loading {file_name} into source.{table_name}...")
        df = pd.read_csv(file_path)
        
        df.to_sql(
            name=table_name,
            con=engine,
            schema='source',
            if_exists='replace',
            index=False
        )
        print(f"Successfully loaded: source.{table_name}")
    else:
        print(f"Warning: File nahi mili -> {file_path}")

print("\nPostgreSQL ke source schema ka setup mukammal ho gaya hai!")