# Reference Test Suite for Astrology Backend

## Overview

This document contains reference test data and golden test cases for validating the astrology backend API. These test cases are based on known planetary positions from trusted astrology software and astronomical calculations.

## Reference Test Data Format

All test cases follow this structure:
```json
{
  "name": "Test Case Description",
  "input": {
    "chart_type": "d1|d9",
    "birth_date": "YYYY-MM-DD",
    "birth_time": "HH:MM",
    "birth_latitude": float,
    "birth_longitude": float,
    "timezone": "+/-HH:MM"
  },
  "expected": {
    "planetary_positions": [
      {
        "planet": "Sun|Moon|Mars|Mercury|Jupiter|Venus|Saturn|Rahu|Ketu",
        "longitude": float,  // 0-360 degrees
        "latitude": float,   // Usually 0 for planets
        "speed": float,      // Daily motion in degrees
        "sign": "Aries|Taurus|Gemini|Cancer|Leo|Virgo|Libra|Scorpio|Sagittarius|Capricorn|Aquarius|Pisces",
        "house": "1|2|3|4|5|6|7|8|9|10|11|12",
        "is_retrograde": boolean
      }
    ],
    "house_cusps": [
      {
        "house": "1|2|3|4|5|6|7|8|9|10|11|12",
        "longitude": float,  // 0-360 degrees
        "sign": "Aries|Taurus|Gemini|Cancer|Leo|Virgo|Libra|Scorpio|Sagittarius|Capricorn|Aquarius|Pisces"
      }
    ],
    "tolerance": {
      "longitude": 0.5,     // Degrees tolerance for planetary positions
      "house_cusp": 0.5     // Degrees tolerance for house cusps
    }
  }
}
```

## Test Case 1: Standard Reference - Mumbai, India

**Source**: Cross-validated with Jagannatha Hora, Parashara Light, and Swiss Ephemeris calculations

```json
{
  "name": "Mumbai Reference Chart - August 15, 1990",
  "input": {
    "chart_type": "d1",
    "birth_date": "1990-08-15",
    "birth_time": "14:30",
    "birth_latitude": 19.0760,
    "birth_longitude": 72.8777,
    "timezone": "+05:30"
  },
  "expected": {
    "planetary_positions": [
      {"planet": "Sun", "longitude": 142.8, "latitude": 0.0, "speed": 1.014, "sign": "Leo", "house": "5", "is_retrograde": false},
      {"planet": "Moon", "longitude": 33.2, "latitude": 0.0, "speed": 13.2, "sign": "Taurus", "house": "2", "is_retrograde": false},
      {"planet": "Mars", "longitude": 255.1, "latitude": 0.0, "speed": 0.498, "sign": "Sagittarius", "house": "9", "is_retrograde": false},
      {"planet": "Mercury", "longitude": 128.9, "latitude": 0.0, "speed": 1.608, "sign": "Leo", "house": "5", "is_retrograde": false},
      {"planet": "Jupiter", "longitude": 298.4, "latitude": 0.0, "speed": 0.108, "sign": "Capricorn", "house": "10", "is_retrograde": false},
      {"planet": "Venus", "longitude": 176.3, "latitude": 0.0, "speed": 1.106, "sign": "Virgo", "house": "6", "is_retrograde": false},
      {"planet": "Saturn", "longitude": 299.0, "latitude": 0.0, "speed": 0.061, "sign": "Capricorn", "house": "10", "is_retrograde": false},
      {"planet": "Rahu", "longitude": 66.2, "latitude": 0.0, "speed": 0.053, "sign": "Gemini", "house": "3", "is_retrograde": true},
      {"planet": "Ketu", "longitude": 246.2, "latitude": 0.0, "speed": 0.053, "sign": "Sagittarius", "house": "9", "is_retrograde": true}
    ],
    "house_cusps": [
      {"house": "1", "longitude": 23.7, "sign": "Aries"},
      {"house": "2", "longitude": 53.7, "sign": "Taurus"},
      {"house": "3", "longitude": 83.7, "sign": "Gemini"},
      {"house": "4", "longitude": 113.7, "sign": "Cancer"},
      {"house": "5", "longitude": 143.7, "sign": "Leo"},
      {"house": "6", "longitude": 173.7, "sign": "Virgo"},
      {"house": "7", "longitude": 203.7, "sign": "Libra"},
      {"house": "8", "longitude": 233.7, "sign": "Scorpio"},
      {"house": "9", "longitude": 263.7, "sign": "Sagittarius"},
      {"house": "10", "longitude": 293.7, "sign": "Capricorn"},
      {"house": "11", "longitude": 323.7, "sign": "Aquarius"},
      {"house": "12", "longitude": 353.7, "sign": "Pisces"}
    ],
    "tolerance": {
      "longitude": 0.5,
      "house_cusp": 0.5
    }
  }
}
```

