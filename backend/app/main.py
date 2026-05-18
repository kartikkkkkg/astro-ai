"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.router import api_router
from backend.app.core.config import settings

app = FastAPI(
    title="AI Astrology Platform API",
    description="API for AI-powered astrology platform with D1/D9 chart generation and interpretation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint to check API health."""
    return {"message": "AI Astrology Platform API is running"}

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "astrology-api"}