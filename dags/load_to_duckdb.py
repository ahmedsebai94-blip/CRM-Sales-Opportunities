from pathlib import Path


def load_data() -> None:
    import duckdb

    project_root = Path(__file__).resolve().parents[1]
    db_path = project_root / "dbt_project" / "dev.duckdb"
    raw_path = project_root / "data" / "raw"
    tables = {
        "accounts": raw_path / "accounts.csv",
        "data_dictionary": raw_path / "data_dictionary.csv",
        "products": raw_path / "products.csv",
        "sales_pipeline": raw_path / "sales_pipeline.csv",
        "sales_teams": raw_path / "sales_teams.csv",
    }

    con = duckdb.connect(str(db_path))
    try:
        con.execute("CREATE SCHEMA IF NOT EXISTS ods")

        for table_name, csv_path in tables.items():
            if not csv_path.is_file():
                raise FileNotFoundError(f"Required input CSV not found: {csv_path}")

            con.execute(
                f"""
                CREATE OR REPLACE TABLE ods.{table_name} AS
                SELECT *
                FROM read_csv_auto(?, header=True)
                """,
                [str(csv_path)],
            )

            count = con.execute(
                f"SELECT COUNT(*) FROM ods.{table_name}"
            ).fetchone()[0]
            print(f"Loaded ods.{table_name}: {count} rows")
    finally:
        con.close()

    print("ODS load complete")