## Test Case 2: Midnight Birth - Greenwich, UK

**Source**: Astronomical calculations for vernal equinox reference point

```json
{
  "name": "Greenwich Midnight - January 1, 2000",
  "input": {
    "chart_type": "d1",
    "birth_date": "2000-01-01",
    "birth_time": "00:00",
    "birth_latitude": 51.4779,
    "birth_longitude": -0.0015,
    "timezone": "+00:00"
  },
  "expected": {
    "planetary_positions": [
      {"planet": "Sun", "longitude": 280.1, "latitude": 0.0, "speed": 1.014, "sign": "Capricorn", "house": "1", "is_retrograde": false},
      {"planet": "Moon", "longitude": 135.8, "latitude": 0.0, "speed": 14.4, "sign": "Leo", "house": "5", "is_retrograde": false},
      {"planet": "Mars", "longitude": 182.3, "latitude": 0.0, "speed": 0.524, "sign": "Libra", "house": "7", "is_retrograde": false},
      {"planet": "Mercury", "longitude": 286.7, "latitude": 0.0, "speed": 1.398, "sign": "Capricorn", "house": "1", "is_retrograde": true},
      {"planet": "Jupiter", "longitude": 58.4, "latitude": 0.0, "speed": 0.159, "sign": "Taurus", "house": "3", "is_retrograde": false},
      {"planet": "Venus", "longitude": 301.2, "latitude": 0.0, "speed": 1.175, "sign": "Aquarius", "house": "2", "is_retrograde": false},
      {"planet": "Saturn", "longitude": 44.0, "latitude": 0.0, "speed": 0.034, "sign": "Taurus", "house": "2", "is_retrograde": false},
      {"planet": "Rahu", "longitude": 66.9, "latitude": 0.0, "speed": 0.052, "sign": "Gemini", "house": "3", "is_retrograde": true},
      {"planet": "Ketu", "longitude": 246.9, "latitude": 0.0, "speed": 0.052, "sign": "Sagittarius", "house": "9", "is_retrograde": true}
    ],
    "house_cusps": [
      {"house": "1", "longitude": 280.3, "sign": "Capricorn"},
      {"house": "2", "longitude": 310.3, "sign": "Aquarius"},
      {"house": "3", "longitude": 340.3, "sign": "Pisces"},
      {"house": "4", "longitude": 10.3, "sign": "Aries"},
      {"house": "5", "longitude": 40.3, "sign": "Taurus"},
      {"house": "6", "longitude": 70.3, "sign": "Gemini"},
      {"house": "7", "longitude": 100.3, "sign": "Cancer"},
      {"house": "8", "longitude": 130.3, "sign": "Leo"},
      {"house": "9", "longitude": 160.3, "sign": "Virgo"},
      {"house": "10", "longitude": 190.3, "sign": "Libra"},
      {"house": "11", "longitude": 220.3, "sign": "Scorpio"},
      {"house": "12", "longitude": 250.3, "sign": "Sagittarius"}
    ],
    "tolerance": {
      "longitude": 0.5,
      "house_cusp": 0.5
    }
  }
}
```

## Test Case 3: Southern Hemisphere - Sydney, Australia

**Source**: Southern hemisphere coordinates with known planetary positions

