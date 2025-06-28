# app/services/reports.py

from sqlalchemy.orm import Session
from sqlalchemy import func, select
from datetime import datetime, timedelta, date # NEW: Import date for specific type hinting
import random
from typing import Dict, Any, List, Optional
import logging
import uuid # Import uuid for dummy IDs

# Import your database models
from app.models.user import User, UserRole
from app.models.content import Content, ContentType, ContentStatus
from app.models.nft import MintedMemorialEntry
from app.models.affiliate import Affiliate
from app.models.referral import Referral

logger = logging.getLogger(__name__)

# --- Admin Reports ---

async def get_users_summary_report(db: Session) -> Dict[str, Any]: # RENAMED from _dummy, now uses DB
    """
    Retrieves a summary of user statistics from the database.
    """
    logger.info("Reports Service: Generating users summary report from database.")

    # Total users
    total_users = db.query(User).count()

    # Users by role
    users_by_role_query = db.query(User.role, func.count(User.id)).group_by(User.role).all()
    users_by_role = {role.value: count for role, count in users_by_role_query} # Convert enum to string

    # New users in last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    new_users_last_30_days = db.query(User).filter(User.created_at >= thirty_days_ago).count()

    return {
        "report_name": "User Summary Report",
        "date_generated": datetime.utcnow().isoformat(),
        "total_users": total_users,
        "users_by_role": users_by_role,
        "new_users_last_30_days": new_users_last_30_days
    }


async def get_content_summary_report_dummy(db: Session) -> Dict[str, Any]:
    """
    Placeholder: Generates a dummy content summary report.
    """
    logger.info("Reports Service: Generating dummy content summary report.")
    return {
        "report_name": "Content Summary Report",
        "date_generated": datetime.utcnow().isoformat(),
        "total_content_items": random.randint(10, 50),
        "content_by_type": {
            "Art": random.randint(5, 20),
            "Music": random.randint(3, 10),
            "Writing": random.randint(2, 8),
            "Photography": random.randint(1, 5),
            "Video": random.randint(1, 5)
        },
        "content_by_status": {
            "published": random.randint(8, 40),
            "pending": random.randint(1, 5),
            "draft": random.randint(1, 3)
        }
    }


async def get_users_report_dummy(db: Session, skip: int = 0, limit: int = 100, role: Optional[UserRole] = None, is_active: Optional[bool] = None) -> List[Dict[str, Any]]:
    """
    Placeholder: Generates a list of dummy user data.
    """
    logger.info(f"Reports Service: Generating dummy users report with skip={skip}, limit={limit}, role={role}, is_active={is_active}.")
    dummy_users = [
        {"id": "1", "username": "admin_user", "email": "admin@example.com", "role": UserRole.ADMIN.value, "is_active": True, "created_at": (datetime.utcnow() - timedelta(days=random.randint(100, 365))).isoformat()},
        {"id": "2", "username": "artist_one", "email": "artist1@example.com", "role": UserRole.ARTIST.value, "is_active": True, "created_at": (datetime.utcnow() - timedelta(days=random.randint(50, 200))).isoformat()},
        {"id": "3", "username": "consumer_a", "email": "consumer_a@example.com", "role": UserRole.CONSUMER.value, "is_active": True, "created_at": (datetime.utcnow() - timedelta(days=random.randint(10, 60))).isoformat()},
        {"id": "4", "username": "moderator_alpha", "email": "mod@example.com", "role": UserRole.MODERATOR.value, "is_active": True, "created_at": (datetime.utcnow() - timedelta(days=random.randint(80, 250))).isoformat()},
        {"id": "5", "username": "inactive_user", "email": "inactive@example.com", "role": UserRole.CONSUMER.value, "is_active": False, "created_at": (datetime.utcnow() - timedelta(days=random.randint(30, 100))).isoformat()},
        {"id": "6", "username": "new_artist", "email": "new_art@example.com", "role": UserRole.ARTIST.value, "is_active": True, "created_at": (datetime.utcnow() - timedelta(days=random.randint(1, 7))).isoformat()},
        {"id": "7", "username": "new_consumer", "email": "new_con@example.com", "role": UserRole.CONSUMER.value, "is_active": True, "created_at": (datetime.utcnow() - timedelta(hours=random.randint(1, 24))).isoformat()},
        {"id": "8", "username": "referred_user_b", "email": "refb@example.com", "role": UserRole.CONSUMER.value, "is_active": True, "created_at": (datetime.utcnow() - timedelta(days=random.randint(10, 40))).isoformat()},
        {"id": "9", "username": "referred_user_c", "email": "refc@example.com", "role": UserRole.CONSUMER.value, "is_active": True, "created_at": (datetime.utcnow() - timedelta(days=random.randint(20, 50))).isoformat()},
        {"id": "10", "username": "independent_user", "email": "independent@example.com", "role": UserRole.CONSUMER.value, "is_active": True, "created_at": (datetime.utcnow() - timedelta(days=random.randint(40, 120))).isoformat()},
        {"id": "100", "username": "new_unique_username", "email": "new_unique_email@example.com", "role": UserRole.REGISTERED_USER.value, "is_active": True, "created_at": (datetime.utcnow() - timedelta(days=random.randint(1, 30))).isoformat()},
    ]

    filtered_users = []
    for user in dummy_users:
        match = True
        if role and user["role"] != role.value:
            match = False
        if is_active is not None and user["is_active"] != is_active:
            match = False
        if match:
            filtered_users.append(user)

    return filtered_users[skip:skip+limit]


