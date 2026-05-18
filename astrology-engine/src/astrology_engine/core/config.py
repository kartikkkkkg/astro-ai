"""
Configuration constants for the astrology engine.
"""
from enum import Enum
from typing import Dict, List, Tuple

class Ayanamsa(str, Enum):
    LAHIRI = "Lahiri"
    RAMAN = "Raman"
    KRISHNAMURTI = "Krishnamurti"
    TRUE_CHITRA = "True Chitra"

# Default ayanamsa
DEFAULT_AYANAMSA = Ayanamsa.LAHIRI

# Zodiac signs in order
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# Nakshatras (lunar mansions) in order
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

# Planets in Vedic astrology
PLANETS = [
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
    "Saturn", "Rahu", "Ketu"
]

# House system (Equal house system for simplicity in MVP)
HOUSE_SYSTEM = "Equal"

# Aspects and their orbs (in degrees)
ASPECTS = {
    "Conjunction": 0,
    "Sextile": 60,
    "Square": 90,
    "Trine": 120,
    "Opposition": 180
}

ASPECT_ORBS = {
    "Conjunction": 8,
    "Sextile": 6,
    "Square": 6,
    "Trine": 8,
    "Opposition": 10
}

# Vimshottari Dasha periods (in years)
VIMHOTTARI_DASHA_PERIODS = {
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17,
    "Ketu": 7,
    "Venus": 20
}

# Nakshatra padas (quarters)
NAKSHATRA_PADAS = 4

# Degrees per nakshatra
DEGREES_PER_NAKSHATRA = 360 / len(NAKSHATRAS)  # 13°20'

# Degrees per zodiac sign
DEGREES_PER_SIGN = 30

# Swiss Ephemeris constants
SEFLG_SPEED = 256  # Speed flag for Swiss Ephemeris
SEFLG_TRUEPOS = 64  # True position flag