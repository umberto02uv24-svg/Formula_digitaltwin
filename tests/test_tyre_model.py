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
    vehicle.tires.reference_vertical_load.value = 1000.0
    vehicle.tires.load_sensitivity_exponent.value = 0.10

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

def test_load_sensitivity_is_one_at_reference_load():
    """Reference load must reproduce the reference friction coefficient."""

    model = create_test_tyre_model()

    result = model.calculate_forces(
        vertical_load=1000.0,
        slip_ratio=0.05,
        slip_angle=0.0,
    )

    assert result.longitudinal_force == pytest.approx(1500.0)


def test_load_sensitivity_reduces_effective_mu_at_higher_load():
    """Effective friction coefficient must decrease at higher load."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.tires.longitudinal_stiffness.value = 100000.0
    vehicle.tires.lateral_stiffness.value = 80000.0
    vehicle.tires.friction_coefficient.value = 1.5
    vehicle.tires.reference_vertical_load.value = 1000.0
    vehicle.tires.load_sensitivity_exponent.value = 0.10

    model = TyreModel(vehicle.tires)

    low_load = model.calculate_forces(
        vertical_load=1000.0,
        slip_ratio=0.05,
        slip_angle=0.0,
    )

    high_load = model.calculate_forces(
        vertical_load=2000.0,
        slip_ratio=0.05,
        slip_angle=0.0,
    )

    low_effective_mu = (
        low_load.longitudinal_force / 1000.0
    )

    high_effective_mu = (
        high_load.longitudinal_force / 2000.0
    )

    assert high_effective_mu < low_effective_mu


def test_load_sensitivity_increases_total_available_force():
    """Higher vertical load must still increase total available force."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.tires.longitudinal_stiffness.value = 100000.0
    vehicle.tires.lateral_stiffness.value = 80000.0
    vehicle.tires.friction_coefficient.value = 1.5
    vehicle.tires.reference_vertical_load.value = 1000.0
    vehicle.tires.load_sensitivity_exponent.value = 0.10

    model = TyreModel(vehicle.tires)

    low_load = model.calculate_forces(
        vertical_load=1000.0,
        slip_ratio=0.05,
        slip_angle=0.0,
    )

    high_load = model.calculate_forces(
        vertical_load=2000.0,
        slip_ratio=0.05,
        slip_angle=0.0,
    )

    assert high_load.longitudinal_force > low_load.longitudinal_force

def test_load_sensitivity_matches_expected_force():
    """Load sensitivity must follow the defined power-law relationship."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.tires.longitudinal_stiffness.value = 100000.0
    vehicle.tires.lateral_stiffness.value = 80000.0
    vehicle.tires.friction_coefficient.value = 1.5
    vehicle.tires.reference_vertical_load.value = 1000.0
    vehicle.tires.load_sensitivity_exponent.value = 0.10

    model = TyreModel(vehicle.tires)

    result = model.calculate_forces(
        vertical_load=2000.0,
        slip_ratio=0.05,
        slip_angle=0.0,
    )

    expected_mu = 1.5 * (2.0 ** -0.10)
    expected_force = expected_mu * 2000.0

    assert result.longitudinal_force == pytest.approx(
        expected_force
    )

def test_pure_longitudinal_slip_is_unchanged_by_combined_slip_model():
    """Pure longitudinal slip must retain the linear tyre response."""

    model = create_test_tyre_model()

    result = model.calculate_forces(
        vertical_load=1000.0,
        slip_ratio=0.01,
        slip_angle=0.0,
    )

    assert result.longitudinal_force == pytest.approx(1000.0)
    assert result.lateral_force == pytest.approx(0.0)

def test_pure_lateral_slip_is_unchanged_by_combined_slip_model():
    """Pure lateral slip must retain the linear tyre response."""

    model = create_test_tyre_model()

    result = model.calculate_forces(
        vertical_load=1000.0,
        slip_ratio=0.0,
        slip_angle=0.01,
    )

    assert result.lateral_force == pytest.approx(-800.0)
    assert result.longitudinal_force == pytest.approx(0.0)

def test_combined_slip_reduces_longitudinal_force():
    """Lateral slip must reduce longitudinal tyre force."""

    model = create_test_tyre_model()

    pure_longitudinal = model.calculate_forces(
        vertical_load=1000.0,
        slip_ratio=0.05,
        slip_angle=0.0,
    )

    combined = model.calculate_forces(
        vertical_load=1000.0,
        slip_ratio=0.05,
        slip_angle=0.20,
    )

    assert abs(combined.longitudinal_force) < (
        abs(pure_longitudinal.longitudinal_force)
    )

def test_combined_slip_respects_friction_limit():
    """Combined slip must remain inside the available friction limit."""

    model = create_test_tyre_model()

    result = model.calculate_forces(
        vertical_load=1000.0,
        slip_ratio=0.20,
        slip_angle=0.20,
    )

    force_magnitude = (
        result.longitudinal_force**2
        + result.lateral_force**2
    ) ** 0.5

    maximum_force = 1.5 * 1000.0

    assert force_magnitude <= maximum_force + 1e-9