async def get_content_report_dummy(db: Session, skip: int = 0, limit: int = 100, content_type: Optional[ContentType] = None, status: Optional[ContentStatus] = None) -> List[Dict[str, Any]]:
    """
    Placeholder: Generates a list of dummy content data.
    """
    logger.info(f"Reports Service: Generating dummy content report with skip={skip}, limit={limit}, type={content_type}, status={status}.")
    dummy_content = [
        {"id": 1, "type": ContentType.ART.value, "status": ContentStatus.PUBLISHED.value, "views": 1500, "sales": 150.00, "created_at": (datetime.utcnow() - timedelta(days=random.randint(5, 20))).isoformat(), "creator_username": "artist_one"},
        {"id": 2, "type": ContentType.MUSIC.value, "status": ContentType.PUBLISHED.value, "views": 2500, "sales": 250.00, "created_at": (datetime.utcnow() - timedelta(days=random.randint(2, 10))).isoformat(), "creator_username": "artist_one"},
        {"id": 3, "type": ContentType.WRITING.value, "status": ContentType.PUBLISHED.value, "views": 800, "sales": 80.00, "created_at": (datetime.utcnow() - timedelta(days=random.randint(10, 30))).isoformat(), "creator_username": "new_unique_username"},
        {"id": 4, "type": ContentType.ART.value, "status": ContentType.PENDING.value, "views": 50, "sales": 0.00, "created_at": (datetime.utcnow() - timedelta(days=random.randint(1, 3))).isoformat(), "creator_username": "new_artist"},
        {"id": 5, "type": ContentType.MUSIC.value, "status": ContentType.PUBLISHED.value, "views": 1200, "sales": 120.00, "created_at": (datetime.utcnow() - timedelta(hours=random.randint(1, 24))).isoformat(), "creator_username": "artist_one"},
        {"id": 6, "type": ContentType.WRITING.value, "status": ContentType.DRAFT.value, "views": 100, "sales": 0.00, "created_at": (datetime.utcnow() - timedelta(days=random.randint(7, 14))).isoformat(), "creator_username": "new_unique_username"},
        {"id": 7, "type": ContentType.ART.value, "status": ContentType.PUBLISHED.value, "views": 3000, "sales": 300.00, "created_at": (datetime.utcnow() - timedelta(hours=random.randint(12, 48))).isoformat(), "creator_username": "artist_one"},
        {"id": 8, "type": ContentType.MUSIC.value, "status": ContentType.PUBLISHED.value, "views": 4000, "sales": 400.00, "created_at": (datetime.utcnow() - timedelta(days=random.randint(3, 8))).isoformat(), "creator_username": "new_artist"},
        {"id": 9, "type": ContentType.ART.value, "status": ContentType.PUBLISHED.value, "views": 2000, "sales": 200.00, "created_at": (datetime.utcnow() - timedelta(hours=random.randint(6, 18))).isoformat(), "creator_username": "new_unique_username"},
        {"id": 10, "type": ContentType.WRITING.value, "status": ContentType.PUBLISHED.value, "views": 1000, "sales": 100.00, "created_at": (datetime.utcnow() - timedelta(days=random.randint(20, 40))).isoformat(), "creator_username": "independent_user"},
        {"id": 11, "type": ContentType.PHOTOGRAPHY.value, "status": ContentType.PUBLISHED.value, "views": 900, "sales": 90.00, "created_at": (datetime.utcnow() - timedelta(hours=random.randint(2, 10))).isoformat(), "creator_username": "new_artist"},
        {"id": 12, "type": ContentType.VIDEO.value, "status": ContentType.PUBLISHED.value, "views": 5000, "sales": 500.00, "created_at": (datetime.utcnow() - timedelta(hours=random.randint(1, 5))).isoformat(), "creator_username": "artist_one"},
        {"id": 13, "type": ContentType.ART.value, "status": ContentType.PUBLISHED.value, "views": 1800, "sales": 180.00, "created_at": (datetime.utcnow() - timedelta(hours=random.randint(10, 30))).isoformat(), "creator_username": "new_unique_username"},
    ]

    filtered_content = []
    for item in dummy_content:
        match = True
        if content_type and item["type"] != content_type.value:
            match = False
        if status and item["status"] != status.value:
            match = False
        if match:
            filtered_content.append(item)

    return filtered_content[skip:skip+limit]

