# app/database.py
import os # THIS SHOULD BE AT THE VERY TOP
from dotenv import load_dotenv # THIS SHOULD BE HERE TOO

# Load environment variables from .env file immediately
load_dotenv() # THIS CALL IS NOW AT THE VERY TOP

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError # For database connection testing

# Database Configuration - This will now read from your .env file
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Database Engine and Session
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_recycle=3600 # Recommended for MySQL to prevent "MySQL server has gone away" errors
)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database Initialization - Create tables if they don't exist
def init_db():
    try:
        # ADDED: checkfirst=True to prevent errors if tables already exist
        Base.metadata.create_all(bind=engine, checkfirst=True)
        print("Database tables created or already exist.")
    except OperationalError as e:
        print(f"Database connection failed or tables could not be created: {e}")
        print("Please ensure your database credentials and remote access are correctly configured.")
        # Re-raise the exception to ensure the application doesn't start in an unstable state
        raise
    except Exception as e:
        print(f"An unexpected error occurred during database initialization: {e}")
        # Re-raise the exception for any other unexpected errors
        raise