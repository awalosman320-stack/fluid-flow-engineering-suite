import math

import pytest

from calculations import (
    calculate_velocity,
    calculate_reynolds_number,
    determine_flow_regime,
    calculate_friction_factor,
    calculate_pressure_drop,
    calculate_pipe_flow,
)

from validation import (
    colebrook_friction_factor,
    compare_friction_factors,
)

from heat_transfer import (
    calculate_conduction_heat_rate,
    calculate_cooling_time,
    cooling_temperature,
)


def test_calculate_velocity():
    velocity = calculate_velocity(
        flow_rate=0.01,
        diameter=0.1,
    )

    expected = 0.01 / (math.pi * 0.1**2 / 4)

    assert velocity == pytest.approx(expected)


def test_calculate_reynolds_number():
    reynolds = calculate_reynolds_number(
        density=1000,
        velocity=1,
        diameter=0.1,
        viscosity=0.001,
    )

    assert reynolds == pytest.approx(100000)


def test_determine_flow_regime_laminar():
    assert determine_flow_regime(1000) == "Laminar"


def test_determine_flow_regime_turbulent():
    assert determine_flow_regime(10000) == "Turbulent"


def test_calculate_friction_factor_laminar():
    friction_factor = calculate_friction_factor(
        reynolds_number=1000,
        roughness=0.0001,
        diameter=0.1,
    )

    assert friction_factor == pytest.approx(0.064)


def test_calculate_pressure_drop():
    pressure_drop = calculate_pressure_drop(
        friction_factor=0.02,
        length=100,
        diameter=0.1,
        density=1000,
        velocity=2,
    )

    expected = (
        0.02
        * (100 / 0.1)
        * (1000 * 2**2 / 2)
    )

    assert pressure_drop == pytest.approx(expected)


def test_calculate_pipe_flow():
    class TestFluid:
        density = 1000
        viscosity = 0.001

    class TestPipe:
        diameter = 0.1
        length = 100
        roughness = 0.0001

    results = calculate_pipe_flow(
        TestFluid(),
        TestPipe(),
        0.01,
    )

    assert "velocity" in results
    assert "reynolds_number" in results
    assert "flow_regime" in results
    assert "friction_factor" in results
    assert "pressure_drop" in results

    assert results["velocity"] > 0
    assert results["reynolds_number"] > 0
    assert results["friction_factor"] > 0
    assert results["pressure_drop"] > 0


def test_colebrook_friction_factor():
    friction_factor = colebrook_friction_factor(
        reynolds_number=100000,
        roughness=0.0001,
        diameter=0.1,
    )

    assert friction_factor > 0
    assert friction_factor < 0.1


def test_compare_friction_factors():
    result = compare_friction_factors(
        calculated_factor=0.02,
        verified_factor=0.021,
    )

    assert result["absolute_difference"] == pytest.approx(0.001)

    assert result["percentage_difference"] == pytest.approx(
        0.001 / 0.021 * 100
    )


def test_conduction_heat_rate():
    heat_rate = calculate_conduction_heat_rate(
        thermal_conductivity=10,
        area=2,
        temperature_hot=100,
        temperature_cold=20,
        thickness=0.1,
    )

    expected = 10 * 2 * (100 - 20) / 0.1

    assert heat_rate == pytest.approx(expected)


def test_cooling_time():
    cooling_time = calculate_cooling_time(
        mass=2,
        specific_heat=1000,
        initial_temperature=100,
        ambient_temperature=20,
        target_temperature=40,
        heat_transfer_coefficient=10,
        area=1,
    )

    assert cooling_time > 0


def test_cooling_temperature():
    temperature = cooling_temperature(
        time=0,
        initial_temperature=100,
        ambient_temperature=20,
        heat_transfer_coefficient=10,
        area=1,
        mass=2,
        specific_heat=1000,
    )

    assert temperature == pytest.approx(100)
