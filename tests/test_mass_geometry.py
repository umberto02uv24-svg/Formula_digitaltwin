import pytest
import copy

from fdt.vehicle.config import FDT01_BASELINE_V1
from fdt.vehicle.mass_geometry import (
    GRAVITY,
    MassGeometryModel,
)


def test_static_loads_sum_to_vehicle_weight():
    """Front and rear axle loads must equal total vehicle weight."""

    model = MassGeometryModel(FDT01_BASELINE_V1)

    result = model.calculate_static_loads()

    expected_weight = 530.0 * GRAVITY

    assert result.total_load == pytest.approx(expected_weight)
    assert (
        result.front_axle_load + result.rear_axle_load
        == pytest.approx(expected_weight)
    )


def test_front_static_load_distribution():
    """Front axle load must match the FDT01 CG position."""

    model = MassGeometryModel(FDT01_BASELINE_V1)

    result = model.calculate_static_loads()

    assert result.front_load_distribution == pytest.approx(0.45)


def test_rear_static_load_distribution():
    """Rear axle load must match the FDT01 CG position."""

    model = MassGeometryModel(FDT01_BASELINE_V1)

    result = model.calculate_static_loads()

    assert result.rear_load_distribution == pytest.approx(0.55)


def test_front_and_rear_load_are_positive():
    """Both axles must carry a positive static load."""

    model = MassGeometryModel(FDT01_BASELINE_V1)

    result = model.calculate_static_loads()

    assert result.front_axle_load > 0
    assert result.rear_axle_load > 0

def test_negative_mass_is_rejected():
    """A negative vehicle mass must not be accepted."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)
    vehicle.mass.mass.value = -530.0

    model = MassGeometryModel(vehicle)

    with pytest.raises(ValueError, match="mass must be positive"):
        model.calculate_static_loads()