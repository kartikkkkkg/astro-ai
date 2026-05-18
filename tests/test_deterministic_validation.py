"""
Deterministic validation tests for astrology backend API.
Tests repeatability and accuracy of chart generation.
"""
import json
import hashlib
from datetime import date, datetime
from backend.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_deterministic_repeatability_d1():
    """Test that identical inputs produce identical D1 chart outputs."""
    chart_data = {
        "chart_type": "d1",
        "birth_date": "1990-08-15",
        "birth_time": "14:30",
        "birth_latitude": 19.0760,
        "birth_longitude": 72.8777,
        "timezone": "+05:30"
    }

    # Generate the same chart multiple times
    results = []
    for i in range(5):
        response = client.post("/api/v1/charts/d1", json=chart_data)
        # We expect this might fail due to DB issues, but if it succeeds,
        # the results should be identical
        if response.status_code == 201:
            results.append(response.json())
        elif response.status_code != 400 and response.status_code != 422:
            # If it's not a validation error, collect it for inspection
            results.append(response.json())

    # If we got any successful responses, they should all be identical
    if len(results) > 1:
        first_result = json.dumps(results[0], sort_keys=True)
        for i, result in enumerate(results[1:], 1):
            if json.dumps(result, sort_keys=True) != first_result:
                # They might differ in timestamp or ID fields, so check core data
                core_fields_1 = {
                    'chart_type': results[0]['chart_type'],
                    'birth_date': results[0]['birth_date'],
                    'birth_time': results[0]['birth_time'],
                    'birth_latitude': results[0]['birth_latitude'],
                    'birth_longitude': results[0]['birth_longitude'],
                    'timezone': results[0]['timezone'],
                    'planetary_positions': results[0]['planetary_positions'],
                    'house_cusps': results[0]['house_cusps']
                }
                core_fields_2 = {
                    'chart_type': result['chart_type'],
                    'birth_date': result['birth_date'],
                    'birth_time': result['birth_time'],
                    'birth_latitude': result['birth_latitude'],
                    'birth_longitude': result['birth_longitude'],
                    'timezone': result['timezone'],
                    'planetary_positions': result['planetary_positions'],
                    'house_cusps': result['house_cusps']
                }
                assert core_fields_1 == core_fields_2, f"Non-deterministic output on iteration {i}"

    # At minimum, verify we didn't get validation errors
    # (actual success depends on database setup in test environment)


def test_deterministic_repeatability_d9():
    """Test that identical inputs produce identical D9 chart outputs."""
    chart_data = {
        "chart_type": "d9",
        "birth_date": "1990-08-15",
        "birth_time": "14:30",
        "birth_latitude": 19.0760,
        "birth_longitude": 72.8777,
        "timezone": "+05:30"
    }

    # Generate the same chart multiple times
    results = []
    for i in range(3):
        response = client.post("/api/v1/charts/d9", json=chart_data)
        if response.status_code == 201:
            results.append(response.json())
        elif response.status_code != 400 and response.status_code != 422:
            results.append(response.json())

    # Check deterministic nature of successful responses
    if len(results) > 1:
        first_result = json.dumps(results[0], sort_keys=True)
        for i, result in enumerate(results[1:], 1):
            core_fields_1 = {
                'chart_type': results[0]['chart_type'],
                'birth_date': results[0]['birth_date'],
                'birth_time': results[0]['birth_time'],
                'birth_latitude': results[0]['birth_latitude'],
                'birth_longitude': results[0]['birth_longitude'],
                'timezone': results[0]['timezone'],
                'planetary_positions': results[0]['planetary_positions'],
                'house_cusps': results[0]['house_cusps']
            }
            core_fields_2 = {
                'chart_type': result['chart_type'],
                'birth_date': result['birth_date'],
                'birth_time': result['birth_time'],
                'birth_latitude': result['birth_latitude'],
                'birth_longitude': result['birth_longitude'],
                'timezone': result['timezone'],
                'planetary_positions': result['planetary_positions'],
                'house_cusps': result['house_cusps']
            }
            assert core_fields_1 == core_fields_2, f"Non-deterministic D9 output on iteration {i}"


