"""
Service layer for interpretation-related operations.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from backend.app import crud, models, schemas

class InterpretationService:
    def __init__(self, db: Session):
        self.db = db

    def get_interpretation_with_chart(self, interpretation_id: int) -> Optional[models.Interpretation]:
        """Get interpretation with pre-loaded chart relationship."""
        return (
            self.db.query(models.Interpretation)
            .filter(models.Interpretation.id == interpretation_id)
            .first()
        )

    def update_interpretation_content(
        self,
        interpretation_id: int,
        content: str,
        quality_score: Optional[float] = None,
        tokens_used: Optional[int] = None,
        processing_time_ms: Optional[int] = None
    ) -> Optional[models.Interpretation]:
        """Update interpretation with AI-generated content."""
        interpretation = self.db.query(models.Interpretation).filter(
            models.Interpretation.id == interpretation_id
        ).first()
        if not interpretation:
            return None

        interpretation.content = content
        if quality_score is not None:
            interpretation.quality_score = quality_score
        if tokens_used is not None:
            interpretation.tokens_used = tokens_used
        if processing_time_ms is not None:
            interpretation.processing_time_ms = processing_time_ms

        self.db.commit()
        self.db.refresh(interpretation)
        return interpretation

# Factory function to create InterpretationService instances per request
def get_interpretation_service(db: Session) -> InterpretationService:
    return InterpretationService(db)