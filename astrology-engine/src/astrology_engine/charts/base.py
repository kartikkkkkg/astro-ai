"""
Base chart calculation service.
"""
import swisseph as swe
from datetime import datetime, date, time
from typing import List, Optional, Dict, Any
from ..core.models import BaseChart, PlanetaryPosition, HouseCusp, AspectInfo, House
from ..core.exceptions import InvalidBirthDataError, CalculationError
from ..utils.coordinates import validate_birth_data, parse_timezone, julian_day, set_ayanamsa
from ..utils.calculations import (
    calculate_planetary_position, calculate_house_cusps, calculate_aspects,
    detect_basic_yogas, calculate_vimshottari_dasha_start, generate_vimshottari_dasha
)
from ..core.config import PLANETS as CONFIG_PLANETS, ZODIAC_SIGNS

class ChartCalculator:
    """
    Main chart calculation service for D1 and D9 charts.
    """

    def __init__(self, ayanamsa: str = None):
        """
        Initialize chart calculator.

        Args:
            ayanamsa: Ayanamsa system to use (defaults to Lahiri)
        """
        set_ayanamsa(ayanamsa)
        self.ayanamsa = ayanamsa or "Lahiri"

    def calculate_chart(self, birth_date: date, birth_time: str,
                       birth_latitude: float, birth_longitude: float,
                       timezone: str = "+00:00", chart_type: str = "D1") -> BaseChart:
        """
        Calculate a complete astrological chart.

        Args:
            birth_date: Date of birth
            birth_time: Time of birth in HH:MM format
            birth_latitude: Latitude of birth place
            birth_longitude: Longitude of birth place
            timezone: Timezone offset from UTC (e.g., "+05:30")
            chart_type: Type of chart ("D1" or "D9")

        Returns:
            BaseChart object with all calculations
        """
        # Validate and normalize input
        birth_date, time_obj = validate_birth_data(
            birth_date, birth_time, birth_latitude, birth_longitude
        )
        timezone_offset = parse_timezone(timezone)

        # Calculate Julian Day
        jd = julian_day(birth_date, time_obj, timezone_offset)

        # Calculate planetary positions
        planetary_positions = self._calculate_planetary_positions(jd)

        # Calculate house cusps
        house_cusps = calculate_house_cusps(jd, birth_latitude, birth_longitude)

        # Assign houses to planets based on house cusps
        planetary_positions = self._assign_houses_to_planets(
            planetary_positions, house_cusps
        )

        # Calculate aspects
        aspects = calculate_aspects(planetary_positions)

        # Detect basic yogas
        # basic_yogas = detect_basic_yogas(planetary_positions, house_cusps)
        # For now, we'll skip returning yogas in the model but calculate them internally

        # Calculate Vimshottari Dasha
        vimshottari_dasha = self._calculate_vimshottari_dasha(
            planetary_positions, jd, timezone_offset
        )

        # Create chart object
        chart = BaseChart(
            birth_date=birth_date,
            birth_time=birth_time,
            birth_latitude=birth_latitude,
            birth_longitude=birth_longitude,
            timezone=timezone,
            ayanamsa=self.ayanamsa,
            planetary_positions=planetary_positions,
            house_cusps=house_cusps,
            aspects=aspects,
            vimshottari_dasha=vimshottari_dasha
        )

        # For divisional charts, we'll calculate on demand
        if chart_type.upper() == "D9":
            # Store D1 data and calculate D9 when needed
            pass

        return chart

    def _calculate_planetary_positions(self, julian_day: float) -> List[PlanetaryPosition]:
        """
        Calculate positions for all planets.

        Args:
            julian_day: Julian Day for calculation

        Returns:
            List of PlanetaryPosition objects
        """
        positions = []

        # Map our planets to Swiss Ephemeris IDs
        planet_map = {
            "Sun": swe.SUN,
            "Moon": swe.MOON,
            "Mars": swe.MARS,
            "Mercury": swe.MERCURY,
            "Jupiter": swe.JUPITER,
            "Venus": swe.VENUS,
            "Saturn": swe.SATURN,
            "Rahu": swe.MEAN_APOG,  # Mean Apogee for Rahu
            "Ketu": swe.TRUE_NODE   # True Node for Ketu
        }

        for planet_name, planet_id in planet_map.items():
            try:
                position = calculate_planetary_position(julian_day, planet_id)
                positions.append(position)
            except Exception as e:
                # Log error but continue with other planets
                # In production, we might want to handle this differently
                pass

        return positions

    def _assign_houses_to_planets(self, positions: List[PlanetaryPosition],
                                house_cusps: List[HouseCusp]) -> List[PlanetaryPosition]:
        """
        Assign house numbers to planets based on house cusps.

        Args:
            positions: List of planetary positions
            house_cusps: List of house cusps

        Returns:
            Updated list of planetary positions with house assignments
        """
        # For each planet, find which house it falls in
        for position in positions:
            planet_longitude = position.longitude

            # Find the house cusp that comes just before the planet's longitude
            house_number = 12  # Default to 12th house
            for i, cusp in enumerate(house_cusps):
                cusp_longitude = cusp.longitude
                next_cusp_longitude = house_cusps[(i + 1) % 12].longitude

                # Handle the case where we cross 0 degrees
                if next_cusp_longitude < cusp_longitude:
                    # We're crossing the 0/360 degree boundary
                    if planet_longitude >= cusp_longitude or planet_longitude < next_cusp_longitude:
                        house_number = int(cusp.house.value)
                        break
                else:
                    # Normal case
                    if cusp_longitude <= planet_longitude < next_cusp_longitude:
                        house_number = int(cusp.house.value)
                        break

            # Update the house
            position.house = House(str(house_number))

        return positions

    def _calculate_vimshottari_dasha(self, positions: List[PlanetaryPosition],
                                   julian_day: float, timezone_offset: float) -> List[Dict[str, Any]]:
        """
        Calculate Vimshottari Dasha periods.

        Args:
            positions: List of planetary positions
            julian_day: Julian Day of birth
            timezone_offset: Timezone offset from UTC in hours

        Returns:
            List of dasha periods
        """
        # Find Moon position
        moon_position = None
        for position in positions:
            if position.planet == "Moon":
                moon_position = position
                break

        if not moon_position:
            # Default to Ketu starting if Moon not found
            starting_planet = "Ketu"
            elapsed_percentage = 0.0
        else:
            # Calculate starting planet and elapsed percentage
            starting_planet, elapsed_percentage = calculate_vimshottari_dasha_start(
                moon_position.longitude
            )

        # Convert Julian Day to datetime for dasha calculation
        # Julian Day to Gregorian date conversion
        year, month, day, hour = swe.revjul(julian_day + timezone_offset/24.0, swe.GREG_CAL)
        birth_datetime = datetime(int(year), int(month), int(day), int(hour))

        # Generate dasha periods
        dashas = generate_vimshottari_dasha(
            starting_planet=starting_planet,
            elapsed_percentage=elapsed_percentage,
            start_datetime=birth_datetime
        )

        # Convert to format expected by model
        # For now, returning list of dicts - will be handled by service layer
        return dashas

    def calculate_divisional_chart(self, base_chart: BaseChart, division: int) -> BaseChart:
        """
        Calculate a divisional chart (D2, D3, D9, etc.) from a base chart.

        Args:
            base_chart: Base D1 chart
            division: Divisional number (2 for D2, 3 for D3, 9 for D9, etc.)

        Returns:
            BaseChart object for the divisional chart
        """
        if division < 2:
            raise ValueError("Divisional chart must be for division 2 or higher")

        # Calculate divisional chart planetary positions
        divisional_positions = []
        for position in base_chart.planetary_positions:
            # Calculate divisional longitude
            # Formula: (longitude * division) % 30 + sign_start
            # But we need to handle the sign changes properly

            # Get the sign number (0-11)
            sign_order = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
            sign_index = sign_order.index(position.sign.value)
            sign_start_longitude = sign_index * 30

            # Position within the sign (0-30 degrees)
            position_in_sign = position.longitude - sign_start_longitude

            # Multiply by division and wrap around 360
            divisional_longitude = (position_in_sign * division) % 30
            divisional_longitude += sign_start_longitude

            # Create new planetary position for divisional chart
            # Note: For divisional charts, we keep the same planetary data
            # but recalculate the sign and house based on divisional longitude
            divisional_position = PlanetaryPosition(
                planet=position.planet,
                longitude=divisional_longitude,
                latitude=position.latitude,
                speed=position.speed,
                sign=self._get_zodiac_sign(divisional_longitude),
                house=House("1"),  # Will be updated below
                nakshatra=self._get_nakshatra(divisional_longitude)[0],
                nakshatra_pada=self._get_nakshatra(divisional_longitude)[1],
                is_retrograde=position.is_retrograde
            )
            divisional_positions.append(divisional_position)

        # Calculate house cusps for divisional chart
        # For divisional charts, we use the same birth time/location
        # but the ascendant is calculated differently
        # For simplicity in MVP, we'll use equal house system based on divisional ascendant

        # Calculate Julian Day for birth time
        jd = julian_day(
            base_chart.birth_date,
            datetime.strptime(base_chart.birth_time, "%H:%M").time(),
            parse_timezone(base_chart.timezone)
        )

        # Calculate house cusps using same location
        house_cusps = calculate_house_cusps(
            jd, base_chart.birth_latitude, base_chart.birth_longitude
        )

        # Assign houses to divisional planets
        divisional_positions = self._assign_houses_to_planets(divisional_positions, house_cusps)

        # Calculate aspects for divisional chart
        aspects = calculate_aspects(divisional_positions)

        # Create divisional chart object
        divisional_chart = BaseChart(
            birth_date=base_chart.birth_date,
            birth_time=base_chart.birth_time,
            birth_latitude=base_chart.birth_latitude,
            birth_longitude=base_chart.birth_longitude,
            timezone=base_chart.timezone,
            ayanamsa=base_chart.ayanamsa,
            planetary_positions=divisional_positions,
            house_cusps=house_cusps,
            aspects=aspects,
            vimshottari_dasha=[]  # Divisional charts typically don't have their own dasha
        )

        return divisional_chart

    def _get_zodiac_sign(self, longitude: float) -> str:
        """Get zodiac sign name from longitude."""
        from ..core.config import ZODIAC_SIGNS, DEGREES_PER_SIGN
        normalized_longitude = longitude % 360
        sign_index = int(normalized_longitude // DEGREES_PER_SIGN)
        return ZODIAC_SIGNS[sign_index]

    def _get_nakshatra(self, longitude: float) -> tuple:
        """Get nakshatra and pada from longitude."""
        from ..utils.calculations import get_nakshatra
        nakshatra_str, pada = get_nakshatra(longitude)
        return nakshatra_str, pada