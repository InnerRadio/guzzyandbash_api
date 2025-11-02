# update_superuser_affiliate.py

import os
import sys
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Add the parent directory to the sys.path to allow imports from 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app.database import Base, get_db
from app.models.user import User

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

# Create engine and session for direct script use
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def update_superuser_affiliate_id():
    db: Session = SessionLocal()
    try:
        # Find the superuser by username
        superuser = db.query(User).filter(User.username == "guzzy_superuser").first()

        if superuser:
            # Set the affiliate_id for the superuser
            # Use the same ID as in DUMMY_AFFILIATES for consistency
            new_affiliate_id = "guzzy_superuser_id"
            if superuser.affiliate_id != new_affiliate_id:
                superuser.affiliate_id = new_affiliate_id
                db.commit()
                print(f"Successfully updated affiliate_id for guzz_superuser to: {new_affiliate_id}")
            else:
                print(f"guzzy_superuser already has affiliate_id: {new_affiliate_id}. No update needed.")
        else:
            print("guzzy_superuser not found in the database. Please ensure the user exists.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting update_superuser_affiliate_id script...")
    update_superuser_affiliate_id()
    print("Script finished.")
