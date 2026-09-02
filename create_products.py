import pandas as pd
import os
from sqlalchemy import create_engine, text

# Database connection
PG_URI = os.getenv("PG_URI", "postgresql://postgres:change_me@localhost:5432/ecommerce_source")
engine = create_engine(PG_URI)

# Get unique product_ids from order_items
query = """
    SELECT DISTINCT product_id 
    FROM source.order_items 
    ORDER BY product_id 
    LIMIT 1000
"""

products = pd.read_sql_query(query, engine)

# Create a minimal products dataset with required columns
products['product_category_name'] = 'misc'
products['product_name_length'] = 10
products['product_description_length'] = 50
products['product_photos_qty'] = 1
products['product_weight_g'] = 1000
products['product_length_cm'] = 10
products['product_height_cm'] = 10
products['product_width_cm'] = 10

# Save to CSV
products.to_csv('data/olist_products_dataset.csv', index=False)
print(f"Created products dataset with {len(products)} products")
