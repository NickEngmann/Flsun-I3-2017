import pytest
import math

# === Pure logic: Thermistor lookup generator (reimplemented from createTemperatureLookupMarlin.py) ===

def thermistor_lookup(
    beta: float = 3950.0,
    r0: float = 100000.0,  # 100kΩ
    t0: float = 25.0,      # °C
    adc_max: int = 4095,
    series_res: float = 4700.0,  # 4.7kΩ pull-up
    num_points: int = 200,
    temp_min: float = 0.0,
    temp_max: float = 300.0,
) -> list:
    """
    Generate (adc_value, temperature) lookup table using Steinhart-Hart approximation.
    Simplified to 2-parameter (beta) model.
    """
    # Handle edge case: num_points=1
    if num_points <= 1:
        t_c = temp_min
        t_k = t_c + 273.15  # Kelvin

        # Invert Steinhart-Hart (simplified beta model):
        # R = R0 * exp(B * (1/T - 1/T0))
        r_th = r0 * math.exp(beta * (1.0 / t_k - 1.0 / (t0 + 273.15)))

        # Voltage divider: Vout = Vcc * R_th / (R_series + R_th)
        # ADC = Vout / Vcc * adc_max
        adc_val = (r_th / (series_res + r_th)) * adc_max
        return [(int(round(adc_val)), round(t_c, 2))]
    
    lookup = []
    for i in range(num_points):
        t_c = temp_min + (temp_max - temp_min) * i / (num_points - 1)
        t_k = t_c + 273.15  # Kelvin

        # Invert Steinhart-Hart (simplified beta model):
        # R = R0 * exp(B * (1/T - 1/T0))
        r_th = r0 * math.exp(beta * (1.0 / t_k - 1.0 / (t0 + 273.15)))

        # Voltage divider: Vout = Vcc * R_th / (R_series + R_th)
        # ADC = Vout / Vcc * adc_max
        adc_val = (r_th / (series_res + r_th)) * adc_max
        lookup.append((int(round(adc_val)), round(t_c, 2)))
    return lookup


# === Tests ===

class TestThermistorLookupGenerator:
    def test_lookup_length(self):
        table = thermistor_lookup(num_points=10)
        assert len(table) == 10

    def test_first_point_at_low_temp(self):
        table = thermistor_lookup(temp_min=0, temp_max=300, num_points=2)
        assert table[0][1] == 0.0  # °C

    def test_last_point_at_high_temp(self):
        table = thermistor_lookup(temp_min=0, temp_max=300, num_points=2)
        assert table[1][1] == 300.0  # °C

    def test_adc_value_monotonic_with_temp(self):
        table = thermistor_lookup(num_points=200)
        adcs = [t[0] for t in table]
        temps = [t[1] for t in table]
        
        # For NTC thermistor, ADC should decrease as temperature increases
        # Check that ADC values are monotonically non-increasing
        for i in range(1, len(adcs)):
            assert adcs[i] <= adcs[i-1], f"ADC not monotonic at index {i}: {adcs[i]} > {adcs[i-1]}"

    def test_known_reference_point(self):
        # At t0=25°C, R = R0, so adc_val = (R0 / (series_res + R0)) * adc_max
        table = thermistor_lookup(beta=3950, r0=100000, t0=25, series_res=4700, num_points=1, temp_min=25, temp_max=25)
        expected_adc = int(round((100000 / (4700 + 100000)) * 4095))
        assert table[0][0] == expected_adc
        assert table[0][1] == 25.0

    def test_high_beta_sharp_resistance_change(self):
        # Higher beta should give sharper resistance change around t0
        table_low_beta = thermistor_lookup(beta=2000, num_points=10, temp_min=20, temp_max=30)
        table_high_beta = thermistor_lookup(beta=5000, num_points=10, temp_min=20, temp_max=30)
        
        # At temperatures away from t0=25°C, high beta should show larger ADC changes
        # Compare ADC difference between 20°C and 30°C
        low_beta_diff = abs(table_low_beta[0][0] - table_low_beta[-1][0])
        high_beta_diff = abs(table_high_beta[0][0] - table_high_beta[-1][0])
        
        # High beta should have larger change (more sensitive)
        assert high_beta_diff > low_beta_diff