from sqlalchemy import create_engine, text, inspect, Column, Float, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, MetaData
from dotenv import load_dotenv
import os
import json
from pathlib import Path
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

# Load environment variables
load_dotenv()

# Database Connection Parameters
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy Base Class
Base = declarative_base()


class Database:
    def __init__(self):
        """Initialize the database connection."""
        print("🔹 Initializing the database connection...")
        self.engine = create_engine(DB_URL, echo=False)
        self.session_factory = sessionmaker(bind=self.engine)
        self.schema_name = "public"  # Use the default schema
        print(f"🔹 Using schema '{self.schema_name}' for table creation...")

    def initialize_schema(self, model_class):
        """
        Create a specific table schema dynamically in the database.
        """
        print(f"🔹 Initializing table '{model_class.__tablename__}' in schema '{self.schema_name}'...")
        with self.engine.connect() as connection:
            connection.execute(text(f"SET search_path TO {self.schema_name}"))
            if not self.engine.dialect.has_table(connection, model_class.__tablename__, schema=self.schema_name):
                model_class.__table__.create(bind=self.engine)
                print(f"✅ Table '{model_class.__tablename__}' created successfully!")
            else:
                print(f"🔸 Table '{model_class.__tablename__}' already exists.")

    def _infer_column_type(self, value):
        """Infer SQL column type based on a Python value."""
        if isinstance(value, int):
            return "INTEGER"
        elif isinstance(value, float):
            return "FLOAT"
        elif isinstance(value, str):
            return "TEXT"
        else:
            return "TEXT"

    def _detect_and_update_schema(self, model_class, data_list):
        """
        Detect new columns and update the table schema dynamically.
        """
        print(f"🔹 Detecting and updating schema for table '{model_class.__tablename__}'...")
        with self.engine.connect() as connection:
            connection.execute(text(f"SET search_path TO {self.schema_name}"))
            inspector = inspect(connection)

            # Fetch existing columns
            existing_columns = {
                col["name"] for col in inspector.get_columns(model_class.__tablename__, schema=self.schema_name)
            }
            print(f"🔸 Existing columns in '{model_class.__tablename__}': {existing_columns}")

            # Detect columns in the JSON file
            all_keys = {key for record in data_list for key in record.keys()}
            print(f"🔸 Detected columns from JSON: {all_keys}")

            # Add missing columns to the table dynamically
            for key in all_keys:
                if key not in existing_columns:
                    sample_value = next(
                        (record[key] for record in data_list if key in record and record[key] is not None), None
                    )
                    column_type = self._infer_column_type(sample_value)
                    alter_query = (
                        f"ALTER TABLE {self.schema_name}.{model_class.__tablename__} ADD COLUMN {key} {column_type}"
                    )
                    print(f"🔸 Adding column '{key}' of type '{column_type}' to table '{model_class.__tablename__}'.")
                    connection.execute(text(alter_query))
                    print(f"✅ Column '{key}' added to table '{model_class.__tablename__}'.")

            connection.commit()  # Ensure changes are committed
            print(f"✅ Schema for '{model_class.__tablename__}' updated successfully.")
        self._reflect_table_schema(model_class)

    def _reflect_table_schema(self, model_class):
        """
        Reflect the updated table schema and synchronize the ORM model.
        """
        print(f"🔹 Reflecting table schema for '{model_class.__tablename__}'...")
        metadata = MetaData(schema=self.schema_name)
        metadata.reflect(bind=self.engine)

        table = metadata.tables[f"{self.schema_name}.{model_class.__tablename__}"]

        # Add new columns to the ORM model dynamically
        for column in table.columns:
            if not hasattr(model_class, column.name):
                setattr(model_class, column.name, Column(column.type))
                print(f"✅ Added runtime column '{column.name}' to model '{model_class.__name__}'.")

        # Update the model's table reference
        model_class.__table__ = table
        print(f"✅ Model '{model_class.__name__}' synchronized with updated table schema.")

    def load_bulk_data(self, file_path: Path, model_class):
        """
        Load JSON data into the database dynamically.
        """
        print(f"🔹 Loading bulk data from '{file_path.name}' into table '{model_class.__tablename__}'...")
        session = self.session_factory()
        try:
            # Load JSON data
            with open(file_path, "r") as f:
                data_list = json.load(f)
            print(f"🔸 Loaded {len(data_list)} records from '{file_path.name}'.")

            # Initialize table and update schema
            self.initialize_schema(model_class)
            self._detect_and_update_schema(model_class, data_list)

            # Prepare and insert data
            objects = [model_class(**record) for record in data_list]
            print(f"🔸 Preparing to insert {len(objects)} records into '{model_class.__tablename__}'...")

            session.bulk_save_objects(objects)
            session.commit()
            print(f"✅ Data from '{file_path.name}' loaded successfully into '{model_class.__tablename__}'!")

        except Exception as e:
            session.rollback()
            print(f"❌ Failed to load data from '{file_path.name}': {e}")
            raise
        finally:
            session.close()

    def close(self):
        """Close the database connection."""
        print(f"✅ Database session closed.")
