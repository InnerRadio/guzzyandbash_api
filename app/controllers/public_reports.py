# /var/www/tarot-api/guzzy_and_bash_productions/app/controllers/public_reports.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from enum import Enum

from app.database import get_db
from app.services import reports as reports_service

# Define the ContentSortBy enum
class ContentSortBy(str, Enum):
    VIEWS = "views"
    SALES = "sales"

router = APIRouter(tags=["Public Reports"]) # CORRECTED: Changed from ["Public Reports", "Marketplace"]

@router.get(
    "/public/reports/top-content",
    response_model=Dict[str, Any],
    summary="Public: Get Top Content Report (Enhanced)",
    description="Retrieves a list of top content items, with optional filtering by content type and sorting by specified metrics (e.g., Views, Sales). Accessible publicly for display and contests."
)
def get_top_content(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100, description="Number of top items to retrieve"),
    content_type: Optional[str] = Query(None, description="Filter by specific content type (e.g., 'Art', 'Music', 'Writing')"),
    sort_by: ContentSortBy = Query(ContentSortBy.VIEWS, description="Metric to sort by (e.g., 'views', 'sales')")
):
    return reports_service.get_top_content_report(
        db=db,
        limit=limit,
        content_type=content_type,
        sort_by=sort_by.value
    )

# NEW ENDPOINT: Public Get Trending Content Report
@router.get(
    "/public/reports/trending-content",
    response_model=Dict[str, Any],
    summary="Public: Get Trending Content Report",
    description="Identifies and retrieves content currently gaining rapid popularity based on recent engagement. Accessible publicly for marketplace trends."
)
def get_trending_content(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100, description="Number of trending items to retrieve"),
    time_period_hours: int = Query(24, ge=1, le=720, description="Time period in hours to consider for 'trending' (e.g., 24 for last 24 hours)")
):
    return reports_service.get_trending_content_report(
        db=db,
        limit=limit,
        time_period_hours=time_period_hours
    )
