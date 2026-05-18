"""
Pydantic schemas for chart-related requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum

class ChartType(str, Enum):
    D1 = "d1"
    D9 = "d9"
    # Future: D2, D3, D10, D60, etc.

class Planet(str, Enum):
    SUN = "Sun"
    MOON = "Moon"
    MARS = "Mars"
    MERCURY = "Mercury"
    JUPITER = "Jupiter"
    VENUS = "Venus"
    SATURN = "Saturn"
    RAHU = "Rahu"
    KETU = "Ketu"

class House(str, Enum):
    HOUSE_1 = "1"
    HOUSE_2 = "2"
    HOUSE_3 = "3"
    HOUSE_4 = "4"
    HOUSE_5 = "5"
    HOUSE_6 = "6"
    HOUSE_7 = "7"
    HOUSE_8 = "8"
    HOUSE_9 = "9"
    HOUSE_10 = "10"
    HOUSE_11 = "11"
    HOUSE_12 = "12"

class ZodiacSign(str, Enum):
    ARIES = "Aries"
    TAURUS = "Taurus"
    GEMINI = "Gemini"
    CANCER = "Cancer"
    LEO = "Leo"
    VIRGO = "Virgo"
    LIBRA = "Libra"
    SCORPIO = "Scorpio"
    SAGITTARIUS = "Sagittarius"
    CAPRICORN = "Capricorn"
    AQUARIUS = "Aquarius"
    PISCES = "Pisces"

class PlanetaryPosition(BaseModel):
    planet: Planet
    longitude: float = Field(..., ge=0, lt=360, description="Longitude in degrees")
    latitude: float = Field(default=0.0, description="Latitude in degrees")
    speed: float = Field(default=0.0, description="Daily motion in degrees")
    sign: ZodiacSign
    house: House
    is_retrograde: bool = False

class HouseCusp(BaseModel):
    house: House
    longitude: float = Field(..., ge=0, lt=360, description="House cusp longitude in degrees")
    sign: ZodiacSign

class ChartBase(BaseModel):
    chart_type: ChartType
    birth_date: date
    birth_time: str = Field(..., pattern=r"^([0-1][0-9]|2[0-3]):[0-5][0-9]$")
    birth_latitude: float = Field(..., ge=-90, le=90)
    birth_longitude: float = Field(..., ge=-180, le=180)
    timezone: str = Field(default="+00:00")

class ChartCreate(ChartBase):
    pass


class ChartUpdate(BaseModel):
    chart_type: Optional[ChartType] = None
    birth_date: Optional[date] = None
    birth_time: Optional[str] = None
    birth_latitude: Optional[float] = None
    birth_longitude: Optional[float] = None
    timezone: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class ChartInDBBase(ChartBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }

class ChartResponse(ChartInDBBase):
    planetary_positions: List[PlanetaryPosition]
    house_cusps: List[HouseCusp]
    # Future fields for advanced charts
    divisional_data: Optional[Dict[str, Any]] = None

class ChartListResponse(BaseModel):
    charts: List[ChartResponse]
    total: int
    page: int
    size: int

# Example request/response payloads (for documentation)
CHART_CREATE_EXAMPLE = {
    "chart_type": "d1",
    "birth_date": "1990-08-15",
    "birth_time": "14:30",
    "birth_latitude": 19.0760,
    "birth_longitude": 72.8777,
    "timezone": "+05:30"
}

CHART_RESPONSE_EXAMPLE = {
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
        # ... more planets
    ],
    "house_cusps": [
        {
            "house": "1",
            "longitude": 23.5,
            "sign": "Aries"
        }
        # ... more houses
    ]
}