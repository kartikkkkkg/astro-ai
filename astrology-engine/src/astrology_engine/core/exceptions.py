"""
Custom exceptions for the astrology engine.
"""
class AstrologyEngineError(Exception):
    """Base exception for astrology engine errors."""
    pass

class InvalidBirthDataError(AstrologyEngineError):
    """Raised when birth data is invalid."""
    pass

class CalculationError(AstrologyEngineError):
    """Raised when a calculation fails."""
    pass

class SwissEphemerisError(AstrologyEngineError):
    """Raised when Swiss Ephemeris returns an error."""
    pass