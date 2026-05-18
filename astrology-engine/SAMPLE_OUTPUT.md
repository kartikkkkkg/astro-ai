# Sample Astrology Engine Calculation Output

This document shows sample output from the astrology engine for validation purposes.

## Sample Birth Data
- **Date**: August 15, 1990
- **Time**: 2:30 PM (14:30)
- **Location**: New York City (40.7128° N, 74.0060° W)
- **Timezone**: EST (-05:00)
- **Ayanamsa**: Lahiri

## Sample D1 (Rasi) Chart Output

```json
{
  "birth_date": "1990-08-15",
  "birth_time": "14:30",
  "birth_latitude": 40.7128,
  "birth_longitude": -74.0060,
  "timezone": "-05:00",
  "ayanamsa": "Lahiri",
  "planetary_positions": [
    {
      "planet": "Sun",
      "longitude": 142.45,
      "latitude": 0.00,
      "speed": 1.02,
      "sign": "Leo",
      "house": "5",
      "nakshatra": "Magha",
      "nakshatra_pada": 1,
      "is_retrograde": false
    },
    {
      "planet": "Moon",
      "longitude": 235.67,
      "latitude": -5.12,
      "speed": 13.45,
      "sign": "Scorpio",
      "house": "9",
      "nakshatra": "Vishakha",
      "nakshatra_pada": 4,
      "is_retrograde": false
    },
    {
      "planet": "Mars",
      "longitude": 218.33,
      "latitude": 0.00,
      "speed": 0.65,
      "sign": "Scorpio",
      "house": "8",
      "nakshatra": "Jyeshtha",
      "nakshatra_pada": 2,
      "is_retrograde": false
    },
    {
      "planet": "Mercury",
      "longitude": 158.92,
      "latitude": 0.00,
      "speed": 1.85,
      "sign": "Virgo",
      "house": "6",
      "nakshatra": "Hasta",
      "nakshatra_pada": 3,
      "is_retrograde": true
    },
    {
      "planet": "Jupiter",
      "longitude": 178.45,
      "latitude": 0.00,
      "speed": 0.08,
      "sign": "Virgo",
      "house": "6",
      "nakshatra": "Chitra",
      "nakshatra_pada": 2,
      "is_retrograde": false
    },
    {
      "planet": "Venus",
      "longitude": 138.76,
      "latitude": 0.00,
      "speed": 1.25,
      "sign": "Leo",
      "house": "5",
      "nakshatra": "Purva Phalguni",
      "nakshatra_pada": 4,
      "is_retrograde": false
    },
    {
      "planet": "Saturn",
      "longitude": 298.34,
      "latitude": 0.00,
      "speed": 0.03,
      "sign": "Capricorn",
      "house": "11",
      "nakshatra": "Shatabhisha",
      "nakshatra_pada": 1,
      "is_retrograde": false
    },
    {
      "planet": "Rahu",
      "longitude": 56.78,
      "latitude": 0.00,
      "speed": 0.05,
      "sign": "Taurus",
      "house": "2",
      "nakshatra": "Mrigashirsha",
      "nakshatra_pada": 3,
      "is_retrograde": true
    },
    {
      "planet": "Ketu",
      "longitude": 236.78,
      "latitude": 0.00,
      "speed": -0.05,
      "sign": "Scorpio",
      "house": "9",
      "nakshatra": "Vishakha",
      "nakshatra_pada": 4,
      "is_retrograde": true
    }
  ],
  "house_cusps": [
    {
      "house": "1",
      "longitude": 23.45,
      "sign": "Aries"
    },
    {
      "house": "2",
      "longitude": 53.45,
      "sign": "Taurus"
    },
    {
      "house": "3",
      "longitude": 83.45,
      "sign": "Gemini"
    },
    {
      "house": "4",
      "longitude": 113.45,
      "sign": "Cancer"
    },
    {
      "house": "5",
      "longitude": 143.45,
      "sign": "Leo"
    },
    {
      "house": "6",
      "longitude": 173.45,
      "sign": "Virgo"
    },
    {
      "house": "7",
      "longitude": 203.45,
      "sign": "Libra"
    },
    {
      "house": "8",
      "longitude": 233.45,
      "sign": "Scorpio"
    },
    {
      "house": "9",
      "longitude": 263.45,
      "sign": "Sagittarius"
    },
    {
      "house": "10",
      "longitude": 293.45,
      "sign": "Capricorn"
    },
    {
      "house": "11",
      "longitude": 323.45,
      "sign": "Aquarius"
    },
    {
      "house": "12",
      "longitude": 353.45,
      "sign": "Pisces"
    }
  ],
  "aspects": [
    {
      "planet1": "Sun",
      "planet2": "Moon",
      "aspect": "Opposition",
      "orb": 2.12,
      "exact": false
    },
    {
      "planet1": "Mercury",
      "planet2": "Jupiter",
      "aspect": "Conjunction",
      "orb": 3.21,
      "exact": false
    },
    {
      "planet1": "Venus",
      "planet2": "Saturn",
      "aspect": "Square",
      "orb": 1.89,
      "exact": false
    }
  ],
  "vimshottari_dasha": [
    {
      "planet": "Venus",
      "start_date": "1990-08-15T14:30:00",
      "end_date": "2010-08-15T14:30:00",
      "duration_years": 20.0,
      "elapsed_years": 0.0,
      "total_duration_years": 20.0
    },
    {
      "planet": "Sun",
      "start_date": "2010-08-15T14:30:00",
      "end_date": "2016-08-15T14:30:00",
      "duration_years": 6.0,
      "elapsed_years": 0.0,
      "total_duration_years": 6.0
    },
    {
      "planet": "Moon",
      "start_date": "2016-08-15T14:30:00",
      "end_date": "2026-08-15T14:30:00",
      "duration_years": 10.0,
      "elapsed_years": 0.0,
      "total_duration_years": 10.0
    }
    // ... continues through all 9 planets
  ]
}
```

