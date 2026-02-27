#!/usr/bin/env python3
"""Tests for createTemperatureLookupMarlin.py - Thermistor lookup table generator for Marlin firmware."""

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


class TestThermistorClass:
    """Tests for the Thermistor class."""
    
    def test_thermistor_initialization(self):
        """Test Thermistor class initialization with default values."""
        from createTemperatureLookupMarlin import Thermistor
        
        thermistor = Thermistor(
            rp=4700,
            t1=25, r1=100000,
            t2=150, r2=1641.9,
            t3=250, r3=226.15
        )
        
        assert thermistor.rp == 4700
        assert thermistor.c1 is not None
        assert thermistor.c2 is not None
        assert thermistor.c3 is not None
    
    def test_thermistor_temp_conversion(self):
        """Test temperature conversion from ADC value."""
        from createTemperatureLookupMarlin import Thermistor
        
        thermistor = Thermistor(
            rp=4700,
            t1=25, r1=100000,
            t2=150, r2=1641.9,
            t3=250, r3=226.15
        )
        
        # At room temperature (25C), ADC should be around mid-range
        temp = thermistor.temp(512)
        assert isinstance(temp, float)
    
    def test_thermistor_adc_conversion(self):
        """Test ADC conversion from temperature."""
        from createTemperatureLookupMarlin import Thermistor
        
        thermistor = Thermistor(
            rp=4700,
            t1=25, r1=100000,
            t2=150, r2=1641.9,
            t3=250, r3=226.15
        )
        
        adc = thermistor.adc(100)
        assert isinstance(adc, float)
        assert 0 <= adc <= 1023  # 10-bit ADC range
    
    def test_thermistor_resistance_conversion(self):
        """Test resistance conversion from ADC value."""
        from createTemperatureLookupMarlin import Thermistor
        
        thermistor = Thermistor(rp=4700, t1=25, r1=100000, t2=150, r2=1641.9, t3=250, r3=226.15)
        
        resistance = thermistor.resist(512)
        assert isinstance(resistance, float)
        assert resistance > 0
    
    def test_thermistor_voltage_conversion(self):
        """Test voltage conversion from ADC value."""
        from createTemperatureLookupMarlin import Thermistor
        
        thermistor = Thermistor(rp=4700, t1=25, r1=100000, t2=150, r2=1641.9, t3=250, r3=226.15)
        
        voltage = thermistor.voltage(512)
        assert isinstance(voltage, float)
        assert 0 <= voltage <= 5  # 0-5V range for 10-bit ADC
    
    def test_thermistor_resolution(self):
        """Test resolution calculation."""
        from createTemperatureLookupMarlin import Thermistor
        
        thermistor = Thermistor(rp=4700, t1=25, r1=100000, t2=150, r2=1641.9, t3=250, r3=226.15)
        
        res = thermistor.resol(512)
        assert isinstance(res, float)


