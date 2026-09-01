import pandas as pd
from pymongo import MongoClient
from sqlalchemy import create_engine, text

PG_URI = "postgresql://postgres:REDACTED@localhost:5432/ecommerce_source"
engine = create_engine(PG_URI)

mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["ecommerce_events"]

print("Extracting Relational Data (Orders & Items) from PostgreSQL...")
orders_df = pd.read_sql_query(
    "SELECT order_id, customer_id, order_status, order_purchase_timestamp FROM source.orders;",
    engine
)

print("Extracting & Aggregating Reviews from MongoDB...")
reviews_data = list(mongo_db["order_reviews"].find(
    {}, 
    {"_id": 0, "order_id": 1, "review_score": 1, "review_comment_message": 1}
))
reviews_df = pd.DataFrame(reviews_data)

# Convert review_score to numeric and aggregate multiple reviews per order
reviews_df["review_score"] = pd.to_numeric(reviews_df["review_score"], errors="coerce")
reviews_summary = reviews_df.groupby("order_id").agg(
    avg_review_score=("review_score", "mean"),
    review_count=("review_score", "count"),
    has_comment=("review_comment_message", lambda x: x.notna().any())
).reset_index()

print("Joining PostgreSQL Orders with MongoDB Reviews...")
enriched_df = pd.merge(orders_df, reviews_summary, on="order_id", how="left")

eniched_df["avg_review_score"] = enriched_df["avg_review_score"].fillna(0)
eniched_df["review_count"] = enriched_df["review_count"].fillna(0).astype(int)
eniched_df["has_comment"] = enriched_df["has_comment"].fillna(False)

print("Writing Enriched Analytics Dataset back to PostgreSQL...")
with engine.begin() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS analytics;"))

# Load into PostgreSQL destination table
enriched_df.to_sql(
    name="enriched_orders",
    con=engine,
    schema="analytics",
    if_exists="replace",
    index=False
)

print("\nETL Pipeline Execution Complete!")
print(f"Successfully loaded {len(enriched_df)} transformed records into 'analytics.enriched_orders'.")