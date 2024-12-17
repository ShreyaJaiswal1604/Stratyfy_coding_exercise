import json
import argparse
from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData, Table, insert
from sqlalchemy.exc import SQLAlchemyError
from app.database import engine

# Initialize MetaData
metadata = MetaData()


def infer_column_type(value):
    """
    Infer SQLAlchemy column type based on the value type.
    """
    if isinstance(value, int):
        return Integer
    elif isinstance(value, float):
        return Float
    else:
        return String


def merge_table_schema(table_name, data_sample):
    """
    Dynamically merge the table schema with new fields from the JSON data.

    Args:
        table_name (str): The name of the table.
        data_sample (dict): A sample JSON record to infer the schema.
    """
    try:
        # Reflect existing tables in the database
        metadata.reflect(bind=engine)
        existing_table = metadata.tables.get(table_name)

        # Check for existing columns if the table exists
        existing_columns = {col.name for col in existing_table.columns} if existing_table else set()
        new_columns = []

        # Infer new columns from data_sample
        for key, value in data_sample.items():
            if key not in existing_columns:
                column_type = infer_column_type(value)
                new_columns.append(Column(key, column_type))
            else:
                print(f"Column '{key}' already exists in '{table_name}', skipping...")

        # If the table doesn't exist, create it
        if existing_table is None:
            print(f"Creating new table '{table_name}'...")
            columns = [Column("id_pk", Integer, primary_key=True, autoincrement=True)] + new_columns
            new_table = Table(table_name, metadata, *columns)
            metadata.create_all(engine)
            print(f"Table '{table_name}' created successfully.")
        else:
            # Dynamically add new columns to the existing table
            with engine.connect() as conn:
                for column in new_columns:
                    print(f"Adding new column '{column.name}' to table '{table_name}'...")
                    alter_query = f"ALTER TABLE {table_name} ADD COLUMN {column.name} {column.type.compile(engine)}"
                    conn.execute(alter_query)
            print(f"Schema for table '{table_name}' updated successfully.")
    except SQLAlchemyError as e:
        print(f"Error updating schema for table '{table_name}': {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def load_json_data_to_table(json_file, table_name):
    """
    Load data from JSON file into the corresponding table.
    Args:
        json_file (str): Path to the JSON file.
        table_name (str): Table name to insert data into.
    """
    try:
        # Load JSON data
        with open(json_file, "r") as file:
            data = json.load(file)

        if not data or not isinstance(data, list):
            print("No data found or invalid JSON format.")
            return

        # Merge schema dynamically
        data_sample = data[0]
        merge_table_schema(table_name, data_sample)

        # Reflect the updated table
        metadata.reflect(bind=engine)
        table = metadata.tables[table_name]

        # Insert data using a single bulk insert
        print(f"Inserting data into table '{table_name}'...")
        with engine.connect() as conn:
            conn.execute(insert(table), data)
            conn.commit()  # Commit transaction
        print(f"Data successfully inserted into table '{table_name}'.")

    except SQLAlchemyError as e:
        print(f"Database error occurred while loading data: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Load JSON data into a database dynamically.")
    parser.add_argument("filepath", type=str, help="Path to the JSON file")
    parser.add_argument("tablename", type=str, help="Name of the table to load data into")
    args = parser.parse_args()

    # Load data into the specified table
    load_json_data_to_table(args.filepath, args.tablename)
