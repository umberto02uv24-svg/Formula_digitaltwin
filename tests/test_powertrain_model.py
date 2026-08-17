import copy

import pytest
from fdt.vehicle.config import FDT01_BASELINE_V1
from fdt.vehicle.powertrain_model import PowertrainModel
from math import pi

def create_test_powertrain_model() -> PowertrainModel:
    """Create a powertrain model with valid test parameters."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    return PowertrainModel(vehicle.powertrain)


def test_zero_speed_produces_zero_power():
    """Zero engine speed must produce zero power."""

    model = create_test_powertrain_model()

    power = model.calculate_engine_power(
        engine_speed_rpm=0.0,
        engine_torque=220.0,
    )

    assert power == pytest.approx(0.0)


def test_zero_torque_produces_zero_power():
    """Zero torque must produce zero power."""

    model = create_test_powertrain_model()

    power = model.calculate_engine_power(
        engine_speed_rpm=8000.0,
        engine_torque=0.0,
    )

    assert power == pytest.approx(0.0)


def test_engine_power_from_torque_and_speed():
    """Engine power must satisfy P = T * omega."""

    model = create_test_powertrain_model()

    power = model.calculate_engine_power(
        engine_speed_rpm=6000.0,
        engine_torque=220.0,
    )

    expected_power = (
        220.0
        * 2.0
        * 3.141592653589793
        * 6000.0
        / 60.0
    )

    assert power == pytest.approx(expected_power)


def test_operating_point_contains_engine_state():
    """Operating point must contain speed, torque, and power."""

    model = create_test_powertrain_model()

    result = model.calculate_operating_point(
        engine_speed_rpm=6000.0,
        engine_torque=220.0,
    )

    assert result.engine_speed_rpm == pytest.approx(6000.0)
    assert result.engine_torque == pytest.approx(220.0)
    assert result.engine_power == pytest.approx(
        220.0
        * 2.0
        * 3.141592653589793
        * 6000.0
        / 60.0
    )


def test_negative_engine_speed_is_rejected():
    """Negative engine speed must be rejected."""

    model = create_test_powertrain_model()

    with pytest.raises(ValueError, match="Engine speed"):
        model.calculate_engine_power(
            engine_speed_rpm=-100.0,
            engine_torque=220.0,
        )


def test_negative_engine_torque_is_rejected():
    """Negative engine torque must be rejected."""

    model = create_test_powertrain_model()

    with pytest.raises(ValueError, match="Engine torque"):
        model.calculate_engine_power(
            engine_speed_rpm=6000.0,
            engine_torque=-10.0,
        )

def test_first_gear_ratio_is_selected():
    """First gear must return the first gear ratio."""

    model = create_test_powertrain_model()

    ratio = model.calculate_gear_ratio(1)

    assert ratio == pytest.approx(3.50)

def test_last_gear_ratio_is_selected():
    """Last gear must return the last gear ratio."""

    model = create_test_powertrain_model()

    ratio = model.calculate_gear_ratio(6)

    assert ratio == pytest.approx(0.85)

def test_invalid_gear_is_rejected():
    """A gear outside the gearbox range must be rejected."""

    model = create_test_powertrain_model()

    with pytest.raises(ValueError, match="outside"):
        model.calculate_gear_ratio(7)

def test_wheel_speed_is_reduced_by_total_ratio():
    """Wheel speed must be engine speed divided by total ratio."""

    model = create_test_powertrain_model()

    wheel_speed = model.calculate_wheel_speed(
        engine_speed_rpm=6000.0,
        gear=1,
    )

    expected = 6000.0 / (3.50 * 3.90)

    assert wheel_speed == pytest.approx(expected)

def test_wheel_torque_is_multiplied_by_total_ratio():
    """Wheel torque must include gearing and drivetrain efficiency."""

    model = create_test_powertrain_model()

    wheel_torque = model.calculate_wheel_torque(
        engine_torque=220.0,
        gear=1,
    )

    expected = 220.0 * 3.50 * 3.90 * 0.95

    assert wheel_torque == pytest.approx(expected)

def test_tractive_force_is_wheel_torque_divided_by_radius():
    """Tractive force must equal wheel torque divided by wheel radius."""

    model = create_test_powertrain_model()

    wheel_torque = model.calculate_wheel_torque(
        engine_torque=220.0,
        gear=1,
    )

    tractive_force = model.calculate_tractive_force(
        engine_torque=220.0,
        gear=1,
        wheel_radius=0.25,
    )

    expected_force = wheel_torque / 0.25

    assert tractive_force == pytest.approx(expected_force)

def test_zero_wheel_radius_is_rejected():
    """Zero wheel radius must be rejected."""

    model = create_test_powertrain_model()

    with pytest.raises(ValueError, match="Wheel radius"):
        model.calculate_tractive_force(
            engine_torque=220.0,
            gear=1,
            wheel_radius=0.0,
        )

def test_zero_wheel_radius_is_rejected():
    """Zero wheel radius must be rejected."""

    model = create_test_powertrain_model()

    with pytest.raises(ValueError, match="Wheel radius"):
        model.calculate_tractive_force(
            engine_torque=220.0,
            gear=1,
            wheel_radius=0.0,
        )

def test_negative_wheel_radius_is_rejected():
    """Negative wheel radius must be rejected."""

    model = create_test_powertrain_model()

    with pytest.raises(ValueError, match="Wheel radius"):
        model.calculate_tractive_force(
            engine_torque=220.0,
            gear=1,
            wheel_radius=-0.25,
        )

def test_tractive_force_has_expected_value():
    """Tractive force must match the expected physical calculation."""

    model = create_test_powertrain_model()

    force = model.calculate_tractive_force(
        engine_torque=220.0,
        gear=1,
        wheel_radius=0.25,
    )

    expected = (
        220.0
        * 3.50
        * 3.90
        * 0.95
        / 0.25
    )

    assert force == pytest.approx(expected)

def test_engine_torque_is_limited():
    """Engine torque must not exceed its maximum value."""

    model = create_test_powertrain_model()

    result = model.limit_engine_operating_point(
        engine_speed_rpm=4000.0,
        engine_torque=300.0,
    )

    maximum_torque = (
        model.parameters.maximum_torque.value
    )

    assert result.engine_torque == pytest.approx(
        maximum_torque
    )

def test_engine_speed_is_limited():
    """Engine speed must not exceed its maximum value."""

    model = create_test_powertrain_model()

    result = model.limit_engine_operating_point(
        engine_speed_rpm=12000.0,
        engine_torque=100.0,
    )

    maximum_speed = (
        model.parameters.maximum_engine_speed.value
    )

    assert result.engine_speed_rpm == pytest.approx(
        maximum_speed
    )

def test_power_limit_reduces_torque_at_high_engine_speed():
    """Power limit must reduce torque when power would be exceeded."""

    model = create_test_powertrain_model()

    result = model.limit_engine_operating_point(
        engine_speed_rpm=10000.0,
        engine_torque=220.0,
    )

    maximum_power = (
        model.parameters.maximum_power.value
    )

    angular_speed = (
        2.0
        * pi
        * result.engine_speed_rpm
        / 60.0
    )

    expected_torque = maximum_power / angular_speed

    assert result.engine_torque == pytest.approx(
        expected_torque
    )

def test_valid_engine_operating_point_is_unchanged():
    """A valid operating point must remain unchanged."""

    model = create_test_powertrain_model()

    result = model.limit_engine_operating_point(
        engine_speed_rpm=6000.0,
        engine_torque=100.0,
    )

    assert result.engine_speed_rpm == pytest.approx(6000.0)
    assert result.engine_torque == pytest.approx(100.0)

def test_limited_operating_point_power_is_consistent():
    """Limited operating point power must equal torque times angular speed."""

    model = create_test_powertrain_model()

    result = model.limit_engine_operating_point(
        engine_speed_rpm=10000.0,
        engine_torque=220.0,
    )

    expected_power = model.calculate_engine_power(
        engine_speed_rpm=result.engine_speed_rpm,
        engine_torque=result.engine_torque,
    )

    assert result.engine_power == pytest.approx(
        expected_power
    )

def test_first_gear_produces_more_tractive_force_than_sixth():
    """Lower gears must produce greater tractive force."""

    model = create_test_powertrain_model()

    first_gear_force = model.calculate_tractive_force(
        engine_torque=200.0,
        gear=1,
        wheel_radius=0.25,
    )

    sixth_gear_force = model.calculate_tractive_force(
        engine_torque=200.0,
        gear=6,
        wheel_radius=0.25,
    )

    assert first_gear_force > sixth_gear_force

def test_tractive_force_is_proportional_to_engine_torque():
    """Tractive force must scale linearly with engine torque."""

    model = create_test_powertrain_model()

    force_100 = model.calculate_tractive_force(
        engine_torque=100.0,
        gear=3,
        wheel_radius=0.25,
    )

    force_200 = model.calculate_tractive_force(
        engine_torque=200.0,
        gear=3,
        wheel_radius=0.25,
    )

    assert force_200 == pytest.approx(
        2.0 * force_100
    )

def test_limited_engine_torque_limits_tractive_force():
    """Engine torque limits must propagate to tractive force."""

    model = create_test_powertrain_model()

    operating_point = model.limit_engine_operating_point(
        engine_speed_rpm=4000.0,
        engine_torque=300.0,
    )

    tractive_force = model.calculate_tractive_force(
        engine_torque=operating_point.engine_torque,
        gear=1,
        wheel_radius=0.25,
    )

    expected_force = (
        operating_point.engine_torque
        * model.parameters.gear_ratios.value[0]
        * model.parameters.final_drive_ratio.value
        * model.parameters.drivetrain_efficiency.value
        / 0.25
    )

    assert tractive_force == pytest.approx(
        expected_force
    )

def test_higher_gear_produces_higher_wheel_speed():
    """Higher gears must produce greater wheel speed."""

    model = create_test_powertrain_model()

    first_gear_speed = model.calculate_wheel_speed(
        engine_speed_rpm=6000.0,
        gear=1,
    )

    sixth_gear_speed = model.calculate_wheel_speed(
        engine_speed_rpm=6000.0,
        gear=6,
    )

    assert sixth_gear_speed > first_gear_speed

