"""
Pydantic schemas for interpretation-related requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class InterpretationType(str, Enum):
    BASIC = "basic"
    DETAILED = "detailed"
    RELATIONSHIP = "relationship"
    CAREER = "career"

class InterpretationBase(BaseModel):
    chart_id: int
    interpretation_type: InterpretationType = InterpretationType.BASIC
    language: str = Field(default="en", pattern=r"^[a-z]{2}$")
    model_used: Optional[str] = None

class InterpretationCreate(InterpretationBase):
    pass


class InterpretationUpdate(BaseModel):
    chart_id: Optional[int] = None
    interpretation_type: Optional[InterpretationType] = None
    language: Optional[str] = None
    model_used: Optional[str] = None
    content: Optional[str] = None
    quality_score: Optional[float] = None
    tokens_used: Optional[int] = None
    processing_time_ms: Optional[int] = None

    model_config = {
        "from_attributes": True
    }

class InterpretationInDBBase(InterpretationBase):
    id: int
    user_id: int
    content: str
    quality_score: Optional[float] = Field(None, ge=0, le=1)
    tokens_used: Optional[int] = None
    processing_time_ms: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }

class InterpretationResponse(InterpretationInDBBase):
    chart: Optional[dict] = None  # Basic chart info for reference

class InterpretationListResponse(BaseModel):
    interpretations: List[InterpretationResponse]
    total: int
    page: int
    size: int

class AsyncInterpretationResponse(BaseModel):
    """Response for asynchronous interpretation requests."""
    task_id: str
    status: str = Field(description="pending, processing, completed, failed")
    estimated_completion: Optional[datetime] = None
    interpretation_id: Optional[int] = None
    message: str

# Example payloads
INTERPRETATION_CREATE_EXAMPLE = {
    "chart_id": 1,
    "interpretation_type": "basic",
    "language": "en"
}

INTERPRETATION_RESPONSE_EXAMPLE = {
    "id": 1,
    "chart_id": 1,
    "user_id": 1,
    "interpretation_type": "basic",
    "language": "en",
    "model_used": "gpt-4",
    "content": "The Sun in Leo in the 5th house indicates...",
    "quality_score": 0.85,
    "tokens_used": 450,
    "processing_time_ms": 2500,
    "created_at": "2024-01-15T10:35:00Z",
    "updated_at": "2024-01-15T10:35:00Z"
}

ASYNC_INTERPRETATION_RESPONSE_EXAMPLE = {
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "processing",
    "estimated_completion": "2024-01-15T10:40:00Z",
    "message": "Interpretation generation started. Results will be available shortly."
}