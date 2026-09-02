import os
import snowflake.connector

account = os.getenv('SNOWFLAKE_ACCOUNT')
user = os.getenv('SNOWFLAKE_USER')
password = os.getenv('SNOWFLAKE_PASSWORD')
database = os.getenv('SNOWFLAKE_DATABASE', 'ECOMMERCE_DW')
warehouse = os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH')
schema = os.getenv('SNOWFLAKE_SCHEMA', 'STAGING')

try:
    print("Connecting to Snowflake...")
    conn = snowflake.connector.connect(
        account=account,
        user=user,
        password=password,
        warehouse=warehouse,
        database=database,
        schema=schema
    )
    
    cursor = conn.cursor()
    
    print("\n=== RAW LAYER ===")
    raw_tables = ['ORDERS', 'CUSTOMERS', 'ORDER_ITEMS', 'MONGO_PRODUCTS']
    for table in raw_tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM ECOMMERCE_DW.RAW.{table}")
            count = cursor.fetchone()[0]
            print(f"RAW.{table}: {count:,} rows")
        except Exception as e:
            print(f"RAW.{table}: ERROR - {e}")
    
    print("\n=== STAGING LAYER (Staging Models) ===")
    staging_tables = ['stg_orders', 'stg_customers', 'stg_order_items', 'stg_products']
    for table in staging_tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {schema}.{table}")
            count = cursor.fetchone()[0]
            print(f"STAGING.{table}: {count:,} rows")
        except Exception as e:
            print(f"STAGING.{table}: ERROR - {e}")
    
    print("\n=== MARTS LAYER (Dimensions & Facts) ===")
    marts_tables = ['dim_customers', 'dim_products', 'fct_orders']
    for table in marts_tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {schema}.{table}")
            count = cursor.fetchone()[0]
            print(f"STAGING.{table}: {count:,} rows")
        except Exception as e:
            print(f"STAGING.{table}: ERROR - {e}")
    
    cursor.close()
    conn.close()
    print("\n✅ Verification complete!")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
