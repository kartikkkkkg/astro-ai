# Backend Integration Documentation

## Overview

This document describes the integration of the `astrology_engine` package into the FastAPI backend. The integration maintains clean architecture boundaries, preserves deterministic calculations, and provides a production-grade API for chart generation.

## Architecture

### Service Layer

The `AstrologyService` in `backend/app/services/astrology_service.py` serves as the adapter between the FastAPI application and the `astrology_engine` package:

- **Dependency Injection**: The service is instantiated as a singleton (`astrology_service`) and can be dependency-injected where needed
- **Async-Safe Wrappers**: All calculation methods use `ThreadPoolExecutor` to avoid blocking the event loop
- **Data Transformation**: Converts between `astrology_engine` internal models and API Pydantic schemas
- **Error Handling**: Properly translates engine exceptions to HTTP error responses

### Key Components

1. **AstrologyService** (`backend/app/services/astrology_service.py`)
   - Wraps `ChartCalculator` and `DivisionalChartService` from `astrology_engine`
   - Provides async methods for chart calculation
   - Includes fallback mock implementations for development
   - Handles data conversion between engine models and API schemas

2. **ChartService Updates** (`backend/app/services/chart_service.py`)
   - Integrated with `AstrologyService` for actual chart calculations
   - Maintains existing database update workflow
   - Provides `calculate_chart_from_input` method for endpoints

3. **Worker Updates** (`backend/app/workers/chart_generation.py`)
   - Uses the updated `ChartService` for actual calculations
   - Maintains background task interface for database updates
   - Properly handles async/sync boundaries

4. **API Endpoints** (`backend/app/api/v1/endpoints/charts.py`)
   - `/generate`: Main endpoint for chart calculation with actual engine integration
   - `/d1`: Convenience endpoint for D1 (natal) chart generation
   - `/d9`: Convenience endpoint for D9 (navamsha) chart generation
   - Preserves backward compatibility with existing endpoints

## API Endpoints

### Chart Generation

#### POST `/api/v1/charts/generate`
Generate a chart with actual astrological calculations.

**Request Body:**
```json
{
  "chart_type": "d1",
  "birth_date": "1990-08-15",
  "birth_time": "14:30",
  "birth_latitude": 19.0760,
  "birth_longitude": 72.8777,
  "timezone": "+05:30"
}
```

**Response:**
```json
{
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
      "is_retrograde": false
    }
    // ... more planets
  ],
  "house_cusps": [
    {
      "house": "1",
      "longitude": 23.5,
      "sign": "Aries"
    }
    // ... more houses
  ],
  "divisional_data": null
}
```

#### POST `/api/v1/charts/d1`
Generate a D1 (natal) chart.

Same request/response format as `/generate`, but chart_type is forced to "d1".

#### POST `/api/v1/charts/d9`
Generate a D9 (navamsha) chart.

Same request/response format as `/generate`, but chart_type is forced to "d9".

### Health Check

#### GET `/api/v1/health`
Returns service health status.

**Response:**
```json
{
  "status": "healthy",
  "service": "astrology-api"
}
```

## Validations

The API implements comprehensive input validation:

1. **Chart Type**: Must be "d1" or "d9"
2. **Birth Date**: Valid date (YYYY-MM-DD)
3. **Birth Time**: Valid time format (HH:MM, 24-hour)
4. **Latitude**: Between -90 and 90 degrees
5. **Longitude**: Between -180 and 180 degrees
6. **Timezone**: Valid offset format (±HH:MM)

## Deterministic Calculations

The integration preserves the deterministic nature of the `astrology_engine`:

- Same input always produces identical output
- Uses Swiss Ephemeris for astronomical calculations
- Consistent house system (Placidus)
- Standard Lahiri ayanamsa (configurable)
- No randomness or external state in calculations

## Error Handling

Standard HTTP error responses:

- **400 Bad Request**: Invalid chart type or validation errors
- **422 Unprocessable Entity**: Pydantic validation failures
- **500 Internal Server Error**: Calculation or database errors
- **404 Not Found**: Chart not found (for GET endpoints)
- **403 Forbidden**: Insufficient permissions

## Usage Examples

### Python Requests

```python
import requests
import json

url = "http://localhost:8000/api/v1/charts/d1"
payload = {
    "chart_type": "d1",
    "birth_date": "1990-08-15",
    "birth_time": "14:30",
    "birth_latitude": 19.0760,
    "birth_longitude": 72.8777,
    "timezone": "+05:30"
}

response = requests.post(url, json=payload)
if response.status_code == 201:
    chart_data = response.json()
    print(f"Sun position: {chart_data['planetary_positions'][0]['longitude']}°")
else:
    print(f"Error: {response.status_code} - {response.json()}")
```

### cURL

```bash
curl -X POST "http://localhost:8000/api/v1/charts/d9" \
  -H "Content-Type: application/json" \
  -d '{
    "chart_type": "d9",
    "birth_date": "1990-08-15",
    "birth_time": "14:30",
    "birth_latitude": 19.0760,
    "birth_longitude": 72.8777,
    "timezone": "+05:30"
  }'
```

## Development Notes

### Mock Mode

When `astrology_engine` is not available (e.g., during initial development), the service falls back to mock implementations that return deterministic but approximate values. This allows API development to proceed without the full engine installed.

### Production Deployment

For production:
1. Ensure `astrology_engine` is installed and accessible
2. Configure appropriate Ayanamsa settings if needed
3. Monitor service performance under load
4. Consider caching frequently requested charts

## Future Enhancements

1. **Additional Divisional Charts**: Support for D2, D3, D10, D30, D60, etc.
2. **Chart Caching**: Implement Redis caching for repeated requests
3. **Batch Operations**: Generate multiple charts in a single request
4. **Advanced Validation**: More specific geographic and temporal validation
5. **Analytics**: Track calculation performance and usage patterns

## Testing

Run the integration tests:
```bash
python -m pytest tests/test_astrology_integration.py -v
```

Note: Full testing requires a test database setup. The tests focus on API validation and service integration.