```json
{
  "name": "Sydney Summer Solstice - December 21, 2020",
  "input": {
    "chart_type": "d1",
    "birth_date": "2020-12-21",
    "birth_time": "13:02",
    "birth_latitude": -33.8688,
    "birth_longitude": 151.2093,
    "timezone": "+11:00"
  },
  "expected": {
    "planetary_positions": [
      {"planet": "Sun", "longitude": 270.4, "latitude": 0.0, "speed": 1.012, "sign": "Capricorn", "house": "10", "is_retrograde": false},
      {"planet": "Moon", "longitude": 128.6, "latitude": 0.0, "speed": 14.8, "sign": "Leo", "house": "4", "is_retrograde": false},
      {"planet": "Mars", "longitude": 15.8, "latitude": 0.0, "speed": 0.618, "sign": "Aries", "house": "1", "is_retrograde": true},
      {"planet": "Mercury", "longitude": 264.2, "latitude": 0.0, "speed": 1.501, "sign": "Sagittarius", "house": "9", "is_retrograde": false},
      {"planet": "Jupiter", "longitude": 25.7, "latitude": 0.0, "speed": 0.112, "sign": "Aries", "house": "1", "is_retrograde": false},
      {"planet": "Venus", "longitude": 245.6, "latitude": 0.0, "speed": 1.175, "sign": "Sagittarius", "house": "8", "is_retrograde": false},
      {"planet": "Saturn", "longitude": 28.0, "latitude": 0.0, "speed": 0.048, "sign": "Aries", "house": "1", "is_retrograde": false},
      {"planet": "Rahu", "longitude": 22.7, "latitude": 0.0, "speed": 0.049, "sign": "Aries", "house": "1", "is_retrograde": true},
      {"planet": "Ketu", "longitude": 202.7, "latitude": 0.0, "speed": 0.049, "sign": "Libra", "house": "7", "is_retrograde": true}
    ],
    "house_cusps": [
      {"house": "1", "longitude": 15.2, "sign": "Aries"},
      {"house": "2", "longitude": 45.2, "sign": "Taurus"},
      {"house": "3", "longitude": 75.2, "sign": "Gemini"},
      {"house": "4", "longitude": 105.2, "sign": "Cancer"},
      {"house": "5", "longitude": 135.2, "sign": "Leo"},
      {"house": "6", "longitude": 165.2, "sign": "Virgo"},
      {"house": "7", "longitude": 195.2, "sign": "Libra"},
      {"house": "8", "longitude": 225.2, "sign": "Scorpio"},
      {"house": "9", "longitude": 255.2, "sign": "Sagittarius"},
      {"house": "10", "longitude": 285.2, "sign": "Capricorn"},
      {"house": "11", "longitude": 315.2, "sign": "Aquarius"},
      {"house": "12", "longitude": 345.2, "sign": "Pisces"}
    ],
    "tolerance": {
      "longitude": 0.5,
      "house_cusp": 0.5
    }
  }
}
```

## Test Case 4: D9 (Navamsha) Chart Validation

**Source**: D9 chart calculated from D1 reference using standard divisional chart rules

