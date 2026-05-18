"""
Background worker for chart generation tasks.
Integrates with astrology_engine for actual chart calculations.
"""
import asyncio
import logging
from typing import Dict, Any
from datetime import date
from backend.app import crud
from backend.app.db.session import SessionLocal
from backend.app.services.chart_service import ChartService
from backend.app.schemas.chart import ChartCreate, ChartType

logger = logging.getLogger(__name__)

def generate_chart_task(
    chart_id: int,
    chart_type: str,
    birth_date: date,
    birth_time: str,
    birth_latitude: float,
    birth_longitude: float,
    timezone: str,
    task_id: str
) -> Dict[str, Any]:
    """
    Generate astrological chart calculations using astrology_engine.
    This would be implemented as a Celery task in production.

    Args:
        chart_id: Database ID of the chart record
        chart_type: Type of chart (d1, d9, etc.)
        birth_date: Date of birth
        birth_time: Time of birth (HH:MM)
        birth_latitude: Latitude of birth place
        birth_longitude: Longitude of birth place
        timezone: Timezone offset
        task_id: Unique task identifier for tracking

    Returns:
        Dictionary with task result information
    """
    logger.info(f"Starting chart generation task {task_id} for chart {chart_id}")

    # Create chart input data
    chart_in = ChartCreate(
        chart_type=ChartType.D9 if chart_type.lower() == "d9" else ChartType.D1,
        birth_date=birth_date,
        birth_time=birth_time,
        birth_latitude=birth_latitude,
        birth_longitude=birth_longitude,
        timezone=timezone
    )

    db = SessionLocal()
    try:
        # Create chart service with dependency injection
        from backend.app.services.astrology_service import AstrologyService
        astrology_service_instance = AstrologyService()
        chart_service = ChartService(db, astrology_service_instance)

        # Calculate chart using asyncio to run the async service method
        # We need to run the async function in a synchronous context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            chart_response = loop.run_until_complete(
                chart_service.calculate_chart_from_input(chart_in)
            )
        finally:
            loop.close()

        # Extract data for database storage
        planetary_positions = [
            {
                "planet": pos.planet.value,
                "longitude": pos.longitude,
                "latitude": pos.latitude,
                "speed": pos.speed,
                "sign": pos.sign.value,
                "house": pos.house.value,
                "is_retrograde": pos.is_retrograde
            }
            for pos in chart_response.planetary_positions
        ]

        house_cusps = [
            {
                "house": cusp.house.value,
                "longitude": cusp.longitude,
                "sign": cusp.sign.value
            }
            for cusp in chart_response.house_cusps
        ]

        # Update chart with calculated data
        updated_chart = chart_service.update_chart_data(
            chart_id=chart_id,
            planetary_positions=planetary_positions,
            house_cusps=house_cusps
        )

        if updated_chart:
            logger.info(f"Chart generation task {task_id} completed successfully")
            return {
                "status": "completed",
                "chart_id": chart_id,
                "task_id": task_id,
                "message": "Chart generation completed"
            }
        else:
            logger.error(f"Chart generation task {task_id} failed: chart not found")
            return {
                "status": "failed",
                "chart_id": chart_id,
                "task_id": task_id,
                "error": "Chart not found"
            }

    except Exception as e:
        logger.error(f"Chart generation task {task_id} failed with error: {str(e)}")
        return {
            "status": "failed",
            "chart_id": chart_id,
            "task_id": task_id,
            "error": str(e)
        }
    finally:
        db.close()