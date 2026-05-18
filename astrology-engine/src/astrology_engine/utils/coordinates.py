"""
Utilities for handling birth coordinates and time conversions.
"""
import swisseph as swe
from datetime import datetime, date, time
from typing import Tuple
from ..core.config import DEFAULT_AYANAMSA
from ..core.exceptions import InvalidBirthDataError, SwissEphemerisError

def set_ayanamsa(ayanamsa: str = None) -> None:
    """
    Set the ayanamsa for Swiss Ephemeris calculations.

    Args:
        ayanamsa: Ayanamsa name (Lahiri, Raman, etc.). Defaults to Lahiri.
    """
    ayanamsa_map = {
        "Lahiri": swe.SIDM_LAHIRI,
        "Raman": swe.SIDM_RAMAN,
        "Krishnamurti": swe.SIDM_KRISHNAMURTI,
        "True Chitra": swe.SIDM_TRUE_CITRA
    }

    ayanamsa = ayanamsa or DEFAULT_AYANAMSA.value
    if ayanamsa not in ayanamsa_map:
        raise InvalidBirthDataError(f"Unsupported ayanamsa: {ayanamsa}")

    swe.set_sid_mode(ayanamsa_map[ayanamsa])

def julian_day(birth_date: date, birth_time: time, timezone_offset: float) -> float:
    """
    Convert birth date and time to Julian Day for Swiss Ephemeris.

    Args:
        birth_date: Date of birth
        birth_time: Time of birth
        timezone_offset: Timezone offset from UTC in hours (e.g., +5.5 for IST)

    Returns:
        Julian Day as float
    """
    # Convert to UTC time
    utc_time = datetime.combine(birth_date, birth_time)
    # Apply timezone offset (negative because offset is east of UTC)
    utc_time = utc_time.replace(tzinfo=None)  # Remove timezone info for calculation
    # Swiss Ephemeris expects UTC
    return swe.julday(utc_time.year, utc_time.month, utc_time.day,
                     utc_time.hour + utc_time.minute/60.0 + utc_time.second/3600.0)

def parse_timezone(timezone_str: str) -> float:
    """
    Parse timezone string (e.g., '+05:30') to offset in hours.

    Args:
        timezone_str: Timezone offset string like '+05:30' or '-04:00'

    Returns:
        Offset in hours as float
    """
    sign = 1 if timezone_str[0] == '+' else -1
    hours = int(timezone_str[1:3])
    minutes = int(timezone_str[4:6]) if len(timezone_str) > 3 else 0
    return sign * (hours + minutes/60.0)

def validate_birth_data(birth_date: date, birth_time: str,
                       birth_latitude: float, birth_longitude: float) -> Tuple[date, time]:
    """
    Validate and normalize birth data.

    Args:
        birth_date: Date of birth
        birth_time: Time of birth in HH:MM format
        birth_latitude: Latitude in degrees (-90 to 90)
        birth_longitude: Longitude in degrees (-180 to 180)

    Returns:
        Tuple of (validated date, time)

    Raises:
        InvalidBirthDataError: If data is invalid
    """
    # Validate date
    if birth_date > date.today():
        raise InvalidBirthDataError("Birth date cannot be in the future")

    # Validate time format
    try:
        time_obj = datetime.strptime(birth_time, "%H:%M").time()
    except ValueError:
        raise InvalidBirthDataError("Birth time must be in HH:MM format")

    # Validate coordinates
    if not (-90 <= birth_latitude <= 90):
        raise InvalidBirthDataError("Latitude must be between -90 and 90 degrees")

    if not (-180 <= birth_longitude <= 180):
        raise InvalidBirthDataError("Longitude must be between -180 and 180 degrees")

    return birth_date, time_obj