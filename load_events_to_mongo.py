import os
import pandas as pd
from pymongo import MongoClient

# 1. MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce"]
collection = db["customer_events"]

# Purana data clear karne ke liye
collection.delete_many({})

# 2. Parquet file ka path (data/raw folder se)
events_file = r"D:\olist-data-platform\data\raw\mongo_customer_events.parquet"

if os.path.exists(events_file):
    print("Reading customer events Parquet file...")
    df_events = pd.read_parquet(events_file)
    
    documents = []
    for _, row in df_events.iterrows():
        def get_val(col_name, default=None):
            return row[col_name] if col_name in row and pd.notna(row[col_name]) else default

        doc = {
            "event_id": str(get_val('event_id')) if get_val('event_id') else None,
            "customer_id": str(get_val('customer_id')) if get_val('customer_id') else None,
            "event_type": str(get_val('event_type')) if get_val('event_type') else "page_view",
            "product_id": str(get_val('product_id')) if get_val('product_id') else None,
            "timestamp": str(get_val('timestamp')) if get_val('timestamp') else None,
            "event_data": {
                "session_id": str(get_val('session_id')) if get_val('session_id') else None,
                "platform": str(get_val('platform')) if get_val('platform') else "web",
                "device": str(get_val('device')) if get_val('device') else None
            },
            "metadata": {
                "source": "olist_synthetic_events",
                "ingested_at": pd.Timestamp.now().isoformat()
            }
        }
        documents.append(doc)
    
    # 3. Bulk insert into MongoDB
    if documents:
        # Batch inserting to handle large number of event records smoothly
        batch_size = 5000
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            collection.insert_many(batch)
            print(f"Inserted batch {i // batch_size + 1} ({len(batch)} documents)...")
            
        print(f"Successfully inserted all {len(documents)} customer event documents into MongoDB (`ecommerce.customer_events`)!")
else:
    print(f"Error: Events file nahi mili -> {events_file}")