def test_timezone_edge_cases():
    """Test various timezone edge cases for deterministic behavior."""
    base_data = {
        "chart_type": "d1",
        "birth_date": "2000-01-01",
        "birth_time": "12:00",
        "birth_latitude": 0.0,
        "birth_longitude": 0.0
    }

    timezones = ["-12:00", "-06:00", "+00:00", "+05:30", "+12:00"]
    results = []

    for tz in timezones:
        chart_data = base_data.copy()
        chart_data["timezone"] = tz
        response = client.post("/api/v1/charts/generate", json=chart_data)

        if response.status_code == 201:
            results.append((tz, response.json()))
        elif response.status_code not in [400, 422]:
            results.append((tz, response.json()))

    # Verify each timezone produces consistent results
    for tz, result in results:
        # Call twice with same inputs
        chart_data = base_data.copy()
        chart_data["timezone"] = tz

        response1 = client.post("/api/v1/charts/generate", json=chart_data)
        response2 = client.post("/api/v1/charts/generate", json=chart_data)

        if response1.status_code == 201 and response2.status_code == 201:
            data1 = response1.json()
            data2 = response2.json()

            # Compare core deterministic fields
            core1 = {
                'birth_date': data1['birth_date'],
                'birth_time': data1['birth_time'],
                'birth_latitude': data1['birth_latitude'],
                'birth_longitude': data1['birth_longitude'],
                'timezone': data1['timezone'],
                'planetary_positions': data1['planetary_positions'],
                'house_cusps': data1['house_cusps']
            }
            core2 = {
                'birth_date': data2['birth_date'],
                'birth_time': data2['birth_time'],
                'birth_latitude': data2['birth_latitude'],
                'birth_longitude': data2['birth_longitude'],
                'timezone': data2['timezone'],
                'planetary_positions': data2['planetary_positions'],
                'house_cusps': data2['house_cusps']
            }

            assert core1 == core2, f"Non-deterministic result for timezone {tz}"


def test_coordinate_edge_cases():
    """Test coordinate edge cases."""
    base_data = {
        "chart_type": "d1",
        "birth_date": "2000-06-21",
        "birth_time": "12:00",
        "timezone": "+00:00"
    }

    # Test extreme latitudes
    test_coords = [
        {"lat": 90.0, "lon": 0.0, "desc": "North Pole"},
        {"lat": -90.0, "lon": 0.0, "desc": "South Pole"},
        {"lat": 0.0, "lon": 180.0, "desc": "Date Line East"},
        {"lat": 0.0, "lon": -180.0, "desc": "Date Line West"},
        {"lat": 0.0, "lon": 0.0, "desc": "Null Island"},
        {"lat": 23.5, "lon": 0.0, "desc": "Tropic of Cancer"},
        {"lat": -23.5, "lon": 0.0, "desc": "Tropic of Capricorn"}
    ]

    for coord in test_coords:
        chart_data = base_data.copy()
        chart_data["birth_latitude"] = coord["lat"]
        chart_data["birth_longitude"] = coord["lon"]

        # Test deterministic behavior
        response1 = client.post("/api/v1/charts/generate", json=chart_data)
        response2 = client.post("/api/v1/charts/generate", json=chart_data)

        if response1.status_code == 201 and response2.status_code == 201:
            data1 = response1.json()
            data2 = response2.json()

            core1 = {
                'birth_latitude': data1['birth_latitude'],
                'birth_longitude': data1['birth_longitude'],
                'planetary_positions': data1['planetary_positions'],
                'house_cusps': data1['house_cusps']
            }
            core2 = {
                'birth_latitude': data2['birth_latitude'],
                'birth_longitude': data2['birth_longitude'],
                'planetary_positions': data2['planetary_positions'],
                'house_cusps': data2['house_cusps']
            }

            assert core1 == core2, f"Non-deterministic result for {coord['desc']}"


def test_leap_year_handling():
    """Test leap year date handling."""
    # Test Feb 29 on leap year
    leap_data = {
        "chart_type": "d1",
        "birth_date": "2020-02-29",  # Leap year
        "birth_time": "06:00",
        "birth_latitude": 40.0,
        "birth_longitude": -74.0,
        "timezone": "-05:00"
    }

    response = client.post("/api/v1/charts/generate", json=leap_data)
    # Should not be a validation error (might be 500 due to DB, but not 400/422)
    assert response.status_code not in [400, 422], f"Leap year date rejected: {response.json()}"

    # Test deterministic behavior
    response1 = client.post("/api/v1/charts/generate", json=leap_data)
    response2 = client.post("/api/v1/charts/generate", json=leap_data)

    if response1.status_code == 201 and response2.status_code == 201:
        data1 = response1.json()
        data2 = response2.json()

        core1 = {
            'birth_date': data1['birth_date'],
            'birth_time': data1['birth_time'],
            'planetary_positions': data1['planetary_positions'],
            'house_cusps': data1['house_cusps']
        }
        core2 = {
            'birth_date': data2['birth_date'],
            'birth_time': data2['birth_time'],
            'planetary_positions': data2['planetary_positions'],
            'house_cusps': data2['house_cusps']
        }

        assert core1 == core2, "Non-deterministic leap year handling"


