# app/crud/user_types.py

from sqlalchemy.orm import Session
from sqlalchemy import select, delete, update

# Import the SQLAlchemy model from app.models.user
from app.models.user import UserTypeOption
# Import the Pydantic schemas from app.schemas.user_schemas
from app.schemas.user_schemas import UserTypeOptionCreate, UserTypeOptionUpdate


def get_user_type_option_by_name(db: Session, name: str):
    """
    Retrieves a UserTypeOption by its name.
    """
    return db.query(UserTypeOption).filter(UserTypeOption.name == name).first()

def get_user_type_option_by_id(db: Session, user_type_id: str):
    """
    Retrieves a UserTypeOption by its ID.
    """
    return db.query(UserTypeOption).filter(UserTypeOption.id == user_type_id).first()

def get_all_user_type_options(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieves all UserTypeOptions.
    """
    return db.query(UserTypeOption).offset(skip).limit(limit).all()

def create_user_type_option(db: Session, user_type: UserTypeOptionCreate):
    """
    Creates a new UserTypeOption in the database.
    """
    db_user_type = UserTypeOption(
        name=user_type.name,
        description=user_type.description,
        is_active=user_type.is_active
    )
    db.add(db_user_type)
    db.commit()
    db.refresh(db_user_type)
    return db_user_type

def update_user_type_option(db: Session, user_type_id: str, user_type_update: UserTypeOptionUpdate):
    """
    Updates an existing UserTypeOption.
    """
    db_user_type = db.query(UserTypeOption).filter(UserTypeOption.id == user_type_id).first()
    if db_user_type:
        update_data = user_type_update.model_dump(exclude_unset=True) # Use model_dump for Pydantic v2
        for key, value in update_data.items():
            setattr(db_user_type, key, value)
        db.add(db_user_type)
        db.commit()
        db.refresh(db_user_type)
    return db_user_type

def delete_user_type_option(db: Session, user_type_id: str):
    """
    Deletes a UserTypeOption by its ID.
    """
    db_user_type = db.query(UserTypeOption).filter(UserTypeOption.id == user_type_id).first()
    if db_user_type:
        db.delete(db_user_type)
        db.commit()
        return True
    return False
