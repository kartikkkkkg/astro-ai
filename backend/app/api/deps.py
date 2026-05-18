"""
Dependencies for FastAPI endpoints.
"""
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.app.db.session import SessionLocal
from backend.app.core.config import settings
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

# Security
reusable_oauth2 = HTTPBearer(
    scheme_name="JWT"
)

def get_db() -> Generator:
    """
    Get database session.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user_id(
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(reusable_oauth2)
) -> int:
    """
    Extract user ID from JWT token.
    For MVP, we'll return a default user ID.
    In production, this would validate the JWT and extract user ID.
    """
    # For MVP, return default user ID
    # TODO: Implement proper JWT validation
    return 1

# Alternative: Simple dependency for MVP that returns a fixed user ID
def get_current_user_id_mock() -> int:
    """
    Mock dependency for MVP that returns a fixed user ID.
    Replace with proper authentication in production.
    """
    return 1