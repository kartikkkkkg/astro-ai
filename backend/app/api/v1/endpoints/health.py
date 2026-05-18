"""
Health check endpoints.
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("", summary="Health check")
async def health_check():
    """Return service health status."""
    return {"status": "healthy", "service": "astrology-api"}