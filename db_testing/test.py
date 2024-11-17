import pandas as pd
import psycopg2
from llm.gait import gAit as Gyatt
from aws.rds import get_db_connection  # Import the new function

# HARDCODDEEEDD WE WILL GET THIS FROM LAMBDA
CSV_FILE_PATH = "profile.csv"
SCHEMA_NAME = "TESSSST2"
TABLE_NAME = "your_table_name"

def create_table_and_insert_data():
    # Get a connection to the RDS database
    conn = get_db_connection()
    cursor = conn.cursor()
    print("Connected to the RDS database.")

    df = pd.read_csv(CSV_FILE_PATH)

    # Generate the SQL to create a table based on the CSV columns
    column_types = ", ".join(
        f"{col} TEXT" for col in df.columns
    )
    
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} ({column_types});"
    
    # try to create a table
    try:
        cursor.execute(create_table_sql)
        conn.commit()
        print(f"Table {TABLE_NAME} created successfully.")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()  # Close the cursor
        conn.close()    # Close the connection

if __name__ == "__main__":
    create_table_and_insert_data()
