# Phase 13: CI/CD, Automated Testing & Monitoring - Implementation Guide

## 1. Automated Data Quality Tests ✅

### Configured Tests
We have implemented comprehensive dbt tests in `dbt_ecommerce/models/schema.yml`:

#### Test Types:
- **Uniqueness Tests** (`unique`): Ensures no duplicate values
  - `order_id` in `stg_orders` and `fct_orders`
  - `customer_id` in `stg_customers` and `dim_customers`
  - `product_id` in `stg_products` and `dim_products`

- **Not Null Tests** (`not_null`): Ensures no missing values
  - All primary keys and critical fields
  - Foreign keys in staging tables

- **Relationship Tests** (`relationships`): Ensures referential integrity
  - `stg_order_items.order_id` → `stg_orders.order_id`
  - `stg_order_items.product_id` → `stg_products.product_id`
  - `stg_orders.customer_id` → `stg_customers.customer_id`
  - `fct_orders.customer_id` → `dim_customers.customer_id`

- **Accepted Values Tests** (`accepted_values`): Validates categorical data
  - `stg_orders.order_status`: created, approved, shipped, delivered, cancelled, invoiced, processing
  - `dim_customers.customer_state`: All valid Brazilian states (AC, AL, AP, AM, BA, CE, DF, ES, GO, MA, MT, MS, MG, PA, PB, PR, PE, PI, RJ, RN, RS, RO, RR, SC, SP, SE, TO)

#### Running Tests:
```bash
# Run all tests
cd dbt_ecommerce
dbt test

# Run tests for specific model
dbt test --select stg_orders

# Run specific test type
dbt test --select test_type:accepted_values
```

---

## 2. CI/CD Pipeline Integration ✅

### GitHub Actions Workflow
File: `.github/workflows/dbt-ci.yml`

**Features:**
- Auto-triggers on push to `main` and pull requests
- Python 3.11 + dbt-core 1.12.3 + dbt-snowflake 1.12.0
- Steps:
  1. Checkout code
  2. Install dependencies
  3. Create dbt profile (using GitHub secrets)
  4. `dbt debug` - Verify Snowflake connection
  5. `dbt parse` - Validate project structure
  6. `dbt run --select marts` - Build mart models
  7. `dbt test` - Run all data quality tests

### GitHub Secrets Required:
Set these in your GitHub repository settings:
- `SNOWFLAKE_ACCOUNT`: Your Snowflake account ID (e.g., `xy12345.us-east-1`)
- `SNOWFLAKE_USER`: Service account username
- `SNOWFLAKE_PASSWORD`: Service account password
- `SNOWFLAKE_DATABASE`: `ECOMMERCE_DW`
- `SNOWFLAKE_WAREHOUSE`: `COMPUTE_WH`

---

## 3. Orchestration & Scheduling ✅

### Airflow DAG: `olist_end_to_end_pipeline`
File: `dags/dbt_orchestration_dag.py`

**Schedule:** `@daily` (runs every day at UTC 00:00)

**Pipeline Tasks:**
1. **extract_sources_to_raw** - Extract PostgreSQL/MongoDB raw data
2. **load_orders_to_snowflake** - Load orders to Snowflake RAW.ORDERS
3. **load_postgre_to_snowflake** - Load PostgreSQL data (generic)
4. **load_mongo_to_snowflake** - Load MongoDB data to Snowflake
5. **dbt_staging** - Run staging models (stg_orders, stg_customers, etc.)
6. **dbt_marts** - Run marts models (dim_customers, dim_products, fct_orders)
7. **dbt_test** - Run all data quality tests
8. **dbt_docs** - Generate dbt documentation

**Dependencies:**
```
extract_sources → [load_orders, load_postgre, load_mongo]
                ↓
            dbt_staging → dbt_marts → dbt_test → dbt_docs
```

**Configuration:**
- **Retries:** 2 attempts before failure
- **Retry Delay:** 5 minutes
- **Owner:** hamayun
- **Email Alerts:** ON (configured for hamayun@example.com)
- **Resource Pools:** 
  - `postgres_pool`: 1 slot (PostgreSQL connection limit)
  - `snowflake_pool`: 1 slot (Snowflake concurrency control)
  - `dbt_pool`: 1 slot (dbt execution limit)

