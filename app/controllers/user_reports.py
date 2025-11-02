# app/controllers/user_reports.py

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user_id
from app.services import reports as reports_service
from app.schemas.user_reports import (
    UserProfileSummary, UserContentItem, UserNFTItem,
    UserActivityLogEntry, UserEarningsReport, UserFullProfile
)
from app.models.content import ContentType, ContentStatus
from datetime import date, datetime

router = APIRouter()

@router.get("/my-profile-summary", response_model=UserProfileSummary, summary="Get summary of current user's profile")
async def get_my_profile_summary(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Retrieves a summary of the current authenticated user's profile from the database.
    This includes basic statistics about their content, NFTs, views, and earnings.
    """
    report_data = await reports_service.get_user_profile_summary(db, user_id)
    if not report_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile summary not found."
        )
    return report_data

@router.get("/my-nft-collection", response_model=List[UserNFTItem], summary="Get NFT collection for current user")
async def get_my_nft_collection(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of NFTs to return")
):
    """
    Retrieves the NFT collection for the current authenticated user from the database.
    """
    nfts = await reports_service.get_user_nft_collection(db, user_id, skip=skip, limit=limit)
    if not nfts:
        # It's generally better to return an empty list for collections rather than 404
        return []
    return nfts

@router.get("/my-content", response_model=List[UserContentItem], summary="Get content items for current user")
async def get_my_content(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
    content_type: Optional[ContentType] = Query(None, description="Filter by content type"),
    status: Optional[ContentStatus] = Query(None, description="Filter by content status"),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of content items to return")
):
    """
    Retrieves a list of content items (blogs, projects, etc.) created by the current authenticated user from the database.
    Supports filtering by content type and status, and pagination.
    """
    content_items = await reports_service.get_user_content(
        db,
        user_id,
        content_type=content_type,
        status=status,
        skip=skip,
        limit=limit
    )
    if not content_items:
        return []
    return content_items

@router.get("/my-activity-log", response_model=List[UserActivityLogEntry], summary="Get activity log for current user")
async def get_my_activity_log(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    start_date: Optional[date] = Query(None, description="Start date for activity log filter (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date for activity log filter (YYYY-MM-DD)"),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of activity log entries to return")
):
    """
    Retrieves the recent activity log for the current authenticated user from the database.
    Supports filtering by event type and date range, and pagination.
    """
    activity_log = await reports_service.get_user_activity_log(
        db,
        user_id,
        event_type=event_type,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit
    )
    if not activity_log:
        return []
    return activity_log

@router.get("/my-earnings", response_model=UserEarningsReport, summary="Get earnings report for current user")
async def get_my_earnings(
    user_id: str = Depends(get_current_user_id),
    start_date: Optional[date] = Query(None, description="Start date for earnings report (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date for earnings report (YYYY-MM-DD)"),
    currency: str = Query("USD", description="Currency for earnings report"),
    db: Session = Depends(get_db)
):
    """
    Retrieves a summary of earnings for the current authenticated user.
    Supports filtering by date range and currency.
    NOTE: This currently returns placeholder data as dedicated database models for earnings are not yet implemented.
    """
    earnings_report = await reports_service.get_user_earnings(
        db,
        user_id,
        start_date=start_date,
        end_date=end_date,
        currency=currency
    )
    return earnings_report

@router.get("/my-full-profile", response_model=UserFullProfile, summary="Get complete profile details for current user")
async def get_my_full_profile(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Retrieves a comprehensive view of the current authenticated user's profile,
    including summary statistics, content, NFTs, and recent activity.
    """
    full_profile_data = await reports_service.get_my_full_profile(db, user_id)
    
    # Construct the full profile response using the data from the service function
    full_profile = UserFullProfile(
        profile_summary=full_profile_data.get("profile_summary"),
        nft_collection=full_profile_data.get("nft_collection"),
        content_items=full_profile_data.get("content_items"),
        activity_log=full_profile_data.get("activity_log"),
        earnings_report=full_profile_data.get("earnings_report"),
        # These fields need to be populated from the actual user object obtained from the database
        email=full_profile_data.get("profile_summary", {}).get("email"),
        username=full_profile_data.get("profile_summary", {}).get("username"),
        role=full_profile_data.get("profile_summary", {}).get("role"),
        is_active=full_profile_data.get("profile_summary", {}).get("is_active"),
        is_verified=full_profile_data.get("profile_summary", {}).get("is_verified"),
        profile_picture_url=full_profile_data.get("profile_summary", {}).get("profile_picture_url"),
        social_links=full_profile_data.get("profile_summary", {}).get("social_links"),
        has_api_access=full_profile_data.get("profile_summary", {}).get("has_api_access"),
        referral_code=full_profile_data.get("profile_summary", {}).get("referral_code"),
        referred_by_user_id=full_profile_data.get("profile_summary", {}).get("referred_by_user_id"),
        referred_by_referral_code=full_profile_data.get("profile_summary", {}).get("referred_by_referral_code")
    )
    return full_profile