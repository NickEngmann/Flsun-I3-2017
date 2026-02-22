import re
import pytest

# === Pure logic: G-code parser (reimplemented from typical FLsun scripts) ===

def parse_gcode_line(line: str):
    """
    Parse a single G-code line into command, params dict, and raw line.
    Returns: (command, params_dict, raw_line)
    Example: "G1 X10.5 Y20.0 E0.3" → ("G1", {"X": 10.5, "Y": 20.0, "E": 0.3}, "G1 X10.5 Y20.0 E0.3")
    """
    original_line = line
    line = line.strip()
    if not line or line.startswith(';') or line.startswith('#'):
        return None, {}, original_line  # comment or empty

    # Extract command (e.g., G1, M104, T0)
    cmd_match = re.match(r'^([A-Za-z]\d+)', line)
    if not cmd_match:
        return None, {}, original_line  # malformed

    command = cmd_match.group(1).upper()
    rest = line[cmd_match.end():].strip()

    # Parse parameters: e.g., "X10.5 Y20" → {"X": 10.5, "Y": 20}
    params = {}
    param_pattern = re.compile(r'([A-Za-z])(-?\d*\.?\d+)')
    for match in param_pattern.finditer(rest):
        key = match.group(1).upper()
        try:
            val = float(match.group(2))
        except ValueError:
            val = match.group(2)  # fallback (e.g., 'S' with string)
        params[key] = val

    return command, params, original_line


# === Tests ===

class TestGcodeParser:
    def test_parse_basic_g1(self):
        cmd, params, raw = parse_gcode_line("G1 X10.5 Y20.0 E0.3")
        assert cmd == "G1"
        assert params == {"X": 10.5, "Y": 20.0, "E": 0.3}
        assert raw == "G1 X10.5 Y20.0 E0.3"

    def test_parse_m104_with_s_value(self):
        cmd, params, raw = parse_gcode_line("M104 S200")
        assert cmd == "M104"
        assert params == {"S": 200.0}

    def test_parse_comment_line(self):
        cmd, params, raw = parse_gcode_line("; This is a comment")
        assert cmd is None
        assert params == {}
        assert raw == "; This is a comment"

    def test_parse_empty_line(self):
        cmd, params, raw = parse_gcode_line("   ")
        assert cmd is None
        assert params == {}
        assert raw == "   "