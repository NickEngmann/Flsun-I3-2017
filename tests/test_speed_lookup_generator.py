import pytest
import math

# === Pure logic: Speed lookup table generator (reimplemented from createSpeedLookupTable.py) ===

def create_speed_lookup(
    max_speed: float = 200.0,
    min_speed: float = 10.0,
    steps: int = 20,
    motor_steps: int = 200,
    microsteps: int = 16,
    pulley_teeth: int = 20,
    belt_pitch: float = 2.0,
) -> list:
    """
    Generate a lookup table of (speed_mm_s, steps_per_s) pairs.
    Based on FLsun I3 speed calibration logic.
    """
    # Handle edge case: steps=1
    if steps <= 1:
        dist_per_step = (belt_pitch * pulley_teeth) / (motor_steps * microsteps)
        speed_mm_s = min_speed
        steps_per_s = speed_mm_s / dist_per_step
        return [(round(speed_mm_s, 2), round(steps_per_s, 2))]
    
    # Distance per step (mm)
    dist_per_step = (belt_pitch * pulley_teeth) / (motor_steps * microsteps)

    speeds = []
    for i in range(steps):
        # Linear spacing in mm/s
        speed_mm_s = min_speed + (max_speed - min_speed) * i / (steps - 1)
        # Steps per second = speed (mm/s) / dist_per_step
        steps_per_s = speed_mm_s / dist_per_step
        speeds.append((round(speed_mm_s, 2), round(steps_per_s, 2)))
    return speeds


# === Tests ===

class TestSpeedLookupGenerator:
    def test_basic_lookup_table_length(self):
        table = create_speed_lookup(steps=5)
        assert len(table) == 5

    def test_first_and_last_values(self):
        table = create_speed_lookup(min_speed=10, max_speed=100, steps=3)
        dist_per_step = (2.0 * 20) / (200 * 16)
        assert table[0] == (10.0, round(10.0 / dist_per_step, 2))
        assert table[2] == (100.0, round(100.0 / dist_per_step, 2))

    def test_step_spacing_is_linear(self):
        table = create_speed_lookup(steps=10)
        # Check that the unrounded values are linearly spaced
        min_speed = 10.0
        max_speed = 200.0
        steps = 10
        expected_step = (max_speed - min_speed) / (steps - 1)
        
        # Calculate expected speeds without rounding
        expected_speeds = [min_speed + expected_step * i for i in range(steps)]
        
        # Compare with actual speeds (accounting for rounding)
        for i, (speed, _) in enumerate(table):
            assert abs(speed - expected_speeds[i]) < 0.01, f"Speed at index {i} deviates too much from expected"