### Starting Airflow:
```bash
# Initialize Airflow database
airflow db init

# Create admin user
airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com

# Start scheduler
airflow scheduler

# Start webserver (in another terminal)
airflow webserver --port 8080
```

Access Airflow UI: http://localhost:8080

---

## 4. Data Quality Monitoring ✅

### dbt Snapshots
Snapshots track changes to dimensions over time:

- **snap_customers** - Tracks customer profile changes
  - Checks: `customer_city`, `customer_state`
  - Unique Key: `customer_id`
  - Strategy: Check strategy (tracks when columns change)

- **snap_orders** - Tracks order status changes
  - Checks: `order_status`, `order_approved_at`, `order_delivered_customer_date`
  - Unique Key: `order_id`
  - Strategy: Check strategy

**Running Snapshots:**
```bash
cd dbt_ecommerce
dbt snapshot
```

### Source Freshness Checks
Configured in `schema.yml` for the RAW layer:
- **Warn after:** 12 hours without data update
- **Error after:** 24 hours without data update

**Running Freshness Checks:**
```bash
cd dbt_ecommerce
dbt source freshness
```

---

## 5. Error Handling & Alerts ✅

### Email Alerts
Configured in `dags/dbt_orchestration_dag.py`:
- **email_on_failure:** TRUE - Send email when task fails
- **retries:** 2 - Retry failed tasks twice
- **retry_delay:** 5 minutes

### Setup Email in Airflow:
Edit `airflow/airflow.cfg`:
```ini
[email]
email_backend = airflow.providers.smtp.utils.smtplib.send_email_smtp

[smtp]
smtp_host = smtp.gmail.com
smtp_port = 587
smtp_user = your-email@gmail.com
smtp_password = your-app-password
smtp_mail_from = airflow@example.com
```

### Monitoring Airflow:
1. Airflow UI: http://localhost:8080
2. Check DAG run status
3. View task logs for failures
4. Review scheduled runs in the calendar view

---

## 6. Best Practices

### dbt Best Practices:
```bash
# Before committing code
dbt run --select +fct_orders  # Run fct_orders and upstream dependencies
dbt test                       # Run all tests
dbt docs generate              # Generate documentation
git add . && git commit -m "Update models and tests"
```

### Airflow Best Practices:
- Always use task pools for resource management
- Enable email alerts for production DAGs
- Review logs regularly for performance issues
- Monitor task execution time trends
- Set up data quality SLAs

### CI/CD Best Practices:
- Every PR runs tests automatically
- Merge only if CI passes
- Tag releases in GitHub
- Document breaking changes

---

## 7. Troubleshooting

### dbt Issues:
```bash
# Check Snowflake connection
dbt debug

# Parse errors without running
dbt parse

# Run with verbose output
dbt run --select marts -d

# Check test results in target/
cat target/run_results.json
```

### Airflow Issues:
```bash
# Check DAG validity
airflow dags list-import-errors

# Trigger DAG manually
airflow dags trigger olist_end_to_end_pipeline

# View task logs
airflow tasks logs olist_end_to_end_pipeline dbt_test

# Clear task state and retry
airflow tasks clear olist_end_to_end_pipeline -t dbt_test
```

### GitHub Actions Issues:
1. Check workflow runs in GitHub → Actions tab
2. Review logs for each failed step
3. Verify secrets are set correctly
4. Check Snowflake service account permissions

---

## 8. Next Steps

### Enhancement Ideas:
- [ ] Add Slack notifications for DAG failures
- [ ] Implement Great Expectations for advanced data profiling
- [ ] Add performance monitoring for dbt runs
- [ ] Set up dbt Cloud for managed orchestration
- [ ] Add data lineage visualization
- [ ] Implement incremental backfill strategies
- [ ] Add SLA monitoring and alerting
- [ ] Create custom dbt macros for reusable tests

---

## Summary

**Phase 13 Complete:**
✅ Automated Data Quality Tests - dbt tests configured for all models
✅ CI/CD Pipeline - GitHub Actions workflow for automated validation
✅ Orchestration & Scheduling - Airflow DAG with daily schedule
✅ Email Alerts - Configured for failure notifications
✅ Data Snapshots - Tracking dimension changes over time
✅ Freshness Checks - Monitoring RAW layer data staleness
✅ Documentation - Complete setup guide and best practices

Your data platform is now production-ready with comprehensive testing, orchestration, and monitoring! 🚀
