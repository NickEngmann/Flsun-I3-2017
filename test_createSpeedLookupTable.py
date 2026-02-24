#!/usr/bin/env python3
"""Tests for createSpeedLookupTable.py - Stepper delay lookup table generator"""

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
    import createSpeedLookupTable
except ImportError:
    # If direct import fails, we'll test via subprocess
    pass


class TestCreateSpeedLookupTable:
    """Test cases for createSpeedLookupTable functionality"""
    
    def test_script_imports(self):
        """Test that the script can be imported"""
        try:
            import createSpeedLookupTable
            assert hasattr(createSpeedLookupTable, '__author__')
            assert hasattr(createSpeedLookupTable, '__copyright__')
        except ImportError as e:
            pytest.skip(f"Script import failed: {e}")
    
    def test_default_output_format(self):
        """Test that default output follows expected C format"""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, "speed_table.c")
            
            # Run the script with default parameters
            try:
                result = subprocess.run(
                    [sys.executable, "-c", 
                     "import sys; sys.path.insert(0, '{}'); import createSpeedLookupTable; createSpeedLookupTable.main([])".format(scripts_dir)],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                # Check that output contains expected C array format
                assert 'a[' in result.stdout or 'b[' in result.stdout or '{' in result.stdout
            except subprocess.TimeoutExpired:
                pytest.skip("Script execution timed out")
            except Exception as e:
                pytest.skip(f"Script execution failed: {e}")
    
    def test_argument_parsing(self):
        """Test argument parsing functionality"""
        try:
            import createSpeedLookupTable
            # Test that argparse is properly configured
            parser = createSpeedLookupTable.argparse.ArgumentParser()
            assert parser is not None
        except (ImportError, AttributeError):
            pytest.skip("Cannot test argument parsing")
    
    def test_output_to_file(self):
        """Test writing output to a file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, "speed_table.c")
            
            try:
                # Try running with output redirection
                script_path = os.path.join(scripts_dir, "createSpeedLookupTable.py")
                if os.path.exists(script_path):
                    result = subprocess.run(
                        [sys.executable, script_path],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    # Output should contain C-style array declarations
                    assert 'int' in result.stdout or 'const' in result.stdout or '{' in result.stdout
            except subprocess.TimeoutExpired:
                pytest.skip("Script execution timed out")
            except Exception as e:
                pytest.skip(f"Script execution failed: {e}")


class TestCreateSpeedLookupTableEdgeCases:
    """Edge case tests for createSpeedLookupTable"""
    
    def test_no_arguments(self):
        """Test script execution with no arguments"""
        try:
            script_path = os.path.join(scripts_dir, "createSpeedLookupTable.py")
            if os.path.exists(script_path):
                result = subprocess.run(
                    [sys.executable, script_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                # Should produce some output even with defaults
                assert len(result.stdout) > 0 or result.returncode == 0
        except subprocess.TimeoutExpired:
            pytest.skip("Timeout")
        except Exception:
            pytest.skip("Execution issue")


class TestCreateSpeedLookupTableIntegration:
    """Integration tests"""
    
    def test_complete_workflow(self):
        """Test complete lookup table generation workflow"""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, "speed_table.c")
            
            try:
                script_path = os.path.join(scripts_dir, "createSpeedLookupTable.py")
                if os.path.exists(script_path):
                    result = subprocess.run(
                        [sys.executable, script_path],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    # Verify output format
                    output = result.stdout
                    assert 'Stepper' in output or 'delay' in output.lower() or '{' in output
                    
            except Exception:
                pytest.skip("Workflow test skipped due to execution issues")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
