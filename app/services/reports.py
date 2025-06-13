# /var/www/tarot-api/guzzy_and_bash_productions/app/services/reports.py

from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date # Added date
from typing import Optional, List, Dict, Any # Added Optional, Dict, Any for type hints
import random # Added for dummy trending content

from app.models.user import User  # Assuming User model is defined here
# from app.models.content import Content # Placeholder: assuming a Content model exists
# from app.models.transaction import Transaction # Placeholder: assuming a Transaction model exists

# Placeholder for a simple "Content" model, you'll replace this with your actual content model
class Content:
    def __init__(self, id: int, type: str, status: str, views: int = 0, sales: float = 0.0, created_at: Optional[datetime] = None):
        self.id = id
        self.type = type
        self.status = status
        self.views = views
        self.sales = sales # Added sales metric
        self.created_at = created_at if created_at is not None else datetime.now() # Added created_at

    @staticmethod
    def get_all_dummy_content():
        # Dummy data with varying created_at times for trending simulation
        now = datetime.now()
        return [
            Content(1, "Art", "published", 1500, 150.00, now - timedelta(days=5)),
            Content(2, "Music", "published", 2500, 250.00, now - timedelta(days=2)),
            Content(3, "Writing", "published", 800, 80.00, now - timedelta(days=10)),
            Content(4, "Art", "pending", 50, 0.00, now - timedelta(days=1)),
            Content(5, "Music", "published", 1200, 120.00, now - timedelta(hours=3)), # Recently created
            Content(6, "Writing", "draft", 100, 0.00, now - timedelta(days=7)),
            Content(7, "Art", "published", 3000, 300.00, now - timedelta(hours=12)), # Recently created, high views
            Content(8, "Music", "published", 4000, 400.00, now - timedelta(days=4)),
            Content(9, "Art", "published", 2000, 200.00, now - timedelta(hours=6)), # Recently created
            Content(10, "Writing", "published", 1000, 100.00, now - timedelta(days=20)),
            Content(11, "Photography", "published", 900, 90.00, now - timedelta(hours=1)), # Very recent
            Content(12, "Video", "published", 5000, 500.00, now - timedelta(hours=2)), # Very recent, high views/sales
            Content(13, "Art", "published", 1800, 180.00, now - timedelta(hours=4)),
        ]

# Placeholder for a simple "User" model, you'll replace this with your actual user model
class UserDummy:
    def __init__(self, id: int, username: str, email: str, role: str, is_active: bool, created_at: datetime):
        self.id = id
        self.username = username
        self.email = email
        self.role = role
        self.is_active = is_active
        self.created_at = created_at

    @staticmethod
    def get_all_dummy_users():
        now = datetime.now()
        return [
            UserDummy(1, "admin_user", "admin@example.com", "ADMIN", True, now - timedelta(days=365)),
            UserDummy(2, "artist_one", "artist1@example.com", "ARTIST", True, now - timedelta(days=90)),
            UserDummy(3, "consumer_a", "consumer_a@example.com", "CONSUMER", True, now - timedelta(days=30)),
            UserDummy(4, "moderator_alpha", "mod@example.com", "MODERATOR", True, now - timedelta(days=180)),
            UserDummy(5, "inactive_user", "inactive@example.com", "CONSUMER", False, now - timedelta(days=60)),
            UserDummy(6, "new_artist", "new_art@example.com", "ARTIST", True, now - timedelta(days=5)),
            UserDummy(7, "new_consumer", "new_con@example.com", "CONSUMER", True, now - timedelta(hours=10)),
        ]

# --- Report Service Functions ---

def get_users_summary_report(db: Session):
    """
    Generates a summary report of users.
    For now, this is a placeholder using dummy data.
    In a real scenario, it would query the User model in the database.
    """
    # Using dummy users for demonstration
    all_users = UserDummy.get_all_dummy_users()
    total_users = len(all_users)

    users_by_role = {}
    for user in all_users:
        users_by_role[user.role] = users_by_role.get(user.role, 0) + 1

    # New users in last 30 days (dummy logic)
    new_users_last_30_days = sum(1 for user in all_users if user.created_at > datetime.now() - timedelta(days=30))

    return {
        "total_users": total_users,
        "users_by_role": users_by_role,
        "new_users_last_30_days": new_users_last_30_days
    }

def get_content_summary_report(db: Session):
    """
    Generates a summary report of content.
    For now, this is a placeholder using dummy data.
    In a real scenario, it would query the Content model in the database.
    """
    # Using dummy content for demonstration
    all_content = Content.get_all_dummy_content()
    total_content_items = len(all_content)

    content_by_type = {}
    content_by_status = {}

    for item in all_content:
        content_by_type[item.type] = content_by_type.get(item.type, 0) + 1
        content_by_status[item.status] = content_by_status.get(item.status, 0) + 1

    return {
        "total_content_items": total_content_items,
        "content_by_type": content_by_type,
        "content_by_status": content_by_status
    }

