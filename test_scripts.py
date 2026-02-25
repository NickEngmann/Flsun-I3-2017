#!/usr/bin/env python
"""Tests for FLsun I3 2017 Python utility scripts."""

import subprocess
import sys
import os


def test_g29_auto_help():
    """Test g29_auto.py help output."""
    script_path = "firmware/Auto Levling 1.1.0-RC7 BLTOUCH (depricated)/buildroot/share/scripts/g29_auto.py"
    result = subprocess.run(["python3", script_path, "--help"], 
                          capture_output=True, text=True)
    assert result.returncode == 0, f"g29_auto.py --help failed: {result.stderr}"
    assert "help" in result.stdout.lower() or "usage" in result.stdout.lower(), \
        "g29_auto.py --help should show usage information"


def test_create_speed_lookup_table_default():
    """Test createSpeedLookupTable.py with default arguments."""
    script_path = "firmware/Auto Levling 1.1.0-RC7 BLTOUCH (depricated)/buildroot/share/scripts/createSpeedLookupTable.py"
    result = subprocess.run(["python3", script_path], 
                          capture_output=True, text=True)
    assert result.returncode == 0, f"createSpeedLookupTable.py failed: {result.stderr}"
    assert "SPEED_LOOKUPTABLE_H" in result.stdout, \
        "Output should contain header guard"
    assert "speed_lookuptable_fast" in result.stdout, \
        "Output should contain fast lookup table"
    assert "speed_lookuptable_slow" in result.stdout, \
        "Output should contain slow lookup table"


def test_create_speed_lookup_table_custom():
    """Test createSpeedLookupTable.py with custom arguments."""
    script_path = "firmware/Auto Levling 1.1.0-RC7 BLTOUCH (depricated)/buildroot/share/scripts/createSpeedLookupTable.py"
    result = subprocess.run(["python3", script_path, "-f", "20", "-d", "16"], 
                          capture_output=True, text=True)
    assert result.returncode == 0, f"createSpeedLookupTable.py with custom args failed: {result.stderr}"
    assert "SPEED_LOOKUPTABLE_H" in result.stdout, \
        "Output should contain header guard"


def test_create_temperature_lookup_marlin_default():
    """Test createTemperatureLookupMarlin.py with default arguments."""
    script_path = "firmware/Auto Levling 1.1.0-RC7 BLTOUCH (depricated)/buildroot/share/scripts/createTemperatureLookupMarlin.py"
    result = subprocess.run(["python3", script_path], 
                          capture_output=True, text=True)
    assert result.returncode == 0, f"createTemperatureLookupMarlin.py failed: {result.stderr}"
    assert "Thermistor lookup table for Marlin" in result.stdout, \
        "Output should contain header comment"
    assert "NUMTEMPS" in result.stdout, \
        "Output should define NUMTEMPS"
    assert "temptable" in result.stdout, \
        "Output should contain temptable"


def test_create_temperature_lookup_marlin_custom():
    """Test createTemperatureLookupMarlin.py with custom arguments."""
    script_path = "firmware/Auto Levling 1.1.0-RC7 BLTOUCH (depricated)/buildroot/share/scripts/createTemperatureLookupMarlin.py"
    result = subprocess.run([
        "python3", script_path, 
        "--rp=4700", "--t1=25:100000", 
        "--t2=150:1641.9", "--t3=250:226.15", "--num-temps=36"
    ], capture_output=True, text=True)
    assert result.returncode == 0, f"createTemperatureLookupMarlin.py with custom args failed: {result.stderr}"
    assert "Thermistor lookup table for Marlin" in result.stdout, \
        "Output should contain header comment"


def test_g29_auto_script_exists():
    """Verify g29_auto.py script exists and is executable."""
    script_path = "firmware/Auto Levling 1.1.0-RC7 BLTOUCH (depricated)/buildroot/share/scripts/g29_auto.py"
    assert os.path.exists(script_path), "g29_auto.py should exist"
    assert os.path.isfile(script_path), "g29_auto.py should be a file"


def test_create_speed_lookup_script_exists():
    """Verify createSpeedLookupTable.py script exists."""
    script_path = "firmware/Auto Levling 1.1.0-RC7 BLTOUCH (depricated)/buildroot/share/scripts/createSpeedLookupTable.py"
    assert os.path.exists(script_path), "createSpeedLookupTable.py should exist"
    assert os.path.isfile(script_path), "createSpeedLookupTable.py should be a file"


def test_create_temperature_lookup_script_exists():
    """Verify createTemperatureLookupMarlin.py script exists."""
    script_path = "firmware/Auto Levling 1.1.0-RC7 BLTOUCH (depricated)/buildroot/share/scripts/createTemperatureLookupMarlin.py"
    assert os.path.exists(script_path), "createTemperatureLookupMarlin.py should exist"
    assert os.path.isfile(script_path), "createTemperatureLookupMarlin.py should be a file"


if __name__ == "__main__":
    # Run all tests
    test_functions = [
        test_g29_auto_help,
        test_create_speed_lookup_table_default,
        test_create_speed_lookup_table_custom,
        test_create_temperature_lookup_marlin_default,
        test_create_temperature_lookup_marlin_custom,
        test_g29_auto_script_exists,
        test_create_speed_lookup_script_exists,
        test_create_temperature_lookup_script_exists,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in test_functions:
        try:
            test_func()
            print(f"PASS: {test_func.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL: {test_func.__name__} - {e}")
            failed += 1
        except Exception as e:
            print(f"ERROR: {test_func.__name__} - {e}")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
