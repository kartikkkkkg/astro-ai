# API Contracts for AI Astrology Platform (MVP)

This document defines the clean API contracts and request/response schemas for the MVP of the AI astrology platform.

## Overview

**Version**: v1  
**Base URL**: `/api/v1`  
**Framework**: FastAPI with Pydantic models for validation  
**Async Processing**: Background tasks for long-running operations (chart generation, AI interpretation)

## Endpoint Naming Conventions

- **Resource-based naming**: `/charts`, `/interpretations`
- **HTTP Methods**: 
  - `POST` for creation
  - `GET` for retrieval
  - `POST` with specific actions for regeneration/retries
- **Versioned**: All endpoints under `/api/v1/`
- **Plural nouns** for collections: `/charts` (not `/chart`)

## Error Response Schema

All error responses follow this format:

```json
{
  "detail": "Human-readable error message",
  "error_code": "OPTIONAL_SPECIFIC_ERROR_CODE",
  "timestamp": "ISO_8601_TIMESTAMP",
  "path": "/the/requested/path"
}
```

HTTP Status Codes:
- `200`: Success
- `201`: Created
- `202`: Accepted (for async operations)
- `400`: Bad Request (validation errors)
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `422`: Unprocessable Entity (validation failed)
- `500`: Internal Server Error
- `503`: Service Unavailable

## Core Endpoints

### 1. Chart Generation Endpoints

#### POST `/api/v1/charts/`
Create a new astrological chart (D1 or D9).

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

**Field Requirements:**
- `chart_type`: "d1" or "d9" (future: extensible to other divisional charts)
- `birth_date`: YYYY-MM-DD format
- `birth_time`: HH:MM format (24-hour)
- `birth_latitude`: -90 to 90 decimal degrees
- `birth_longitude`: -180 to 180 decimal degrees
- `timezone`: UTC offset format (+/-HH:MM)

**Success Response (201):**
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
  "planetary_positions": [],
  "house_cusps": []
}
```

*Note: Chart data is populated asynchronously by background workers.*

#### GET `/api/v1/charts/{chart_id}`
Retrieve a specific chart by ID.

**Response (200):**
Same structure as creation response, but with populated `planetary_positions` and `house_cusps` arrays.

#### GET `/api/v1/charts/`
List user's charts with pagination.

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum records to return (default: 100)

**Response (200):**
```json
{
  "charts": [
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
      "planetary_positions": [...],
      "house_cusps": [...]
    }
  ],
  "total": 1,
  "page": 1,
  "size": 1
}
```

#### POST `/api/v1/charts/{chart_id}/regenerate`
Regenerate an existing chart.

**Response (200):**
Same as chart creation response - returns chart with placeholder data that will be updated asynchronously.

### 2. AI Interpretation Endpoints

#### POST `/api/v1/interpretations/`
Generate AI interpretation for a chart (async processing).

**Request Body:**
```json
{
  "chart_id": 1,
  "interpretation_type": "basic",
  "language": "en"
}
```

**Field Requirements:**
- `chart_id`: Existing chart ID that belongs to the user
- `interpretation_type`: "basic" (future: "detailed", "relationship", "career")
- `language`: ISO 639-1 language code (default: "en")

**Success Response (202 Accepted):**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "interpretation_id": 1,
  "message": "Interpretation generation started. Results will be available shortly."
}
```

#### GET `/api/v1/interpretations/{interpretation_id}`
Retrieve a specific interpretation by ID.

**Response (200):**
```json
{
  "id": 1,
  "chart_id": 1,
  "user_id": 1,
  "interpretation_type": "basic",
  "language": "en",
  "model_used": "gpt-4",
  "content": "The Sun in Leo in the 5th house indicates strong creative expression and leadership qualities...",
  "quality_score": 0.85,
  "tokens_used": 450,
  "processing_time_ms": 2500,
  "created_at": "2024-01-15T10:35:00Z",
  "updated_at": "2024-01-15T10:35:00Z"
}
```

#### GET `/api/v1/interpretations/`
List user's interpretations with pagination.

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum records to return (default: 100)

**Response (200):**
Same structure as single interpretation response, wrapped in a list with pagination metadata.

#### GET `/api/v1/interpretations/task/{task_id}/status`
Check status of an asynchronous interpretation task.

