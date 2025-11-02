# app/services/reports.py

import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from typing import List, Dict, Any, Optional
from datetime import date, datetime, timedelta, timezone # Added timezone import
import logging

from app.models.content import Content, ContentType, ContentStatus
from app.models.user import User
# CORRECTED: Import NFT instead of MintedMemorialEntry
from app.models.nft import NFT
# CORRECTED: Adjust get_nfts_by_minter_user to align with new model name if necessary,
# or assume it's fetching the new NFT objects.
from app.services.nft_service import get_nfts_by_minter_user
from app.models.activity_log import ActivityLog

logger = logging.getLogger(__name__)

async def get_user_profile_summary(db: Session, user_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves a user profile summary for the specified user from the database.
    Returns None if the user is not found.
    """
    logger.info(f"Reports Service: Retrieving profile summary for user_id: {user_id} from database.")

    # Fetch user details
    user = db.scalar(select(User).filter(User.id == user_id))

    if not user:
        logger.warning(f"Reports Service: User with ID {user_id} not found for profile summary.")
        return None # Return None if user not found, controller will handle 404

    # Get total content created
    total_content_created = db.scalar(
        select(func.count(Content.id)).filter(Content.owner_user_id == user_id)
    )

    # Prepare profile summary
    profile_summary = {
        "user_id": user.id,
        "email": user.email,
        "username": user.username,
        "role": user.role.value,
        "is_active": user.is_active,
        "is_verified": user.is_verified,
        "profile_picture_url": user.profile_picture_url,
        "social_links": user.social_links,
        "has_api_access": user.has_api_access,
        "referral_code": user.referral_code,
        "referred_by_user_id": user.referred_by_user_id,
        "referred_by_referral_code": user.referred_by_referral_code,
        "created_at": user.created_at.isoformat(),
        "last_updated_at": user.last_updated_at.isoformat(),
        # Initialize with default values
        "nft_collection": [],
        "content_items": [],
        "activity_log": [],
        "earnings_report": {
            "report_name": "User Earnings Report",
            "date_generated": datetime.now(),
            "total_content_sales_value": 0.0,
            "total_commissions_received": 0.0,
            "currency": "USD",
            "earnings_breakdown": []
        }
    }

    # Fetch NFT collection, recent content, and activity log
    # CORRECTED: get_user_nft_collection should now fetch NFT objects
    nft_collection = await get_user_nft_collection(db, user_id, skip=0, limit=100)
    recent_content = await get_user_content(db, user_id, limit=3)
    recent_activity_log = await get_user_activity_log(db, user_id, limit=3)
    earnings_report = await get_user_earnings(db, user_id) # Using the production-ready earnings function

    profile_summary["nft_collection"] = [
        {
            "id": nft.id,
            "token_id": nft.token_id,
            "name": nft.name,
            "image_url": nft.image_url,
            "minted_at": nft.minted_at.isoformat()
        } for nft in nft_collection
    ]
    profile_summary["content_items"] = [
        {
            "id": content.id,
            "title": content.title,
            "content_type": content.content_type.value,
            "created_at": content.created_at.isoformat()
        } for content in recent_content
    ]
    profile_summary["activity_log"] = [
        {
            "id": log.id,
            "action": log.action,
            "timestamp": log.timestamp.isoformat()
        } for log in recent_activity_log
    ]
    profile_summary["earnings_report"] = earnings_report # Assign the full report

    return profile_summary

async def get_user_content(db: Session, user_id: str, limit: int = 5) -> List[Content]:
    """
    Retrieves recent content items created by the user.
    """
    logger.info(f"Reports Service: Retrieving recent content for user_id: {user_id}")
    return db.scalars(
        select(Content)
        .filter(Content.owner_user_id == user_id)
        .order_by(Content.created_at.desc())
        .limit(limit)
    ).all()

async def get_user_nft_collection(db: Session, user_id: str, skip: int = 0, limit: int = 10) -> List[NFT]:
    """
    Retrieves the NFT collection for a given user.
    """
    logger.info(f"Reports Service: Retrieving NFT collection for user_id: {user_id}")
    # CORRECTED: Use NFT model directly
    return db.scalars(
        select(NFT)
        .filter(NFT.owner_id == user_id)
        .offset(skip)
        .limit(limit)
    ).all()


async def get_user_activity_log(db: Session, user_id: str, limit: int = 5) -> List[ActivityLog]:
    """
    Retrieves recent activity logs for a given user.
    """
    logger.info(f"Reports Service: Retrieving recent activity log for user_id: {user_id}")
    return db.scalars(
        select(ActivityLog)
        .filter(ActivityLog.user_id == user_id)
        .order_by(ActivityLog.timestamp.desc())
        .limit(limit)
    ).all()

async def get_user_earnings(db: Session, user_id: str) -> Dict[str, Any]:
    """
    Calculates the total earnings for a user from content sales and commissions.
    This is a more production-ready example that aggregates data.
    """
    logger.info(f"Reports Service: Calculating earnings for user_id: {user_id}")

    # Total sales from content owned by the user
    total_content_sales = db.scalar(
        select(func.sum(Content.sales))
        .filter(Content.owner_user_id == user_id)
    ) or 0.0

    # Total commissions received (if your User model or another model tracks this)
    # For now, let's assume a placeholder or a simple calculation
    # In a real system, you'd likely have a 'commissions' table or similar.
    # To properly get 'user' object if it's not passed, you might need:
    user_instance = db.scalar(select(User).filter(User.id == user_id))
    total_commissions_received = user_instance.total_commissions_earned if user_instance and hasattr(user_instance, 'total_commissions_earned') else 0.0


    earnings_breakdown = [
        {"source": "Content Sales", "amount": total_content_sales, "currency": "USD"},
        {"source": "Referral Commissions", "amount": total_commissions_received, "currency": "USD"}
    ]

    report = {
        "report_name": "User Earnings Report",
        "date_generated": datetime.now(),
        "total_content_sales_value": total_content_sales,
        "total_commissions_received": total_commissions_received,
        "currency": "USD",
        "earnings_breakdown": earnings_breakdown
    }
    return report

async def get_users_summary_report(db: Session) -> Dict[str, Any]:
    """
    Generates a summary report of all users, including total counts,
    users by role, and new users in the last 30 days.
    """
    logger.info("Reports Service: Generating users summary report.")

    total_users = db.scalar(select(func.count(User.id)))
    active_users = db.scalar(select(func.count(User.id)).filter(User.is_active == True))
    verified_users = db.scalar(select(func.count(User.id)).filter(User.is_verified == True))

    users_by_role = db.execute(
        select(User.role, func.count(User.id))
        .group_by(User.role)
    ).all()
    users_by_role_dict = {role.value: count for role, count in users_by_role}

    thirty_days_ago = datetime.now() - timedelta(days=30)
    new_users_last_30_days = db.scalar(
        select(func.count(User.id))
        .filter(User.created_at >= thirty_days_ago)
    )

    # Basic API Usage (dummy data)
    total_requests = 100000
    authenticated_requests = 75000
    unauthenticated_requests = 25000

    return {
        "total_users": total_users,
        "active_users": active_users,
        "verified_users": verified_users,
        "users_by_role": users_by_role_dict,
        "new_users_last_30_days": new_users_last_30_days,
        "api_usage_summary": {
            "total_requests": total_requests,
            "authenticated_requests": authenticated_requests,
            "unauthenticated_requests": unauthenticated_requests
        },
        "report_generated_at": datetime.now().isoformat()
    }

# 👇 NEW CODE ADDED HERE 👇
async def get_users_report(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    role: Optional[str] = None,
    is_active: Optional[bool] = None
) -> List[Dict[str, Any]]:
    """
    Retrieves a detailed list of users, with optional filtering by role and active status.
    """
    logger.info(f"Reports Service: Retrieving detailed users report with filters: role={role}, is_active={is_active}, skip={skip}, limit={limit}")

    query = select(User)

    if role:
        # Assuming User.role is an Enum or comparable string value
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    users = db.scalars(
        query.offset(skip).limit(limit)
    ).all()

    # Format the user data for the report
    detailed_users_data = []
    for user in users:
        detailed_users_data.append({
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role.value,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "created_at": user.created_at.isoformat(),
            "last_updated_at": user.last_updated_at.isoformat(),
            # Add any other user fields you want in the detailed report
        })
    return detailed_users_data
# 👆 NEW CODE ADDED HERE 👆

# --- NEWLY ADDED CODE TO PREVENT API CRASH ---
async def get_content_summary_report(db: Session) -> Dict[str, Any]:
    """
    Placeholder for fetching a summary of content data.
    You will need to implement the actual logic here to query your
    content-related models (e.g., Content, Post, Article, etc.)
    For now, it returns dummy data to prevent API crash.

    Example if you have a Content model (uncomment and adapt 'Content' as needed):
    # from app.models.content import Content
    # total_content = await db.scalar(select(func.count(Content.id)))
    # published_content = await db.scalar(select(func.count(Content.id)).where(Content.status == ContentStatus.PUBLISHED))
    # drafts = await db.scalar(select(func.count(Content.id)).where(Content.status == ContentStatus.DRAFT))
    """
    logger.info("Reports Service: Generating content summary report (placeholder).")
    return {
        "status": "success",
        "message": "Content summary report placeholder executed. Implement actual logic for content models here.",
        "total_content_items": 0,  # Replace with actual count
        "published_items": 0,      # Replace with actual count
        "draft_items": 0,          # Replace with actual count
        "last_updated_at": datetime.now(timezone.utc).isoformat() # Placeholder for timestamp
    }


async def get_nft_minting_report_dummy(db: Session) -> Dict[str, Any]:
    """
    Generates a dummy NFT minting report.
    """
    logger.info("Reports Service: Generating dummy NFT minting report.")
    today = date.today()
    return [{
        "report_name": "NFT Minting Activity Report",
        "date_generated": datetime.now(),
        "period_start": today - timedelta(days=30),
        "period_end": today,
        "total_mints_period": 500,
        "successful_mints_period": 480,
        "failed_mints_period": 20,
        "top_minters_period": [
            {"user_id": str(uuid.uuid4()), "mints": 50},
            {"user_id": str(uuid.uuid4()), "mints": 45}
        ],
        "average_mint_time_seconds": 15.5
    }]

async def get_financial_overview_report_dummy(db: Session) -> Dict[str, Any]:
    """
    Generates a dummy financial overview report.
    """
    logger.info("Reports Service: Generating dummy financial overview report.")
    return {
        "report_name": "Financial Overview Report",
        "date_generated": datetime.now(),
        "total_revenue": 15000.00,
        "total_expenses": 7500.00,
        "net_profit": 7500.00,
        "currency": "USD",
        "period": "Last Quarter"
    }

async def get_ipfs_cost_report_dummy(db: Session) -> Dict[str, Any]:
    """
    Generates a dummy IPFS cost report.
    """
    logger.info("Reports Service: Generating dummy IPFS cost report.")
    return {
        "report_name": "IPFS Storage & Retrieval Cost Report",
        "date_generated": datetime.now(),
        "month": "July",
        "storage_cost_usd": 150.75,
        "retrieval_cost_usd": 80.20,
        "total_cost_usd": 230.95
    }

async def get_user_engagement_report_dummy(db: Session) -> Dict[str, Any]:
    """
    Generates a dummy user engagement report.
    """
    logger.info("Reports Service: Generating dummy user engagement report.")
    return {
        "report_name": "User Engagement Report",
        "date_generated": datetime.now(),
        "active_users_daily": 1200,
        "content_views_daily": 5000,
        "average_session_duration_minutes": 10.5,
        "new_registrations_daily": 50
    }

async def get_users_by_referral_report_dummy(db: Session) -> List[Dict[str, Any]]:
    """
    Generates a dummy report on users acquired through referral programs.
    """
    logger.info("Reports Service: Generating dummy users by referral report.")
    return [
        {"referral_code": "ALPHA-123", "referred_users_count": 25, "total_commissions_usd": 125.50},
        {"referral_code": "BETA-456", "referred_users_count": 18, "total_commissions_usd": 90.00},
        {"referral_code": "GAMMA-789", "referred_users_count": 10, "total_commissions_usd": 50.00},
    ]

async def get_affiliate_commissions_report_dummy(db: Session) -> Dict[str, Any]:
    """
    Generates a dummy affiliate commissions report.
    """
    logger.info("Reports Service: Generating dummy affiliate commissions report.")
    return {
        "report_name": "Affiliate Commissions Overview",
        "date_generated": datetime.now(),
        "total_commissions_paid_usd": 2500.00,
        "total_affiliates_active": 50,
        "top_affiliates": [
            {"user_id": str(uuid.uuid4()), "commissions_usd": 500.00},
            {"user_id": str(uuid.uuid4()), "commissions_usd": 350.00}
        ]
    }