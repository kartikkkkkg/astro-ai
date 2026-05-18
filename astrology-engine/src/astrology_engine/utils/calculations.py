"""
Core astrological calculation utilities.
"""
import math
import swisseph as swe
from typing import List, Tuple, Optional, Dict, Any
from ..core.config import ZODIAC_SIGNS, NAKSHATRAS, PLANETS, DEGREES_PER_SIGN, DEGREES_PER_NAKSHATRA
from ..core.models import PlanetaryPosition, HouseCusp, AspectInfo, Aspect, Planet, ZodiacSign, House, Nakshatra
from ..core.exceptions import CalculationError, SwissEphemerisError
from .coordinates import julian_day, validate_birth_data, parse_timezone
from datetime import datetime, date, time

def normalize_longitude(longitude: float) -> float:
    """
    Normalize longitude to 0-360 range.

    Args:
        longitude: Longitude in degrees (can be negative or >360)

    Returns:
        Normalized longitude between 0 and 360
    """
    while longitude < 0:
        longitude += 360
    while longitude >= 360:
        longitude -= 360
    return longitude

def get_zodiac_sign(longitude: float) -> ZodiacSign:
    """
    Get zodiac sign from longitude.

    Args:
        longitude: Longitude in degrees (0-360)

    Returns:
        Zodiac sign
    """
    normalized_longitude = normalize_longitude(longitude)
    sign_index = int(normalized_longitude // DEGREES_PER_SIGN)
    return ZODIAC_SIGNS[sign_index]

def get_nakshatra(longitude: float) -> Tuple[Nakshatra, int]:
    """
    Get nakshatra and pada from longitude.

    Args:
        longitude: Longitude in degrees (0-360)

    Returns:
        Tuple of (nakshatra, pada)
    """
    normalized_longitude = normalize_longitude(longitude)
    nakshatra_index = int(normalized_longitude // DEGREES_PER_NAKSHATRA)
    pada = int((normalized_longitude % DEGREES_PER_NAKSHATRA) / (DEGREES_PER_NAKSHATRA / 4)) + 1
    return NAKSHATRAS[nakshatra_index], pada

def calculate_planetary_position(julian_day: float, planet_id: int) -> PlanetaryPosition:
    """
    Calculate planetary position for a given Julian Day and planet.

    Args:
        julian_day: Julian Day for calculation
        planet_id: Swiss Ephemeris planet ID

    Returns:
        PlanetaryPosition object
    """
    try:
        # Calculate position with speed
        try:
            result, ret = swe.calc_ut(julian_day, planet_id, swe.FLG_SPEED)
        except swe.Error as e:
            raise SwissEphemerisError(f"Swiss Ephemeris error for planet {planet_id}: {str(e)}")

        longitude = normalize_longitude(result[0])
        latitude = result[1]
        speed = result[3]  # Speed in longitude

        # Get zodiac sign
        sign = get_zodiac_sign(longitude)

        # Get nakshatra and pada
        nakshatra, nakshatra_pada = get_nakshatra(longitude)

        # Determine if retrograde (negative speed for most planets)
        is_retrograde = speed < 0

        # Map Swiss Ephemeris planet ID to our Planet enum
        planet_map = {
            swe.SUN: Planet.SUN,
            swe.MOON: Planet.MOON,
            swe.MARS: Planet.MARS,
            swe.MERCURY: Planet.MERCURY,
            swe.JUPITER: Planet.JUPITER,
            swe.VENUS: Planet.VENUS,
            swe.SATURN: Planet.SATURN,
            swe.MEAN_APOG: Planet.RAHU,  # Rahu is Mean Apogee
            swe.TRUE_NODE: Planet.KETU   # Ketu is True Node
        }

        planet = planet_map.get(planet_id)
        if planet is None:
            raise CalculationError(f"Unsupported planet ID: {planet_id}")

        # For MVP, we'll use equal house system (house calculated separately)
        # House will be determined later based on ascendant
        house = House.HOUSE_1  # Placeholder

        return PlanetaryPosition(
            planet=planet,
            longitude=longitude,
            latitude=latitude,
            speed=speed,
            sign=sign,
            house=house,
            nakshatra=nakshatra,
            nakshatra_pada=nakshatra_pada,
            is_retrograde=is_retrograde
        )

    except Exception as e:
        if isinstance(e, (SwissEphemerisError, CalculationError)):
            raise
        raise CalculationError(f"Failed to calculate planetary position: {str(e)}")

def calculate_house_cusps(julian_day: float, lat: float, lon: float) -> List[HouseCusp]:
    """
    Calculate house cusps using Placidus system (default) or Equal house system.

    Args:
        julian_day: Julian Day for calculation
        lat: Latitude of birth place
        lon: Longitude of birth place

    Returns:
        List of HouseCusp objects for houses 1-12
    """
    try:
        # Calculate houses using Placidus system
        # For Swiss Ephemeris, we need to calculate the ascendant first
        # Then we can calculate house cusps

        # Try different house systems
        house_cusps_list = []

        # For MVP, we'll use Equal house system for simplicity
        # In Equal house system, each house is exactly 30 degrees
        # First house starts at ascendant

        # Calculate ascendant
        try:
            # Try Placidus house system first
            house_result = swe.houses(julian_day, lat, lon, b'P')
            # house_result is a tuple: (cusps, ascmc)
            # ascendant is the first element of ascmc (second tuple)
            ascendant = house_result[1][0]
        except swe.Error:
            # Fallback to Ascendant only if Placidus fails
            try:
                house_result = swe.houses(julian_day, lat, lon, b'A')
                # house_result is a tuple: (cusps, ascmc)
                # ascendant is the first element of ascmc (second tuple)
                ascendant = house_result[1][0]
            except swe.Error as e:
                raise SwissEphemerisError("Failed to calculate ascendant")

        ascendant = normalize_longitude(ascendant)  # Ascendant is already extracted

        # Create house cusps for Equal house system
        for i in range(12):
            house_number = i + 1
            house_longitude = normalize_longitude(ascendant + (i * DEGREES_PER_SIGN))
            sign = get_zodiac_sign(house_longitude)

            house_cusps_list.append(HouseCusp(
                house=House(str(house_number)),
                longitude=house_longitude,
                sign=sign
            ))

        return house_cusps_list

    except Exception as e:
        if isinstance(e, SwissEphemerisError):
            raise
        raise CalculationError(f"Failed to calculate house cusps: {str(e)}")

def calculate_aspects(positions: List[PlanetaryPosition]) -> List[AspectInfo]:
    """
    Calculate aspects between planets.

    Args:
        positions: List of planetary positions

    Returns:
        List of AspectInfo objects
    """
    aspects = []
    from ..core.config import ASPECTS, ASPECT_ORBS

    # Compare each pair of planets
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            pos1 = positions[i]
            pos2 = positions[j]

            # Calculate angular difference
            diff = abs(pos1.longitude - pos2.longitude)
            # Normalize to 0-180 range (shorter arc)
            if diff > 180:
                diff = 360 - diff

            # Check each aspect type
            for aspect_name, exact_angle in ASPECTS.items():
                orb = abs(diff - exact_angle)
                max_orb = ASPECT_ORBS[aspect_name]

                if orb <= max_orb:
                    aspect_enum = Aspect(aspect_name)
                    aspects.append(AspectInfo(
                        planet1=pos1.planet,
                        planet2=pos2.planet,
                        aspect=aspect_enum,
                        orb=orb,
                        exact=(orb < 0.1)  # Consider exact if orb < 0.1 degrees
                    ))
                    break  # Only assign one aspect per pair (closest)

    return aspects

def detect_basic_yogas(positions: List[PlanetaryPosition], house_cusps: List[HouseCusp]) -> List[Dict[str, Any]]:
    """
    Detect basic yogas (planetary combinations) in the chart.
    This is a framework for future expansion.

    Args:
        positions: List of planetary positions
        house_cusps: List of house cusps

    Returns:
        List of detected yogas with descriptions
    """
    yogas = []

    # Create a mapping of planet to house for easy lookup
    planet_house_map = {pos.planet: int(pos.house.value) for pos in positions}

    # Example: Gaja Kesari Yoga (Jupiter in Kendra from Moon)
    jupiter_pos = next((p for p in positions if p.planet == Planet.JUPITER), None)
    moon_pos = next((p for p in positions if p.planet == Planet.MOON), None)

    if jupiter_pos and moon_pos:
        jupiter_house = int(jupiter_pos.house.value)
        moon_house = int(moon_pos.house.value)

        # Kendra houses: 1, 4, 7, 10
        kendra_houses = {1, 4, 7, 10}

        # Check if Jupiter is in Kendra from Moon
        relative_house = ((jupiter_house - moon_house) % 12) + 1
        if relative_house in kendra_houses:
            yogas.append({
                "name": "Gaja Kesari Yoga",
                "description": "Jupiter in Kendra from Moon - indicates wisdom, prosperity, and good fortune",
                "planets_involved": [Planet.JUPITER, Planet.MOON],
                "houses_involved": [jupiter_house, moon_house]
            })

    # Example: Budhaditya Yoga (Mercury conjunct Sun)
    mercury_pos = next((p for p in positions if p.planet == Planet.MERCURY), None)
    sun_pos = next((p for p in positions if p.planet == Planet.SUN), None)

    if mercury_pos and sun_pos:
        # Check if they are conjunct (within orb)
        diff = abs(mercury_pos.longitude - sun_pos.longitude)
        if diff > 180:
            diff = 360 - diff
        if diff <= 8:  # Conjunction orb
            yogas.append({
                "name": "Budhaditya Yoga",
                "description": "Mercury conjunct Sun - indicates intelligence, good communication skills",
                "planets_involved": [Planet.MERCURY, Planet.SUN],
                "houses_involved": [int(mercury_pos.house.value), int(sun_pos.house.value)]
            })

    # Future: Add more yoga detection logic here
    # Raj Yogas, Dhana Yogas, etc.

    return yogas

def calculate_vimshottari_dasha_start(moon_longitude: float) -> Tuple[Planet, float]:
    """
    Calculate the starting planet and elapsed period for Vimshottari Dasha based on Moon's nakshatra.

    Args:
        moon_longitude: Moon's longitude in degrees

    Returns:
        Tuple of (starting_planet, elapsed_percentage)
    """
    from ..core.config import NAKSHATRAS, VIMHOTTARI_DASHA_PERIODS

    # Nakshatra lords for Vimshottari Dasha (in order)
    NAKSHATRA_LORDS = [
        Planet.KETU,    # Ashwini
        Planet.VENUS,   # Bharani
        Planet.SUN,     # Krittika
        Planet.MOON,    # Rohini
        Planet.MARS,    # Mrigashirsha
        Planet.RAHU,    # Ardra
        Planet.JUPITER, # Punarvasu
        Planet.SATURN,  # Pushya
        Planet.MERCURY, # Ashlesha
        Planet.KETU,    # Magha
        Planet.VENUS,   # Purva Phalguni
        Planet.SUN,     # Uttara Phalguni
        Planet.MOON,    # Hasta
        Planet.MARS,    # Chitra
        Planet.RAHU,    # Swati
        Planet.JUPITER, # Vishakha
        Planet.SATURN,  # Anuradha
        Planet.MERCURY, # Jyeshtha
        Planet.KETU,    # Mula
        Planet.VENUS,   # Purva Ashadha
        Planet.SUN,     # Uttara Ashadha
        Planet.MOON,    # Shravana
        Planet.MARS,    # Dhanishta
        Planet.RAHU,    # Shatabhisha
        Planet.JUPITER, # Purva Bhadrapada
        Planet.SATURN,  # Uttara Bhadrapada
        Planet.MERCURY  # Revati
    ]

    # Get nakshatra index
    normalized_longitude = normalize_longitude(moon_longitude)
    nakshatra_index = int(normalized_longitude // DEGREES_PER_NAKSHATRA)

    # Get the nakshatra lord
    starting_planet = NAKSHATRA_LORDS[nakshatra_index]

    # Calculate elapsed percentage in the nakshatra
    nakshatra_start = nakshatra_index * DEGREES_PER_NAKSHATRA
    nakshatra_end = nakshatra_start + DEGREES_PER_NAKSHATRA
    position_in_nakshatra = normalized_longitude - nakshatra_start
    elapsed_percentage = position_in_nakshatra / DEGREES_PER_NAKSHATRA

    return starting_planet, elapsed_percentage

def generate_vimshottari_dasha(starting_planet: Planet, elapsed_percentage: float,
                             start_datetime: datetime) -> List[Dict[str, Any]]:
    """
    Generate Vimshottari Dasha periods.

    Args:
        starting_planet: Planet that starts the dasha cycle
        elapsed_percentage: Percentage already elapsed in the starting planet's period (0-1)
        start_datetime: Starting datetime for the dasha calculation

    Returns:
        List of dasha periods with start/end dates and planets
    """
    from ..core.config import VIMHOTTARI_DASHA_PERIODS
    from datetime import timedelta

    # Order of planets in Vimshottari Dasha cycle
    DASHA_ORDER = [
        Planet.KETU, Planet.VENUS, Planet.SUN, Planet.MOON,
        Planet.MARS, Planet.RAHU, Planet.JUPITER, Planet.SATURN,
        Planet.MERCURY
    ]

    # Find starting index
    try:
        start_index = DASHA_ORDER.index(starting_planet)
    except ValueError:
        # Fallback to Ketu if planet not found
        start_index = 0
        starting_planet = Planet.KETU

    dashas = []
    current_time = start_datetime

    # Process planets in order starting from the calculated index
    for i in range(len(DASHA_ORDER)):
        planet_index = (start_index + i) % len(DASHA_ORDER)
        planet = DASHA_ORDER[planet_index]

        # Get duration for this planet
        total_duration_years = VIMHOTTARI_DASHA_PERIODS[planet]

        # For the starting planet, we've already elapsed some percentage
        if i == 0:
            elapsed_years = total_duration_years * elapsed_percentage
            remaining_years = total_duration_years - elapsed_years
        else:
            elapsed_years = 0
            remaining_years = total_duration_years

        # Calculate period
        period_start = current_time
        period_end = current_time + timedelta(days=remaining_years * 365.25)

        dashas.append({
            "planet": planet,
            "start_date": period_start,
            "end_date": period_end,
            "duration_years": remaining_years,
            "elapsed_years": elapsed_years if i == 0 else 0,
            "total_duration_years": total_duration_years
        })

        # Move to next period
        current_time = period_end

        # If we've completed a full cycle, break
        if i >= len(DASHA_ORDER) - 1:
            break

    return dashas