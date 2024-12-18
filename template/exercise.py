from webapp.database import Database
from webapp.models import Sundae, Sale
from pathlib import Path

def main():
    BASE_DIR = Path(__file__).resolve().parent
    SUNDAES_FILE = BASE_DIR / "webapp/data/sundaes.json"
    SALES_FILE = BASE_DIR / "webapp/data/sales.json"

    print("🔹 Starting the database process...")

    # Initialize the database
    db = Database()

    # Load data dynamically
    db.load_bulk_data(SUNDAES_FILE, Sundae)
    db.load_bulk_data(SALES_FILE, Sale)

    # Finalize
    db.close()


if __name__ == "__main__":
    main()