class TestArgumentParsing:
    """Tests for command-line argument parsing."""
    
    def test_default_arguments(self):
        """Test default argument values."""
        result = subprocess.run(
            ['python3', 'createTemperatureLookupMarlin.py'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        assert result.returncode == 0
    
    def test_custom_pullup_resistor(self):
        """Test custom pull-up resistor argument."""
        result = subprocess.run(
            ['python3', 'createTemperatureLookupMarlin.py', '--rp=10000'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        assert result.returncode == 0
    
    def test_custom_temperature_points(self):
        """Test custom temperature points."""
        result = subprocess.run(
            ['python3', 'createTemperatureLookupMarlin.py',
             '--t1=30:100000', '--t2=150:1600', '--t3=250:200'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        assert result.returncode == 0
    
    def test_custom_number_of_temps(self):
        """Test custom number of temperature points."""
        result = subprocess.run(
            ['python3', 'createTemperatureLookupMarlin.py', '--num-temps=50'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        assert result.returncode == 0
    
    def test_combined_custom_arguments(self):
        """Test combined custom arguments."""
        result = subprocess.run(
            ['python3', 'createTemperatureLookupMarlin.py',
             '--rp=10000', '--num-temps=40',
             '--t1=20:100000', '--t2=100:2000', '--t3=200:300'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        assert result.returncode == 0


class TestOutputFormat:
    """Tests for output format of createTemperatureLookupMarlin."""
    
    def test_output_has_comment_header(self):
        """Test output contains comment header."""
        result = subprocess.run(
            ['python3', 'createTemperatureLookupMarlin.py'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        assert 'Thermistor lookup table for Marlin' in result.stdout
    
    def test_output_has_define_numtemps(self):
        """Test output contains NUMTEMPS define."""
        result = subprocess.run(
            ['python3', 'createTemperatureLookupMarlin.py'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        assert '#define NUMTEMPS' in result.stdout
    
    def test_output_has_const_short_table(self):
        """Test output contains temptable declaration."""
        result = subprocess.run(
            ['python3', 'createTemperatureLookupMarlin.py'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        assert 'const short temptable' in result.stdout
        assert 'PROGMEM' in result.stdout
    
    def test_table_entries_format(self):
        """Test table entries are in correct format."""
        result = subprocess.run(
            ['python3', 'createTemperatureLookupMarlin.py'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        # Check for entries like { (short) (value), temp }
        pattern = r'\{\s*\(short\)\s*\([\d.]+\s*\*\s*OVERSAMPLENR\)\s*,\s*[\d-]+\s*\}'
        assert re.search(pattern, result.stdout) is not None
    
    def test_output_has_steinhart_hart_coefficients(self):
        """Test output contains Steinhart-Hart coefficients."""
        result = subprocess.run(
            ['python3', 'createTemperatureLookupMarlin.py'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        assert 'Steinhart-Hart Coefficients' in result.stdout
    
    def test_output_has_theoretical_limits(self):
        """Test output contains theoretical temperature limits."""
        result = subprocess.run(
            ['python3', 'createTemperatureLookupMarlin.py'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        assert 'Theoretical limits' in result.stdout
    
    def test_numtemps_matches_entries(self):
        """Test that NUMTEMPS matches actual table entries."""
        result = subprocess.run(
            ['python3', 'createTemperatureLookupMarlin.py'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        
        # Extract NUMTEMPS value
        numtemps_match = re.search(r'#define NUMTEMPS\s+(\d+)', result.stdout)
        assert numtemps_match is not None
        numtemps = int(numtemps_match.group(1))
        
        # Count actual table entries
        entries = re.findall(r'\{\s*\(short\)\s*\([\d.]+\s*\*\s*OVERSAMPLENR\)\s*,\s*[\d-]+\s*\}', result.stdout)
        assert len(entries) == numtemps


class TestTemperatureRange:
    """Tests for temperature range calculations."""
    
    def test_temperature_range_valid(self):
        """Test that temperature range is valid."""
        result = subprocess.run(
            ['python3', 'createTemperatureLookupMarlin.py'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        
        # Extract temperatures from output
        temps = re.findall(r',\s*([\d-]+)\s*\}', result.stdout)
        assert len(temps) > 0
        
        # All temperatures should be within reasonable range (0-350C)
        for temp in temps:
            temp_val = int(temp)
            assert 0 <= temp_val <= 350, f"Temperature {temp_val} out of range"
    
    def test_temps_in_descending_order(self):
        """Test that temperatures are in descending order."""
        result = subprocess.run(
            ['python3', 'createTemperatureLookupMarlin.py'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        
        temps = re.findall(r',\s*([\d-]+)\s*\}', result.stdout)
        temps = [int(t) for t in temps]
        
        # Should be in descending order
        for i in range(len(temps) - 1):
            assert temps[i] > temps[i + 1], f"Temperatures not in descending order: {temps[i]} <= {temps[i+1]}"


class TestEdgeCases:
    """Tests for edge cases and error handling."""
    
    def test_very_high_pullup_resistor(self):
        """Test with very high pull-up resistor."""
        result = subprocess.run(
            ['python3', 'createTemperatureLookupMarlin.py', '--rp=100000'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        assert result.returncode == 0
    
    def test_very_low_pullup_resistor(self):
        """Test with very low pull-up resistor."""
        result = subprocess.run(
            ['python3', 'createTemperatureLookupMarlin.py', '--rp=100'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        assert result.returncode == 0
    
    def test_single_temperature_point(self):
        """Test with single temperature point."""
        result = subprocess.run(
            ['python3', 'createTemperatureLookupMarlin.py', '--num-temps=2'],
            capture_output=True,
            text=True,
            cwd=scripts_dir
        )
        assert result.returncode == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
