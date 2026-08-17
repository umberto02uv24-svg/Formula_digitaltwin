import copy

import pytest

from fdt.vehicle.axle_model import AxleTyreModel
from fdt.vehicle.config import FDT01_BASELINE_V1
from fdt.vehicle.tyre_model import TyreModel


def create_test_axle_model() -> AxleTyreModel:
    """Create an axle model with valid test tyre parameters."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.tires.longitudinal_stiffness.value = 100000.0
    vehicle.tires.lateral_stiffness.value = 80000.0
    vehicle.tires.friction_coefficient.value = 1.5
    vehicle.tires.reference_vertical_load.value = 1000.0
    vehicle.tires.load_sensitivity_exponent.value = 0.10

    tyre_model = TyreModel(vehicle.tires)

    return AxleTyreModel(tyre_model)

def test_axle_load_is_distributed_equally():
    """Axle load must be distributed equally between both tyres."""

    model = create_test_axle_model()

    result = model.calculate_forces(
        axle_vertical_load=2000.0,
        left_slip_ratio=0.01,
        left_slip_angle=0.0,
        right_slip_ratio=0.01,
        right_slip_angle=0.0,
    )

    assert result.left_longitudinal_force == pytest.approx(
        result.right_longitudinal_force
    )

def test_zero_slip_produces_zero_axle_forces():
    """Zero slip must produce zero total axle forces."""

    model = create_test_axle_model()

    result = model.calculate_forces(
        axle_vertical_load=2000.0,
        left_slip_ratio=0.0,
        left_slip_angle=0.0,
        right_slip_ratio=0.0,
        right_slip_angle=0.0,
    )

    assert result.total_longitudinal_force == pytest.approx(0.0)
    assert result.total_lateral_force == pytest.approx(0.0)

def test_total_axle_force_is_sum_of_left_and_right():
    """Total axle force must equal the sum of both tyre forces."""

    model = create_test_axle_model()

    result = model.calculate_forces(
        axle_vertical_load=2000.0,
        left_slip_ratio=0.01,
        left_slip_angle=0.02,
        right_slip_ratio=0.015,
        right_slip_angle=0.01,
    )

    assert result.total_longitudinal_force == pytest.approx(
        result.left_longitudinal_force
        + result.right_longitudinal_force
    )

    assert result.total_lateral_force == pytest.approx(
        result.left_lateral_force
        + result.right_lateral_force
    )

def test_different_slips_produce_different_forces():
    """Different tyre slips must produce different tyre forces."""

    model = create_test_axle_model()

    result = model.calculate_forces(
        axle_vertical_load=2000.0,
        left_slip_ratio=0.01,
        left_slip_angle=0.0,
        right_slip_ratio=0.02,
        right_slip_angle=0.0,
    )

    assert (
        result.left_longitudinal_force
        != pytest.approx(result.right_longitudinal_force)
    )

def test_negative_axle_load_is_rejected():
    """A non-positive axle load must be rejected."""

    model = create_test_axle_model()

    with pytest.raises(ValueError, match="Axle vertical load"):
        model.calculate_forces(
            axle_vertical_load=-100.0,
            left_slip_ratio=0.0,
            left_slip_angle=0.0,
            right_slip_ratio=0.0,
            right_slip_angle=0.0,
        )

