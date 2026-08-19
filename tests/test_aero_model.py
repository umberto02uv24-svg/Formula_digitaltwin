import copy

import pytest

from fdt.vehicle.aero_model import AeroModel
from fdt.vehicle.config import FDT01_BASELINE_V1


def create_test_aero_model() -> AeroModel:
    """Create an aerodynamic model with known test parameters."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.aerodynamics.air_density.value = 1.225
    vehicle.aerodynamics.frontal_area.value = 1.2
    vehicle.aerodynamics.drag_coefficient.value = 0.9
    vehicle.aerodynamics.lift_coefficient.value = 1.5
    vehicle.aerodynamics.front_aero_balance.value = 0.45

    return AeroModel(vehicle.aerodynamics)


def test_zero_velocity_produces_zero_aero_forces():
    """Zero velocity must produce zero aerodynamic forces."""

    model = create_test_aero_model()

    result = model.calculate_forces(velocity=0.0)

    assert result.drag_force == pytest.approx(0.0)
    assert result.downforce == pytest.approx(0.0)


def test_drag_force_is_proportional_to_velocity_squared():
    """Drag must scale with velocity squared."""

    model = create_test_aero_model()

    low = model.calculate_forces(velocity=10.0)
    high = model.calculate_forces(velocity=20.0)

    assert high.drag_force == pytest.approx(
        4.0 * low.drag_force
    )


def test_downforce_is_proportional_to_velocity_squared():
    """Downforce must scale with velocity squared."""

    model = create_test_aero_model()

    low = model.calculate_forces(velocity=10.0)
    high = model.calculate_forces(velocity=20.0)

    assert high.downforce == pytest.approx(
        4.0 * low.downforce
    )


def test_drag_force_has_expected_value():
    """Drag must match the aerodynamic equation."""

    model = create_test_aero_model()

    result = model.calculate_forces(velocity=50.0)

    expected = (
        0.5
        * 1.225
        * 50.0**2
        * 0.9
        * 1.2
    )

    assert result.drag_force == pytest.approx(expected)


def test_downforce_has_expected_value():
    """Downforce must match the aerodynamic equation."""

    model = create_test_aero_model()

    result = model.calculate_forces(velocity=50.0)

    expected = (
        0.5
        * 1.225
        * 50.0**2
        * 1.5
        * 1.2
    )

    assert result.downforce == pytest.approx(expected)


def test_downforce_is_greater_than_drag_with_higher_cl():
    """Higher lift coefficient must produce greater downforce."""

    model = create_test_aero_model()

    result = model.calculate_forces(velocity=50.0)

    assert result.downforce > result.drag_force


def test_negative_velocity_is_rejected():
    """Negative velocity must be rejected."""

    model = create_test_aero_model()

    with pytest.raises(
        ValueError,
        match="Velocity cannot be negative",
    ):
        model.calculate_forces(velocity=-1.0)


def test_missing_air_density_is_rejected():
    """Missing air density must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)
    vehicle.aerodynamics.air_density.value = None

    model = AeroModel(vehicle.aerodynamics)

    with pytest.raises(
        ValueError,
        match="Air density is required",
    ):
        model.calculate_forces(velocity=50.0)


def test_missing_frontal_area_is_rejected():
    """Missing frontal area must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)
    vehicle.aerodynamics.frontal_area.value = None

    model = AeroModel(vehicle.aerodynamics)

    with pytest.raises(
        ValueError,
        match="Frontal area is required",
    ):
        model.calculate_forces(velocity=50.0)


def test_missing_drag_coefficient_is_rejected():
    """Missing drag coefficient must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)
    vehicle.aerodynamics.drag_coefficient.value = None

    model = AeroModel(vehicle.aerodynamics)

    with pytest.raises(
        ValueError,
        match="Drag coefficient is required",
    ):
        model.calculate_forces(velocity=50.0)


def test_missing_lift_coefficient_is_rejected():
    """Missing lift coefficient must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)
    vehicle.aerodynamics.lift_coefficient.value = None

    model = AeroModel(vehicle.aerodynamics)

    with pytest.raises(
        ValueError,
        match="Lift coefficient is required",
    ):
        model.calculate_forces(velocity=50.0)


def test_negative_air_density_is_rejected():
    """Negative air density must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)
    vehicle.aerodynamics.air_density.value = -1.0

    model = AeroModel(vehicle.aerodynamics)

    with pytest.raises(
        ValueError,
        match="Air density must be positive",
    ):
        model.calculate_forces(velocity=50.0)


