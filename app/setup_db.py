from app.database import Base, engine, SessionLocal
from app.utils.loader import load_data

# File paths to the JSON files
SUNDAES_FILE = "data/sundaes.json"
SALES_FILE = "data/sales.json"

def initialize_database():
    """
    Create tables in the database and load data.
    """
    print("Creating tables in the database...")
    Base.metadata.create_all(bind=engine)  # Create tables based on ORM models
    print("Tables created successfully!")

    print("Loading data into tables...")
    with SessionLocal() as db:
        load_data(db, SUNDAES_FILE, SALES_FILE)
    print("Database setup complete!")

if __name__ == "__main__":
    print("Initializing the database...")
    initialize_database()
