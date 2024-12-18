##################################################################################################################################################################################################################

from sqlalchemy import create_engine, text, inspect, Column, Float, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, MetaData
from dotenv import load_dotenv
import os
import json
from pathlib import Path
from webapp.models import Base, Sundae, Sale
from datetime import datetime
import uuid

# Load environment variables
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Database:
    def __init__(self):
        print("🔹 Initializing the database connection...")
        self.engine = create_engine(DB_URL, echo=False)
        self.session_factory = sessionmaker(bind=self.engine)
        self.schema_name = "public"
        print(f"🔹 Using schema '{self.schema_name}' for table creation...")

        # Create tables in the main schema
        self.initialize_schema()

    def initialize_schema(self):
        """Create tables in the main schema."""
        with self.engine.connect() as connection:
            connection.execute(text(f"SET search_path TO {self.schema_name}"))
            print(f"🔸 Search path set to schema '{self.schema_name}'.")
            Base.metadata.drop_all(bind=self.engine)
            Base.metadata.create_all(bind=self.engine)
            print(f"✅ Tables created successfully in schema '{self.schema_name}'!")

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
        """Detect new columns and update the table schema."""
        print(f"🔹 Detecting and updating schema for table '{model_class.__tablename__}'...")
        with self.engine.connect() as connection:
            connection.execute(text(f"SET search_path TO {self.schema_name}"))
            inspector = inspect(connection)

            existing_columns = {
                col["name"] for col in inspector.get_columns(model_class.__tablename__, schema=self.schema_name)
            }
            print(f"🔸 Existing columns in '{model_class.__tablename__}': {existing_columns}")

            all_keys = {key for record in data_list for key in record.keys()}
            print(f"🔸 Detected columns from JSON: {all_keys}")

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

            connection.commit()  # Ensure the transaction is committed
            print(f"✅ Schema for '{model_class.__tablename__}' updated successfully.")
        self._reflect_table_schema(model_class)

    def _reflect_table_schema(self, model_class):
        """Reflect the table schema and update the ORM model."""
        print(f"🔹 Reflecting table schema for '{model_class.__tablename__}'...")
        metadata = MetaData(schema=self.schema_name)
        metadata.reflect(bind=self.engine)

        table = metadata.tables[f"{self.schema_name}.{model_class.__tablename__}"]

        for column in table.columns:
            if not hasattr(model_class, column.name):
                setattr(model_class, column.name, Column(column.type))
                print(f"✅ Added runtime column '{column.name}' to model '{model_class.__name__}'.")

        model_class.__table__ = table
        print(f"✅ Model '{model_class.__name__}' synchronized with updated table schema.")

    def load_bulk_data(self, file_path: Path, model_class):
        """Load JSON data dynamically into the database."""
        print(f"🔹 Loading bulk data from '{file_path.name}' into table '{model_class.__tablename__}'...")
        session = self.session_factory()
        try:
            with open(file_path, "r") as f:
                data_list = json.load(f)
            print(f"🔸 Loaded {len(data_list)} records from '{file_path.name}'.")

            self._detect_and_update_schema(model_class, data_list)

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
        """Clean up the database session."""
        print(f"✅ Database session closed.")


##################################################################################################################################################################################################################
