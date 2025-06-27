# /var/www/guzzyandbash_app/app/controllers/user_types.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Path for get_db: Confirmed from your user.py's import of Base
from ..database import get_db

# Models and Schemas are in app/models/user.py
from ..models.user import UserTypeOption, UserTypeOptionResponse

router = APIRouter(tags=["User Types"]) # MODIFIED: This is the ONLY place we define the tag for this router

@router.get(
    "/user-types/options",
    response_model=List[UserTypeOptionResponse],
    summary="Retrieve all available user type options",
    description="Fetches a list of all dynamically configurable user types (e.g., Artist, Artist, Musician)."
    # REMOVED: tags=["User Types"] from here, as it's defined on the router itself
)
def get_all_user_type_options(db: Session = Depends(get_db)):
    """
    Retrieve all active user type options from the database.
    """
    user_type_options = db.query(UserTypeOption).filter(UserTypeOption.is_active == True).all()
    return user_type_options