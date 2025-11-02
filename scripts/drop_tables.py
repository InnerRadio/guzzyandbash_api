# scripts/drop_tables.py
import os
import sys

# Add the project root to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import engine, Base

def drop_all_tables():
    """Drops all tables defined in Base.metadata."""
    print("Attempting to drop all database tables...")
    Base.metadata.drop_all(bind=engine)
    print("All tables dropped successfully (if they existed).")

if __name__ == "__main__":
    drop_all_tables()
