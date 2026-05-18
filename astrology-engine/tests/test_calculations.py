"""
Unit tests for astrology engine calculations.
"""
import unittest

from datetime import date, time
from astrology_engine.utils.coordinates import validate_birth_data, parse_timezone, julian_day
from astrology_engine.utils.calculations import (
    get_zodiac_sign, get_nakshatra, normalize_longitude,
    calculate_planetary_position, calculate_house_cusps,
    calculate_aspects, detect_basic_yogas,
    calculate_vimshottari_dasha_start, generate_vimshottari_dasha
)
from astrology_engine.charts.base import ChartCalculator
from astrology_engine.core.models import PlanetaryPosition, HouseCusp, AspectInfo
from astrology_engine.core.config import ZODIAC_SIGNS, NAKSHATRAS, PLANETS, DEFAULT_AYANAMSA


class TestAstrologyCalculations(unittest.TestCase):
    """Test cases for astrological calculations."""

    def setUp(self):
        """Set up test data."""
        # Test birth data: August 15, 1990, 2:30 PM, New York
        self.test_birth_date = date(1990, 8, 15)
        self.test_birth_time = "14:30"
        self.test_latitude = 40.7128  # New York City latitude
        self.test_longitude = -74.0060  # New York City longitude
        self.test_timezone = "-05:00"  # EST

    def test_coordinate_validation(self):
        """Test birth data validation."""
        # Valid data should not raise exception
        try:
            validated_date, validated_time = validate_birth_data(
                self.test_birth_date, self.test_birth_time,
                self.test_latitude, self.test_longitude
            )
            self.assertEqual(validated_date, self.test_birth_date)
            self.assertEqual(validated_time.strftime("%H:%M"), self.test_birth_time)
        except Exception as e:
            self.fail(f"Valid birth data raised exception: {e}")

        # Invalid future date should raise exception
        future_date = date.today().replace(year=date.today().year + 1)
        with self.assertRaises(Exception):
            validate_birth_data(
                future_date, self.test_birth_time,
                self.test_latitude, self.test_longitude
            )

        # Invalid latitude should raise exception
        with self.assertRaises(Exception):
            validate_birth_data(
                self.test_birth_date, self.test_birth_time,
                95.0, self.test_longitude  # Latitude > 90
            )

    def test_timezone_parsing(self):
        """Test timezone string parsing."""
        self.assertEqual(parse_timezone("+05:30"), 5.5)
        self.assertEqual(parse_timezone("-04:00"), -4.0)
        self.assertEqual(parse_timezone("+00:00"), 0.0)
        self.assertEqual(parse_timezone("-05:30"), -5.5)

    def test_longitude_normalization(self):
        """Test longitude normalization to 0-360 range."""
        self.assertEqual(normalize_longitude(-10), 350)
        self.assertEqual(normalize_longitude(370), 10)
        self.assertEqual(normalize_longitude(0), 0)
        self.assertEqual(normalize_longitude(360), 0)
        self.assertEqual(normalize_longitude(180), 180)

    def test_zodiac_sign_calculation(self):
        """Test zodiac sign determination from longitude."""
        # Test known longitudes
        self.assertEqual(get_zodiac_sign(0), "Aries")
        self.assertEqual(get_zodiac_sign(30), "Taurus")
        self.assertEqual(get_zodiac_sign(90), "Cancer")
        self.assertEqual(get_zodiac_sign(180), "Libra")
        self.assertEqual(get_zodiac_sign(270), "Capricorn")

        # Test edge cases
        self.assertEqual(get_zodiac_sign(29.999), "Aries")
        self.assertEqual(get_zodiac_sign(30.0), "Taurus")
        self.assertEqual(get_zodiac_sign(359.999), "Pisces")

    def test_nakshatra_calculation(self):
        """Test nakshatra and pada calculation."""
        # Test first nakshatra (Ashwini) - 0 to 13°20'
        nakshatra, pada = get_nakshatra(5.0)
        self.assertEqual(nakshatra, "Ashwini")
        self.assertIn(pada, [1, 2, 3, 4])

        # Test middle of nakshatra
        nakshatra, pada = get_nakshatra(5.0)  # Middle of Ashwini
        self.assertEqual(nakshatra, "Ashwini")
        self.assertEqual(pada, 2)  # Should be in second pada

        # Test last nakshatra (Revati) - 346°40' to 360°
        nakshatra, pada = get_nakshatra(350.0)
        self.assertEqual(nakshatra, "Revati")

    def test_julian_day_calculation(self):
        """Test Julian Day calculation."""
        jd = julian_day(
            self.test_birth_date,
            time(14, 30),  # 2:30 PM
            parse_timezone(self.test_timezone)
        )
        # Julian Day should be a reasonable number for 1990
        self.assertGreater(jd, 2440000)  # After 1970
        self.assertLess(jd, 2460000)     # Before 2020

    def test_longitude_normalization_edge_cases(self):
        """Test edge cases for longitude normalization."""
        self.assertEqual(normalize_longitude(-360), 0)
        self.assertEqual(normalize_longitude(-720), 0)
        self.assertEqual(normalize_longitude(720), 0)
        self.assertEqual(normalize_longitude(359.999), 359.999)
        self.assertAlmostEqual(normalize_longitude(360.001), 0.001, places=10)

    def test_chart_calculator_initialization(self):
        """Test that ChartCalculator initializes correctly."""
        calculator = ChartCalculator(ayanamsa="Lahiri")
        self.assertIsNotNone(calculator)
        self.assertEqual(calculator.ayanamsa, "Lahiri")

        calculator_default = ChartCalculator()
        self.assertIsNotNone(calculator_default)
        self.assertEqual(calculator_default.ayanamsa, DEFAULT_AYANAMSA.value)  # Default from config

    def test_calculate_divisional_chart_method_exists(self):
        """Test that divisional chart method exists."""
        calculator = ChartCalculator()
        self.assertTrue(hasattr(calculator, 'calculate_divisional_chart'))


if __name__ == "__main__":
    unittest.main()