**Response (200):**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "interpretation_id": 1,
  "message": "Interpretation generation completed."
}
```

*Status values: "pending", "processing", "completed", "failed"*

### 3. Health Check Endpoints

#### GET `/api/v1/health/`
Basic health check.

**Response (200):**
```json
{
  "status": "healthy",
  "service": "astrology-api"
}
```

#### GET `/`
Root endpoint (no version prefix).

**Response (200):**
```json
{
  "message": "AI Astrology Platform API is running"
}
```

## Data Models

### Chart Structure

```javascript
{
  "id": Integer,
  "user_id": Integer,
  "chart_type": String ("d1", "d9", ...),
  "birth_date": Date,
  "birth_time": String (HH:MM),
  "birth_latitude": Float,
  "birth_longitude": Float,
  "timezone": String (+/-HH:MM),
  "created_at": DateTime,
  "updated_at": DateTime,
  "planetary_positions": [
    {
      "planet": String ("Sun", "Moon", "Mars", ...),
      "longitude": Float (0-360 degrees),
      "latitude": Float (usually 0 for geocentric),
      "speed": Float (daily motion in degrees),
      "sign": String ("Aries", "Taurus", ...),
      "house": String ("1", "2", ..., "12"),
      "is_retrograde": Boolean
    }
  ],
  "house_cusps": [
    {
      "house": String ("1", "2", ..., "12"),
      "longitude": Float (0-360 degrees),
      "sign": String ("Aries", "Taurus", ...)
    }
  ]
}
```

### Interpretation Structure

```javascript
{
  "id": Integer,
  "chart_id": Integer,
  "user_id": Integer,
  "interpretation_type": String ("basic", "detailed", ...),
  "language": String ("en", "es", ...),
  "model_used": String (nullable, e.g., "gpt-4", "claude-3"),
  "content": String (the actual interpretation text),
  "quality_score": Float (0.0-1.0, nullable),
  "tokens_used": Integer (nullable),
  "processing_time_ms": Integer (nullable),
  "created_at": DateTime,
  "updated_at": DateTime
}
```

## Async Processing Strategy

### Why Async?
- Chart generation: Astronomical calculations can be computationally intensive
- AI interpretation: LLM API calls can take several seconds
- User experience: Prevent blocking HTTP requests

### Implementation
- **Background Tasks**: FastAPI `BackgroundTasks` for simple async operations
- **Future**: Celery with Redis broker for production-scale async processing
- **Task Tracking**: UUID-based task IDs for status checking
- **Database Updates**: Workers update records when processing completes

### Flow
1. User requests chart/interpretation creation
2. API creates pending database record
3. Background task is triggered with record ID
4. Worker processes the request (chart calculation or AI generation)
5. Worker updates database record with results
6. User polls endpoint or checks task status for completion

## Extensibility Features

### Adding New Chart Types (D10, D60, etc.)
1. Add new value to `ChartType` enum in schemas
2. Update validation in chart creation endpoint
3. Implement calculation logic in astrology-engine service
4. No API contract changes needed - existing endpoints automatically support new types

### Adding New Interpretation Types
1. Add new value to `InterpretationType` enum in schemas
2. Update validation in interpretation creation endpoint
3. Implement logic in AI layer service
4. No API contract changes needed

### Future Multi-Agent Support
The interpretation endpoint is designed to support future multi-agent reasoning:
- Current: Single AI model generates interpretation
- Future: Orchestrator dispatches to specialized agents (life path, relationship, career, etc.)
- Response format remains the same - only internal processing changes

## Security Considerations

### Input Validation
- All inputs validated via Pydantic models
- Birth coordinates validated for realistic ranges
- Time format strictly enforced
- Chart types restricted to supported values

### Authentication (MVP Placeholder)
- Current: Mock dependency returns fixed user ID (1)
- Production: Replace with JWT validation
- All endpoints verify resource ownership

### Rate Limiting
- Configured in settings (60 requests/minute default)
- Implement via middleware in production

## Example Usage Flow

### Chart Generation + Interpretation
1. **POST** `/api/v1/charts/` with birth data → Returns chart ID immediately
2. **Poll** `/api/v1/charts/{id}` or wait for webhook (future) until chart data populated
3. **POST** `/api/v1/interpretations/` with chart ID → Returns task ID immediately
4. **Poll** `/api/v1/interpretations/task/{task_id}/status` until "completed"
5. **GET** `/api/v1/interpretations/{id}` to retrieve final interpretation

### Chart Regeneration
1. **POST** `/api/v1/charts/{id}/regenerate` → Returns chart with cleared data
2. **Poll** chart endpoint until background worker repopulates data