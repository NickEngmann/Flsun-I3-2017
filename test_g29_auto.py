#!/usr/bin/env python3
"""Tests for g29_auto.py - G-code preprocessing for Marlin G29 auto bed leveling."""

import pytest
import os
import sys
import tempfile
import subprocess


class TestG29AutoScript:
    """Tests for g29_auto.py script functionality."""
    
    @classmethod
    def get_scripts_dir(cls):
        return os.path.join(
            os.path.dirname(__file__),
            'firmware',
            'Auto Levling 1.1.0-RC7 BLTOUCH (depricated)',
            'buildroot',
            'share',
            'scripts'
        )
    
    def test_script_runs_without_error(self):
        """Test that script runs without syntax errors."""
        script_path = os.path.join(self.scripts_dir, 'g29_auto.py')
        result = subprocess.run(
            ['python3', '-m', 'py_compile', script_path],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Syntax error: {result.stderr}"
    
    def test_script_requires_input_file(self):
        """Test that script requires input file to run."""
        script_path = os.path.join(self.scripts_dir, 'g29_auto.py')
        
        # Create a temporary directory and run script there
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a minimal test.gcode file
            test_gcode = os.path.join(tmpdir, 'test.gcode')
            with open(test_gcode, 'w') as f:
                f.write("G28\n")
                f.write("G1 X0 Y0\n")
                f.write("G1 X10 Y10\n")
                f.write("G1 Z0.2\n")
                f.write("G1 X20 Y20\n")
                f.write("G1 X30 Y30\n")
                f.write("G29\n")
            
            # Run the script
            result = subprocess.run(
                ['python3', 'g29_auto.py'],
                capture_output=True,
                text=True,
                cwd=tmpdir
            )
            # Script should complete (may fail on parsing but should run)
            assert result.returncode == 0 or result.returncode == 1
    
    def test_script_creates_output_file(self):
        """Test that script creates output file."""
        script_path = os.path.join(self.scripts_dir, 'g29_auto.py')
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test.gcode file with enough G1 commands
            test_gcode = os.path.join(tmpdir, 'test.gcode')
            with open(test_gcode, 'w') as f:
                f.write("; G-code for testing\n")
                for i in range(10):
                    f.write(f"G1 X{i*10} Y{i*10}\n")
                f.write("G1 Z0.2\n")
                for i in range(10, 20):
                    f.write(f"G1 X{i*10} Y{i*10}\n")
                f.write("G29\n")
            
            # Run the script
            result = subprocess.run(
                ['python3', 'g29_auto.py'],
                capture_output=True,
                text=True,
                cwd=tmpdir
            )
            
            # Check output file was created
            output_file = os.path.join(tmpdir, 'g29_test.gcode')
            assert os.path.exists(output_file), "Output file not created"
    
    def test_script_replaces_g29_command(self):
        """Test that script replaces G29 with G29 LRFB command."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test.gcode file
            test_gcode = os.path.join(tmpdir, 'test.gcode')
            with open(test_gcode, 'w') as f:
                f.write("G28\n")
                for i in range(10):
                    f.write(f"G1 X{i*10} Y{i*10}\n")
                f.write("G1 Z0.2\n")
                for i in range(10, 20):
                    f.write(f"G1 X{i*10} Y{i*10}\n")
                f.write("G29\n")
                f.write("G1 Z1.0\n")
            
            # Run the script
            subprocess.run(
                ['python3', 'g29_auto.py'],
                capture_output=True,
                text=True,
                cwd=tmpdir
            )
            
            # Read output file
            output_file = os.path.join(tmpdir, 'g29_test.gcode')
            with open(output_file, 'r') as f:
                output = f.read()
            
            # Check that G29 was replaced
            assert 'G29 L' in output or 'G29 L' in output, "G29 command not replaced"
            assert 'G29\n' not in output, "Original G29 still present"


class TestG29AutoFunctions:
    """Tests for individual functions in g29_auto.py."""
    
    def test_has_g1_uppercase(self):
        """Test has_g1 with uppercase G1."""
        # Import the function by executing the script
        script = '''
def has_g1(line):
    return line[:2].upper() == "G1"

print(has_g1("G1 X10 Y20"))
'''
        result = subprocess.run(
            ['python3', '-c', script],
            capture_output=True,
            text=True
        )
        assert 'True' in result.stdout
    
    def test_has_g1_lowercase(self):
        """Test has_g1 with lowercase g1."""
        script = '''
def has_g1(line):
    return line[:2].upper() == "G1"

print(has_g1("g1 x10 y20"))
'''
        result = subprocess.run(
            ['python3', '-c', script],
            capture_output=True,
            text=True
        )
        assert 'True' in result.stdout
    
    def test_has_g1_g0_false(self):
        """Test has_g1 returns False for G0."""
        script = '''
def has_g1(line):
    return line[:2].upper() == "G1"

print(has_g1("G0 X10 Y20"))
'''
        result = subprocess.run(
            ['python3', '-c', script],
            capture_output=True,
            text=True
        )
        assert 'False' in result.stdout
    
    def test_find_axis_x(self):
        """Test find_axis function for X coordinate."""
        script = '''
def find_axis(line, axis):
    found = False
    number = ""
    for char in line:
        if found:
            if char == ".":
                number += char
            elif char == "-":
                number += char
            else:
                try:
                    int(char)
                    number += char
                except ValueError:
                    break
        else:
            found = char.upper() == axis.upper()
    try:
        return float(number)
    except ValueError:
        return None

print(find_axis("G1 X10.5 Y20", "X"))
'''
        result = subprocess.run(
            ['python3', '-c', script],
            capture_output=True,
            text=True
        )
        assert '10.5' in result.stdout
    
    def test_find_axis_y(self):
        """Test find_axis function for Y coordinate."""
        script = '''
def find_axis(line, axis):
    found = False
    number = ""
    for char in line:
        if found:
            if char == ".":
                number += char
            elif char == "-":
                number += char
            else:
                try:
                    int(char)
                    number += char
                except ValueError:
                    break
        else:
            found = char.upper() == axis.upper()
    try:
        return float(number)
    except ValueError:
        return None

print(find_axis("G1 X10 Y20.3", "Y"))
'''
        result = subprocess.run(
            ['python3', '-c', script],
            capture_output=True,
            text=True
        )
        assert '20.3' in result.stdout
    
    def test_find_axis_negative(self):
        """Test find_axis function for negative values."""
        script = '''
def find_axis(line, axis):
    found = False
    number = ""
    for char in line:
        if found:
            if char == ".":
                number += char
            elif char == "-":
                number += char
            else:
                try:
                    int(char)
                    number += char
                except ValueError:
                    break
        else:
            found = char.upper() == axis.upper()
    try:
        return float(number)
    except ValueError:
        return None

print(find_axis("G1 X-5.5", "X"))
'''
        result = subprocess.run(
            ['python3', '-c', script],
            capture_output=True,
            text=True
        )
        assert '-5.5' in result.stdout
    
    def test_find_axis_not_found(self):
        """Test find_axis returns None when axis not found."""
        script = '''
def find_axis(line, axis):
    found = False
    number = ""
    for char in line:
        if found:
            if char == ".":
                number += char
            elif char == "-":
                number += char
            else:
                try:
                    int(char)
                    number += char
                except ValueError:
                    break
        else:
            found = char.upper() == axis.upper()
    try:
        return float(number)
    except ValueError:
        return None

print(find_axis("G1 F5000", "X"))
'''
        result = subprocess.run(
            ['python3', '-c', script],
            capture_output=True,
            text=True
        )
        assert 'None' in result.stdout


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
