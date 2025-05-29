from app.session import Base
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text


class ApplicationConfig(Base):
    """Stores global configuration settings for the application."""

    __tablename__ = "application_config"

    id = Column(Integer, primary_key=True, autoincrement=True)
    config_key = Column(String(50), unique=True, nullable=False)
    config_value = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)


class QuoteRequest(Base):
    """Tracks what the user asked for when requesting an insurance quote."""

    __tablename__ = "quote_requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True)  # Reference to a user, if you add auth
    policy_type = Column(String(20), nullable=False)
    age = Column(Integer, nullable=False)
    coverage = Column(Integer, nullable=False)
    location = Column(String(100), nullable=False)
    requested_at = Column(DateTime, nullable=False)


class QuoteResult(Base):
    """Stores the result of a quote request for auditing or future display."""

    __tablename__ = "quote_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(Integer, ForeignKey("quote_requests.id"), nullable=False)
    premium = Column(Float, nullable=False)
    fetched_at = Column(DateTime, nullable=False)
    raw_response = Column(Text, nullable=True)  # Store full API response if needed
