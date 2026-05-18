# IMPORT STRATEGY GUIDE: Astrology Engine

## Overview
This document defines the correct import strategy for the astrology-engine package once properly structured. It covers internal package imports, external usage, and testing patterns.

## Target Package Structure
Assuming the recommended structure from PACKAGE_ARCHITECTURE_REPORT.md:
```
astrology-engine/
├── src/
│   └── astrology_engine/          # ← THE PACKAGE
│       ├── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py
│       │   ├── models.py
│       │   └── exceptions.py
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── calculations.py
│       │   └── coordinates.py
│       ├── charts/
│       │   ├── __init__.py
│       │   └── base.py
│       ├── divisional/
│       │   ├── __init__.py
│       │   └── service.py
│       ├── interpretations/
│       │   └── __init__.py
│       └── api/
│           └── __init__.py
└── tests/
    ├── __init__.py
    └── test_calculations.py
```

## Internal Package Imports (Within src/astrology_engine/)

### Relative Import Pattern (Preferred)
Use relative imports for intra-package communication:
```python
# From calculations.py to coordinates.py (same level)
from .coordinates import julian_day, validate_birth_data, parse_timezone

# From calculations.py to core config (one level up)
from ..core.config import ZODIAC_SIGNS, NAKSHATRAS, PLANETS, DEGREES_PER_SIGN, DEGREES_PER_NAKSHATRA

# From calculations.py to core models (one level up)
from ..core.models import PlanetaryPosition, HouseCusp, AspectInfo, Aspect, Planet, ZodiacSign, House, Nakshatra

# From calculations.py to core exceptions (one level up)
from ..core.exceptions import CalculationError, SwissEphemerisError
```

### Absolute Import Alternative (Within Package)
Also acceptable but less portable:
```python
# Absolute imports from package root
from astrology_engine.core.config import ZODIAC_SIGNS
from astrology_engine.utils.coordinates import julian_day
```

**Note**: Relative imports are preferred within the package as they make the package more portable and resistant to top-level name changes.

## External Usage (After Installation)

Once the package is installed via `pip install -e .` or `pip install .`:

### Standard Import Pattern
```python
# Primary recommended pattern
from astrology_engine.utils.coordinates import validate_birth_data, parse_timezone, julian_day
from astrology_engine.utils.calculations import (
    get_zodiac_sign, 
    get_nakshatra, 
    normalize_longitude,
    calculate_planetary_position,
    calculate_house_cusps,
    calculate_aspects,
    detect_basic_yogas,
    calculate_vimshottari_dasha_start,
    generate_vimshottari_dasha
)
from astrology_engine.charts.base import ChartCalculator
from astrology_engine.core.models import PlanetaryPosition, HouseCusp
from astrology_engine.core.config import DEFAULT_AYANAMSA, ZODIAC_SIGNS, NAKSHATRAS

# For type hints
from astrology_engine.core.models import BaseChart
```

### Package-Level Imports
```python
import astrology_engine
from astrology_engine import utils, core, charts

# Then access submodules
utils.coordinates.validate_birth_data()
core.models.PlanetaryPosition
```

## Testing Import Strategy

### Unit Tests (tests/test_calculations.py)
Tests should NOT manipulate sys.path. Instead, they should:
1. Run from the project root with `python -m pytest` or
2. Use standard imports assuming the package is installed

**Correct test import pattern:**
```python
# NO sys.path manipulation needed when properly installed
from astrology_engine.utils.coordinates import validate_birth_data, parse_timezone, julian_day
from astrology_engine.utils.calculations import (
    get_zodiac_sign, 
    get_nakshatra, 
    normalize_longitude,
    calculate_planetary_position, 
    calculate_house_cusps,
    calculate_aspects, 
    detect_basic_yogas,
    calculate_vimshottari_dasha_start, 
    generate_vimshottari_dasha
)
from astrology_engine.charts.base import ChartCalculator
from astrology_engine.core.models import PlanetaryPosition, HouseCusp, AspectInfo
from astrology_engine.core.config import ZODIAC_SIGNS, NAKSHATRAS, PLANETS, DEFAULT_AYANAMSA
```

