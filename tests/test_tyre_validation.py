import copy

import pytest

from fdt.vehicle.config import FDT01_BASELINE_V1
from fdt.vehicle.tyre_model import TyreModel


def create_validation_tyre_model() -> TyreModel:
    """Create a tyre model with controlled validation parameters."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.tires.longitudinal_stiffness.value = 100000.0
    vehicle.tires.lateral_stiffness.value = 80000.0
    vehicle.tires.friction_coefficient.value = 1.5
    vehicle.tires.reference_vertical_load.value = 1000.0
    vehicle.tires.load_sensitivity_exponent.value = 0.10

    return TyreModel(vehicle.tires)


def calculate_force_magnitude(
    longitudinal_force: float,
    lateral_force: float,
) -> float:
    """Calculate the magnitude of the combined tyre force."""

    return (
        longitudinal_force**2
        + lateral_force**2
    ) ** 0.5


def test_longitudinal_force_is_antisymmetric():
    """Longitudinal force must change sign with slip ratio."""

    model = create_validation_tyre_model()

    positive = model.calculate_forces(
        vertical_load=1000.0,
        slip_ratio=0.01,
        slip_angle=0.0,
    )

    negative = model.calculate_forces(
        vertical_load=1000.0,
        slip_ratio=-0.01,
        slip_angle=0.0,
    )

    assert positive.longitudinal_force == pytest.approx(
        -negative.longitudinal_force
    )


def test_lateral_force_is_antisymmetric():
    """Lateral force must change sign with slip angle."""

    model = create_validation_tyre_model()

    positive = model.calculate_forces(
        vertical_load=1000.0,
        slip_ratio=0.0,
        slip_angle=0.01,
    )

    negative = model.calculate_forces(
        vertical_load=1000.0,
        slip_ratio=0.0,
        slip_angle=-0.01,
    )

    assert positive.lateral_force == pytest.approx(
        -negative.lateral_force
    )


def test_longitudinal_force_increases_with_slip():
    """Longitudinal force magnitude must increase with slip."""

    model = create_validation_tyre_model()

    low_slip = model.calculate_forces(
        vertical_load=1000.0,
        slip_ratio=0.005,
        slip_angle=0.0,
    )

    high_slip = model.calculate_forces(
        vertical_load=1000.0,
        slip_ratio=0.01,
        slip_angle=0.0,
    )

    assert abs(high_slip.longitudinal_force) > (
        abs(low_slip.longitudinal_force)
    )


def test_lateral_force_increases_with_slip_angle():
    """Lateral force magnitude must increase with slip angle."""

    model = create_validation_tyre_model()

    low_angle = model.calculate_forces(
        vertical_load=1000.0,
        slip_ratio=0.0,
        slip_angle=0.005,
    )

    high_angle = model.calculate_forces(
        vertical_load=1000.0,
        slip_ratio=0.0,
        slip_angle=0.01,
    )

    assert abs(high_angle.lateral_force) > (
        abs(low_angle.lateral_force)
    )


def test_available_force_increases_with_vertical_load():
    """Available tyre force must increase with vertical load."""

    model = create_validation_tyre_model()

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

    assert abs(high_load.longitudinal_force) > (
        abs(low_load.longitudinal_force)
    )


def test_effective_friction_decreases_with_vertical_load():
    """Effective friction coefficient must decrease with load."""

    model = create_validation_tyre_model()

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

    low_mu = (
        abs(low_load.longitudinal_force)
        / 1000.0
    )

    high_mu = (
        abs(high_load.longitudinal_force)
        / 2000.0
    )

    assert high_mu < low_mu


def test_friction_limit_is_respected_at_multiple_loads():
    """Tyre forces must remain inside the friction limit."""

    model = create_validation_tyre_model()

    test_loads = [
        500.0,
        1000.0,
        1500.0,
        2000.0,
        3000.0,
    ]

    for vertical_load in test_loads:
        result = model.calculate_forces(
            vertical_load=vertical_load,
            slip_ratio=0.20,
            slip_angle=0.20,
        )

        force_magnitude = calculate_force_magnitude(
            result.longitudinal_force,
            result.lateral_force,
        )

        effective_mu = (
            1.5
            * (
                vertical_load / 1000.0
            ) ** -0.10
        )

        maximum_force = (
            effective_mu * vertical_load
        )

        assert force_magnitude <= maximum_force + 1e-6


def test_combined_slip_reduces_longitudinal_force():
    """Lateral slip must reduce longitudinal force."""

    model = create_validation_tyre_model()

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


def test_combined_slip_reduces_lateral_force():
    """Longitudinal slip must reduce lateral force."""

    model = create_validation_tyre_model()

    pure_lateral = model.calculate_forces(
        vertical_load=1000.0,
        slip_ratio=0.0,
        slip_angle=0.05,
    )

    combined = model.calculate_forces(
        vertical_load=1000.0,
        slip_ratio=0.20,
        slip_angle=0.05,
    )

    assert abs(combined.lateral_force) < (
        abs(pure_lateral.lateral_force)
    )


def test_zero_slip_produces_zero_force():
    """Zero longitudinal and lateral slip must produce zero force."""

    model = create_validation_tyre_model()

    result = model.calculate_forces(
        vertical_load=1000.0,
        slip_ratio=0.0,
        slip_angle=0.0,
    )

    assert result.longitudinal_force == pytest.approx(0.0)
    assert result.lateral_force == pytest.approx(0.0)