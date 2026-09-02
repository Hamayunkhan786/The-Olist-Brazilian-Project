import pandas as pd
from pymongo import MongoClient

mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["ecommerce_events"]

print("Restructuring product_catalog into nested MongoDB documents...")
products_raw = list(mongo_db["product_catalog"].find({}, {"_id": 0}))

nested_products = []
for p in products_raw:
    doc = {
        "_id": p.get("product_id"),
        "product_id": p.get("product_id"),
        "category": {
            "original": p.get("product_category_name")
        },
        "content": {
            "name_length": p.get("product_name_lenght"),
            "description_length": p.get("product_description_lenght"),
            "photos_count": p.get("product_photos_qty")
        },
        "dimensions": {
            "weight_g": p.get("product_weight_g"),
            "length_cm": p.get("product_length_cm"),
            "height_cm": p.get("product_height_cm"),
            "width_cm": p.get("product_width_cm")
        }
    }
    nested_products.append(doc)

mongo_db["products_nested"].drop()
mongo_db["products_nested"].insert_many(nested_products)
print(f"Successfully created 'products_nested' with {len(nested_products)} documents!")