### Test Execution
- **Preferred**: `python -m pytest tests/` from project root
- **Alternative**: `pytest tests/` (if pytest in path)
- **Avoid**: Direct script execution with sys.path manipulation

## Demo/Script Import Strategy

### After Proper Packaging
Demo scripts like `validation_demo.py` should use standard imports:
```python
# Correct pattern for installed package
from astrology_engine.utils.coordinates import validate_birth_data, parse_timezone, julian_day
from astrology_engine.utils.calculations import (
    get_zodiac_sign,
    get_nakshatra,
    normalize_longitude,
    calculate_planetary_position,
    calculate_house_cusps,
    calculate_aspects,
    detect_basic_yogas,
    calculate_vimshottari_dasha_start,
    generate_vimshottari_dasha
)
from astrology_engine.charts.base import ChartCalculator
from astrology_engine.core.models import PlanetaryPosition, HouseCusp
from astrology_engine.core.config import ZODIAC_SIGNS, NAKSHATRAS, PLANETS, DEFAULT_AYANAMSA
```

### Development Workflow
During development before installation:
1. Install in development mode: `pip install -e .`
2. Then run demos/scripts normally without sys.path manipulation

## pyproject.toml Configuration for Correct Imports

The pyproject.toml should be configured to expose the package correctly:

```toml
[tool.setuptools.packages]
find = {where = ["src"]}

[tool.setuptools.package-dir]
"" = "src"

# This makes the installable package named "astrology_engine"
# containing all modules under src/astrology_engine/
```

## Import Validation Checklist

### After restructuring and installing with `pip install -e .`:

✅ **Package can be imported:**
```python
import astrology_engine
print(astrology_engine.__version__)  # If defined
```

✅ **Submodules accessible:**
```python
from astrology_engine.utils.coordinates import julian_day
from astrology_engine.core.models import PlanetaryPosition
```

✅ **Relative imports work internally:**
No "attempted relative import beyond top-level package" errors

✅ **Tests pass without sys.path manipulation:**
```bash
python -m pytest tests/ -v
```

✅ **Demos run from any directory:**
```bash
# From anywhere after installation
python /path/to/astrology-engine/examples/validation_demo.py
```

## Common Import Pitfalls to Avoid

### ❌ DO NOT:
```python
# Fragile path manipulation (avoid in production code)
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Confusing absolute paths that break portability
from src.utils.coordinates import julian_day  # Only works if src is in path

# Mixed strategies in same file
from ..core.config import something  # Relative
from src.utils.coordinates import something_else  # Absolute/src-based
```

### ✅ DO:
```python
# Clean relative imports within package (after proper structuring)
from ..core.config import ZODIAC_SIGNS
from .coordinates import julian_day

# Clean external usage after installation
from astrology_engine.utils.coordinates import julian_day
```

## Migration Path

To transition from current broken state to correct imports:

1. **Restructure directories** -> Move all src/* contents to src/astrology_engine/
2. **Fix __init__.py files** -> Remove src/__init__.py, ensure src/astrology_engine/__init__.py exists
3. **Verify internal relative imports** -> They should work as-written after restructuring
4. **Update pyproject.toml** -> Ensure proper package discovery
5. **Install in development mode** -> `pip install -e .`
6. **Remove sys.path manipulation** -> From all scripts and tests
7. **Validate** -> Run tests and demos from various directories

## Summary

The correct import strategy for astrology-engine relies on:
- Proper package structure with `src/astrology_engine/` as the package root
- Relative imports (`from ..core.config`, `from .coordinates`) for internal package communication
- Standard absolute imports (`from astrology_engine.utils.coordinates import ...`) for external usage
- Zero sys.path manipulation in production code, tests, or demos
- Development workflow using `pip install -e .` for editable installs

This strategy ensures the package works reliably across development, testing, and production environments.