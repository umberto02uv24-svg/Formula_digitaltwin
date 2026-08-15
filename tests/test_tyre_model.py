import copy

import pytest

from fdt.vehicle.config import FDT01_BASELINE_V1
from fdt.vehicle.tyre_model import TyreModel


def create_test_tyre_model() -> TyreModel:
    """Create a tyre model with valid test parameters."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.tires.longitudinal_stiffness.value = 100000.0
    vehicle.tires.lateral_stiffness.value = 80000.0
    vehicle.tires.friction_coefficient.value = 1.5

    return TyreModel(vehicle.tires)


def test_zero_slip_produces_zero_forces():
    """Zero slip must produce zero longitudinal and lateral force."""

    model = create_test_tyre_model()

    result = model.calculate_forces(
        vertical_load=1500.0,
        slip_ratio=0.0,
        slip_angle=0.0,
    )

    assert result.longitudinal_force == pytest.approx(0.0)
    assert result.lateral_force == pytest.approx(0.0)


def test_longitudinal_force_is_proportional_to_slip():
    """Longitudinal force must follow the linear stiffness."""

    model = create_test_tyre_model()

    result = model.calculate_forces(
        vertical_load=1500.0,
        slip_ratio=0.01,
        slip_angle=0.0,
    )

    assert result.longitudinal_force == pytest.approx(1000.0)
    assert result.lateral_force == pytest.approx(0.0)


def test_lateral_force_is_proportional_to_slip_angle():
    """Lateral force must follow the linear cornering stiffness."""

    model = create_test_tyre_model()

    result = model.calculate_forces(
        vertical_load=1500.0,
        slip_ratio=0.0,
        slip_angle=0.01,
    )

    assert result.lateral_force == pytest.approx(-800.0)
    assert result.longitudinal_force == pytest.approx(0.0)


def test_friction_circle_limits_combined_force():
    """Combined tyre force must not exceed the friction limit."""

    model = create_test_tyre_model()

    result = model.calculate_forces(
        vertical_load=1000.0,
        slip_ratio=0.05,
        slip_angle=0.05,
    )

    force_magnitude = (
        result.longitudinal_force**2
        + result.lateral_force**2
    ) ** 0.5

    maximum_force = 1.5 * 1000.0

    assert force_magnitude == pytest.approx(maximum_force)


def test_negative_vertical_load_is_rejected():
    """A non-positive vertical load must be rejected."""

    model = create_test_tyre_model()

    with pytest.raises(ValueError, match="Vertical load"):
        model.calculate_forces(
            vertical_load=-100.0,
            slip_ratio=0.0,
            slip_angle=0.0,
        )