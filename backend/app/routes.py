from app.models import QuoteRequest, QuoteResult
from app.schemas import (
    PremiumRequest,
    PremiumResponse,
    QuoteRequestRead,
    QuoteResultRead,
)
from app.session import get_db
from app.utils import fetch_premium, save_quote, save_quote_result
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Hello World"}


@router.post("/calculate-premium", response_model=PremiumResponse)
def calculate_premium(req: PremiumRequest, db: Session = Depends(get_db)):
    # 1) Persist the incoming request
    quote_req = save_quote(db, req)
    # 2) Call external API
    try:
        premium, raw = fetch_premium(req)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
    # 3) Persist the result
    save_quote_result(db, quote_req.id, premium, raw)
    return PremiumResponse(
        policy_type=req.policy_type, coverage=req.coverage, premium=premium
    )


@router.get("/requests", response_model=list[QuoteRequestRead])
def list_requests(db: Session = Depends(get_db)):
    return db.query(QuoteRequest).all()


@router.get("/results", response_model=list[QuoteResultRead])
def list_results(db: Session = Depends(get_db)):
    return db.query(QuoteResult).all()
