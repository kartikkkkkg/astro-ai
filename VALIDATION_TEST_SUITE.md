# Astrology Backend Validation Test Suite

## Overview

This document defines the validation test suite for verifying the deterministic accuracy and repeatability of the astrology backend API. The suite includes reference charts, golden test cases, and regression tests.

## Reference Charts

### Test Case 1: Standard Reference Chart
- **Date**: August 15, 1990
- **Time**: 14:30 (2:30 PM)
- **Latitude**: 19.0760 (Mumbai, India)
- **Longitude**: 72.8777
- **Timezone**: +05:30
- **Expected Sun Position**: Leo (approximately 142-144°)
- **Expected Moon Position**: Taurus (approximately 30-32°)

### Test Case 2: Midnight Birth
- **Date**: January 1, 2000
- **Time**: 00:00 (midnight)
- **Latitude**: 0.0 (Equator)
- **Longitude**: 0.0 (Prime Meridian)
- **Timezone**: +00:00

### Test Case 3: Extreme Latitude
- **Date**: June 21, 2020 (Summer Solstice)
- **Time**: 12:00 (noon)
- **Latitude**: 78.2232 (Ny-Ålesund, Svalbard)
- **Longitude**: 15.6469
- **Timezone**: +01:00

### Test Case 4: Western Hemisphere
- **Date**: December 25, 2021
- **Time**: 09:15
- **Latitude**: 34.0522 (Los Angeles)
- **Longitude**: -118.2437
- **Timezone**: -08:00 (PST)

### Test Case 5: Eastern Hemisphere
- **Date**: March 20, 2022 (Equinox)
- **Time**: 06:30
- **Latitude**: -33.8688 (Sydney, Australia)
- **Longitude**: 151.2093
- **Timezone**: +11:00 (AEDT)

## Golden Test Data

Expected values for Test Case 1 (Mumbai, Aug 15, 1990 14:30 IST):

### Planetary Positions (Approximate)
- **Sun**: 142.5° Leo, 5th House
- **Moon**: 32.0° Taurus, 2nd House
- **Mars**: 255.8° Sagittarius, 9th House
- **Mercury**: 128.3° Leo, 5th House
- **Jupiter**: 298.7° Capricorn, 10th House
- **Venus**: 176.5° Virgo, 6th House
- **Saturn**: 299.2° Capricorn, 10th House
- **Rahu**: 66.3° Gemini, 3rd House
- **Ketu**: 246.3° Sagittarius, 9th House

### House Cusps (Equal House System Approximation)
- **House 1**: 23.5° Aries
- **House 2**: 53.5° Taurus
- **House 3**: 83.5° Gemini
- **House 4**: 113.5° Cancer
- **House 5**: 143.5° Leo
- **House 6**: 173.5° Virgo
- **House 7**: 203.5° Libra
- **House 8**: 233.5° Scorpio
- **House 9**: 263.5° Sagittarius
- **House 10**: 293.5° Capricorn
- **House 11**: 323.5° Aquarius
- **House 12**: 353.5° Pisces

## Validation Test Implementation

### Test Categories

1. **Deterministic Repeatability Tests**
   - Same input produces identical output across multiple calls
   - Test with various timezones and coordinate combinations

2. **Accuracy Validation Tests**
   - Compare against known reference values
   - Validate planetary longitudes within ±0.5° tolerance
   - Validate house placements correctness

3. **Edge Case Tests**
   - Date boundaries (leap years, year transitions)
   - Time boundaries (midnight, DST transitions)
   - Coordinate extremes (poles, equator, dateline)
   - Invalid input handling

4. **Divisional Chart Tests**
   - D1 chart accuracy
   - D9 chart accuracy
   - Nakshatra and pada calculations
   - Aspect calculations
   - Vimshottari dasha start calculations

## Test Implementation Plan

### Phase 1: Basic API Connectivity
- Verify all endpoints are accessible
- Test validation error responses
- Confirm successful chart generation

### Phase 2: Deterministic Repeatability
- Call same endpoint 10 times with identical input
- Verify all outputs are byte-for-byte identical
- Test across different times of day to rule out caching

### Phase 3: Accuracy Validation
- Compare generated charts against golden test data
- Validate planetary positions within tolerance
- Validate house cusp calculations
- Validate nakshatra and pada assignments

### Phase 4: Edge Case Testing
- Test leap year dates (Feb 29)
- Test timezone edge cases (+12:00, -12:00)
- Test coordinate extremes (90°N, 90°S, 180°E/W)
- Test midnight births across timezones
- Test DST transition dates

### Phase 5: Divisional Chart Validation
- Test D1 chart generation
- Test D9 chart generation from D1 base
- Validate nakshatra calculations for both charts
- Validate aspect calculations
- Verify house placements are mathematically consistent

## Success Criteria

1. **Deterministic Repeatability**: 100% identical outputs for identical inputs
2. **Accuracy**: Planetary positions within ±0.5° of reference values
3. **Error Handling**: Appropriate HTTP status codes for invalid inputs
4. **Performance**: Reasonable response times (<5 seconds for calculation)
5. **Consistency**: Mathematical relationships between charts preserved

## Reporting

Test results will be documented in:
- VALIDATION_REPORT.md: Summary of test results and findings
- REFERENCE_TEST_DATASET.json: Golden test data for automated validation
- REGRESSION_TEST_SUITE.py: Automated test scripts for CI/CD

## Tools Required

- pytest for test execution
- requests or httpx for API testing
- json for test data handling
- datetime for date/time calculations

## Notes

- Tolerance of ±0.5° accounts for minor differences in ayanamsa precision
- House system validation may vary based on implementation (Placidus vs Equal House)
- Nakshatra validation uses standard 27 nakshatra system with 4 padas each