def get_top_content_report(
    db: Session,
    limit: int = 10,
    content_type: Optional[str] = None,
    sort_by: str = "views"
):
    """
    Generates a report of top content items, with filtering and sorting.
    For now, this uses dummy data.
    """
    all_content = Content.get_all_dummy_content()

    # 1. Filter by content_type if provided
    if content_type:
        all_content = [item for item in all_content if item.type.lower() == content_type.lower()]

    # 2. Sort by the specified metric
    if sort_by == "views":
        sorted_content = sorted(all_content, key=lambda x: x.views, reverse=True)
    elif sort_by == "sales":
        sorted_content = sorted(all_content, key=lambda x: x.sales, reverse=True)
    else:
        sorted_content = all_content # No specific sort if not views/sales

    # 3. Apply limit
    top_items_data = []
    for item in sorted_content[:limit]:
        top_items_data.append({
            "id": item.id,
            "type": item.type,
            "status": item.status,
            "views": item.views,
            "sales": item.sales,
            "created_at": item.created_at.isoformat() # Include created_at
        })

    return {
        "top_content": top_items_data,
        "metric": sort_by
    }

# NEW SERVICE FUNCTION: Admin Get Detailed Users Report
def get_admin_users_report(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    user_role: Optional[str] = None,
    is_active: Optional[bool] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    """
    Retrieves a detailed list of users with optional filtering and pagination.
    For now, this uses dummy data. In a real scenario, it would query the User model.
    """
    all_users = UserDummy.get_all_dummy_users()
    filtered_users = []

    for user in all_users:
        matches_role = user_role is None or user.role.lower() == user_role.lower()
        matches_active = is_active is None or user.is_active == is_active

        matches_start_date = start_date is None or user.created_at.date() >= start_date
        matches_end_date = end_date is None or user.created_at.date() <= end_date

        if matches_role and matches_active and matches_start_date and matches_end_date:
            filtered_users.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat()
            })

    return filtered_users[skip : skip + limit]

# NEW SERVICE FUNCTION: Admin Get Detailed Content Report
def get_admin_content_report(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    content_type: Optional[str] = None,
    content_status: Optional[str] = None,
    creator_id: Optional[int] = None,
    min_views: Optional[int] = None,
    min_sales: Optional[float] = None
):
    """
    Retrieves a detailed list of content items with optional filtering and pagination.
    For now, this uses dummy data. In a real scenario, it would query the Content model.
    """
    all_content = Content.get_all_dummy_content()
    filtered_content = []

    for item in all_content:
        matches_type = content_type is None or item.type.lower() == content_type.lower()
        matches_status = content_status is None or item.status.lower() == content_status.lower()
        # For creator_id, assuming Content has a creator_id attribute (dummy data does not yet)
        # matches_creator = creator_id is None or item.creator_id == creator_id 
        matches_creator = True # Placeholder for now as dummy Content lacks creator_id

        matches_min_views = min_views is None or item.views >= min_views
        matches_min_sales = min_sales is None or item.sales >= min_sales

        if matches_type and matches_status and matches_creator and matches_min_views and matches_min_sales:
            filtered_content.append({
                "id": item.id,
                "type": item.type,
                "status": item.status,
                "views": item.views,
                "sales": item.sales,
                "created_at": item.created_at.isoformat()
            })

    return filtered_content[skip : skip + limit]

# NEW SERVICE FUNCTION: Public Get Trending Content Report
def get_trending_content_report(
    db: Session,
    limit: int = 10,
    time_period_hours: int = 24
):
    """
    Identifies and retrieves content currently gaining rapid popularity based on recent engagement.
    For now, this uses dummy data with a simplified "trending" logic.
    """
    all_content = Content.get_all_dummy_content()

    # Filter content created within the specified time period
    time_threshold = datetime.now() - timedelta(hours=time_period_hours)
    recent_content = [item for item in all_content if item.created_at >= time_threshold and item.status == "published"]

    # Simple trending logic: prioritize by recent views/sales, potentially add a random factor
    # For dummy data, we'll sort by a combination of recentness and views/sales, then apply a bit of randomness
    # In a real system, this would involve complex metrics and possibly machine learning

    # Sort by a derived 'trend_score'
    def get_trend_score(item):
        # Simple score: higher views/sales + more recent = higher score
        age_factor = (datetime.now() - item.created_at).total_seconds() / (time_period_hours * 3600) # 0 to 1, smaller is better
        # If item is very recent, age_factor will be close to 0, which means 1 - age_factor is close to 1
        # We want more recent to have a *higher* score contribution

        # Weighted sum: Views contribute, Sales contribute, Recency contributes
        # Adjust weights based on desired "trending" definition
        score = (item.views * 0.5) + (item.sales * 1.0) + ((1 - age_factor) * 1000) # Example weights
        return score

    # Sort the recent content by the calculated trend score
    sorted_trending_content = sorted(recent_content, key=get_trend_score, reverse=True)

    trending_items_data = []
    for item in sorted_trending_content[:limit]:
        trending_items_data.append({
            "id": item.id,
            "type": item.type,
            "status": item.status,
            "views": item.views,
            "sales": item.sales,
            "created_at": item.created_at.isoformat(),
            "trend_score": round(get_trend_score(item), 2) # Show the score for debugging/understanding
        })

    return {
        "trending_content": trending_items_data,
        "time_period_hours": time_period_hours
    }