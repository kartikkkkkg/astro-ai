"""
Chart generation and retrieval endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import logging

from app.crud import crud
from app import schemas
from app.schemas.chart import ChartType
from app.api import deps
from app.services.chart_service import get_chart_service
from app.services.astrology_service import AstrologyService
from app.workers.chart_generation import generate_chart_task

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/generate", response_model=schemas.ChartResponse, status_code=status.HTTP_201_CREATED)
async def generate_chart(
    *,
    db: Session = Depends(deps.get_db),
    chart_in: schemas.ChartCreate,
    background_tasks: BackgroundTasks,
    current_user_id: int = Depends(deps.get_current_user_id_mock)
):
    """
    Generate a new astrological chart (D1 or D9) with actual calculations.
    """
    # Validate chart type
    if chart_in.chart_type not in [ChartType.D1, ChartType.D9]:
        raise HTTPException(
            status_code=400,
            detail=f"Chart type {chart_in.chart_type.value} not supported. Supported types: d1, d9"
        )

    try:
        # Calculate chart using astrology engine
        chart_service_instance = get_chart_service(db)
        chart_response = await chart_service_instance.calculate_chart_from_input(chart_in)

        # Create chart record in database with calculated data
        chart = crud.chart.create_with_owner(
            db=db, obj_in=chart_in, owner_id=current_user_id
        )

        # TODO: Store calculated data in database (for now, we'll rely on async worker)
        # Trigger async chart generation to update database
        task_id = str(uuid.uuid4())
        background_tasks.add_task(
            generate_chart_task,
            chart_id=chart.id,
            chart_type=chart_in.chart_type.value,
            birth_date=chart_in.birth_date,
            birth_time=chart_in.birth_time,
            birth_latitude=chart_in.birth_latitude,
            birth_longitude=chart_in.birth_longitude,
            timezone=chart_in.timezone,
            task_id=task_id
        )

        # Set the IDs in the response (these would come from the database in a real implementation)
        chart_response.id = chart.id
        chart_response.user_id = chart.user_id

        return chart_response

    except Exception as e:
        logger.error(f"Chart generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Chart generation failed: {str(e)}"
        )

@router.post("/d1", response_model=schemas.ChartResponse, status_code=status.HTTP_201_CREATED)
async def generate_d1_chart(
    *,
    db: Session = Depends(deps.get_db),
    chart_in: schemas.ChartCreate,
    background_tasks: BackgroundTasks,
    current_user_id: int = Depends(deps.get_current_user_id_mock)
):
    """
    Generate a new D1 (natal) chart with actual calculations.
    """
    # Force chart type to D1
    chart_in.chart_type = schemas.ChartType.D1

    # Delegate to the general generate endpoint
    return await generate_chart(
        db=db,
        chart_in=chart_in,
        background_tasks=background_tasks,
        current_user_id=current_user_id
    )

@router.post("/d9", response_model=schemas.ChartResponse, status_code=status.HTTP_201_CREATED)
async def generate_d9_chart(
    *,
    db: Session = Depends(deps.get_db),
    chart_in: schemas.ChartCreate,
    background_tasks: BackgroundTasks,
    current_user_id: int = Depends(deps.get_current_user_id_mock)
):
    """
    Generate a new D9 (navamsha) chart with actual calculations.
    """
    # Force chart type to D9
    chart_in.chart_type = schemas.ChartType.D9

    # Delegate to the general generate endpoint
    return await generate_chart(
        db=db,
        chart_in=chart_in,
        background_tasks=background_tasks,
        current_user_id=current_user_id
    )

@router.post("", response_model=schemas.ChartResponse, status_code=status.HTTP_201_CREATED)
async def create_chart(
    *,
    db: Session = Depends(deps.get_db),
    chart_in: schemas.ChartCreate,
    background_tasks: BackgroundTasks,
    current_user_id: int = Depends(deps.get_current_user_id_mock)
):
    """
    Generate a new astrological chart (D1 or D9) - placeholder version for backward compatibility.
    For actual calculations, use /generate, /d1, or /d9 endpoints.
    """
    # Validate chart type
    if chart_in.chart_type not in [ChartType.D1, ChartType.D9]:
        raise HTTPException(
            status_code=400,
            detail=f"Chart type {chart_in.chart_type.value} not supported. Supported types: d1, d9"
        )

    # Create chart record in database
    chart = crud.chart.create_with_owner(
        db=db, obj_in=chart_in, owner_id=current_user_id
    )

    # Trigger async chart generation (placeholder)
    task_id = str(uuid.uuid4())
    background_tasks.add_task(
        generate_chart_task,
        chart_id=chart.id,
        chart_type=chart_in.chart_type,
        birth_date=chart_in.birth_date,
        birth_time=chart_in.birth_time,
        birth_latitude=chart_in.birth_latitude,
        birth_longitude=chart_in.birth_longitude,
        timezone=chart_in.timezone,
        task_id=task_id
    )

    # Return chart with placeholder data (will be updated by worker)
    chart_dict = schemas.ChartResponse.model_validate(chart, from_attributes=True).model_dump()
    chart_dict.update({
        "planetary_positions": [],  # Will be populated by worker
        "house_cusps": []           # Will be populated by worker
    })

    return schemas.ChartResponse(**chart_dict)

@router.get("/{chart_id}", response_model=schemas.ChartResponse)
async def get_chart(
    chart_id: int,
    db: Session = Depends(deps.get_db),
    current_user_id: int = Depends(deps.get_current_user_id_mock)
):
    """
    Get a specific chart by ID.
    """
    chart = crud.chart.get(db=db, id=chart_id)
    if not chart:
        raise HTTPException(status_code=404, detail="Chart not found")
    if chart.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return chart

@router.get("", response_model=schemas.ChartListResponse)
async def get_charts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user_id: int = Depends(deps.get_current_user_id_mock)
):
    """
    Retrieve user's charts with pagination.
    """
    charts = crud.chart.get_multi_by_owner(
        db=db, owner_id=current_user_id, skip=skip, limit=limit
    )
    total = crud.chart.get_count_by_owner(db=db, owner_id=current_user_id)

    return schemas.ChartListResponse(
        charts=charts,
        total=total,
        page=(skip // limit) + 1,
        size=len(charts)
    )

@router.post("/{chart_id}/regenerate", response_model=schemas.ChartResponse)
async def regenerate_chart(
    *,
    db: Session = Depends(deps.get_db),
    chart_id: int,
    background_tasks: BackgroundTasks,
    current_user_id: int = Depends(deps.get_current_user_id_mock)
):
    """
    Regenerate an existing chart (useful for recalculations).
    """
    chart = crud.chart.get(db=db, id=chart_id)
    if not chart:
        raise HTTPException(status_code=404, detail="Chart not found")
    if chart.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # Trigger async chart regeneration
    task_id = str(uuid.uuid4())
    background_tasks.add_task(
        generate_chart_task,
        chart_id=chart.id,
        chart_type=chart.chart_type,
        birth_date=chart.birth_date,
        birth_time=chart.birth_time,
        birth_latitude=chart.birth_latitude,
        birth_longitude=chart.birth_longitude,
        timezone=chart.timezone,
        task_id=task_id
    )

    # Return chart with placeholder data (will be updated by worker)
    chart_dict = schemas.ChartResponse.model_validate(chart, from_attributes=True).model_dump()
    chart_dict.update({
        "planetary_positions": [],  # Will be populated by worker
        "house_cusps": []           # Will be populated by worker
    })

    return schemas.ChartResponse(**chart_dict)