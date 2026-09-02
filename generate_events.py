import random
import os
from datetime import datetime, timedelta
from pymongo import MongoClient
from sqlalchemy import create_engine
import pandas as pd

pg_engine = create_engine(os.getenv("PG_URI", "postgresql://postgres:change_me@localhost:5432/ecommerce_source"))
customer_ids = pd.read_sql("SELECT customer_id FROM source.customers LIMIT 5000;", pg_engine)["customer_id"].tolist()

mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["ecommerce_events"]
product_ids = mongo_db["products_nested"].distinct("product_id")

event_types = ["product_view", "product_search", "add_to_cart", "remove_from_cart", "checkout_started", "purchase"]
devices = [
    {"type": "mobile", "os": "Android", "browser": "Chrome"},
    {"type": "mobile", "os": "iOS", "browser": "Safari"},
    {"type": "desktop", "os": "Windows", "browser": "Edge"}
]

print("Generating 100,000 synthetic clickstream customer events...")
events = []
start_date = datetime(2026, 1, 1)

for i in range(100000):
    evt_time = start_date + timedelta(seconds=random.randint(0, 15000000))
    evt = {
        "_id": f"evt_{i+1:07d}",
        "event_id": f"evt_{i+1:07d}",
        "customer_id": random.choice(customer_ids),
        "product_id": random.choice(product_ids),
        "event_type": random.choice(event_types),
        "timestamp": evt_time.isoformat(),
        "device": random.choice(devices),
        "session_id": f"sess_{random.randint(10000, 99999)}"
    }
    events.append(evt)

mongo_db["customer_events"].drop()
mongo_db["customer_events"].insert_many(events)
print(f"Successfully inserted {len(events)} events into 'customer_events' collection!")