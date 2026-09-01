import os
import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce"]
collection = db["products"]

collection.delete_many({})

data_folder = r"D:\olist-data-platform\data"
products_file = os.path.join(data_folder, "olist_products_dataset.csv")

if os.path.exists(products_file):
    print("Reading products CSV...")
    df_products = pd.read_csv(products_file)
    
    documents = []
    for _, row in df_products.iterrows():
        def get_val(col_name, default=None):
            return row[col_name] if col_name in row and pd.notna(row[col_name]) else default

        doc = {
            "_id": str(get_val('product_id')),
            "product_id": str(get_val('product_id')),
            "category": {
                "original": str(get_val('product_category_name')) if get_val('product_category_name') else None
            },
            "content": {
                "name_length": int(get_val('product_name_length', get_val('product_name_lenght', 0))),
                "description_length": int(get_val('product_description_length', get_val('product_description_lenght', 0))),
                "photos_count": int(get_val('product_photos_qty', 0))
            },
            "dimensions": {
                "weight_g": float(get_val('product_weight_g', 0.0)),
                "length_cm": float(get_val('product_length_cm', 0.0)),
                "height_cm": float(get_val('product_height_cm', 0.0)),
                "width_cm": float(get_val('product_width_cm', 0.0))
            },
            "metadata": {
                "source": "olist",
                "ingested_at": pd.Timestamp.now().isoformat()
            }
        }
        documents.append(doc)
    
    if documents:
        collection.insert_many(documents)
        print(f"Successfully inserted {len(documents)} nested product documents into MongoDB (`ecommerce.products`)!")
else:
    print(f"Error: Products file not found -> {products_file}")