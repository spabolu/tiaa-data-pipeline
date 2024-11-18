import pandas as pd
from io import StringIO
from aws.rds import get_db_connection

def Populate_RDS(dataframes, schema_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Step 1: Create schema
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name};")

        for entry in dataframes:
            df = entry["dataframe"]
            table_name = entry["name"].split('/')[1]
            table_name = table_name.split('.')[0]
            
            # Step 2: Create tables
            create_table(cursor, schema_name, table_name, df)
            
            # Step 3: Populate table
            populate_table(cursor, conn, schema_name, table_name, df)

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
        
def infer_column_types(df):
    dtype_mapping = {
        'int64': 'INTEGER',
        'float64': 'REAL',
        'object': 'TEXT',
        'bool': 'BOOLEAN',
        'datetime64[ns]': 'TIMESTAMP'
    }
    column_types = []
    for column, dtype in df.dtypes.items():
        sql_type = dtype_mapping.get(str(dtype), 'TEXT')  # Default to TEXT for unknown types
        column_types.append(f"{column} {sql_type}")
    return ", ".join(column_types)

def create_table(cursor, schema_name, table_name, df):
    column_types = infer_column_types(df)
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
        {column_types}
    );
    """
    print(create_table_sql)
    
    cursor.execute(create_table_sql)
    print(f"Table {table_name} in schema {schema_name} created successfully.")

def populate_table(cursor, conn, schema_name, table_name, df):
    buffer = StringIO()
    df.to_csv(buffer, index=False, header=False)
    buffer.seek(0)
    copy_sql = f"""
    COPY {schema_name}.{table_name} FROM STDIN WITH CSV;
    """
    cursor.copy_expert(copy_sql, buffer)
    conn.commit()


# MOCK FUNCTION CALL
# portfolio = pd.read_csv("portfolio.csv")
# profile = pd.read_csv("profile.csv")
# transcript = pd.read_csv("transcript.csv")

# dataframes = [
#     {"name": "portfolio", "dataframe": portfolio},
#     {"name": "profile", "dataframe": profile},
#     {"name": "transcript", "dataframe": transcript}
# ]
# Populate_RDS(dataframes, "test2")
    
# def AI_generate_tables_with_relationships(dataframes, connection):
#     ai = gAit()
#     cursor = connection.cursor()

#     for entry in dataframes:
#         name, df = entry['name'], entry['dataframe']

#         # Infer column types
#         dtype_mapping = {
#             'int64': 'INTEGER',
#             'float64': 'REAL',
#             'object': 'TEXT',
#             'bool': 'BOOLEAN',
#             'datetime64[ns]': 'TIMESTAMP'
#         }
#         column_definitions = ", ".join(
#             f"{col} {dtype_mapping.get(str(dtype), 'TEXT')}" for col, dtype in df.dtypes.items()
#         )

#         # AI Prompt for SQL generation
#         prompt = f"""
#         Given the following data and schema inference, generate SQL code to create a table named `{name}` 
#         in a relational database. Ensure proper data types are used and infer any potential relationships 
#         (e.g., foreign keys) based on shared columns with other tables:
#         - Dataframe Name: {name}
#         - Columns and Types: {column_definitions}
#         - Example Rows: {df.head(10).to_string(index=False)}
#         """
#         sql_script = ai.ask_llm(prompt)

#         # Print and execute the generated SQL
#         print(f"Generated SQL for {name}:\n{sql_script}")
#         try:
#             cursor.execute(sql_script)
#             print(f"Table {name} created successfully.")
#         except Exception as e:
#             print(f"Error creating table {name}: {e}")
#             connection.rollback()

# # MOCK FUNCTION CALL
# portfolio = pd.read_csv("portfolio.csv")
# profile = pd.read_csv("profile.csv")
# transcript = pd.read_csv("transcript.csv")

# dataframes = [
#     {"name": "portfolio", "dataframe": portfolio},
#     {"name": "profile", "dataframe": profile},
#     {"name": "transcript", "dataframe": transcript}
# ]
# Populate_RDS(dataframes, "test2")