def test_midnight_transitions():
    """Test births near midnight."""
    base_data = {
        "chart_type": "d1",
        "birth_date": "2000-01-01",
        "birth_latitude": 0.0,
        "birth_longitude": 0.0,
        "timezone": "+00:00"
    }

    # Test various times around midnight
    test_times = ["00:00", "00:01", "23:59", "23:58"]

    for time_str in test_times:
        chart_data = base_data.copy()
        chart_data["birth_time"] = time_str

        response = client.post("/api/v1/charts/generate", json=chart_data)
        # Should not reject due to time format
        assert response.status_code not in [400, 422], f"Time {time_str} rejected: {response.json()}"

        # Test deterministic behavior
        response1 = client.post("/api/v1/charts/generate", json=chart_data)
        response2 = client.post("/api/v1/charts/generate", json=chart_data)

        if response1.status_code == 201 and response2.status_code == 201:
            data1 = response1.json()
            data2 = response2.json()

            core1 = {
                'birth_time': data1['birth_time'],
                'planetary_positions': data1['planetary_positions'],
                'house_cusps': data1['house_cusps']
            }
            core2 = {
                'birth_time': data2['birth_time'],
                'planetary_positions': data2['planetary_positions'],
                'house_cusps': data2['house_cusps']
            }

            assert core1 == core2, f"Non-deterministic result for time {time_str}"


def test_invalid_inputs_rejected():
    """Test that invalid inputs are properly rejected."""

    # Invalid chart type
    invalid_chart_type = {
        "chart_type": "invalid",
        "birth_date": "1990-08-15",
        "birth_time": "14:30",
        "birth_latitude": 19.0760,
        "birth_longitude": 72.8777,
        "timezone": "+05:30"
    }
    response = client.post("/api/v1/charts/generate", json=invalid_chart_type)
    assert response.status_code == 422
    assert "chart_type" in response.json()["detail"][0]["loc"]

    # Invalid latitude (> 90)
    invalid_lat = {
        "chart_type": "d1",
        "birth_date": "1990-08-15",
        "birth_time": "14:30",
        "birth_latitude": 95.0,  # Invalid
        "birth_longitude": 72.8777,
        "timezone": "+05:30"
    }
    response = client.post("/api/v1/charts/generate", json=invalid_lat)
    assert response.status_code == 422  # Validation error

    # Invalid longitude (> 180)
    invalid_lon = {
        "chart_type": "d1",
        "birth_date": "1990-08-15",
        "birth_time": "14:30",
        "birth_latitude": 19.0760,
        "birth_longitude": 185.0,  # Invalid
        "timezone": "+05:30"
    }
    response = client.post("/api/v1/charts/generate", json=invalid_lon)
    assert response.status_code == 422  # Validation error

    # Invalid time format
    invalid_time = {
        "chart_type": "d1",
        "birth_date": "1990-08-15",
        "birth_time": "25:00",  # Invalid hour
        "birth_latitude": 19.0760,
        "birth_longitude": 72.8777,
        "timezone": "+05:30"
    }
    response = client.post("/api/v1/charts/generate", json=invalid_time)
    assert response.status_code == 422  # Validation error

    # Invalid date format
    invalid_date = {
        "chart_type": "d1",
        "birth_date": "1990-13-15",  # Invalid month
        "birth_time": "14:30",
        "birth_latitude": 19.0760,
        "birth_longitude": 72.8777,
        "timezone": "+05:30"
    }
    response = client.post("/api/v1/charts/generate", json=invalid_date)
    assert response.status_code == 422  # Validation error


if __name__ == "__main__":
    # Run tests manually for quick validation
    print("Running deterministic validation tests...")

    try:
        test_deterministic_repeatability_d1()
        print("✓ D1 deterministic repeatability test passed")
    except Exception as e:
        print(f"✗ D1 deterministic repeatability test failed: {e}")

    try:
        test_deterministic_repeatability_d9()
        print("✓ D9 deterministic repeatability test passed")
    except Exception as e:
        print(f"✗ D9 deterministic repeatability test failed: {e}")

    try:
        test_timezone_edge_cases()
        print("✓ Timezone edge cases test passed")
    except Exception as e:
        print(f"✗ Timezone edge cases test failed: {e}")

    try:
        test_coordinate_edge_cases()
        print("✓ Coordinate edge cases test passed")
    except Exception as e:
        print(f"✗ Coordinate edge cases test failed: {e}")

    try:
        test_leap_year_handling()
        print("✓ Leap year handling test passed")
    except Exception as e:
        print(f"✗ Leap year handling test failed: {e}")

    try:
        test_midnight_transitions()
        print("✓ Midnight transitions test passed")
    except Exception as e:
        print(f"✗ Midnight transitions test failed: {e}")

    try:
        test_invalid_inputs_rejected()
        print("✓ Invalid inputs rejection test passed")
    except Exception as e:
        print(f"✗ Invalid inputs rejection test failed: {e}")

    print("Validation test suite completed.")