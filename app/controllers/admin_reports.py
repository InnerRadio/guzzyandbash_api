# app/controllers/admin_reports.py

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_active_admin_user, get_current_active_superuser
from app.services import reports as reports_service
from app.models.user import User, UserRole # Import User and UserRole for type hinting and filtering
from app.models.content import ContentType, ContentStatus # Import for type hinting in queries

# MODIFIED: Added prefix and tags for standardization
router = APIRouter(
    prefix="/admin_reports",
    tags=["Admin Reports"]
)

# --- Admin Reports ---

@router.get(
    "/users-summary", # MODIFIED: Path is now relative to prefix
    response_model=Dict[str, Any], # Response model for the report
    summary="Get User Summary Report (Admin Only)",
    description="Provides a summary of user statistics, including total users, users by role, and new users in the last 30 days. Requires Admin or Super User role."
)
async def get_users_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin_user) # Ensures admin or superuser access
):
    """
    Retrieves a summary of user statistics from the database.
    """
    report_data = await reports_service.get_users_summary_report(db)
    return report_data

@router.get(
    "/content-summary", # MODIFIED: Path is now relative to prefix
    response_model=Dict[str, Any],
    summary="Get Content Summary Report (Admin Only)",
    description="Provides a summary of content statistics, including total content items and content by type/status. Requires Admin or Super User role."
)
async def get_content_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin_user)
):
    """
    Retrieves a summary of content statistics (currently dummy data).
    """
    report_data = await reports_service.get_content_summary_report_dummy(db)
    return report_data


@router.get(
    "/users", # MODIFIED: Path is now relative to prefix
    response_model=List[Dict[str, Any]],
    summary="Get Detailed Users Report (Admin Only)",
    description="Provides a detailed list of users with filtering and pagination. Requires Admin or Super User role."
)
async def get_detailed_users_report(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    role: Optional[UserRole] = Query(None, description="Filter users by role"),
    is_active: Optional[bool] = Query(None, description="Filter users by active status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin_user)
):
    """
    Retrieves a detailed list of users (currently dummy data).
    """
    report_data = await reports_service.get_users_report_dummy(db, skip=skip, limit=limit, role=role, is_active=is_active)
    return report_data

@router.get(
    "/content", # MODIFIED: Path is now relative to prefix
    response_model=List[Dict[str, Any]],
    summary="Get Detailed Content Report (Admin Only)",
    description="Provides a detailed list of content items with filtering and pagination. Requires Admin or Super User role."
)
async def get_detailed_content_report(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    content_type: Optional[ContentType] = Query(None, description="Filter content by type"), # Use Enum for type hinting
    status: Optional[ContentStatus] = Query(None, description="Filter content by status"), # Use Enum for type hinting
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin_user)
):
    """
    Retrieves a detailed list of content items (currently dummy data).
    """
    report_data = await reports_service.get_content_report_dummy(db, skip=skip, limit=limit, content_type=content_type, status=status)
    return report_data


# --- Superuser Reports (requiring Super_User role) ---

@router.get(
    "/superuser/reports/token-usage", # MODIFIED: Path is now relative to prefix
    response_model=Dict[str, Any],
    summary="Get Token Usage Report (Super User Only)",
    description="Provides statistics on API token usage. Requires Super User role."
)
async def get_token_usage_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    Retrieves a token usage report (currently dummy data).
    """
    report_data = await reports_service.get_token_usage_report_dummy(db)
    return report_data

@router.get(
    "/superuser/reports/nft-mint-activity", # MODIFIED: Path is now relative to prefix
    response_model=List[Dict[str, Any]],
    summary="Get NFT Mint Activity Report (Super User Only)",
    description="Provides a detailed report on NFT minting activity. Requires Super User role."
)
async def get_nft_mint_activity_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    Retrieves an NFT minting activity report (currently dummy data).
    """
    report_data = await reports_service.get_nft_mint_activity_report_dummy(db)
    return report_data

@router.get(
    "/superuser/reports/financial", # MODIFIED: Path is now relative to prefix
    response_model=Dict[str, Any],
    summary="Get Financial Report (Super User Only)",
    description="Provides an overview of financial statistics. Requires Super User role."
)
async def get_financial_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    Retrieves a financial report (currently dummy data).
    """
    report_data = await reports_service.get_financial_report_dummy(db)
    return report_data

@router.get(
    "/superuser/reports/ipfs-costs", # MODIFIED: Path is now relative to prefix
    response_model=Dict[str, Any],
    summary="Get IPFS Costs Report (Super User Only)",
    description="Provides a report on IPFS storage and retrieval costs. Requires Super User role."
)
async def get_ipfs_costs_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    Retrieves an IPFS costs report (currently dummy data).
    """
    report_data = await reports_service.get_ipfs_costs_report_dummy(db)
    return report_data

@router.get(
    "/superuser/reports/engagement", # MODIFIED: Path is now relative to prefix
    response_model=Dict[str, Any],
    summary="Get Engagement Report (Super User Only)",
    description="Provides user engagement statistics. Requires Super User role."
)
async def get_engagement_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    Retrieves an engagement report (currently dummy data).
    """
    report_data = await reports_service.get_engagement_report_dummy(db)
    return report_data

@router.get(
    "/superuser/reports/users-by-referral", # MODIFIED: Path is now relative to prefix
    response_model=List[Dict[str, Any]],
    summary="Get Users by Referral Report (Super User Only)",
    description="Provides a report on users acquired through referral programs. Requires Super User role."
)
async def get_users_by_referral_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    Retrieves a report on users by referral (currently dummy data).
    """
    report_data = await reports_service.get_users_by_referral_report_dummy(db)
    return report_data

@router.get(
    "/superuser/reports/affiliate-commissions", # MODIFIED: Path is now relative to prefix
    response_model=Dict[str, Any],
    summary="Get Affiliate Commissions Report (Super User Only)",
    description="Provides a report on affiliate commissions. Requires Super User role."
)
async def get_affiliate_commissions_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    Retrieves an affiliate commissions report (currently dummy data).
    """
    report_data = await reports_service.get_affiliate_commissions_report_dummy(db)
    return report_data

# REMOVED DUPLICATE PUBLIC REPORTS: These are now handled by app/controllers/public_reports.py
