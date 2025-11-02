# app/crud/user.py
# This file contains CRUD (Create, Read, Update, Delete) operations for User entities,
# interacting directly with the MySQL database via SQLAlchemy.

# Standard library imports
import uuid
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime
import json # Import json for explicit serialization

# SQLAlchemy imports
from sqlalchemy.orm import Session
from sqlalchemy import exc # For database exceptions

# Application-specific imports
from app.models.user import User, UserRole # Import the SQLAlchemy User model and UserRole enum
from app.schemas.user_schemas import UserCreate, UserUpdate # Import Pydantic schemas for User
from app.core.security import get_password_hash # For hashing passwords

# Configure logging for this module
logger = logging.getLogger(__name__)

# DEBUGGING LINE: This will print the path of this file when it's loaded
print(f"DEBUG: app.crud.user is loaded from: {__file__}")

# --- CRUD Operations for User ---

def get_user(db: Session, user_id: str) -> Optional[User]:
    """
    Retrieves a single User from the database by their ID.
    """
    logger.debug(f"Attempting to retrieve User with ID: {user_id}")
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    Retrieves a single User from the database by their username.
    """
    logger.debug(f"Attempting to retrieve User with username: {username}")
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Retrieves a single User from the database by their email address.
    """
    logger.debug(f"Attempting to retrieve User with email: {email}")
    return db.query(User).filter(User.email == email).first()

def get_user_by_referral_code(db: Session, referral_code: str) -> Optional[User]:
    """
    Retrieves a single User from the database by their referral code.
    Returns None if no user is found with the given referral code.
    """
    logger.debug(f"Attempting to retrieve User with referral_code: {referral_code}")
    return db.query(User).filter(User.referral_code == referral_code).first()

def get_user_by_affiliate_id(db: Session, affiliate_id: str) -> Optional[User]:
    """
    Retrieves a single User from the database by their affiliate ID.
    Returns None if no user is found with the given affiliate ID.
    """
    logger.debug(f"Attempting to retrieve User with affiliate_id: {affiliate_id}")
    return db.query(User).filter(User.affiliate_id == affiliate_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Retrieves a list of Users from the database.
    """
    logger.debug(f"Attempting to retrieve users with skip: {skip}, limit: {limit}")
    return db.query(User).offset(skip).limit(limit).all()

def create_user(
    db: Session,
    user: UserCreate,
    affiliate_id: Optional[str] = None,
    referral_code: Optional[str] = None
) -> User:
    """
    Creates a new User in the database, handling full_name to first_name/last_name mapping
    and explicit JSON serialization for social_links.
    """
    logger.debug(f"Attempting to create user with username: {user.username}, email: {user.email}")
    # Check for existing user by username or email
    existing_user_by_username = get_user_by_username(db, user.username)
    if existing_user_by_username:
        logger.warning(f"Attempted to create user with duplicate username: {user.username}")
        return None # Indicate user creation failed due to duplicate username

    existing_user_by_email = get_user_by_email(db, user.email)
    if existing_user_by_email:
        logger.warning(f"Attempted to create user with duplicate email: {user.email}")
        return None # Indicate user creation failed due to duplicate email

    # Hash the password using the utility function from security.py
    hashed_password = get_password_hash(user.password)

    # Generate UUID for the user ID
    user_id = str(uuid.uuid4())

    # Use provided referral_code, or generate one if not provided
    final_referral_code = referral_code if referral_code else str(uuid.uuid4())[:8]

    # Ensure uniqueness for generated referral_code (if newly generated)
    if not referral_code: # Only check for uniqueness if we just generated it
        while get_user_by_referral_code(db, final_referral_code):
            logger.debug(f"Generated referral code {final_referral_code} already exists, regenerating.")
            final_referral_code = str(uuid.uuid4())[:8]

    # --- Start NEW/MODIFIED LOGIC: Parse full_name and explicitly serialize social_links ---
    first_name = None
    last_name = None
    if user.full_name:
        name_parts = user.full_name.split(maxsplit=1)
        first_name = name_parts[0]
        if len(name_parts) > 1:
            last_name = name_parts[1]

    # Explicitly convert social_links dictionary to JSON string, or set to None if empty
    social_links_for_db = None
    if user.social_links: # If the Pydantic field has a non-empty dict
        social_links_for_db = json.dumps(user.social_links)
    # --- END NEW/MODIFIED LOGIC ---

    db_user = User(
        id=user_id,
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        first_name=first_name,
        last_name=last_name,
        profile_picture_url=user.profile_picture_url,
        social_links=social_links_for_db, # Use the explicitly serialized string/None
        referral_code=final_referral_code,
        affiliate_id=affiliate_id,
        role=user.role,
        created_at=datetime.utcnow(),
        last_updated_at=datetime.utcnow()
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(f"Successfully created user with ID: {db_user.id} and username: {db_user.username}")
        return db_user
    except exc.IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error during user creation: {e}", exc_info=True)
        return None # Or raise HTTPException
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating User: {e}", exc_info=True)
        raise # Re-raise to be handled by API endpoint

def update_user(db: Session, user_id: str, user_update: UserUpdate) -> Optional[User]:
    """
    Updates an existing User's details, handling full_name and social_links serialization.
    """
    logger.debug(f"Attempting to update User with ID: {user_id}")
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        logger.warning(f"User with ID {user_id} not found for update.")
        return None

    update_data = user_update.model_dump(exclude_unset=True)

    # Handle password update separately
    if "password" in update_data and update_data["password"]:
        db_user.hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]

    # Handle full_name update for existing user
    if "full_name" in update_data and update_data["full_name"] is not None:
        name_parts = update_data["full_name"].split(maxsplit=1)
        db_user.first_name = name_parts[0]
        db_user.last_name = name_parts[1] if len(name_parts) > 1 else None
        del update_data["full_name"]

    # Explicitly serialize social_links for update if present
    if "social_links" in update_data and update_data["social_links"] is not None:
        # If the input is an empty dict, we want to store None or '{}'
        if update_data["social_links"]:
            db_user.social_links = json.dumps(update_data["social_links"])
        else:
            db_user.social_links = None # Or '{}' depending on desired empty state
        del update_data["social_links"]


    for key, value in update_data.items():
        setattr(db_user, key, value)

    db_user.last_updated_at = datetime.utcnow() # Update timestamp

    try:
        db.commit()
        db.refresh(db_user)
        logger.info(f"Successfully updated User with ID: {db_user.id}")
        return db_user
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating User {db_user.id}: {e}", exc_info=True)
        raise # Re-raise to be handled by API endpoint

def delete_user(db: Session, user_id: str) -> bool:
    """
    Deletes a User from the database by their ID.
    """
    logger.debug(f"Attempting to delete User with ID: {user_id}")
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        try:
            db.delete(db_user)
            db.commit()
            logger.info(f"Successfully deleted User with ID: {user_id}")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting User {user_id}: {e}", exc_info=True)
            raise # Re-raise to be handled by API endpoint
    logger.warning(f"User with ID {user_id} not found for deletion.")
    return False

def update_user_password(db: Session, user: User, hashed_password: str) -> Optional[User]:
    """
    Updates a user's password in the database.
    """
    logger.debug(f"Attempting to update password for User ID: {user.id}")
    user.hashed_password = hashed_password
    user.last_updated_at = datetime.utcnow()
    try:
        db.commit()
        db.refresh(user)
        logger.info(f"Successfully updated password for User ID: {user.id}")
        return user
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating password for User ID {user.id}: {e}", exc_info=True)
        raise # Re-raise to be handled by API endpoint