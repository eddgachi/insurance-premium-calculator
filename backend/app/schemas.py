# backend/app/schemas.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PremiumRequest(BaseModel):
    policy_type: str = Field(..., pattern="^(auto|home|life)$")
    age: int = Field(..., ge=18)
    coverage: int = Field(..., gt=0)
    location: str = Field(..., min_length=1)


class PremiumResponse(BaseModel):
    policy_type: str
    coverage: int
    premium: float


class QuoteRequestRead(BaseModel):
    id: int
    policy_type: str
    age: int
    coverage: int
    location: str
    requested_at: datetime

    class Config:
        from_attributes = True


class QuoteResultRead(BaseModel):
    id: int
    request_id: int
    premium: float
    fetched_at: datetime
    raw_response: Optional[str]

    class Config:
        from_attributes = True
