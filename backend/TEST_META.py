import pandas as pd
from io import StringIO
from datetime import datetime
from aws.rds import get_db_connection

def Populate_Metadata(dataframes, schema_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        print("TRYING")
        # Step 1: Create the metadata table
        create_metadata_table(cursor, schema_name)

        print("TABLE CREATED")
        
        for entry in dataframes:
            df = entry["dataframe"]
            file_path = entry["name"]
            print
            table_name = file_path.split('/')[1].split('.')[0]

            # Step 4: Populate the metadata table
            populate_metadata_table(cursor, schema_name, table_name, df)

        conn.commit()  # Commit all changes

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def create_metadata_table(cursor, schema_name):
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {schema_name}.metadata (
        id SERIAL PRIMARY KEY,
        data_source_name TEXT,
        column_descriptions TEXT,
        creation_time TIMESTAMP,
        num_rows INTEGER
    );
    """
    cursor.execute(create_table_sql)
    print(f"Metadata table in schema {schema_name} created successfully.")

def populate_metadata_table(cursor, schema_name, table_name, df):
    """Populate the metadata table with information about the CSV file."""
    data_source_name = table_name
    
    column_descriptions = ", ".join([f"{col}: {str(dtype)}" for col, dtype in df.dtypes.items()])
    creation_time = datetime.now()
    num_rows = len(df)

    insert_sql = f"""
    INSERT INTO {schema_name}.metadata (data_source_name, column_descriptions, creation_time, num_rows)
    VALUES (%s, %s, %s, %s);
    """
    cursor.execute(insert_sql, (data_source_name, column_descriptions, creation_time, num_rows))
    print(f"Metadata for {data_source_name} inserted into metadata table.")


# MOCK FUNCTION CALL
portfolio = pd.read_csv("portfolio.csv")
profile = pd.read_csv("profile.csv")
transcript = pd.read_csv("transcript.csv")

dataframes = [
    {"name": "test2/portfolio.csv", "dataframe": portfolio},
    {"name": "test2/profile.csv", "dataframe": profile},
    {"name": "test2/transcript.csv", "dataframe": transcript}
]
Populate_Metadata(dataframes, "test2")
