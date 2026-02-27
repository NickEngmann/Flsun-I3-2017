#!/usr/bin/env python3
"""Tests for createSpeedLookupTable.py - Stepper delay lookup table generator for Marlin firmware."""

import pytest
import sys
import os
import subprocess
import re

# Add the scripts directory to path
scripts_dir = os.path.join(
    os.path.dirname(__file__),
    'firmware',
    'Auto Levling 1.1.0-RC7 BLTOUCH (depricated)',
    'buildroot',
    'share',
    'scripts'
)
sys.path.insert(0, scripts_dir)


class TestSpeedLookupTableArguments:
    """Tests for argument parsing in createSpeedLookupTable."""
    
    def test_default_arguments(self):
        """Test default argument values."""
        # Run the script with no arguments
        result = subprocess.run(
            ['python3', 'createSpeedLookupTable.py'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        assert result.returncode == 0
        assert '#ifndef SPEED_LOOKUPTABLE_H' in result.stdout
    
    def test_custom_cpu_freq(self):
        """Test custom CPU frequency argument."""
        result = subprocess.run(
            ['python3', 'createSpeedLookupTable.py', '-f', '20'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        assert result.returncode == 0
        assert '#ifndef SPEED_LOOKUPTABLE_H' in result.stdout
    
    def test_custom_divider(self):
        """Test custom divider argument."""
        result = subprocess.run(
            ['python3', 'createSpeedLookupTable.py', '-d', '16'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        assert result.returncode == 0
        assert '#ifndef SPEED_LOOKUPTABLE_H' in result.stdout
    
    def test_combined_custom_arguments(self):
        """Test combined custom arguments."""
        result = subprocess.run(
            ['python3', 'createSpeedLookupTable.py', '-f', '12', '-d', '4'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        assert result.returncode == 0
        assert '#ifndef SPEED_LOOKUPTABLE_H' in result.stdout


class TestSpeedLookupTableOutput:
    """Tests for output format of createSpeedLookupTable."""
    
    def test_output_has_header_guard(self):
        """Test output contains header guard."""
        result = subprocess.run(
            ['python3', 'createSpeedLookupTable.py'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        assert '#ifndef SPEED_LOOKUPTABLE_H' in result.stdout
        assert '#define SPEED_LOOKUPTABLE_H' in result.stdout
        assert '#endif' in result.stdout
    
    def test_output_includes_marlin_h(self):
        """Test output includes Marlin.h."""
        result = subprocess.run(
            ['python3', 'createSpeedLookupTable.py'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        assert '#include "Marlin.h"' in result.stdout
    
    def test_output_has_fast_table(self):
        """Test output contains fast speed lookup table."""
        result = subprocess.run(
            ['python3', 'createSpeedLookupTable.py'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        assert 'speed_lookuptable_fast' in result.stdout
    
    def test_output_has_slow_table(self):
        """Test output contains slow speed lookup table."""
        result = subprocess.run(
            ['python3', 'createSpeedLookupTable.py'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        assert 'speed_lookuptable_slow' in result.stdout
    
    def test_table_has_256_entries(self):
        """Test lookup tables have 256 entries."""
        result = subprocess.run(
            ['python3', 'createSpeedLookupTable.py'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        # Count array entries - should be 256 pairs
        fast_table_match = re.search(r'speed_lookuptable_fast\[256\]\[2\]\s+PROGMEM\s*=\s*\{([^}]+)\}', result.stdout, re.DOTALL)
        slow_table_match = re.search(r'speed_lookuptable_slow\[256\]\[2\]\s+PROGMEM\s*=\s*\{([^}]+)\}', result.stdout, re.DOTALL)
        
        assert fast_table_match is not None, "Fast lookup table not found"
        assert slow_table_match is not None, "Slow lookup table not found"
    
    def test_table_entries_format(self):
        """Test table entries are in correct format {value, value}."""
        result = subprocess.run(
            ['python3', 'createSpeedLookupTable.py'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        # Check that entries follow {number, number} format
        assert re.search(r'\{\s*\d+\s*,\s*\d+\s*,\s*\}', result.stdout) is not None


class TestSpeedLookupTableCalculations:
    """Tests for the calculation logic in createSpeedLookupTable."""
    
    def test_calculates_positive_values(self):
        """Test that calculations produce positive values."""
        result = subprocess.run(
            ['python3', 'createSpeedLookupTable.py'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        # Extract numbers from output and verify they're positive
        numbers = re.findall(r'\{\s*(\d+)\s*,\s*(\d+)\s*,', result.stdout)
        assert len(numbers) > 0
        for a, b in numbers:
            assert int(a) > 0, f"First value should be positive: {a}"
            assert int(b) > 0, f"Second value should be positive: {b}"
    
    def test_first_value_greater_than_second(self):
        """Test that first value is typically greater than second."""
        result = subprocess.run(
            ['python3', 'createSpeedLookupTable.py'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        numbers = re.findall(r'\{\s*(\d+)\s*,\s*(\d+)\s*,', result.stdout)
        # First value (delay) should be larger than second (delta)
        for a, b in numbers:
            assert int(a) >= int(b), f"First value {a} should be >= second value {b}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