def test_negative_frontal_area_is_rejected():
    """Negative frontal area must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)
    vehicle.aerodynamics.frontal_area.value = -1.0

    model = AeroModel(vehicle.aerodynamics)

    with pytest.raises(
        ValueError,
        match="Frontal area must be positive",
    ):
        model.calculate_forces(velocity=50.0)


def test_negative_drag_coefficient_is_rejected():
    """Negative drag coefficient must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)
    vehicle.aerodynamics.drag_coefficient.value = -1.0

    model = AeroModel(vehicle.aerodynamics)

    with pytest.raises(
        ValueError,
        match="Drag coefficient cannot be negative",
    ):
        model.calculate_forces(velocity=50.0)


def test_negative_lift_coefficient_is_rejected():
    """Negative lift coefficient must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)
    vehicle.aerodynamics.lift_coefficient.value = -1.0

    model = AeroModel(vehicle.aerodynamics)

    with pytest.raises(
        ValueError,
        match="Lift coefficient cannot be negative",
    ):
        model.calculate_forces(velocity=50.0)

def test_aero_balance_sums_to_total_downforce():
    """Front and rear downforce must sum to total downforce."""

    model = create_test_aero_model()

    result = model.calculate_forces(velocity=50.0)

    assert (
        result.front_downforce
        + result.rear_downforce
    ) == pytest.approx(result.downforce)

def test_front_downforce_follows_aero_balance():
    """Front downforce must follow the configured aero balance."""

    model = create_test_aero_model()

    result = model.calculate_forces(velocity=50.0)

    assert result.front_downforce == pytest.approx(
        result.downforce * 0.45
    )

def test_rear_downforce_follows_aero_balance():
    """Rear downforce must follow the configured aero balance."""

    model = create_test_aero_model()

    result = model.calculate_forces(velocity=50.0)

    assert result.rear_downforce == pytest.approx(
        result.downforce * 0.55
    )

def test_missing_front_aero_balance_is_rejected():
    """Missing front aero balance must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)
    vehicle.aerodynamics.front_aero_balance.value = None

    model = AeroModel(vehicle.aerodynamics)

    with pytest.raises(
        ValueError,
        match="Front aero balance is required",
    ):
        model.calculate_forces(velocity=50.0)

def test_front_aero_balance_above_one_is_rejected():
    """Front aero balance above one must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)
    vehicle.aerodynamics.front_aero_balance.value = 1.01

    model = AeroModel(vehicle.aerodynamics)

    with pytest.raises(
        ValueError,
        match="Front aero balance must be between 0 and 1",
    ):
        model.calculate_forces(velocity=50.0)

def test_front_aero_balance_below_zero_is_rejected():
    """Negative front aero balance must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)
    vehicle.aerodynamics.front_aero_balance.value = -0.01

    model = AeroModel(vehicle.aerodynamics)

    with pytest.raises(
        ValueError,
        match="Front aero balance must be between 0 and 1",
    ):
        model.calculate_forces(velocity=50.0)

def test_zero_front_aero_balance_puts_all_downforce_rear():
    """Zero front aero balance must put all downforce at the rear."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)
    vehicle.aerodynamics.front_aero_balance.value = 0.0

    model = AeroModel(vehicle.aerodynamics)

    result = model.calculate_forces(velocity=50.0)

    assert result.front_downforce == pytest.approx(0.0)
    assert result.rear_downforce == pytest.approx(result.downforce)

def test_full_front_aero_balance_puts_all_downforce_front():
    """Full front aero balance must put all downforce at the front."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)
    vehicle.aerodynamics.front_aero_balance.value = 1.0

    model = AeroModel(vehicle.aerodynamics)

    result = model.calculate_forces(velocity=50.0)

    assert result.front_downforce == pytest.approx(result.downforce)
    assert result.rear_downforce == pytest.approx(0.0)

def test_aero_load_is_conserved():
    """Front and rear aero loads must equal total downforce."""

    model = create_test_aero_model()

    result = model.calculate_forces(velocity=75.0)

    assert (
        result.front_downforce
        + result.rear_downforce
    ) == pytest.approx(result.downforce)
