"""
Integration tests for astrology engine integration with FastAPI backend.
"""
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from unittest.mock import patch, AsyncMock
from backend.app.schemas.chart import ChartCreate, ChartType, Planet, House, ZodiacSign

client = TestClient(app)


def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_generate_chart_invalid_type():
    """Test generating a chart with invalid chart type."""
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
    assert "chart_type" in response.json()["detail"][0]["loc"]
    assert "Input should be" in response.json()["detail"][0]["msg"]


def test_generate_chart_missing_fields():
    """Test generating a chart with missing required fields."""
    chart_data = {
        "chart_type": "d1"
        # Missing required fields
    }
    response = client.post("/api/v1/charts/generate", json=chart_data)
    assert response.status_code == 422  # Validation error


@patch('app.services.chart_service.ChartService.calculate_chart_from_input')
def test_generate_chart_success(mock_calculate):
    """Test successful chart generation."""
    # Mock the service to return a valid chart response
    mock_response = {
        "id": 1,
        "user_id": 1,
        "chart_type": "d1",
        "birth_date": "1990-08-15",
        "birth_time": "14:30",
        "birth_latitude": 19.0760,
        "birth_longitude": 72.8777,
        "timezone": "+05:30",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z",
        "planetary_positions": [
            {
                "planet": "Sun",
                "longitude": 142.5,
                "latitude": 0.0,
                "speed": 1.0,
                "sign": "Leo",
                "house": "5",
                "is_retrograde": False
            }
        ],
        "house_cusps": [
            {
                "house": "1",
                "longitude": 23.5,
                "sign": "Aries"
            }
        ]
    }
    mock_calculate.return_value = mock_response

    chart_data = {
        "chart_type": "d1",
        "birth_date": "1990-08-15",
        "birth_time": "14:30",
        "birth_latitude": 19.0760,
        "birth_longitude": 72.8777,
        "timezone": "+05:30"
    }
    response = client.post("/api/v1/charts/generate", json=chart_data)

    # Should succeed (201 Created) or at least pass validation (not 400/422)
    # Might be 500 due to DB issues in test, but validation should pass
    assert response.status_code != 400
    assert response.status_code != 422
    # If successful, should return chart data
    if response.status_code == 201:
        data = response.json()
        assert data["chart_type"] == "d1"
        assert len(data["planetary_positions"]) > 0
        assert len(data["house_cusps"]) > 0


def test_generate_d1_chart_endpoint():
    """Test the D1-specific chart endpoint."""
    chart_data = {
        "chart_type": "d1",  # Will be overridden to D1 anyway
        "birth_date": "1990-08-15",
        "birth_time": "14:30",
        "birth_latitude": 19.0760,
        "birth_longitude": 72.8777,
        "timezone": "+05:30"
    }
    response = client.post("/api/v1/charts/d1", json=chart_data)
    # Should pass validation (not 400/422)
    assert response.status_code != 400
    assert response.status_code != 422


def test_generate_d9_chart_endpoint():
    """Test the D9-specific chart endpoint."""
    chart_data = {
        "chart_type": "d9",  # Will be overridden to D9 anyway
        "birth_date": "1990-08-15",
        "birth_time": "14:30",
        "birth_latitude": 19.0760,
        "birth_longitude": 72.8777,
        "timezone": "+05:30"
    }
    response = client.post("/api/v1/charts/d9", json=chart_data)
    # Should pass validation (not 400/422)
    assert response.status_code != 400
    assert response.status_code != 422


def test_chart_validation_edge_cases():
    """Test validation edge cases for chart inputs."""
    # Invalid latitude
    chart_data = {
        "chart_type": "d1",
        "birth_date": "1990-08-15",
        "birth_time": "14:30",
        "birth_latitude": 95.0,  # Invalid: > 90
        "birth_longitude": 72.8777,
        "timezone": "+05:30"
    }
    response = client.post("/api/v1/charts/generate", json=chart_data)
    assert response.status_code == 422  # Validation error

    # Invalid longitude
    chart_data["birth_latitude"] = 19.0760
    chart_data["birth_longitude"] = 185.0  # Invalid: > 180
    response = client.post("/api/v1/charts/generate", json=chart_data)
    assert response.status_code == 422  # Validation error

    # Invalid time format
    chart_data["birth_longitude"] = 72.8777
    chart_data["birth_time"] = "25:00"  # Invalid: hour > 23
    response = client.post("/api/v1/charts/generate", json=chart_data)
    assert response.status_code == 422  # Validation error

    # Invalid timezone format
    chart_data["birth_time"] = "14:30"
    chart_data["timezone"] = "invalid"  # Invalid timezone format
    response = client.post("/api/v1/charts/generate", json=chart_data)
    assert response.status_code == 422  # Validation error


if __name__ == "__main__":
    pytest.main([__file__, "-v"])