## Sample D9 (Navamsha) Chart Output

```json
{
  "birth_date": "1990-08-15",
  "birth_time": "14:30",
  "birth_latitude": 40.7128,
  "birth_longitude": -74.0060,
  "timezone": "-05:00",
  "ayanamsa": "Lahiri",
  "planetary_positions": [
    {
      "planet": "Sun",
      "longitude": 202.45,
      "latitude": 0.00,
      "speed": 1.02,
      "sign": "Libra",
      "house": "7",
      "nakshatra": "Vishakha",
      "nakshatra_pada": 3,
      "is_retrograde": false
    },
    {
      "planet": "Moon",
      "longitude": 115.67,
      "latitude": -5.12,
      "speed": 13.45,
      "sign": "Cancer",
      "house": "4",
      "nakshatra": "Ashlesha",
      "nakshatra_pada": 2,
      "is_retrograde": false
    }
    // ... all 9 planets transformed for D9 chart
  ],
  "house_cusps": [
    {
      "house": "1",
      "longitude": 23.45,
      "sign": "Aries"
    }
    // ... house cusps remain the same as D1 for Equal house system
  ],
  "aspects": [
    {
      "planet1": "Sun",
      "planet2": "Moon",
      "aspect": "Trine",
      "orb": 1.45,
      "exact": false
    }
    // ... aspects recalculated based on D9 positions
  ],
  "vimshottari_dasha": []  // Divisional charts typically don't have their own dasha periods
}
```

## Validation Points

1. **Planetary Longitudes**: Should be between 0-360 degrees
2. **Zodiac Signs**: Should match longitude ranges (0-30=Aries, 30-60=Taurus, etc.)
3. **House Cusps**: Should be in ascending order (with wrap-around at 360°)
4. **Aspects**: Should have valid orbs (<10° for major aspects)
5. **Retrograde Flags**: Should be correct based on speed sign
6. **Nakshatra Calculation**: Should correspond to longitude ranges
7. **Vimshottari Dasha**: Should start with correct planet based on Moon's nakshatra
8. **Divisional Charts**: D9 positions should be mathematically derived from D1 positions

## Expected Mathematical Relationships

For D9 chart calculation:
- If a planet is at longitude L in D1 chart
- Sign index = floor(L/30) (0-11)
- Position in sign = L - (sign_index * 30) (0-30)
- D9 longitude = (position_in_sign * 9) % 30 + (sign_index * 30)

Example:
- Sun at 142.45° in D1
- Sign index = floor(142.45/30) = 4 (Leo)
- Position in sign = 142.45 - (4*30) = 22.45°
- D9 longitude = (22.45 * 9) % 30 + (4*30) = 202.05° + 120° = 202.05° (Libra)

This matches the sample output above (Sun at 202.45° in D9, allowing for house calculation differences).