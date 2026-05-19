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
    Parse timezone string (e.g., '+05:30', 'EST', 'PST') to offset in hours.

    Args:
        timezone_str: Timezone offset string like '+05:30', '-04:00', 'EST', 'PST', etc.

    Returns:
        Offset in hours as float
    """
    # Handle common timezone abbreviations
    tz_abbrev_to_offset = {
        'EST': -5.0,  # Eastern Standard Time
        'EDT': -4.0,  # Eastern Daylight Time
        'CST': -6.0,  # Central Standard Time
        'CDT': -5.0,  # Central Daylight Time
        'MST': -7.0,  # Mountain Standard Time
        'MDT': -6.0,  # Mountain Daylight Time
        'PST': -8.0,  # Pacific Standard Time
        'PDT': -7.0,  # Pacific Daylight Time
        'AKST': -9.0, # Alaska Standard Time
        'AKDT': -8.0, # Alaska Daylight Time
        'HST': -10.0, # Hawaii Standard Time
        'HDT': -9.0,  # Hawaii Daylight Time
        'UTC': 0.0,
        'GMT': 0.0,
    }

    if timezone_str.upper() in tz_abbrev_to_offset:
        return tz_abbrev_to_offset[timezone_str.upper()]

    # Handle ISO format like '+05:30' or '-04:00'
    if len(timezone_str) >= 3 and (timezone_str[0] == '+' or timezone_str[0] == '-'):
        sign = 1 if timezone_str[0] == '+' else -1
        try:
            hours = int(timezone_str[1:3])
            minutes = int(timezone_str[4:6]) if len(timezone_str) > 5 else 0
            return sign * (hours + minutes/60.0)
        except ValueError:
            # Fallback to 0 if parsing fails
            return 0.0

    # Default to UTC if unrecognized
    return 0.0

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