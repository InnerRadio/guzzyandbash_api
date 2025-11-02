from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime, date

# --- User-Specific Report Schemas ---

class UserProfileSummary(BaseModel):
    report_name: str
    date_generated: datetime
    total_content_created: int
    total_nfts_owned: int
    total_views_on_content: int
    total_earnings_usd: float
    last_login: datetime

class UserContentItem(BaseModel):
    content_id: str
    title: str
    content_type: str
    status: str
    views: int
    created_at: datetime
    last_updated_at: datetime # CORRECTED: Changed from 'last_updated' to 'last_updated_at'

class UserNFTItem(BaseModel):
    nft_id: str
    title: str
    token_id: str
    minted_at: datetime # CORRECTED: Changed from 'mint_date' to 'minted_at'
    price_usd: float
    is_listed_for_sale: bool

class UserActivityLogEntry(BaseModel):
    log_id: str
    timestamp: datetime
    event_type: str
    description: str
    details: Optional[Dict[str, Any]] = None # Use Dict[str, Any] for flexible details

class UserEarningsReport(BaseModel):
    report_name: str
    date_generated: datetime
    total_content_sales_value: float
    total_commissions_received: float
    currency: str
    earnings_breakdown: List[Dict[str, Any]] # Flexible for now, can be more detailed later

# --- Comprehensive User Profile Schema ---

class UserFullProfile(BaseModel):
    profile_summary: UserProfileSummary
    nft_collection: List[UserNFTItem]
    content_items: List[UserContentItem] # Changed from 'recent_content' for consistency
    activity_log: List[UserActivityLogEntry] # Changed from 'recent_activity_log' for consistency
    earnings_report: UserEarningsReport
    # Add other top-level user data that isn't part of the summary but needed for a full view
    email: EmailStr
    username: str
    role: str
    is_active: bool
    is_verified: bool
    profile_picture_url: Optional[HttpUrl] = None
    social_links: Optional[Dict[str, Any]] = None
    has_api_access: bool
    referral_code: Optional[str] = None
    referred_by_user_id: Optional[str] = None
    referred_by_referral_code: Optional[str] = None
    affiliate_commission_rate: Optional[float] = None
    is_affiliate: bool
    # Add created_at and last_updated_at from the User model
    created_at: datetime
    last_updated_at: datetime