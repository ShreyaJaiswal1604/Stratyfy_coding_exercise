from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine.url import URL
from dotenv import load_dotenv
import os
import urllib.parse  # For URL encoding

# Load environment variables from the .env file
load_dotenv()


# Dynamically build the DATABASE_URL from environment variables
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),       # Database username
    password=os.getenv("DB_PASSWORD"),           # URL-encoded Database password
    host=os.getenv("DB_HOST"),           # Database host
    port=os.getenv("DB_PORT"),           # Database port
    database=os.getenv("DB_NAME")        # Database name
)

print(f"Connecting to: {DATABASE_URL}")  # Debugging connection string

# Create a database engine using the constructed DATABASE_URL
engine = create_engine(DATABASE_URL, echo=True)

# Create a session maker to handle database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy ORM models
Base = declarative_base()

def get_db():
    """
    Dependency to get a database session for API endpoints.
    Ensures the session is properly closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
