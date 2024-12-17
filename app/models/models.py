import json
import os
from sqlalchemy import (
    create_engine, MetaData, Table, Column, Integer, String, Float, inspect
)
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from app.database import engine

# Initialize MetaData
metadata = MetaData()

def infer_column_type(value):
    """
    Infer SQLAlchemy column type based on the value's Python type.
    """
    if isinstance(value, int):
        return Integer
    elif isinstance(value, float):
        return Float
    else:
        return String

def update_table_schema(table_name, json_file):
    """
    Update the table schema based on changes in the JSON file.
    Args:
        table_name (str): The name of the table.
        json_file (str): Path to the JSON file.
    """
    try:
        with open(json_file, "r") as file:
            data = json.load(file)

        if not data or not isinstance(data, list):
            print(f"No valid data found in {json_file}.")
            return

        # Extract a sample row to infer schema
        data_sample = data[0]
        print(f"Inferring schema for table '{table_name}'...")

        inspector = inspect(engine)

        # Check if table already exists
        if table_name in inspector.get_table_names():
            print(f"Table '{table_name}' already exists. Checking for schema changes...")
            with engine.connect() as conn:
                # Reflect the existing table
                existing_table = Table(table_name, metadata, autoload_with=engine)

                # Compare existing columns with new schema
                existing_columns = {col.name for col in existing_table.columns}

                # Identify new or missing columns
                for key, value in data_sample.items():
                    if key not in existing_columns:
                        print(f"Adding new column '{key}' to table '{table_name}'...")
                        alter_sql = f"ALTER TABLE {table_name} ADD COLUMN {key} {infer_column_type(value).__visit_name__.upper()}"
                        conn.execute(alter_sql)

                print(f"Schema for table '{table_name}' updated successfully.")
        else:
            # Create a new table if it doesn't exist
            print(f"Creating new table '{table_name}'...")
            columns = [Column("id", Integer, primary_key=True, autoincrement=True)]
            for key, value in data_sample.items():
                columns.append(Column(key, infer_column_type(value)))

            new_table = Table(table_name, metadata, *columns)
            metadata.create_all(engine)
            print(f"Table '{table_name}' created successfully.")

        # Load the data
        print(f"Loading data into table '{table_name}'...")
        with engine.connect() as conn:
            conn.execute(Table(table_name, metadata, autoload_with=engine).insert(), data)
        print(f"Data loaded into table '{table_name}' successfully.")

    except SQLAlchemyError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")
