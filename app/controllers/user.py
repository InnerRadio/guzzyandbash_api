from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Assuming standard imports for dependencies, models, and services based on project structure
from ..dependencies import get_db, get_current_active_user
from app.schemas.user_schemas import UserResponse as UserSchema
# from ..schemas.affiliate_reports import AffiliateSummary 
from ..services import user as user_service
from ..services import affiliate_reports as affiliate_reports_service 

router = APIRouter()

# --- GET /api/auth/users/me (Enhanced with Affiliate Logic) ---

@router.get("/users/me", response_model=UserSchema)
async def read_users_me(
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retrieves the profile information of the currently authenticated user, 
    enhanced to include Affiliate Program data (summary, referrals, earnings).
    """
    
    # Convert Pydantic model to dict for modification
    user_data = current_user.dict()
    
    # The affiliate_id is assumed to be a field on the core User model/schema
    affiliate_id = user_data.get("affiliate_id")
    
    # Check if the user has an affiliate ID to trigger fetching performance data
    if affiliate_id:
        try:
            # 1. Fetch affiliate summary metrics using the service
            affiliate_summary_data = affiliate_reports_service.get_affiliate_summary_report(
                db=db, 
                affiliate_id=affiliate_id
            )
            
            # 2. Augment the user data structure with the affiliate metrics
            user_data["affiliate_summary"] = affiliate_summary_data 
            user_data["is_affiliate"] = True
            
        except Exception as e:
            # IMPORTANT: If the service call fails, we log it and return basic user data, 
            print(f"Error fetching affiliate data for user {current_user.id}: {e}")
            user_data["affiliate_summary"] = {}
            user_data["is_affiliate"] = False
            
    else:
        # If no affiliate_id exists on the user model, assume they are not an affiliate
        user_data["affiliate_summary"] = {}
        user_data["is_affiliate"] = False

    return user_data

# --- GET /api/auth/users/{user_id} (Standard Logic) ---

@router.get("/users/{user_id}", response_model=UserSchema, status_code=status.HTTP_200_OK)
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the profile information for a specific user by their ID.
    """
    db_user = user_service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user
