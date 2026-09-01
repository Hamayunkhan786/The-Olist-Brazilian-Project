import os
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import pandas as pd
from pymongo import MongoClient
import json

# 1. MongoDB Connection Configuration
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["ecommerce_mongo_db"]  # Apne MongoDB database ka naam yahan likhein

# 2. Snowflake Connection Configuration
snowflake_conn = snowflake.connector.connect(
    user='HAMAYUNKHAN',
    password='03287568610aA@',
    account='dqvneja-gp96469',
    warehouse='COMPUTE_WH',
    database='ECOMMERCE_DW',
    schema='RAW'
)

# MongoDB collection mapping -> Snowflake VARIANT table name
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

        # MongoDB ke '_id' object ko string mein convert karna taake pandas handle kar sake
        for doc in documents:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])

        # Snowflake ke VARIANT column ke liye data ko JSON string ya dict ke taur par DataFrame mein dalna
        # write_pandas dictionary/JSON ko VARIANT mein map kar deta hai jab data proper format mein ho
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