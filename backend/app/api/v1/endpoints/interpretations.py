"""
AI interpretation generation and retrieval endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from backend.app.crud.chart import chart as crud_chart
from backend.app import schemas
from backend.app.api import deps
from backend.app.services.interpretation_service import get_interpretation_service
from backend.app.workers.ai_interpretation import generate_interpretation_task

router = APIRouter()

@router.post("", response_model=schemas.AsyncInterpretationResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_interpretation(
    *,
    db: Session = Depends(deps.get_db),
    interpretation_in: schemas.InterpretationCreate,
    background_tasks: BackgroundTasks,
    current_user_id: int = Depends(deps.get_current_user_id_mock)
):
    """
    Generate AI interpretation for a chart (async processing).
    """
    # Verify chart exists and belongs to user
    chart = crud_chart.get(db=db, id=interpretation_in.chart_id)
    if not chart:
        raise HTTPException(status_code=404, detail="Chart not found")
    if chart.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # Create interpretation record (pending)
    interpretation = crud.interpretation.create_with_owner(
        db=db, obj_in=interpretation_in, user_id=current_user_id
    )

    # Trigger async AI interpretation generation
    task_id = str(uuid.uuid4())
    background_tasks.add_task(
        generate_interpretation_task,
        chart_id=chart.id,
        interpretation_id=interpretation.id,
        interpretation_type=interpretation_in.interpretation_type,
        language=interpretation_in.language,
        task_id=task_id
    )

    # Return async response
    interpretation_service_instance = get_interpretation_service(db)
    return schemas.AsyncInterpretationResponse(
        task_id=task_id,
        status="pending",
        interpretation_id=interpretation.id,
        message="Interpretation generation started. Results will be available shortly."
    )

@router.get("/{interpretation_id}", response_model=schemas.InterpretationResponse)
async def get_interpretation(
    interpretation_id: int,
    db: Session = Depends(deps.get_db),
    current_user_id: int = Depends(deps.get_current_user_id_mock)
):
    """
    Get a specific interpretation by ID.
    """
    interpretation = crud.interpretation.get(db=db, id=interpretation_id)
    if not interpretation:
        raise HTTPException(status_code=404, detail="Interpretation not found")
    if interpretation.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return interpretation

@router.get("", response_model=schemas.InterpretationListResponse)
async def get_interpretations(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user_id: int = Depends(deps.get_current_user_id_mock)
):
    """
    Retrieve user's interpretations with pagination.
    """
    interpretations = crud.interpretation.get_multi_by_owner(
        db=db, owner_id=current_user_id, skip=skip, limit=limit
    )
    total = crud.interpretation.get_count_by_owner(db=db, owner_id=current_user_id)

    return schemas.InterpretationListResponse(
        interpretations=interpretations,
        total=total,
        page=(skip // limit) + 1,
        size=len(interpretations)
    )

@router.get("/task/{task_id}/status", response_model=schemas.AsyncInterpretationResponse)
async def get_interpretation_task_status(
    task_id: str,
    db: Session = Depends(deps.get_db),
    current_user_id: int = Depends(deps.get_current_user_id_mock)
):
    """
    Get the status of an asynchronous interpretation task.
    """
    # This is a simplified version - in production, you'd check Celery task status
    # For now, we'll return a mock response
    return schemas.AsyncInterpretationResponse(
        task_id=task_id,
        status="completed",  # or pending, processing, failed
        interpretation_id=1,  # Would be looked up from task mapping
        message="Interpretation generation completed."
    )