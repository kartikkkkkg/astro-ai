"""
SQLAlchemy model for astrological charts.
"""
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, DateTime, Date, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.base_class import Base

class Chart(Base):
    __tablename__ = "charts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    chart_type = Column(String(10), nullable=False)  # d1, d9, etc.
    birth_date = Column(Date, nullable=False)
    birth_time = Column(String(5), nullable=False)  # HH:MM format
    birth_latitude = Column(Float, nullable=False)
    birth_longitude = Column(Float, nullable=False)
    timezone = Column(String(10), nullable=False, default="+00:00")

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    interpretations = relationship("Interpretation", back_populates="chart", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Chart(id={self.id}, chart_type='{self.chart_type}', birth_date='{self.birth_date}')>"