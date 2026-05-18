"""
API router for version 1 endpoints.
"""
from fastapi import APIRouter
from .endpoints import charts, interpretations, health

api_router = APIRouter()

# Include routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(charts.router, prefix="/charts", tags=["charts"])
api_router.include_router(interpretations.router, prefix="/interpretations", tags=["interpretations"])