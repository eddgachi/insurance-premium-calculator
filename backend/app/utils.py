import os
from datetime import datetime

import requests
from sqlalchemy.orm import Session

from .models import QuoteRequest, QuoteResult
from .schemas import PremiumRequest

# Load RapidAPI configuration from environment
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")
BASE_URL = f"https://{RAPIDAPI_HOST}"


def fetch_premium(req: PremiumRequest) -> tuple[float, str]:
    url = f"{BASE_URL}/{req.policy_type}"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST,
    }
    params = {
        "age": req.age,
        "coverage": req.coverage,
        "location": req.location,
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 429:
            raise Exception("Rate limit exceeded. Please try again later.")
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        raise Exception(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        raise Exception(f"Network error occurred: {req_err}")

    raw = response.text
    data = response.json()
    premium = data.get("premium")

    if premium is None:
        raise ValueError("No 'premium' field in API response")

    return premium, raw


def save_quote(db: Session, req: PremiumRequest) -> QuoteRequest:
    """Persist a QuoteRequest to the database."""
    quote = QuoteRequest(
        policy_type=req.policy_type,
        age=req.age,
        coverage=req.coverage,
        location=req.location,
        requested_at=datetime.utcnow(),
    )
    db.add(quote)
    db.commit()
    db.refresh(quote)
    return quote


def save_quote_result(
    db: Session, request_id: int, premium: float, raw_response: str
) -> QuoteResult:
    """Persist a QuoteResult tied to a QuoteRequest."""
    result = QuoteResult(
        request_id=request_id,
        premium=premium,
        fetched_at=datetime.utcnow(),
        raw_response=raw_response,
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result