# --- User-Specific Reports (Dummy Data) ---

async def get_user_profile_summary_dummy(db: Session, user_id: str) -> Dict[str, Any]:
    """
    Placeholder: Generates a dummy summary of a user's profile.
    """
    logger.info(f"Reports Service: Generating dummy user profile summary for user_id: {user_id}.")
    return {
        "report_name": f"User Profile Summary for {user_id}",
        "date_generated": datetime.utcnow().isoformat(),
        "total_content_created": random.randint(5, 20),
        "total_nfts_owned": random.randint(1, 10),
        "total_views_on_content": random.randint(1000, 10000),
        "total_earnings_usd": round(random.uniform(50.00, 500.00), 2),
        "last_login": (datetime.utcnow() - timedelta(hours=random.randint(1, 24))).isoformat(),
    }

async def get_user_nft_collection_dummy(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    """
    Placeholder: Generates a list of dummy NFT data for a specific user.
    """
    logger.info(f"Reports Service: Generating dummy NFT collection for user_id: {user_id}, skip={skip}, limit={limit}.")
    dummy_nfts = []
    for i in range(random.randint(1, 10)):
        dummy_nfts.append({
            "nft_id": str(uuid.uuid4()),
            "title": f"Dummy NFT {i+1} by {user_id}",
            "token_id": f"dummy_token_{random.randint(1000, 9999)}",
            "mint_date": (datetime.utcnow() - timedelta(days=random.randint(1, 365))).isoformat(),
            "price_usd": round(random.uniform(10.00, 1000.00), 2),
            "is_listed_for_sale": random.choice([True, False]),
        })
    return dummy_nfts[skip:skip+limit]

async def get_user_content_dummy(db: Session, user_id: str, skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Placeholder: Generates a list of dummy content items created by a specific user.
    """
    logger.info(f"Reports Service: Generating dummy user content for user_id: {user_id}, skip={skip}, limit={limit}, status={status}.")
    dummy_user_content = []
    content_statuses = ["published", "draft", "pending", "rejected"]
    for i in range(random.randint(3, 15)):
        item_status = random.choice(content_statuses)
        if status is None or item_status == status:
            dummy_user_content.append({
                "content_id": str(uuid.uuid4()),
                "title": f"Dummy Content {i+1} by {user_id}",
                "content_type": random.choice(["Art", "Music", "Writing", "Video"]),
                "status": item_status,
                "views": random.randint(100, 5000),
                "created_at": (datetime.utcnow() - timedelta(days=random.randint(10, 180))).isoformat(),
                "last_updated": datetime.utcnow().isoformat(),
            })
    return dummy_user_content[skip:skip+limit]

async def get_user_activity_log_dummy(db: Session, user_id: str, skip: int = 0, limit: int = 100, activity_type: Optional[str] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
    """
    Placeholder: Generates a list of dummy activity log entries for a specific user.
    """
    logger.info(f"Reports Service: Generating dummy user activity log for user_id: {user_id}, type={activity_type}, start_date={start_date}, end_date={end_date}.")
    dummy_activity_log = []
    activity_types = ["login", "purchase", "view_nft", "create_content", "comment", "like"]
    for i in range(random.randint(10, 50)):
        activity_time = datetime.utcnow() - timedelta(days=random.randint(0, 90), hours=random.randint(0, 23))
        event_type = random.choice(activity_types)
        
        if (activity_type is None or event_type == activity_type) and \
           (start_date is None or activity_time >= start_date) and \
           (end_date is None or activity_time <= end_date):
            dummy_activity_log.append({
                "log_id": str(uuid.uuid4()),
                "timestamp": activity_time.isoformat(),
                "event_type": event_type,
                "description": f"User {user_id} performed {event_type} event {i+1}",
                "details": {"ip_address": f"192.168.1.{random.randint(1, 254)}"}
            })
    return dummy_activity_log[skip:skip+limit]

async def get_user_earnings_dummy(db: Session, user_id: str, start_date: Optional[date] = None, end_date: Optional[date] = None, currency: str = "USD") -> Dict[str, Any]:
    """
    Placeholder: Generates a dummy earnings summary for a specific user (e.g., content creator).
    """
    logger.info(f"Reports Service: Generating dummy user earnings for user_id: {user_id}, start_date={start_date}, end_date={end_date}, currency={currency}.")
    total_content_sales = round(random.uniform(100.00, 2000.00), 2)
    total_commissions_received = round(random.uniform(10.00, 200.00), 2)
    
    return {
        "report_name": f"User Earnings Report for {user_id}",
        "date_generated": datetime.utcnow().isoformat(),
        "total_content_sales_value": total_content_sales,
        "total_commissions_received": total_commissions_received,
        "currency": currency,
        "earnings_breakdown": [
            {"date": (datetime.utcnow() - timedelta(days=random.randint(1, 30))).isoformat(), "amount": round(random.uniform(5.00, 100.00), 2), "source": "Content Sale", "content_id": str(uuid.uuid4())},
            {"date": (datetime.utcnow() - timedelta(days=random.randint(1, 30))).isoformat(), "amount": round(random.uniform(1.00, 20.00), 2), "source": "Referral Commission", "referral_id": str(uuid.uuid4())}
        ]
    }

# --- Affiliate Reports (Dummy Data) ---

async def get_affiliate_summary_report_dummy(db: Session, affiliate_id: str) -> Dict[str, Any]:
    """
    Placeholder: Generates a dummy summary report for a specific affiliate.
    """
    logger.info(f"Reports Service: Generating dummy affiliate summary report for affiliate_id: {affiliate_id}.")
    return {
        "report_name": f"Affiliate Summary Report for {affiliate_id}",
        "date_generated": datetime.utcnow().isoformat(),
        "total_referrals": random.randint(10, 50),
        "total_clicks": random.randint(100, 500),
        "estimated_earnings_usd": round(random.uniform(50.00, 500.00), 2),
        "conversion_rate": round(random.uniform(0.05, 0.20), 2),
    }

async def get_affiliate_referrals_report_dummy(db: Session, affiliate_id: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    """
    Placeholder: Generates a list of dummy referral details for a specific affiliate.
    """
    logger.info(f"Reports Service: Generating dummy affiliate referrals report for affiliate_id: {affiliate_id}, skip={skip}, limit={limit}.")
    dummy_referrals = []
    for i in range(random.randint(5, 15)):
        dummy_referrals.append({
            "referred_user_id": str(uuid.uuid4()),
            "referred_username": f"referred_user_{i+1}",
            "registration_date": (datetime.utcnow() - timedelta(days=random.randint(1, 90))).isoformat(),
            "first_purchase_value": round(random.uniform(10.00, 100.00), 2) if random.random() > 0.3 else 0.00,
            "commission_earned": round(random.uniform(1.00, 10.00), 2) if random.random() > 0.3 else 0.00,
        })
    return dummy_referrals[skip:skip+limit]

async def get_affiliate_clicks_report_dummy(db: Session, affiliate_id: str, skip: int = 0, limit: int = 100, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
    """
    Placeholder: Generates a list of dummy link click details for a specific affiliate.
    """
    logger.info(f"Reports Service: Generating dummy affiliate clicks report for affiliate_id: {affiliate_id}, skip={skip}, limit={limit}, start_date={start_date}, end_date={end_date}.")
    dummy_clicks = []
    for i in range(random.randint(20, 50)):
        click_date = datetime.utcnow() - timedelta(days=random.randint(1, 60))
        if (start_date is None or click_date >= start_date) and \
           (end_date is None or click_date <= end_date):
            dummy_clicks.append({
                "click_id": str(uuid.uuid4()),
                "click_timestamp": click_date.isoformat(),
                "ip_address": f"192.168.1.{random.randint(1, 254)}",
                "user_agent": "Mozilla/5.0 (Dummy)",
                "referred_user_id": str(uuid.uuid4()) if random.random() > 0.5 else None, # Simulate some clicks leading to signups
            })
    return dummy_clicks[skip:skip+limit]

async def get_affiliate_earnings_report_dummy(db: Session, affiliate_id: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> Dict[str, Any]:
    """
    Placeholder: Generates a dummy earnings summary for a specific affiliate.
    """
    logger.info(f"Reports Service: Generating dummy affiliate earnings report for affiliate_id: {affiliate_id}, start_date={start_date}, end_date={end_date}.")
    
    total_commissions = round(random.uniform(50.00, 1000.00), 2)
    total_referred_sales = round(random.uniform(500.00, 10000.00), 2)
    
    return {
        "report_name": f"Affiliate Earnings Report for {affiliate_id}",
        "date_generated": datetime.utcnow().isoformat(),
        "total_commissions_earned": total_commissions,
        "total_referred_sales_value": total_referred_sales,
        "commission_details": [
            {"date": (datetime.utcnow() - timedelta(days=random.randint(1, 30))).isoformat(), "amount": round(random.uniform(1.00, 50.00), 2), "source": "NFT Sale" if random.random() > 0.5 else "Subscription"},
            {"date": (datetime.utcnow() - timedelta(days=random.randint(1, 30))).isoformat(), "amount": round(random.uniform(1.00, 50.00), 2), "source": "NFT Sale" if random.random() > 0.5 else "Subscription"}
        ]
    }


# --- Superuser Reports ---

async def get_token_usage_report_dummy(db: Session) -> Dict[str, Any]:
    """
    Placeholder: Generates a dummy token usage report.
    """
    logger.info("Reports Service: Generating dummy token usage report.")
    today = datetime.utcnow().date()
    usage_by_day = [
        {"date": (today - timedelta(days=i)).isoformat(), "calls": random.randint(800, 4000)}
        for i in range(7)
    ]
    return {
        "report_name": "Token Usage Report",
        "date_range": {"start": "beginning", "end": "now"},
        "total_api_calls": random.randint(200000, 500000),
        "unique_tokens_used": random.randint(300, 500),
        "most_active_token_ids": [str(random.randint(1000, 9999)) for _ in range(3)],
        "usage_by_day": usage_by_day
    }

async def get_nft_mint_activity_report_dummy(db: Session) -> List[Dict[str, Any]]:
    """
    Placeholder: Generates a dummy NFT minting activity report.
    """
    logger.info("Reports Service: Generating dummy NFT mint activity report.")

    dummy_mints = []
    statuses = ["success", "failed", "pending"]
    for i in range(10):
        status = random.choice(statuses)
        mint_entry = {
            "mint_id": f"mint-{random.randint(10000, 99999)}",
            "nft_id": f"nft-{random.randint(1000, 9999)}",
            "minter_id": str(uuid.uuid4()),
            "status": status,
            "mint_date": (datetime.utcnow() - timedelta(days=random.randint(0, 30))).isoformat(),
            "transaction_hash": f"0x{uuid.uuid4().hex}" if status == "success" else None,
            "error_message": "Insufficient funds" if status == "failed" and random.random() > 0.5 else None
        }
        dummy_mints.append(mint_entry)
    return dummy_mints

async def get_financial_report_dummy(db: Session) -> Dict[str, Any]:
    """
    Placeholder: Generates a dummy financial overview report.
    """
    logger.info("Reports Service: Generating dummy financial report.")
    total_revenue = round(random.uniform(5000.00, 10000.00), 2)
    total_expenses = round(random.uniform(10000.00, 20000.00), 2)
    net_profit = round(total_revenue - total_expenses, 2)
    return {
        "report_name": "Financial Overview",
        "date_range": {"start": "beginning", "end": "now"},
        "total_revenue": total_revenue,
        "total_expenses": total_expenses,
        "net_profit": net_profit,
        "currency": "USD",
        "revenue_breakdown_by_source": {
            "NFT Sales": round(total_revenue * 0.6, 2),
            "Service Fees": round(total_revenue * 0.3, 2),
            "Other": round(total_revenue * 0.1, 2)
        }
    }

async def get_ipfs_costs_report_dummy(db: Session) -> Dict[str, Any]:
    """
    Placeholder: Generates a dummy IPFS costs report.
    """
    logger.info("Reports Service: Generating dummy IPFS costs report.")
    total_storage_gb = round(random.uniform(1000.00, 5000.00), 2)
    total_retrieval_gb = round(random.uniform(500.00, 2000.00), 2)
    estimated_monthly_cost = round(random.uniform(100.00, 500.00), 2)
    return {
        "report_name": "IPFS Costs Report",
        "date_range": {"start": "beginning", "end": "now"},
        "total_storage_gb": total_storage_gb,
        "total_retrieval_gb": total_retrieval_gb,
        "estimated_monthly_cost_usd": estimated_monthly_cost,
        "cost_by_content_type": {
            "NFT Images": round(estimated_monthly_cost * 0.1, 2),
            "Memorial Data": round(estimated_monthly_cost * 0.3, 2),
            "User Profile Assets": round(estimated_monthly_cost * 0.2, 2)
        }
    }


async def get_engagement_report_dummy(db: Session) -> Dict[str, Any]:
    """
    Placeholder: Generates a dummy engagement report.
    """
    logger.info("Reports Service: Generating dummy engagement report.")
    return {
        "report_name": "Engagement Report",
        "date_range": {"start": "beginning", "end": "now"},
        "total_page_views": random.randint(1000000, 2000000),
        "unique_visitors": random.randint(200000, 400000),
        "average_session_duration_seconds": random.randint(60, 200),
        "content_type_filter": "All",
        "top_engaged_content_ids": [f"content-{random.randint(1000, 9999)}" for _ in range(5)],
        "engagement_metrics_by_type": {
            "Memorial Entries": {"views": random.randint(10000, 50000), "interactions": random.randint(500, 2000)},
            "NFTs": {"views": random.randint(10000, 50000), "interactions": random.randint(500, 2000)},
            "User Profiles": {"views": random.randint(5000, 10000), "interactions": random.randint(100, 500)}
        }
    }

async def get_users_by_referral_report_dummy(db: Session) -> List[Dict[str, Any]]:
    """
    Placeholder: Generates a dummy report on users acquired by referral.
    """
    logger.info("Reports Service: Generating dummy users by referral report.")
    return [
        {
            "referrer_identifier": "Direct/Unknown",
            "total_referred_users": random.randint(5, 10),
            "referred_users": [
                {"id": str(i), "username": f"user_{i}", "email": f"user{i}@example.com", "created_at": (datetime.utcnow() - timedelta(days=random.randint(1, 365))).isoformat(), "referring_affiliate_id": None, "referring_referral_code": None}
                for i in range(1, 8)
            ]
        },
        {
            "referrer_identifier": "aff123", # Example affiliate ID
            "total_referred_users": random.randint(1, 5),
            "referred_users": [
                {"id": str(uuid.uuid4()), "username": f"ref_user_{i}", "email": f"ref_user{i}@example.com", "created_at": (datetime.utcnow() - timedelta(days=random.randint(1, 60))).isoformat(), "referring_affiliate_id": "aff123", "referring_referral_code": None}
                for i in range(1, 4)
            ]
        },
        {
            "referrer_identifier": "ANOTHERREF", # Example referral code
            "total_referred_users": random.randint(1, 3),
            "referred_users": [
                {"id": str(uuid.uuid4()), "username": f"ref_code_user_{i}", "email": f"ref_code_user{i}@example.com", "created_at": (datetime.utcnow() - timedelta(days=random.randint(1, 90))).isoformat(), "referring_affiliate_id": None, "referring_referral_code": "ANOTHERREF"}
                for i in range(1, 2)
            ]
        }
    ]

async def get_affiliate_commissions_report_dummy(db: Session) -> Dict[str, Any]:
    """
    Placeholder: Generates a dummy affiliate commissions report.
    """
    logger.info("Reports Service: Generating dummy affiliate commissions report.")
    overall_total_commissions = round(random.uniform(2000.00, 5000.00), 2)
    overall_referred_sales_value = round(random.uniform(30000.00, 60000.00), 2)
    overall_num_referred_transactions = random.randint(300, 600)

    commissions_by_affiliate = {}
    for _ in range(random.randint(3, 7)): # Simulate 3-7 affiliates
        affiliate_id = uuid.uuid4().hex[:8]
        commissions_by_affiliate[affiliate_id] = {
            "total_commissions_earned": round(random.uniform(50.00, 1500.00), 2),
            "referred_sales_value": round(random.uniform(1000.00, 10000.00), 2),
            "number_of_referred_transactions": random.randint(1, 100)
        }

    return {
        "report_name": "Affiliate Commissions Report",
        "date_range": {"start": "beginning", "end": "now"},
        "overall_total_commissions": overall_total_commissions,
        "overall_referred_sales_value": overall_referred_sales_value,
        "overall_num_referred_transactions": overall_num_referred_transactions,
        "commissions_by_affiliate": commissions_by_affiliate
    }


# --- Public Reports ---

async def get_top_content_report_dummy(db: Session, metric: str = "views") -> Dict[str, Any]:
    """
    Placeholder: Generates a dummy top content report.
    """
    logger.info(f"Reports Service: Generating dummy top content report by metric: {metric}.")
    dummy_content = [
        {"id": 1, "type": "Art", "status": "published", "views": 1500, "sales": 150.00, "created_at": (datetime.utcnow() - timedelta(days=random.randint(5, 20))).isoformat()},
        {"id": 2, "type": "Music", "status": "published", "views": 2500, "sales": 250.00, "created_at": (datetime.utcnow() - timedelta(days=random.randint(2, 10))).isoformat()},
        {"id": 3, "type": "Writing", "status": "published", "views": 800, "sales": 80.00, "created_at": (datetime.utcnow() - timedelta(days=random.randint(10, 30))).isoformat()},
        {"id": 4, "type": "Art", "status": "pending", "views": 50, "sales": 0.00, "created_at": (datetime.utcnow() - timedelta(days=random.randint(1, 3))).isoformat()},
        {"id": 5, "type": "Music", "status": "published", "views": 1200, "sales": 120.00, "created_at": (datetime.utcnow() - timedelta(hours=random.randint(1, 24))).isoformat()},
        {"id": 6, "type": "Writing", "status": "draft", "views": 100, "sales": 0.00, "created_at": (datetime.utcnow() - timedelta(days=random.randint(7, 14))).isoformat()},
        {"id": 7, "type": "Art", "status": "published", "views": 3000, "sales": 300.00, "created_at": (datetime.utcnow() - timedelta(hours=random.randint(12, 48))).isoformat()},
        {"id": 8, "type": "Music", "status": "published", "views": 4000, "sales": 400.00, "created_at": (datetime.utcnow() - timedelta(days=random.randint(3, 8))).isoformat()},
        {"id": 9, "type": "Art", "status": "published", "views": 2000, "sales": 200.00, "created_at": (datetime.utcnow() - timedelta(hours=random.randint(6, 18))).isoformat()},
        {"id": 10, "type": "Writing", "status": "published", "views": 1000, "sales": 100.00, "created_at": (datetime.utcnow() - timedelta(days=random.randint(20, 40))).isoformat()},
        {"id": 11, "type": "Photography", "status": "published", "views": 900, "sales": 90.00, "created_at": (datetime.utcnow() - timedelta(hours=random.randint(2, 10))).isoformat()},
        {"id": 12, "type": "Video", "status": "published", "views": 5000, "sales": 500.00, "created_at": (datetime.utcnow() - timedelta(hours=random.randint(1, 5))).isoformat()},
        {"id": 13, "type": "Art", "status": "published", "views": 1800, "sales": 180.00, "created_at": (datetime.utcnow() - timedelta(hours=random.randint(10, 30))).isoformat()},
    ]

    # Sort content by the requested metric (views or sales) in descending order
    if metric == "views":
        sorted_content = sorted(dummy_content, key=lambda x: x["views"], reverse=True)
    elif metric == "sales":
        sorted_content = sorted(dummy_content, key=lambda x: x["sales"], reverse=True)
    else:
        sorted_content = dummy_content # Default sort if metric is not recognized

    # Return top N items (e.g., top 10)
    return {"top_content": sorted_content[:10], "metric": metric}


async def get_trending_content_report_dummy(db: Session, time_period_hours: int = 24) -> Dict[str, Any]:
    """
    Placeholder: Generates a dummy trending content report based on recent views and a simulated 'trend score'.
    """
    logger.info(f"Reports Service: Generating dummy trending content report for last {time_period_hours} hours.")

    dummy_content = [
        {"id": 1, "type": "Art", "status": "published", "views": 1500, "sales": 150.00, "created_at": (datetime.utcnow() - timedelta(days=random.randint(5, 20))).isoformat()},
        {"id": 2, "type": "Music", "status": "published", "views": 2500, "sales": 250.00, "created_at": (datetime.utcnow() - timedelta(days=random.randint(2, 10))).isoformat()},
        {"id": 3, "type": "Writing", "status": "published", "views": 800, "sales": 80.00, "created_at": (datetime.utcnow() - timedelta(days=random.randint(10, 30))).isoformat()},
        {"id": 4, "type": "Art", "status": "pending", "views": 50, "sales": 0.00, "created_at": (datetime.utcnow() - timedelta(days=random.randint(1, 3))).isoformat()},
        {"id": 5, "type": "Music", "status": "published", "views": 1200, "sales": 120.00, "created_at": (datetime.utcnow() - timedelta(hours=random.randint(1, 24))).isoformat()},
        {"id": 6, "type": "Writing", "status": "draft", "views": 100, "sales": 0.00, "created_at": (datetime.utcnow() - timedelta(days=random.randint(7, 14))).isoformat()},
        {"id": 7, "type": "Art", "status": "published", "views": 3000, "sales": 300.00, "created_at": (datetime.utcnow() - timedelta(hours=random.randint(12, 48))).isoformat()},
        {"id": 8, "type": "Music", "status": "published", "views": 4000, "sales": 400.00, "created_at": (datetime.utcnow() - timedelta(days=random.randint(3, 8))).isoformat()},
        {"id": 9, "type": "Art", "status": "published", "views": 2000, "sales": 200.00, "created_at": (datetime.utcnow() - timedelta(hours=random.randint(6, 18))).isoformat()},
        {"id": 10, "type": "Writing", "status": "published", "views": 1000, "sales": 100.00, "created_at": (datetime.utcnow() - timedelta(days=random.randint(20, 40))).isoformat()},
        {"id": 11, "type": "Photography", "status": "published", "views": 900, "sales": 90.00, "created_at": (datetime.utcnow() - timedelta(hours=random.randint(2, 10))).isoformat()},
        {"id": 12, "type": "Video", "status": "published", "views": 5000, "sales": 500.00, "created_at": (datetime.utcnow() - timedelta(hours=random.randint(1, 5))).isoformat()},
        {"id": 13, "type": "Art", "status": "published", "views": 1800, "sales": 180.00, "created_at": (datetime.utcnow() - timedelta(hours=random.randint(10, 30))).isoformat()},
    ]

    # Filter content created within the last 'time_period_hours' and calculate a dummy trend score
    trending_items = []
    time_threshold = datetime.utcnow() - timedelta(hours=time_period_hours)

    for item in dummy_content:
        # Only consider published content for trending
        if item["status"] == "published":
            item_created_at = datetime.fromisoformat(item["created_at"])
            # Simple trend score: recent views + recent sales, weighted
            # For dummy, let's just use current views and add a recency factor
            recency_factor = 1.0
            if item_created_at > time_threshold:
                time_diff_hours = (datetime.utcnow() - item_created_at).total_seconds() / 3600
                if time_diff_hours > 0:
                    recency_factor = max(0.5, 1.0 - (time_diff_hours / time_period_hours)) # More recent = higher factor

            trend_score = item["views"] * recency_factor + (item["sales"] * 5) # Sales weighted more
            item["trend_score"] = round(trend_score, 2)
            trending_items.append(item)

    # Sort by trend_score in descending order
    sorted_trending = sorted(trending_items, key=lambda x: x.get("trend_score", 0), reverse=True)

    return {"trending_content": sorted_trending[:6], "time_period_hours": time_period_hours}
