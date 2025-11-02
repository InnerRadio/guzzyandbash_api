from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any, List

# --- DUMMY DATA (To be replaced with real DB queries) ---

def get_affiliate_summary_report(db: Session, affiliate_id: str) -> Dict[str, Any]:
    print(f"STUB: Fetching dummy summary report for affiliate: {affiliate_id}")
    return {
        "report_name": "Affiliate Summary Report (DUMMY)",
        "date_generated": datetime.now().isoformat(),
        "total_referrals": 42,
        "total_clicks": 1850,
        "total_commissions_earned": 985.50,
        "total_payouts": 500.00,
        "pending_commissions": 485.50,
    }

def get_affiliate_referrals_report(db: Session, affiliate_id: str) -> List[Dict[str, Any]]:
    print(f"STUB: Fetching dummy referrals report for affiliate: {affiliate_id}")
    return []

def get_affiliate_clicks_report(db: Session, affiliate_id: str) -> List[Dict[str, Any]]:
    print(f"STUB: Fetching dummy clicks report for affiliate: {affiliate_id}")
    return []

def get_affiliate_earnings_report(db: Session, affiliate_id: str) -> Dict[str, Any]:
    print(f"STUB: Fetching dummy earnings report for affiliate: {affiliate_id}")
    return {
        "report_name": "Affiliate Earnings Report (DUMMY)",
        "date_generated": datetime.now().isoformat(),
        "total_earnings_period": 100.00,
        "total_payouts_period": 0.00,
        "currency": "USD",
        "earnings_breakdown": []
    }