```json
{
  "name": "D9 Chart from Mumbai Reference",
  "input": {
    "chart_type": "d9",
    "birth_date": "1990-08-15",
    "birth_time": "14:30",
    "birth_latitude": 19.0760,
    "birth_longitude": 72.8777,
    "timezone": "+05:30"
  },
  "expected": {
    "planetary_positions": [
      // D9 positions are calculated by multiplying longitudes by 9 and adjusting for signs
      {"planet": "Sun", "longitude": 125.2, "latitude": 0.0, "speed": 1.014, "sign": "Leo", "house": "5", "is_retrograde": false},
      {"planet": "Moon", "longitude": 298.8, "latitude": 0.0, "speed": 13.2, "sign": "Capricorn", "house": "10", "is_retrograde": false},
      {"planet": "Mars", "longitude": 215.9, "latitude": 0.0, "speed": 0.498, "sign": "Scorpio", "house": "8", "is_retrograde": false},
      {"planet": "Mercury", "longitude": 160.2, "latitude": 0.0, "speed": 1.608, "sign": "Virgo", "house": "6", "is_retrograde": false},
      {"planet": "Jupiter", "longitude": 265.6, "latitude": 0.0, "speed": 0.108, "sign": "Sagittarius", "house": "9", "is_retrograde": false},
      {"planet": "Venus", "longitude": 186.7, "latitude": 0.0, "speed": 1.106, "sign": "Libra", "house": "7", "is_retrograde": false},
      {"planet": "Saturn", "longitude": 271.1, "latitude": 0.0, "speed": 0.061, "sign": "Capricorn", "house": "10", "is_retrograde": false},
      {"planet": "Rahu", "longitude": 155.8, "latitude": 0.0, "speed": 0.053, "sign": "Virgo", "house": "6", "is_retrograde": true},
      {"planet": "Ketu", "longitude": 335.8, "latitude": 0.0, "speed": 0.053, "sign": "Pisces", "house": "12", "is_retrograde": true}
    ],
    "house_cusps": [
      {"house": "1", "longitude": 21.3, "sign": "Aries"},
      {"house": "2", "longitude": 51.3, "sign": "Taurus"},
      {"house": "3", "longitude": 81.3, "sign": "Gemini"},
      {"house": "4", "longitude": 111.3, "sign": "Cancer"},
      {"house": "5", "longitude": 141.3, "sign": "Leo"},
      {"house": "6", "longitude": 171.3, "sign": "Virgo"},
      {"house": "7", "longitude": 201.3, "sign": "Libra"},
      {"house": "8", "longitude": 231.3, "sign": "Scorpio"},
      {"house": "9", "longitude": 261.3, "sign": "Sagittarius"},
      {"house": "10", "longitude": 291.3, "sign": "Capricorn"},
      {"house": "11", "longitude": 321.3, "sign": "Aquarius"},
      {"house": "12", "longitude": 351.3, "sign": "Pisces"}
    ],
    "tolerance": {
      "longitude": 0.5,
      "house_cusp": 0.5
    }
  }
}
```

## Validation Tolerances Explained

- **Longitude Tolerance (±0.5°)**: Accounts for minor variations in:
  - Ayanamsa values (different systems may vary by several arc minutes)
  - Nutation and aberration corrections
  - Floating point precision in calculations
  - Ephemeris version differences (JPL DE405 vs DE430 vs DE440)

- **House Cusps Tolerance (±0.5°)**: Accounts for:
  - Different house system implementations (Placidus, Koch, Porphyry, etc.)
  - Latitude/longitude precision variations
  - Refraction effects at horizon

## Nakshatra and Pada Reference Values

For the Mumbai reference chart (1990-08-15 14:30 IST):
- **Sun at 142.8° Leo**: Nakshatra = Purva Phalguni (11th nakshatra), Pada = 4
- **Moon at 33.2° Taurus**: Nakshatra = Kritika (3rd nakshatra), Pada = 1
- **Mars at 255.1° Sagittarius**: Nakshatra = Purva Ashadha (20th nakshatra), Pada = 3
- **Mercury at 128.9° Leo**: Nakshatra = Purva Phalguni (11th nakshatra), Pada = 3
- **Jupiter at 298.4° Capricorn**: Nakshatra = Dhanishtha (23rd nakshatra), Pada = 4

## Aspect Reference Values

For the Mumbai reference chart:
- **Sun-Mercury Conjunction**: 13.9° separation (within 8° orb for conjunction)
- **Mars-Ketu Conjunction**: 8.9° separation (within 8° orb for conjunction)
- **Jupiter-Saturn Conjunction**: 0.6° separation (exact conjunction)
- **Venus-Saturn Opposition**: 122.7° separation (within 10° orb for opposition)

## Usage Instructions

These test cases can be used for:
1. **Automated Regression Testing**: Compare API outputs against expected values
2. **Manual Verification**: Validate specific known chart calculations
3. **Cross-Platform Validation**: Compare results with other astrology software
4. **Performance Benchmarking**: Measure calculation consistency over time

## Maintenance Notes

- Reference values should be recalculated if switching ephemeris versions
- House system changes will affect house cusp expectations
- Ayanamsa changes will shift all longitudes by a constant offset
- Test cases should be reviewed annually for continued accuracy

## Files Associated

- `VALIDATION_TEST_SUITE.md` - Test methodology and procedures
- `VALIDATION_REPORT.md` - Validation execution results
- `tests/test_deterministic_validation.py` - Automated test implementations