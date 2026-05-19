"""
SQLAlchemy model for AI interpretations.
"""
from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.base_class import Base

class Interpretation(Base):
    __tablename__ = "interpretations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    chart_id = Column(Integer, ForeignKey("charts.id"), nullable=False)
    interpretation_type = Column(String(20), nullable=False)  # basic, detailed, etc.
    language = Column(String(2), nullable=False, default="en")
    model_used = Column(String(50), nullable=True)
    content = Column(Text, nullable=False)
    quality_score = Column(Float, nullable=True)  # 0.0 to 1.0
    tokens_used = Column(Integer, nullable=True)
    processing_time_ms = Column(Integer, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    chart = relationship("Chart", back_populates="interpretations")

    def __repr__(self):
        return f"<Interpretation(id={self.id}, chart_id={self.chart_id}, type='{self.interpretation_type}')>"