# app/controllers/user_reports.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime, date # Ensure both datetime and date are available

from app.database import get_db
from app.services import reports as reports_service
from app.models.user import User, UserRole
from app.dependencies import get_current_active_user # MODIFIED: Use get_current_active_user

# Define the APIRouter for user-specific reports
# MODIFIED: Added prefix to the router itself for cleaner URLs
router = APIRouter(prefix="/user_reports", tags=["User Reports"])

# --- User-Specific Reports (Requiring Authentication for the Current User) ---

@router.get(
    "/my-profile-summary",
    response_model=Dict[str, Any],
    summary="Get My Profile Summary (Authenticated User)",
    description="Provides a summary of the authenticated user's profile data, including content statistics, NFT count, and basic account info. Requires active user authentication.",
    tags=["User Reports"]
)
async def get_my_profile_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user) # MODIFIED: Use get_current_active_user
):
    """
    Retrieves a summary report for the currently authenticated user's profile.
    """
    # Calls the reports service function (will return dummy data initially)
    report_data = await reports_service.get_user_profile_summary_dummy(db, user_id=current_user.id) # MODIFIED: Pass current_user.id
    return report_data

@router.get(
    "/my-nft-collection",
    response_model=List[Dict[str, Any]],
    summary="Get My NFT Collection (Authenticated User)",
    description="Provides a list of NFTs owned by the authenticated user. Requires active user authentication.",
    tags=["User Reports"]
)
async def get_my_nft_collection(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user), # MODIFIED: Use get_current_active_user
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """
    Retrieves a detailed list of NFTs owned by the currently authenticated user.
    """
    # Calls the reports service function (will return dummy data initially)
    report_data = await reports_service.get_user_nft_collection_dummy(db, user_id=current_user.id, skip=skip, limit=limit) # MODIFIED: Pass current_user.id
    return report_data

@router.get(
    "/my-content",
    response_model=List[Dict[str, Any]], # Assuming a list of content items
    summary="User: Get My Content Report",
    description="Retrieves a list of content items created by the authenticated user, with optional filtering and pagination."
)
async def get_my_content_report( # Renamed from get_my_content_report to match original, but will use consistent service call
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user), # MODIFIED: Use get_current_active_user
    skip: int = Query(0, ge=0, description="Number of items to skip (for pagination)"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of items to return"),
    content_type: Optional[str] = Query(None, description="Filter by content type (e.g., 'Art', 'Music')"),
    content_status: Optional[str] = Query(None, description="Filter by content status (e.g., 'published', 'pending', 'rejected')")
):
    # Calls the reports service function (will return dummy data initially)
    report_data = await reports_service.get_user_content_dummy( # MODIFIED: Use new dummy function name
        db=db,
        user_id=current_user.id, # MODIFIED: Pass current_user.id
        skip=skip,
        limit=limit,
        content_type=content_type,
        content_status=content_status
    )
    return report_data

@router.get(
    "/my-activity-log",
    response_model=List[Dict[str, Any]],
    summary="Get My Activity Log (Authenticated User)",
    description="Provides a log of recent activities for the authenticated user (e.g., logins, purchases, content interactions). Requires active user authentication.",
    tags=["User Reports"]
)
async def get_my_activity_log(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user), # MODIFIED: Use get_current_active_user
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    activity_type: Optional[str] = Query(None, description="Filter activity by type (e.g., 'login', 'purchase', 'view')"),
    start_date: Optional[datetime] = Query(None, description="Filter activity from this date (YYYY-MM-DD)"),
    end_date: Optional[datetime] = Query(None, description="Filter activity up to this date (YYYY-MM-DD)"),
):
    """
    Retrieves a detailed log of recent activities for the currently authenticated user.
    """
    # Calls the reports service function (will return dummy data initially)
    report_data = await reports_service.get_user_activity_log_dummy(db, user_id=current_user.id, skip=skip, limit=limit, activity_type=activity_type, start_date=start_date, end_date=end_date) # MODIFIED: Pass current_user.id
    return report_data

@router.get(
    "/my-earnings",
    response_model=Dict[str, Any], # Assuming a summary of earnings
    summary="User: Get My Earnings Report",
    description="Provides a summary of earnings for the authenticated user, primarily for content creators/artists."
)
async def get_my_earnings_report( # Renamed from get_my_earnings_report to match original, but will use consistent service call
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user), # MODIFIED: Use get_current_active_user
    start_date: Optional[date] = Query(None, description="Start date for earnings calculation (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date for earnings calculation (YYYY-MM-DD)"),
    currency: Optional[str] = Query("USD", description="Currency to report earnings in (e.g., 'XRP', 'USD')")
):
    # Calls the reports service function (will return dummy data initially)
    report_data = await reports_service.get_user_earnings_dummy( # MODIFIED: Use new dummy function name
        db=db,
        user_id=current_user.id, # MODIFIED: Pass current_user.id
        start_date=start_date,
        end_date=end_date,
        currency=currency
    )
    return report_data
