"""
Data models for astrological calculations.
"""
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from enum import Enum

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

class Nakshatra(str, Enum):
    ASHWINI = "Ashwini"
    BHARANI = "Bharani"
    KRITTIKA = "Krittika"
    ROHINI = "Rohini"
    MRIGASHIRSHA = "Mrigashirsha"
    ARDRA = "Ardra"
    PUNARVASU = "Punarvasu"
    PUSHYA = "Pushya"
    ASHLESHA = "Ashlesha"
    MAGHA = "Magha"
    PURVA_PHALGUNI = "Purva Phalguni"
    UTTARA_PHALGUNI = "Uttara Phalguni"
    HASTA = "Hasta"
    CHITRA = "Chitra"
    SWATI = "Swati"
    VISHAKHA = "Vishakha"
    ANURADHA = "Anuradha"
    JYESHTHA = "Jyeshtha"
    MULA = "Mula"
    PURVA_ASADHA = "Purva Ashadha"
    UTTARA_ASADHA = "Uttara Ashadha"
    SHRAVANA = "Shravana"
    DHANISHTHA = "Dhanishta"
    SHATABHISHA = "Shatabhisha"
    PURVA_BHADRAPADA = "Purva Bhadrapada"
    UTTARA_BHADRAPADA = "Uttara Bhadrapada"
    REVATI = "Revati"

class Aspect(str, Enum):
    CONJUNCTION = "Conjunction"
    SEXTILE = "Sextile"
    SQUARE = "Square"
    TRINE = "Trine"
    OPPOSITION = "Opposition"

class PlanetaryPosition(BaseModel):
    planet: Planet
    longitude: float = Field(..., ge=0, lt=360, description="Longitude in degrees")
    latitude: float = Field(default=0.0, description="Latitude in degrees")
    speed: float = Field(default=0.0, description="Daily motion in degrees")
    sign: ZodiacSign
    house: House
    nakshatra: Nakshatra
    nakshatra_pada: int = Field(..., ge=1, le=4, description="Nakshatra pada (1-4)")
    is_retrograde: bool = False

    @field_validator('longitude')
    @classmethod
    def longitude_must_be_valid(cls, v):
        if not 0 <= v < 360:
            raise ValueError('Longitude must be between 0 and 360 degrees')
        return v

class HouseCusp(BaseModel):
    house: House
    longitude: float = Field(..., ge=0, lt=360, description="House cusp longitude in degrees")
    sign: ZodiacSign

class AspectInfo(BaseModel):
    planet1: Planet
    planet2: Planet
    aspect: Aspect
    orb: float = Field(..., ge=0, description="Orb of aspect in degrees")
    exact: bool = Field(default=False, description="Whether aspect is exact")

class DashaPeriod(BaseModel):
    planet: Planet
    start_date: datetime
    end_date: datetime
    duration_years: float

class ChartBase(BaseModel):
    birth_date: date
    birth_time: str = Field(..., pattern=r"^([0-1][0-9]|2[0-3]):[0-5][0-9]$")
    birth_latitude: float = Field(..., ge=-90, le=90)
    birth_longitude: float = Field(..., ge=-180, le=180)
    timezone: str = Field(default="+00:00")
    ayanamsa: str = Field(default="Lahiri")

class DivisionalChartInfo(BaseModel):
    division: int  # 1 for D1, 2 for D2, 9 for D9, etc.
    multiplier: int  # Used in divisional chart calculation
    description: str

class BaseChart(ChartBase):
    """Base chart containing all calculated data."""
    planetary_positions: List[PlanetaryPosition]
    house_cusps: List[HouseCusp]
    aspects: List[AspectInfo]
    vimshottari_dasha: List[DashaPeriod]
    # Divisional charts will be calculated on demand

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat()
        }
    )