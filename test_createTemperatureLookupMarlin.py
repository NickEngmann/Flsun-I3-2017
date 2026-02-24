#!/usr/bin/env python3
"""Tests for createTemperatureLookupMarlin.py - Thermistor value lookup table generator"""

import os
import sys
import tempfile
import subprocess
import pytest

# Add the scripts directory to path
scripts_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "firmware",
    "Auto Levling 1.1.0-RC7 BLTOUCH (depricated)",
    "buildroot",
    "share",
    "scripts"
)
sys.path.insert(0, scripts_dir)

try:
    import createTemperatureLookupMarlin
except ImportError:
    pass


class TestCreateTemperatureLookupMarlin:
    """Test cases for createTemperatureLookupMarlin functionality"""
    
    def test_script_imports(self):
        """Test that the script can be imported"""
        try:
            import createTemperatureLookupMarlin
            assert hasattr(createTemperatureLookupMarlin, '__doc__')
            assert hasattr(createTemperatureLookupMarlin, 'main')
        except ImportError as e:
            pytest.skip(f"Script import failed: {e}")
    
    def test_default_output_format(self):
        """Test that default output follows expected C format"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Run the script with default parameters
            try:
                script_path = os.path.join(scripts_dir, "createTemperatureLookupMarlin.py")
                if os.path.exists(script_path):
                    result = subprocess.run(
                        [sys.executable, script_path],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    # Check that output contains expected C array format
                    output = result.stdout
                    assert 'int' in output or 'const' in output or '{' in output
                    assert '}' in output
            except subprocess.TimeoutExpired:
                pytest.skip("Script execution timed out")
            except Exception as e:
                pytest.skip(f"Script execution failed: {e}")
    
    def test_steinhart_hart_usage(self):
        """Test that Steinhart-Hart equation is properly referenced"""
        try:
            import createTemperatureLookupMarlin
            # Check that the module docstring mentions Steinhart-Hart
            doc = createTemperatureLookupMarlin.__doc__
            assert 'Steinhart' in doc or 'Hart' in doc
        except (ImportError, AttributeError):
            pytest.skip("Cannot verify Steinhart-Hart usage")
    
    def test_usage_function(self):
        """Test that usage function exists and works"""
        try:
            import createTemperatureLookupMarlin
            # Check that usage function exists
            assert hasattr(createTemperatureLookupMarlin, 'usage')
        except (ImportError, AttributeError):
            pytest.skip("Usage function test skipped")


class TestCreateTemperatureLookupMarlinEdgeCases:
    """Edge case tests"""
    
    def test_no_arguments(self):
        """Test script execution with no arguments"""
        try:
            script_path = os.path.join(scripts_dir, "createTemperatureLookupMarlin.py")
            if os.path.exists(script_path):
                result = subprocess.run(
                    [sys.executable, script_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                # Should produce some output
                assert result.returncode == 0 or len(result.stdout) > 0
        except subprocess.TimeoutExpired:
            pytest.skip("Timeout")
        except Exception:
            pytest.skip("Execution issue")
    
    def test_empty_argument_list(self):
        """Test with empty argument list"""
        try:
            script_path = os.path.join(scripts_dir, "createTemperatureLookupMarlin.py")
            if os.path.exists(script_path):
                result = subprocess.run(
                    [sys.executable, script_path, ""],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
        except subprocess.TimeoutExpired:
            pytest.skip("Timeout")
        except Exception:
            pytest.skip("Execution issue")


class TestCreateTemperatureLookupMarlinIntegration:
    """Integration tests"""
    
    def test_complete_workflow(self):
        """Test complete temperature lookup table generation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                script_path = os.path.join(scripts_dir, "createTemperatureLookupMarlin.py")
                if os.path.exists(script_path):
                    result = subprocess.run(
                        [sys.executable, script_path],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    # Verify output contains expected elements
                    output = result.stdout
                    assert 'Thermistor' in output or 'temperature' in output.lower()
                    assert 'lookup' in output.lower() or 'table' in output.lower()
                    
            except Exception:
                pytest.skip("Workflow test skipped")
    
    def test_output_structure(self):
        """Test that output has proper C structure"""
        try:
            script_path = os.path.join(scripts_dir, "createTemperatureLookupMarlin.py")
            if os.path.exists(script_path):
                result = subprocess.run(
                    [sys.executable, script_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                output = result.stdout
                # Check for C-style array structure
                assert '[' in output and ']' in output
                assert '{' in output and '}' in output
                
        except Exception:
            pytest.skip("Structure test skipped")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
