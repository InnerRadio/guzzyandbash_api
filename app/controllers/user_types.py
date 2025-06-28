# app/controllers/user_types.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import UserTypeOption, User # User model is still here for dependencies
from app.crud import user_types as crud_user_types
from app.dependencies import get_current_active_user, get_current_active_superuser

# NEW: Import UserTypeOptionResponse, UserTypeOptionCreate, UserTypeOptionUpdate from app.schemas.user_schemas
from app.schemas.user_schemas import UserTypeOptionResponse, UserTypeOptionCreate, UserTypeOptionUpdate

# Corrected APIRouter definition with prefix
router = APIRouter(prefix="/user_types", tags=["User Types"])

# --- User Type Options CRUD Operations ---

@router.post(
    "/", # Adjusted endpoint path to match router prefix
    response_model=UserTypeOptionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new User Type Option (Superuser only)",
    response_description="The newly created User Type Option."
)
async def create_user_type_option(
    user_type: UserTypeOptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser) # Only superusers can create
):
    """
    Creates a new user type option in the database.
    Requires Superuser privileges.
    """
    # Use crud operations
    db_user_type = crud_user_types.get_user_type_option_by_name(db, name=user_type.name)
    if db_user_type:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Type Option with this name already exists")
    return crud_user_types.create_user_type_option(db=db, user_type=user_type)

@router.get(
    "/", # Adjusted endpoint path to match router prefix
    response_model=List[UserTypeOptionResponse],
    summary="Get all User Type Options",
    response_description="A list of all User Type Options."
)
async def get_all_user_type_options(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieves a list of all user type options available in the database.
    Requires authentication.
    """
    return crud_user_types.get_all_user_type_options(db)

@router.get(
    "/{user_type_id}",
    response_model=UserTypeOptionResponse,
    summary="Get User Type Option by ID",
    response_description="Details of a specific User Type Option."
)
async def get_user_type_option(
    user_type_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieves a specific user type option by its ID.
    Requires authentication.
    """
    db_user_type = crud_user_types.get_user_type_option_by_id(db, user_type_id=user_type_id)
    if not db_user_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Type Option not found")
    return db_user_type

@router.put(
    "/{user_type_id}",
    response_model=UserTypeOptionResponse,
    summary="Update a User Type Option by ID (Superuser only)",
    response_description="The updated User Type Option."
)
async def update_user_type_option(
    user_type_id: str,
    user_type_update: UserTypeOptionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser) # Only superusers can update
):
    """
    Updates an existing user type option by its ID.
    Requires Superuser privileges.
    """
    db_user_type = crud_user_types.get_user_type_option_by_id(db, user_type_id=user_type_id)
    if not db_user_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Type Option not found")
    return crud_user_types.update_user_type_option(db=db, user_type_id=user_type_id, user_type_update=user_type_update)

@router.delete(
    "/{user_type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a User Type Option by ID (Superuser only)",
    response_description="No content upon successful deletion."
)
async def delete_user_type_option(
    user_type_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser) # Only superusers can delete
):
    """
    Deletes a user type option by its ID.
    Requires Superuser privileges.
    """
    success = crud_user_types.delete_user_type_option(db, user_type_id=user_type_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Type Option not found")
    return
