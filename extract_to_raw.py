import os
import pandas as pd
import psycopg2
from bson.codec_options import CodecOptions
from pymongo import MongoClient

# 1. Output directory for raw files
OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("--- Starting Python Ingestion from PostgreSQL & MongoDB ---")


def to_safe_string(value):
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)

try:
    pg_conn = psycopg2.connect(
        dbname=os.getenv("PGDATABASE", "ecommerce_source"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", "REDACTED"),
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432")
    )
    
    tables = ["customers", "orders", "order_items", "payments", "sellers", "geolocation"]
    for table in tables:
        db_table = "order_payments" if table == "payments" else table
        query = f"SELECT * FROM source.{db_table}"
        
        df_pg = pd.read_sql(query, pg_conn)
        file_path = os.path.join(OUTPUT_DIR, f"pg_{table}.parquet")
        df_pg.to_parquet(file_path, index=False)
        print(f"[PostgreSQL] Extracted table 'source.{db_table}' -> {file_path} ({len(df_pg)} rows)")
        
    pg_conn.close()
except Exception as e:
    print(f"PostgreSQL Extraction Error: {e}")

try:
    mongo_client = MongoClient(
        os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    )
    db = mongo_client["ecommerce_events"]
    mongo_codec_options = CodecOptions(unicode_decode_error_handler="replace")
    
    collections = ["product_catalog", "order_reviews", "customer_events"]
    for coll_name in collections:
        collection = db[coll_name].with_options(codec_options=mongo_codec_options)
        data = list(collection.find({}, {"_id": 0}))
        if data:
            df_mongo = pd.DataFrame(data)
            
            # Convert byte values before pandas attempts to decode them.
            for col in df_mongo.columns:
                df_mongo[col] = df_mongo[col].map(to_safe_string)
            
            file_path = os.path.join(OUTPUT_DIR, f"mongo_{coll_name}.parquet")
            df_mongo.to_parquet(file_path, index=False)
            print(f"[MongoDB] Extracted collection '{coll_name}' -> {file_path} ({len(df_mongo)} rows)")
        else:
            print(f"[MongoDB] Collection '{coll_name}' is empty.")
            
    mongo_client.close()
except Exception as e:
    print(f"MongoDB Extraction Error: {e}")

print("--- Ingestion to Raw Files Completed Successfully ---")