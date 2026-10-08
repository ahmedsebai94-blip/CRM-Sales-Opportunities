# CRM Sales ETL

An Apache Airflow, dbt, and DuckDB project that loads CRM sales CSV files,
builds analytical models, and checks data quality.

## Requirements

- Docker Desktop
- Astro CLI

## Run locally

1. Open a terminal in this directory (`dags_airflow2`).
2. Start the local Airflow environment:

   ```powershell
   astro dev start
   ```

3. Open the Airflow UI at the URL printed by Astro CLI.
4. Unpause and trigger `crm_sales_etl_pipeline_`.
5. Check the three tasks in order:
   `load_csv_to_duckdb` → `run_dbt_models` → `test_dbt_models`.

The DAG runs daily, does not backfill old runs, and retries a failed task once
after five minutes.

## Pipeline and data

The source files are in `data/raw/`:

- `accounts.csv`
- `data_dictionary.csv`
- `products.csv`
- `sales_pipeline.csv`
- `sales_teams.csv`

Airflow loads these files into the `ods` schema of
`dbt_project/dev.duckdb`. dbt then creates staging views in `main_stg` and
analytical tables in `main_dwh`. The DuckDB profile is in `include/profiles.yml`.

The fact table is at the grain of one sales opportunity. Open opportunities
may not have an account, close date, or close value; those fields are therefore
allowed to be null where applicable. See [docs/DATA_MODEL.md](docs/DATA_MODEL.md)
for conceptual, logical, and physical diagrams and field details.
For full project setup, architecture, task behavior, tests, and troubleshooting,
see the [Arabic project documentation](docs/PROJECT_DOCUMENTATION_AR.md).

## Dependencies and configuration

Python dependencies are declared in `requirements.txt` (`duckdb` and
`dbt-duckdb`). Astro installs them when building the local runtime image.
`include/profiles.yml` configures dbt to use the DuckDB file in the project.

## Validation

The pipeline was validated in the Astro runtime:

- 10 dbt models built successfully.
- 12 dbt data tests passed.
- Airflow reported no DAG import errors.

## Submission contents

The submission ZIP contains the Astro project, source CSVs, dbt models,
configuration, and documentation. It omits local secrets, generated DuckDB
files, logs, caches, and virtual environments; these are recreated locally.

The sibling `../dbt_project/` directory is a separate standalone dbt project;
the Airflow DAG does not use it. The sibling script
`../scripts/load_to_ods.py` writes to that standalone project's DuckDB file.
Keep both sibling paths if you still use that loader; the active Astro
pipeline uses only `./dbt_project/` and `./dags/`.
