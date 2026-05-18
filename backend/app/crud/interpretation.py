"""
CRUD operations for interpretation model.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from .base import CRUDBase
from ..models.interpretation import Interpretation
from ..schemas.interpretation import InterpretationCreate, InterpretationUpdate

class CRUDInterpretation(CRUDBase[Interpretation, InterpretationCreate, InterpretationUpdate]):
    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Interpretation]:
        return (
            db.query(self.model)
            .filter(Interpretation.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_count_by_owner(self, db: Session, *, owner_id: int) -> int:
        return db.query(self.model).filter(Interpretation.owner_id == owner_id).count()

    def create_with_owner(
        self, db: Session, *, obj_in: InterpretationCreate, owner_id: int
    ) -> Interpretation:
        obj_in_data = obj_in.model_dump()
        obj_in_data["user_id"] = owner_id
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

interpretation = CRUDInterpretation(Interpretation)