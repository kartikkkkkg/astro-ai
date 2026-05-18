# NAKSHATRA AND PADA BOUNDARY SPECIFICATION

## Overview
This document defines the mathematical and astrological conventions for nakshatra (lunar mansion) and pada (quarter) calculations in the astrology-engine package.

## Fundamental Constants

### Nakshatra System
- Total nakshatras: 27
- Degrees per nakshatra: 360° / 27 = 13°20' = 13.333...° (repeating)
- Degrees per pada: (360° / 27) / 4 = 3°20' = 3.333...° (repeating)

### Mathematical Representation
For precise calculations, we use:
```
DEGREES_PER_NakshATRA = 360 / 27 = 40/3 = 13.333333333333334°
DEGREES_PER_PADA = (360 / 27) / 4 = 10/3 = 3.3333333333333335°
```

## Boundary Convention

### Inclusive/Exclusive Rules
To avoid ambiguity at boundaries, we adopt the following convention:
- **Lower bound**: Inclusive [ 
- **Upper bound**: Exclusive )
- This means: [nakshatra_start, nakshatra_start + DEGREES_PER_NAKSHATRA)
- And for padas: [pada_start, pada_start + DEGREES_PER_PADA)

### Nakshatra Boundaries
For nakshatra index `n` (0-26):
- Start longitude: n × DEGREES_PER_NAKSHATRA
- End longitude: (n + 1) × DEGREES_PER_NAKSHATRA (exclusive)
- Valid range: [n × 13.333..., (n + 1) × 13.333...)

### Pada Boundaries
Within a nakshatra, for pada index `p` (0-3):
- Start longitude: nakshatra_start + p × DEGREES_PER_PADA
- End longitude: nakshatra_start + (p + 1) × DEGREES_PER_PADA (exclusive)
- Valid range: [nakshatra_start + p × 3.333..., nakshatra_start + (p + 1) × 3.333...)

## Pada Calculation Formula
Given a longitude L (0 ≤ L < 360):

1. Normalize L to [0, 360) range
2. nakshatra_index = floor(L / DEGREES_PER_NAKSHATRA)
3. position_in_nakshatra = L - (nakshatra_index × DEGREES_PER_NAKSHATRA)
4. pada_index = floor(position_in_nakshatra / DEGREES_PER_PADA)
5. pada_number = pada_index + 1 (1-based indexing for human consumption)

## Validation Test Cases

### Exact Boundary Points
| Longitude | Expected Nakshatra | Expected Pada | Reasoning |
|-----------|-------------------|---------------|-----------|
| 0.000000° | Ashwini (1) | 1 | Start of first nakshatra |
| 3.333333° | Ashwini (1) | 2 | End of Pada 1 / Start of Pada 2 |
| 6.666666° | Ashwini (1) | 3 | End of Pada 2 / Start of Pada 3 |
| 10.000000° | Ashwini (1) | 4 | End of Pada 3 / Start of Pada 4 |
| 13.333333° | Bharani (2) | 1 | Start of second nakshatra |

### Interior Points
| Longitude | Expected Nakshatra | Expected Pada | Reasoning |
|-----------|-------------------|---------------|-----------|
| 1.666666° | Ashwini (1) | 1 | Within first pada |
| 5.000000° | Ashwini (1) | 2 | Within second pada |
| 8.333333° | Ashwini(1) | 3 | Within third pada |
| 11.666666° | Ashwini(1) | 4 | Within fourth pada |

### Transition Points (Edge Cases)
These test the precision of our calculations at exact boundaries:

| Longitude (Decimal) | Description |
|---------------------|-------------|
| 0.0 | Exact start of Ashwini Pada 1 |
| 10/3 | Exact end of Ashwini Pada 1 / Start of Pada 2 |
| 20/3 | Exact end of Ashwini Pada 2 / Start of Pada 3 |
| 30/3 | Exact end of Ashwini Pada 3 / Start of Pada 4 |
| 40/3 | Exact start of Bharani Pada 1 |

## Current Implementation Analysis

The current implementation uses:
```python
nakshatra_index = int(normalized_longitude // DEGREES_PER_NAKSHATRA)
pada = int((normalized_longitude % DEGREES_PER_NAKSHATRA) / (DEGREES_PER_NAKSHATRA / 4)) + 1
```

This follows the mathematical specification exactly.

### Test Case: 6.667°
Let's trace through the calculation:

1. normalized_longitude = 6.667 (already in [0,360))
2. nakshatra_index = int(6.667 // 13.333...) = int(0.5) = 0 → Ashwini
3. position_in_nakshatra = 6.667 % 13.333... = 6.667
4. pada_index = int(6.667 / (13.333.../4)) = int(6.667 / 3.333...) = int(2.0001) = 2
5. pada_number = 2 + 1 = 3

The result is Pada 3, which is mathematically correct for longitude 6.667°.

### The Discrepancy
The test validation_demo.py expects:
- 6.667° → ("Ashwini", 2)  [Pada 2]

But according to our boundary specification:
- Ashwini Pada 2 covers [3.333..., 6.666...)
- Ashwini Pada 3 covers [6.666..., 10.000...)
- Since 6.667° ≥ 6.666°, it belongs to Pada 3

## Resolution Options

### Option 1: Adjust Test Expectation (RECOMMENDED)
The mathematical implementation is correct according to standard Vedic astrology boundaries.
The test expectation of "Middle of Ashwini" for 6.667° is incorrect.
- True middle of Ashwini = 13.333.../2 = 6.666...°
- At exactly 6.666...°, we're at the Pada 2/Pada 3 boundary
- Our convention places this boundary point in Pada 3 (upper bound exclusive)

### Option 2: Change Boundary Convention
We could adopt a different convention where boundaries are rounded down, but this would:
1. Create inconsistency with standard mathematical floor division
2. Potentially cause issues at other boundaries
3. Deviate from common practice in astronomical calculations

## Recommendation
Keep the current mathematically correct implementation and update the test expectation in validation_demo.py to reflect the proper boundary convention.

The nakshatra calculation logic is sound and follows established astrological-mathematical principles.