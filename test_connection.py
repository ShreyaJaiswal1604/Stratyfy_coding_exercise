from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Build DATABASE_URL
DATABASE_URL = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

def test_db_connection():
    """Test connection to PostgreSQL database."""
    try:
        print(f"Testing connection to: {DATABASE_URL}")
        engine = create_engine(DATABASE_URL, echo=True)
        with engine.connect() as connection:
            # Use text() to wrap the raw SQL query
            result = connection.execute(text("SELECT 1;"))
            print("Database connection successful!")
            print(f"Test query result: {result.fetchone()[0]}")
    except OperationalError as e:
        print("Failed to connect to the database.")
        print(f"Error: {e}")
    finally:
        print("Connection test complete.")

if __name__ == "__main__":
    test_db_connection()
