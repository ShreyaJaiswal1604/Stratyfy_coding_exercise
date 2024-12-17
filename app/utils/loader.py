#from app.database import SessionLocal
from app.models.models import Sundae, Sale
import json

def load_data(db, sundae_file: str, sales_file: str):
    """
    Load data into the database from the JSON files in the correct order.

    Args:
        db (Session): SQLAlchemy database session.
        sundae_file (str): Path to the sundae menu JSON file.
        sales_file (str): Path to the sales transaction JSON file.
    """
    # Step 1: Load Sundaes Data
    print("Loading sundaes data...")
    try:
        with open(sundae_file, "r") as file:
            sundaes = json.load(file)
            for sundae in sundaes:
                db.add(Sundae(
                    id=sundae["id"],
                    name=sundae["name"],
                    description=sundae["description"]
                ))
        db.commit()
        print("Sundaes data loaded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error loading sundaes data: {e}")

    # Step 2: Load Sales Data
    print("Loading sales data...")
    try:
        with open(sales_file, "r") as file:
            sales = json.load(file)
            for sale in sales:
                db.add(Sale(
                    sundae_id=sale["sundae_id"],
                    timestamp=sale["timestamp"],
                    quantity=sale.get("quantity", 1)  # Default quantity to 1
                ))
        db.commit()
        print("Sales data loaded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error loading sales data: {e}")
