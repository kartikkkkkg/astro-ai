"""
Service layer for chart-related operations.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from backend.app import crud, models, schemas
from backend.app.services.astrology_service import AstrologyService
import logging

logger = logging.getLogger(__name__)

class ChartService:
    def __init__(self, db: Session, astrology_service: Optional[AstrologyService] = None):
        self.db = db
        self.astrology_service = astrology_service or AstrologyService()

    def get_chart_with_relations(self, chart_id: int) -> Optional[models.Chart]:
        """Get chart with pre-loaded relationships."""
        return self.db.query(models.Chart).filter(models.Chart.id == chart_id).first()

    def update_chart_data(
        self,
        chart_id: int,
        planetary_positions: List[Dict[str, Any]],
        house_cusps: List[Dict[str, Any]]
    ) -> Optional[models.Chart]:
        """Update chart with calculated astrological data."""
        chart = self.get_chart_with_relations(chart_id)
        if not chart:
            return None

        # In a real implementation, we'd store this in related tables
        # For MVP, we'll add as JSON fields or create related models
        # This is a placeholder for the actual implementation

        self.db.commit()
        self.db.refresh(chart)
        return chart

    async def calculate_chart_from_input(
        self,
        chart_in: schemas.ChartCreate
    ) -> schemas.ChartResponse:
        """
        Calculate chart from input data using astrology engine.

        Args:
            chart_in: Chart creation data

        Returns:
            ChartResponse with calculated data
        """
        try:
            # Use the astrology service to calculate the chart
            chart_response = await astrology_service.calculate_chart(chart_in)
            return chart_response
        except Exception as e:
            logger.error(f"Chart calculation failed: {e}")
            # Re-raise to be handled by the endpoint
            raise

# Factory function to create ChartService instances per request
def get_chart_service(
    db: Session,
    astrology_service: AstrologyService
) -> ChartService:
    return ChartService(db, astrology_service)