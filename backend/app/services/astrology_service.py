"""
Astrology Engine service adapter for FastAPI backend.

This service provides a clean interface to the astrology_engine package,
handling dependency injection, async wrappers, and data transformation
between the engine's internal models and the API schemas.
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional, Dict, Any
from datetime import date, datetime
import logging

from backend.app.schemas.chart import (
    ChartCreate, ChartResponse, PlanetaryPosition, HouseCusp,
    ChartType, Planet, House, ZodiacSign
)
from backend.app.models.chart import Chart as ChartModel

# Import astrology_engine components
import sys
import os
from pathlib import Path

# Get the absolute path to the astrology-engine src directory
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
astrology_engine_src = os.path.join(project_root, 'astrology-engine', 'src')

# Add src to Python path if not already present
if astrology_engine_src not in sys.path:
    sys.path.insert(0, astrology_engine_src)

try:
    from astrology_engine.charts.base import ChartCalculator
    from astrology_engine.divisional.service import DivisionalChartService
    from astrology_engine.core.models import BaseChart as EngineBaseChart
    from astrology_engine.core.models import PlanetaryPosition as EnginePlanetaryPosition
    from astrology_engine.core.models import HouseCusp as EngineHouseCusp
    from astrology_engine.core.exceptions import InvalidBirthDataError, CalculationError
except ImportError as e:
    logging.warning(f"Could not import astrology_engine: {e}")
    # Fallback for development - will be replaced when properly installed
    ChartCalculator = None
    DivisionalChartService = None
    EngineBaseChart = None
    EnginePlanetaryPosition = None
    EngineHouseCusp = None
    InvalidBirthDataError = Exception
    CalculationError = Exception

logger = logging.getLogger(__name__)


class AstrologyService:
    """
    Service layer for astrology calculations using astrology_engine.

    This service adapts the astrology_engine package for use in the FastAPI backend,
    providing async-safe wrappers and clean data transformation.
    """

    def __init__(self, ayanamsa: str = "Lahiri"):
        """
        Initialize the astrology service.

        Args:
            ayanamsa: Ayanamsa system to use (defaults to Lahiri)
        """
        self.ayanamsa = ayanamsa
        self._executor = ThreadPoolExecutor(max_workers=4)

        # Initialize engines if available
        if ChartCalculator is not None:
            self.chart_calculator = ChartCalculator(ayanamsa=ayanamsa)
            self.divisional_service = DivisionalChartService(ayanamsa=ayanamsa)
        else:
            self.chart_calculator = None
            self.divisional_service = None
            logger.warning("Astrology engine not available - using mock implementations")

    async def calculate_chart(
        self,
        chart_in: ChartCreate
    ) -> ChartResponse:
        """
        Calculate an astrological chart (D1 or D9) based on input data.

        Args:
            chart_in: Chart creation data

        Returns:
            ChartResponse with calculated planetary positions and house cusps

        Raises:
            InvalidBirthDataError: If input data is invalid
            CalculationError: If calculation fails
        """
        loop = asyncio.get_event_loop()

        # Run calculation in thread pool to avoid blocking
        result = await loop.run_in_executor(
            self._executor,
            self._calculate_chart_sync,
            chart_in
        )

        return result

    def _calculate_chart_sync(
        self,
        chart_in: ChartCreate
    ) -> ChartResponse:
        """
        Synchronous chart calculation (runs in thread pool).
        """
        if self.chart_calculator is None:
            # Mock implementation for development
            return self._generate_mock_chart_response(chart_in)

        try:
            # Calculate base chart (D1)
            chart_type = "D9" if chart_in.chart_type == ChartType.D9 else "D1"

            engine_chart = self.chart_calculator.calculate_chart(
                birth_date=chart_in.birth_date,
                birth_time=chart_in.birth_time,
                birth_latitude=chart_in.birth_latitude,
                birth_longitude=chart_in.birth_longitude,
                timezone=chart_in.timezone,
                chart_type=chart_type
            )

            # Convert engine chart to API response
            return self._engine_chart_to_response(engine_chart, chart_in)

        except Exception as e:
            logger.error(f"Chart calculation failed: {e}")
            raise CalculationError(f"Failed to calculate chart: {str(e)}")

    async def calculate_divisional_chart(
        self,
        base_chart_data: ChartResponse,
        division: int
    ) -> ChartResponse:
        """
        Calculate a divisional chart from a base chart.

        Args:
            base_chart_data: Base chart (typically D1) data
            division: Divisional number (2 for D2, 9 for D9, etc.)

        Returns:
            ChartResponse for the divisional chart
        """
        loop = asyncio.get_event_loop()

        # Run calculation in thread pool to avoid blocking
        result = await loop.run_in_executor(
            self._executor,
            self._calculate_divisional_chart_sync,
            base_chart_data,
            division
        )

        return result

    def _calculate_divisional_chart_sync(
        self,
        base_chart_data: ChartResponse,
        division: int
    ) -> ChartResponse:
        """
        Synchronous divisional chart calculation (runs in thread pool).
        """
        if self.divisional_service is None or self.chart_calculator is None:
            # Mock implementation for development
            return self._generate_mock_divisional_chart(base_chart_data, division)

        try:
            # Convert API response back to engine chart
            base_engine_chart = self._response_to_engine_chart(base_chart_data)

            # Calculate divisional chart
            divisional_engine_chart = self.divisional_service.calculate_divisional_chart(
                base_chart=base_engine_chart,
                division=division
            )

            # Convert back to API response
            chart_type = ChartType.D9 if division == 9 else ChartType.D1  # Default to D1 for other divisions
            chart_in = ChartCreate(
                chart_type=chart_type,
                birth_date=base_engine_chart.birth_date,
                birth_time=base_engine_chart.birth_time,
                birth_latitude=base_engine_chart.birth_latitude,
                birth_longitude=base_engine_chart.birth_longitude,
                timezone=base_engine_chart.timezone
            )

            return self._engine_chart_to_response(divisional_engine_chart, chart_in)

        except Exception as e:
            logger.error(f"Divisional chart calculation failed: {e}")
            raise CalculationError(f"Failed to calculate divisional chart: {str(e)}")

    def _engine_chart_to_response(
        self,
        engine_chart: EngineBaseChart,
        chart_in: ChartCreate
    ) -> ChartResponse:
        """
        Convert astrology_engine BaseChart to API ChartResponse.
        """
        # Convert planetary positions
        planetary_positions = []
        for pos in engine_chart.planetary_positions:
            api_pos = PlanetaryPosition(
                planet=Planet(pos.planet.value),
                longitude=pos.longitude,
                latitude=pos.latitude,
                speed=pos.speed,
                sign=ZodiacSign(pos.sign.value),
                house=House(pos.house.value),
                is_retrograde=pos.is_retrograde
            )
            planetary_positions.append(api_pos)

        # Convert house cusps
        house_cusps = []
        for cusp in engine_chart.house_cusps:
            api_cusp = HouseCusp(
                house=House(cusp.house.value),
                longitude=cusp.longitude,
                sign=ZodiacSign(cusp.sign.value)
            )
            house_cusps.append(api_cusp)

        # Create response
        return ChartResponse(
            id=0,  # Will be set by database
            user_id=0,  # Will be set by database
            chart_type=chart_in.chart_type,
            birth_date=engine_chart.birth_date,
            birth_time=engine_chart.birth_time,
            birth_latitude=engine_chart.birth_latitude,
            birth_longitude=engine_chart.birth_longitude,
            timezone=engine_chart.timezone,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            planetary_positions=planetary_positions,
            house_cusps=house_cusps,
            divisional_data=None  # Will be populated separately if needed
        )

    def _response_to_engine_chart(self, response: ChartResponse) -> EngineBaseChart:
        """
        Convert API ChartResponse to astrology_engine BaseChart.
        """
        # Convert planetary positions
        engine_positions = []
        for pos in response.planetary_positions:
            engine_pos = EnginePlanetaryPosition(
                planet=pos.planet.value,
                longitude=pos.longitude,
                latitude=pos.latitude,
                speed=pos.speed,
                sign=pos.sign.value,
                house=pos.house.value,
                nakshatra="Ashwini",  # Default - would need to calculate
                nakshatra_pada=1,     # Default - would need to calculate
                is_retrograde=pos.is_retrograde
            )
            engine_positions.append(engine_pos)

        # Convert house cusps
        engine_cusps = []
        for cusp in response.house_cusps:
            engine_cusp = EngineHouseCusp(
                house=cusp.house.value,
                longitude=cusp.longitude,
                sign=cusp.sign.value
            )
            engine_cusps.append(engine_cusp)

        # Create engine chart
        return EngineBaseChart(
            birth_date=response.birth_date,
            birth_time=response.birth_time,
            birth_latitude=response.birth_latitude,
            birth_longitude=response.birth_longitude,
            timezone=response.timezone,
            ayanamsa=self.ayanamsa,
            planetary_positions=engine_positions,
            house_cusps=engine_cusps,
            aspects=[],  # Would need to recalculate
            vimshottari_dasha=[]  # Would need to recalculate
        )

    def _generate_mock_chart_response(self, chart_in: ChartCreate) -> ChartResponse:
        """
        Generate mock chart response for development when astrology_engine is not available.
        """
        # Generate mock planetary positions
        planetary_positions = [
            PlanetaryPosition(
                planet=Planet.SUN,
                longitude=0.0,
                latitude=0.0,
                speed=1.0,
                sign=ZodiacSign.ARIES,
                house=House.HOUSE_1,
                is_retrograde=False
            ),
            PlanetaryPosition(
                planet=Planet.MOON,
                longitude=30.0,
                latitude=0.0,
                speed=0.5,
                sign=ZodiacSign.TAURUS,
                house=House.HOUSE_2,
                is_retrograde=False
            ),
            PlanetaryPosition(
                planet=Planet.MARS,
                longitude=60.0,
                latitude=0.0,
                speed=0.8,
                sign=ZodiacSign.GEMINI,
                house=House.HOUSE_3,
                is_retrograde=False
            ),
            PlanetaryPosition(
                planet=Planet.MERCURY,
                longitude=90.0,
                latitude=0.0,
                speed=1.2,
                sign=ZodiacSign.CANCER,
                house=House.HOUSE_4,
                is_retrograde=False
            ),
            PlanetaryPosition(
                planet=Planet.JUPITER,
                longitude=120.0,
                latitude=0.0,
                speed=0.1,
                sign=ZodiacSign.LEO,
                house=House.HOUSE_5,
                is_retrograde=False
            ),
            PlanetaryPosition(
                planet=Planet.VENUS,
                longitude=150.0,
                latitude=0.0,
                speed=0.7,
                sign=ZodiacSign.VIRGO,
                house=House.HOUSE_6,
                is_retrograde=False
            ),
            PlanetaryPosition(
                planet=Planet.SATURN,
                longitude=180.0,
                latitude=0.0,
                speed=0.05,
                sign=ZodiacSign.LIBRA,
                house=House.HOUSE_7,
                is_retrograde=False
            ),
            PlanetaryPosition(
                planet=Planet.RAHU,
                longitude=210.0,
                latitude=0.0,
                speed=0.05,
                sign=ZodiacSign.SCORPIO,
                house=House.HOUSE_8,
                is_retrograde=True
            ),
            PlanetaryPosition(
                planet=Planet.KETU,
                longitude=30.0,  # Opposite Rahu
                latitude=0.0,
                speed=0.05,
                sign=ZodiacSign.TAURUS,
                house=House.HOUSE_2,
                is_retrograde=True
            )
        ]

        # Generate mock house cusps (Equal house system)
        house_cusps = []
        signs = [ZodiacSign.ARIES, ZodiacSign.TAURUS, ZodiacSign.GEMINI, ZodiacSign.CANCER,
                ZodiacSign.LEO, ZodiacSign.VIRGO, ZodiacSign.LIBRA, ZodiacSign.SCORPIO,
                ZodiacSign.SAGITTARIUS, ZodiacSign.CAPRICORN, ZodiacSign.AQUARIUS, ZodiacSign.PISCES]

        for i in range(12):
            house_cusp = HouseCusp(
                house=House(str(i + 1)),
                longitude=i * 30.0,
                sign=signs[i]
            )
            house_cusps.append(house_cusp)

        return ChartResponse(
            id=0,  # Will be set by database
            user_id=0,  # Will be set by database
            chart_type=chart_in.chart_type,
            birth_date=chart_in.birth_date,
            birth_time=chart_in.birth_time,
            birth_latitude=chart_in.birth_latitude,
            birth_longitude=chart_in.birth_longitude,
            timezone=chart_in.timezone,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            planetary_positions=planetary_positions,
            house_cusps=house_cusps,
            divisional_data=None
        )

    def _generate_mock_divisional_chart(
        self,
        base_chart_data: ChartResponse,
        division: int
    ) -> ChartResponse:
        """
        Generate mock divisional chart for development.
        """
        # For mock, just modify the longitudes based on division
        planetary_positions = []
        for pos in base_chart_data.planetary_positions:
            # Apply divisional transformation (simplified)
            divided_longitude = (pos.longitude * division) % 360

            # Determine new sign
            signs = list(ZodiacSign)
            sign_index = int(divided_longitude // 30) % 12
            new_sign = signs[sign_index]

            # Determine new house (simplified - would need proper calculation)
            new_house = House(str(((int(pos.house.value) - 1 + division) % 12) + 1))

            divided_pos = PlanetaryPosition(
                planet=pos.planet,
                longitude=divided_longitude,
                latitude=pos.latitude,
                speed=pos.speed,
                sign=new_sign,
                house=new_house,
                is_retrograde=pos.is_retrograde
            )
            planetary_positions.append(divided_pos)

        # House cusps remain the same for mock
        house_cusps = base_chart_data.house_cusps

        chart_type = ChartType.D9 if division == 9 else ChartType.D1

        return ChartResponse(
            id=0,  # Will be set by database
            user_id=0,  # Will be set by database
            chart_type=chart_type,
            birth_date=base_chart_data.birth_date,
            birth_time=base_chart_data.birth_time,
            birth_latitude=base_chart_data.birth_latitude,
            birth_longitude=base_chart_data.birth_longitude,
            timezone=base_chart_data.timezone,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            planetary_positions=planetary_positions,
            house_cusps=house_cusps,
            divisional_data=None
        )

    def shutdown(self):
        """
        Shutdown the service and cleanup resources.
        """
        if hasattr(self, '_executor'):
            self._executor.shutdown(wait=True)


# Global service instance removed - now using dependency injection
# astrology_service = AstrologyService()  # Removed for proper DI