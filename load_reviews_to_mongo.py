import os
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import BulkWriteError

client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce"]
collection = db["reviews"]

collection.delete_many({})

reviews_file = r"D:\olist-data-platform\data\raw\mongo_order_reviews.parquet"

if os.path.exists(reviews_file):
    print("Reading reviews Parquet file...")
    df_reviews = pd.read_parquet(reviews_file)
    
    # Duplicate review_ids remove karna
    if 'review_id' in df_reviews.columns:
        initial_count = len(df_reviews)
        df_reviews = df_reviews.drop_duplicates(subset=['review_id'])
        print(f"Removed {initial_count - len(df_reviews)} duplicate rows from source.")
    
    documents = []
    for _, row in df_reviews.iterrows():
        def get_val(col_name, default=None):
            return row[col_name] if col_name in row and pd.notna(row[col_name]) else default

        doc = {
            "_id": str(get_val('review_id')),
            "review_id": str(get_val('review_id')),
            "order_id": str(get_val('order_id')),
            "score": int(get_val('review_score', 0)),
            "comment": {
                "title": str(get_val('review_comment_title')) if get_val('review_comment_title') else None,
                "message": str(get_val('review_comment_message')) if get_val('review_comment_message') else None
            },
            "timestamps": {
                "creation_date": str(get_val('review_creation_date')) if get_val('review_creation_date') else None,
                "answer_timestamp": str(get_val('review_answer_timestamp')) if get_val('review_answer_timestamp') else None
            },
            "metadata": {
                "source": "olist",
                "ingested_at": pd.Timestamp.now().isoformat()
            }
        }
        documents.append(doc)
    
    # 3. Safe bulk insert with ordered=False
    if documents:
        try:
            result = collection.insert_many(documents, ordered=False)
            print(f"Successfully inserted {len(result.inserted_ids)} review documents into MongoDB (`ecommerce.reviews`)!")
        except BulkWriteError as bwe:
            inserted_count = bwe.details.get('nInserted', 0)
            print(f"Inserted successfully with some duplicates skipped: {inserted_count} documents added.")
else:
    print(f"Error: Reviews file nahi mili -> {reviews_file}")