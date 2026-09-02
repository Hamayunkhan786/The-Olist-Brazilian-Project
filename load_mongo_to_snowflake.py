import os
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import pandas as pd
from pymongo import MongoClient
import json

mongo_client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017/"))
mongo_db = mongo_client[os.getenv("MONGO_DB", "ecommerce_mongo_db")]

snowflake_conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER", "your_user"),
    password=os.getenv("SNOWFLAKE_PASSWORD", "change_me"),
    account=os.getenv("SNOWFLAKE_ACCOUNT", "your_account"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
    database=os.getenv("SNOWFLAKE_DATABASE", "ECOMMERCE_DW"),
    schema=os.getenv("SNOWFLAKE_SCHEMA", "RAW")
)

mongo_collections_to_sync = {
    "products": "MONGO_PRODUCTS",
    "reviews": "MONGO_REVIEWS",
    "category_translations": "MONGO_CATEGORY_TRANSLATIONS",
    "customer_events": "MONGO_CUSTOMER_EVENTS"
}

try:
    print("Connecting to MongoDB...")
    
    for mongo_col, sf_table in mongo_collections_to_sync.items():
        print(f"Fetching documents from MongoDB collection: {mongo_col}...")
        collection = mongo_db[mongo_col]
        documents = list(collection.find({}))
        
        if not documents:
            print(f"No documents found in {mongo_col}. Skipping...")
            continue

        for doc in documents:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])

        df = pd.DataFrame({
            'raw_data': [json.dumps(doc) for doc in documents]
        })
        
        print(f"Loaded {len(df)} documents from {mongo_col}. Inserting into Snowflake table {sf_table}...")

        success, nchunks, nrows, _ = write_pandas(
            conn=snowflake_conn,
            df=df,
            table_name=sf_table,
            database='ECOMMERCE_DW',
            schema='RAW',
            auto_create_table=False
        )
        print(f"Successfully loaded {nrows} rows into Snowflake table {sf_table}!\n")

    print("All MongoDB collections successfully synced to Snowflake VARIANT tables!")

except Exception as e:
    print(f"Error during MongoDB data ingestion: {e}")

finally:
    mongo_client.close()
    snowflake_conn.close()
    print("Connections closed.")