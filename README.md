# Olist E-commerce Data Platform

A full-stack data engineering project that ingests transactional data from PostgreSQL and MongoDB into Snowflake, and then transforms it using dbt Core into analytics-ready staging and mart models.

## Architecture Overview

```text
PostgreSQL / MongoDB
        |
        v
Python ingestion scripts + Airflow DAGs
        |
        v
Snowflake RAW layer
        |
        v
dbt Core transformations
        |
        v
Staging + Marts layer
        |
        v
Business reporting dashboards / analytics
```

## Tech Stack

- Python
- Pandas
- SQLAlchemy
- PostgreSQL
- MongoDB
- Snowflake
- dbt Core
- Apache Airflow
- Docker

## Project Goals

- Ingest source data from operational systems into a raw warehouse layer
- Build reusable staging models for clean transformations
- Create dimension and fact tables for reporting
- Implement dbt tests for data quality
- Maintain a production-ready project structure for portfolio use

## Key Models

- `dim_customers`
- `dim_products`
- `fct_orders`

## Repository Structure

```text
.
├── dags/
│   └── ecommerce_pipeline_dag.py
├── data/
│   └── raw/
├── dbt_ecommerce/
│   ├── models/
│   ├── snapshots/
│   ├── tests/
│   ├── dbt_project.yml
│   └── README.md
├── .env.example
├── .gitignore
├── dbt_profiles.example.yml
├── extract_to_raw.py
├── load_orders_to_snowflake.py
├── etl_pipeline.py
├── docker-compose.yml
├── Dockerfile.airflow
├── README.md
└── requirements.txt (if used in your environment)
```

## Local Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

If you are using the environment already prepared in this project, make sure the correct virtualenv is activated before running scripts.

3. Copy example environment secrets:

```bash
copy .env.example .env
```

Then update the values with your local PostgreSQL, MongoDB, and Snowflake credentials.

4. Copy the dbt profile template:

```bash
copy dbt_profiles.example.yml dbt_profiles.yml
```

Update the file with your Snowflake account information and keep it local-only.

## Public Demo Data

This repository intentionally keeps only a tiny, anonymized sample dataset in the `sample_data/` folder for public sharing.

- Real production-like CSVs and all local warehouse data remain on the developer machine and are ignored by Git.
- Sensitive values, credentials, and generated warehouse artifacts are never committed.
- The sample CSVs are designed to demonstrate the data model without exposing real customer or order records.

## Data Ingestion

To move PostgreSQL source data into Snowflake RAW layer:

```bash
python load_orders_to_snowflake.py
```

You can also run the Airflow DAG from the project scheduler for scheduled extraction.

## dbt Commands

Run staging and marts models:

```bash
cd dbt_ecommerce
dbt run --select marts
```

Run a full project refresh:

```bash
dbt run --full-refresh
```

Run tests:

```bash
dbt test
```

## Security Notes

- Never commit real credentials or `.env` files.
- Keep local connection files outside version control.
- Use environment variables or `.env` files for local development.
- The root `.gitignore` has been configured to protect sensitive local files.

## Future Enhancements

- Add CI/CD using GitHub Actions
- Add more dbt tests for business logic validation
- Add a metrics layer for dashboard consumption
- Containerize the full platform for one-command setup

## License

This project is intended for learning, portfolio, and demonstration purposes.
