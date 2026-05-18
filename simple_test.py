#!/usr/bin/env python3
"""
Simple test to verify astrology engine components work.
"""

import sys
import os

# Get the absolute path to the src directory
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'astro-ai', 'astrology-engine', 'src')

# Add src to Python path
sys.path.insert(0, src_dir)

print(f"Python path: {sys.path[:3]}...")
print(f"Source directory: {src_dir}")
print(f"Source directory exists: {os.path.exists(src_dir)}")

try:
    # Test basic imports
    import swisseph
    print(f"✓ Swiss Ephemeris imported: version {swisseph.__version__}")
except ImportError as e:
    print(f"✗ Failed to import swisseph: {e}")
    sys.exit(1)

try:
    from utils.coordinates import validate_birth_data, parse_timezone, julian_day
    from datetime import date, time
    print("✓ Coordinates module imported")
except ImportError as e:
    print(f"✗ Failed to import coordinates: {e}")
    sys.exit(1)

try:
    from utils.calculations import get_zodiac_sign, get_nakshatra, normalize_longitude
    print("✓ Calculations module imported")
except ImportError as e:
    print(f"✗ Failed to import calculations: {e}")
    sys.exit(1)

try:
    from charts.base import ChartCalculator
    print("✓ Charts module imported")
except ImportError as e:
    print(f"✗ Failed to import charts: {e}")
    sys.exit(1)

# Test basic functionality
print("\n--- Testing Basic Functionality ---")

# Test coordinate validation
try:
    validated_date, validated_time = validate_birth_data(
        date(1990, 8, 15), "14:30", 40.7128, -74.0060
    )
    print("✓ Coordinate validation passed")
except Exception as e:
    print(f"✗ Coordinate validation failed: {e}")

# Test timezone parsing
try:
    tz = parse_timezone("-05:00")
    print(f"✓ Timezone parsing: -05:00 = {tz} hours")
except Exception as e:
    print(f"✗ Timezone parsing failed: {e}")

# Test julian day
try:
    jd = julian_day(date(1990, 8, 15), time(14, 30), -5.0)
    print(f"✓ Julian Day calculation: {jd:.2f}")
except Exception as e:
    print(f"✗ Julian Day calculation failed: {e}")

# Test longitude normalization
try:
    test_vals = [(-10, 350), (0, 0), (90, 90), (180, 180), (270, 270), (360, 0), (370, 10)]
    for inp, expected in test_vals:
        result = normalize_longitude(inp)
        assert result == expected, f"Expected {expected}, got {result} for input {inp}"
    print("✓ Longitude normalization tests passed")
except Exception as e:
    print(f"✗ Longitude normalization failed: {e}")

# Test zodiac sign
try:
    test_cases = [(0, "Aries"), (30, "Taurus"), (90, "Cancer"), (180, "Libra"), (270, "Capricorn")]
    for lon, expected in test_cases:
        result = get_zodiac_sign(lon)
        assert result == expected, f"Expected {expected} for {lon}°, got {result}"
    print("✓ Zodiac sign calculation passed")
except Exception as e:
    print(f"✗ Zodiac sign calculation failed: {e}")

# Test nakshatra
try:
    nakshatra, pada = get_nakshatra(5.0)
    print(f"✓ Nakshatra calculation: 5° = {nakshatra}, pada {pada}")
except Exception as e:
    print(f"✗ Nakshatra calculation failed: {e}")

print("\n--- Testing Chart Calculation ---")

try:
    # Initialize calculator
    calc = ChartCalculator(ayanamsa="Lahiri")
    print("✓ ChartCalculator initialized")

    # Calculate a simple chart
    chart = calc.calculate_chart(
        birth_date=date(1990, 8, 15),
        birth_time="14:30",
        birth_latitude=40.7128,
        birth_longitude=-74.0060,
        timezone="-05:00",
        chart_type="D1"
    )
    print("✓ D1 chart calculation completed")
    print(f"  - Planets calculated: {len(chart.planetary_positions)}")
    print(f"  - Houses calculated: {len(chart.house_cusps)}")
    print(f"  - Aspects found: {len(chart.aspects)}")

    # Show a sample planet
    if chart.planetary_positions:
        sun = next((p for p in chart.planetary_positions if p.planet.value == "Sun"), None)
        if sun:
            print(f"  - Sun: {sun.longitude:.2f}° in {sun.sign.value} house {sun.house.value}")

        moon = next((p for p in chart.planetary_positions if p.planet.value == "Moon"), None)
        if moon:
            print(f"  - Moon: {moon.longitude:.2f}° in {moon.sign.value} house {moon.house.value}")

except Exception as e:
    print(f"✗ Chart calculation failed: {e}")
    import traceback
    traceback.print_exc()

print("\n--- Test Complete ---")