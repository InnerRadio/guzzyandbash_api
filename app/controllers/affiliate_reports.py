from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..dependencies import get_db, get_current_active_user
from ..models.user import User # Assuming User model is used
from ..services import affiliate_reports as affiliate_reports_service
from ..schemas.user_schemas import UserResponse as UserSchema 

router = APIRouter(prefix="/affiliate_reports", tags=["Affiliate Reports"])

# --- GET /api/v1/affiliate_reports/my-summary ---

@router.get("/my-summary", status_code=status.HTTP_200_OK)
async def get_my_affiliate_summary(
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    affiliate_id = current_user.affiliate_id 
    if not affiliate_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not registered as an affiliate.")
    
    summary = affiliate_reports_service.get_affiliate_summary_report(db, affiliate_id)
    return summary


# --- GET /api/v1/affiliate_reports/my-referrals ---

@router.get("/my-referrals", status_code=status.HTTP_200_OK)
async def get_my_affiliate_referrals(
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    affiliate_id = current_user.affiliate_id 
    if not affiliate_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not registered as an affiliate.")
        
    referrals = affiliate_reports_service.get_affiliate_referrals_report(db, affiliate_id)
    return referrals


# --- GET /api/v1/affiliate_reports/my-clicks ---

@router.get("/my-clicks", status_code=status.HTTP_200_OK)
async def get_my_affiliate_clicks(
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    affiliate_id = current_user.affiliate_id 
    if not affiliate_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not registered as an affiliate.")
        
    clicks = affiliate_reports_service.get_affiliate_clicks_report(db, affiliate_id)
    return clicks


# --- GET /api/v1/affiliate_reports/my-earnings ---

@router.get("/my-earnings", status_code=status.HTTP_200_OK)
async def get_my_affiliate_earnings(
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    affiliate_id = current_user.affiliate_id 
    if not affiliate_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not registered as an affiliate.")
        
    earnings_report = affiliate_reports_service.get_affiliate_earnings_report(db, affiliate_id)
    return earnings_report
