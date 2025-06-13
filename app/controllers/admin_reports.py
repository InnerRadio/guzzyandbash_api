# /var/www/tarot-api/guzzy_and_bash_productions/app/controllers/admin_reports.py

from fastapi import APIRouter, Depends, HTTPException, status, Query # Added Query for pagination/filtering
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional # Added Optional
from datetime import datetime, date # Added date for date filtering

from app.database import get_db
from app.services import reports as reports_service
from app.models.user import User # Import User model for potential type hints in responses

# Placeholder for a simple admin dependency for now.
def get_current_admin_user():
    # In a real application, this would verify the user's admin role from their token.
    # For testing, we'll temporarily allow access.
    return True # Temporarily allow access for testing purposes

router = APIRouter(tags=["Admin Reports"])

# Existing Endpoints:
@router.get(
    "/admin/reports/users-summary",
    response_model=Dict[str, Any], # Adjust response model as needed
    summary="Admin: Get Users Summary Report",
    description="Provides a basic summary of user statistics for administrative oversight."
)
def get_users_summary(
    db: Session = Depends(get_db),
    current_admin_user: bool = Depends(get_current_admin_user)
):
    if not current_admin_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access admin reports"
        )
    return reports_service.get_users_summary_report(db)

@router.get(
    "/admin/reports/content-summary",
    response_model=Dict[str, Any], # Adjust response model as needed
    summary="Admin: Get Content Summary Report",
    description="Provides a basic summary of content statistics for administrative oversight."
)
def get_content_summary(
    db: Session = Depends(get_db),
    current_admin_user: bool = Depends(get_current_admin_user)
):
    if not current_admin_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access admin reports"
        )
    return reports_service.get_content_summary_report(db)

# NEW ENDPOINT: Admin Get Users List Report
@router.get(
    "/admin/reports/users",
    response_model=List[Dict[str, Any]], # Adjust response model as needed for user data
    summary="Admin: Get Detailed Users Report",
    description="Retrieves a detailed list of users, with optional filtering and pagination. This report is for administrative use only."
)
def get_admin_users_report(
    db: Session = Depends(get_db),
    current_admin_user: bool = Depends(get_current_admin_user),
    skip: int = Query(0, ge=0, description="Number of items to skip (for pagination)"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of items to return"),
    user_role: Optional[str] = Query(None, description="Filter by user role (e.g., 'ADMIN', 'CONSUMER', 'ARTIST')"),
    is_active: Optional[bool] = Query(None, description="Filter by user active status"),
    start_date: Optional[date] = Query(None, description="Filter users registered on or after this date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Filter users registered on or before this date (YYYY-MM-DD)")
):
    if not current_admin_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access admin reports"
        )
    return reports_service.get_admin_users_report(
        db=db,
        skip=skip,
        limit=limit,
        user_role=user_role,
        is_active=is_active,
        start_date=start_date,
        end_date=end_date
    )

# NEW ENDPOINT: Admin Get Content List Report
@router.get(
    "/admin/reports/content",
    response_model=List[Dict[str, Any]], # Adjust response model as needed for content data
    summary="Admin: Get Detailed Content Report",
    description="Retrieves a detailed list of content items, with optional filtering and pagination. This report is for administrative use only."
)
def get_admin_content_report(
    db: Session = Depends(get_db),
    current_admin_user: bool = Depends(get_current_admin_user),
    skip: int = Query(0, ge=0, description="Number of items to skip (for pagination)"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of items to return"),
    content_type: Optional[str] = Query(None, description="Filter by content type (e.g., 'Art', 'Music')"),
    content_status: Optional[str] = Query(None, description="Filter by content status (e.g., 'published', 'pending', 'rejected')"),
    creator_id: Optional[int] = Query(None, description="Filter by content creator's user ID"),
    min_views: Optional[int] = Query(None, ge=0, description="Filter by minimum number of views"),
    min_sales: Optional[float] = Query(None, ge=0, description="Filter by minimum sales amount")
):
    if not current_admin_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access admin reports"
        )
    return reports_service.get_admin_content_report(
        db=db,
        skip=skip,
        limit=limit,
        content_type=content_type,
        content_status=content_status,
        creator_id=creator_id,
        min_views=min_views,
        min_sales=min_sales
    )