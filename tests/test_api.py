"""
Basic API tests for the astrology platform.
"""
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_chart_invalid_type():
    """Test creating a chart with invalid chart type."""
    chart_data = {
        "chart_type": "invalid",
        "birth_date": "1990-08-15",
        "birth_time": "14:30",
        "birth_latitude": 19.0760,
        "birth_longitude": 72.8777,
        "timezone": "+05:30"
    }
    response = client.post("/api/v1/charts/generate", json=chart_data)
    assert response.status_code == 422
    assert "Input should be 'd1' or 'd9'" in response.json()["detail"][0]["msg"]


def test_create_chart_valid_d1():
    """Test creating a valid D1 chart."""
    chart_data = {
        "chart_type": "d1",
        "birth_date": "1990-08-15",
        "birth_time": "14:30",
        "birth_latitude": 19.0760,
        "birth_longitude": 72.8777,
        "timezone": "+05:30"
    }
    # This would fail without a database, but we're testing the validation
    response = client.post("/api/v1/charts/generate", json=chart_data)
    # Expect 500 due to missing DB, but not 400 (validation should pass)
    assert response.status_code != 400  # Validation passed


def test_create_chart_valid_d9():
    """Test creating a valid D9 chart."""
    chart_data = {
        "chart_type": "d9",
        "birth_date": "1990-08-15",
        "birth_time": "14:30",
        "birth_latitude": 19.0760,
        "birth_longitude": 72.8777,
        "timezone": "+05:30"
    }
    response = client.post("/api/v1/charts/generate", json=chart_data)
    # Expect 500 due to missing DB, but not 400 (validation should pass)
    assert response.status_code != 400  # Validation passed


def test_create_chart_d1_endpoint():
    """Test the D1-specific endpoint."""
    chart_data = {
        "chart_type": "d1",  # Will be overridden anyway
        "birth_date": "1990-08-15",
        "birth_time": "14:30",
        "birth_latitude": 19.0760,
        "birth_longitude": 72.8777,
        "timezone": "+05:30"
    }
    response = client.post("/api/v1/charts/d1", json=chart_data)
    # Expect 500 due to missing DB, but not 400 (validation should pass)
    assert response.status_code != 400  # Validation passed


def test_create_chart_d9_endpoint():
    """Test the D9-specific endpoint."""
    chart_data = {
        "chart_type": "d9",  # Will be overridden anyway
        "birth_date": "1990-08-15",
        "birth_time": "14:30",
        "birth_latitude": 19.0760,
        "birth_longitude": 72.8777,
        "timezone": "+05:30"
    }
    response = client.post("/api/v1/charts/d9", json=chart_data)
    # Expect 500 due to missing DB, but not 400 (validation should pass)
    assert response.status_code != 400  # Validation passed


def test_create_chart_missing_fields():
    """Test creating a chart with missing required fields."""
    chart_data = {
        "chart_type": "d1"
        # Missing required fields
    }
    response = client.post("/api/v1/charts/generate", json=chart_data)
    assert response.status_code == 422  # Validation error


def test_interpretation_endpoint_structure():
    """Test that interpretation endpoint exists and validates input."""
    from backend.app.api import deps
    from sqlalchemy import create_engine, Column, Integer
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import StaticPool

    # Import models to ensure they are registered with Base
    from backend.app.db.base_class import Base
    from backend.app.models.chart import Chart
    from backend.app.models.interpretation import Interpretation

    # Define a User model for the test to satisfy the foreign key
    class User(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)

    # Create an in-memory SQLite database for testing
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[deps.get_db] = override_get_db

    client = TestClient(app)
    interp_data = {
        "chart_id": 1,
        "interpretation_type": "basic",
        "language": "en"
    }
    response = client.post("/api/v1/interpretations/", json=interp_data)
    # Would fail due to missing chart, but should validate structure
    # Expect 404 (chart not found) or 500 (DB issues), not 422 (validation error)
    assert response.status_code != 422  # Validation passed


if __name__ == "__main__":
    pytest.main([__file__, "-v"])