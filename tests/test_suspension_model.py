import copy

import pytest

from fdt.vehicle.config import FDT01_BASELINE_V1
from fdt.vehicle.suspension_model import SuspensionModel
from fdt.vehicle.damper_model import DamperModel

def create_test_suspension_model() -> SuspensionModel:
    """Create a suspension model with valid test parameters."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.suspension.front_spring_stiffness.value = 50000.0
    vehicle.suspension.rear_spring_stiffness.value = 60000.0

    vehicle.suspension.front_motion_ratio.value = 0.80
    vehicle.suspension.rear_motion_ratio.value = 0.75

    return SuspensionModel(vehicle.suspension)


# ---------------------------------------------------------------------------
# M3.5.1 — Spring model
# ---------------------------------------------------------------------------


def test_front_spring_force_is_proportional_to_displacement():
    """Front spring force must follow F = kx."""

    model = create_test_suspension_model()

    result = model.calculate_spring_force(
        front_displacement=0.010,
        rear_displacement=0.0,
    )

    assert result.front_force == pytest.approx(500.0)
    assert result.rear_force == pytest.approx(0.0)


def test_rear_spring_force_is_proportional_to_displacement():
    """Rear spring force must follow F = kx."""

    model = create_test_suspension_model()

    result = model.calculate_spring_force(
        front_displacement=0.0,
        rear_displacement=0.010,
    )

    assert result.front_force == pytest.approx(0.0)
    assert result.rear_force == pytest.approx(600.0)


def test_zero_displacement_produces_zero_spring_force():
    """Zero displacement must produce zero spring force."""

    model = create_test_suspension_model()

    result = model.calculate_spring_force(
        front_displacement=0.0,
        rear_displacement=0.0,
    )

    assert result.front_force == pytest.approx(0.0)
    assert result.rear_force == pytest.approx(0.0)


def test_spring_force_scales_linearly_with_displacement():
    """Spring force must scale linearly with displacement."""

    model = create_test_suspension_model()

    low = model.calculate_spring_force(
        front_displacement=0.010,
        rear_displacement=0.010,
    )

    high = model.calculate_spring_force(
        front_displacement=0.020,
        rear_displacement=0.020,
    )

    assert high.front_force == pytest.approx(
        2.0 * low.front_force
    )

    assert high.rear_force == pytest.approx(
        2.0 * low.rear_force
    )


def test_negative_displacement_is_allowed():
    """Negative displacement represents spring extension."""

    model = create_test_suspension_model()

    result = model.calculate_spring_force(
        front_displacement=-0.010,
        rear_displacement=-0.010,
    )

    assert result.front_force == pytest.approx(-500.0)
    assert result.rear_force == pytest.approx(-600.0)


def test_missing_front_spring_stiffness_is_rejected():
    """Missing front spring stiffness must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.suspension.front_spring_stiffness.value = None
    vehicle.suspension.rear_spring_stiffness.value = 60000.0

    model = SuspensionModel(vehicle.suspension)

    with pytest.raises(
        ValueError,
        match="Front spring stiffness is required",
    ):
        model.calculate_spring_force(
            front_displacement=0.010,
            rear_displacement=0.010,
        )


def test_missing_rear_spring_stiffness_is_rejected():
    """Missing rear spring stiffness must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.suspension.front_spring_stiffness.value = 50000.0
    vehicle.suspension.rear_spring_stiffness.value = None

    model = SuspensionModel(vehicle.suspension)

    with pytest.raises(
        ValueError,
        match="Rear spring stiffness is required",
    ):
        model.calculate_spring_force(
            front_displacement=0.010,
            rear_displacement=0.010,
        )


def test_negative_front_spring_stiffness_is_rejected():
    """Negative front spring stiffness must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.suspension.front_spring_stiffness.value = -50000.0
    vehicle.suspension.rear_spring_stiffness.value = 60000.0

    model = SuspensionModel(vehicle.suspension)

    with pytest.raises(
        ValueError,
        match="Front spring stiffness cannot be negative",
    ):
        model.calculate_spring_force(
            front_displacement=0.010,
            rear_displacement=0.010,
        )


def test_negative_rear_spring_stiffness_is_rejected():
    """Negative rear spring stiffness must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.suspension.front_spring_stiffness.value = 50000.0
    vehicle.suspension.rear_spring_stiffness.value = -60000.0

    model = SuspensionModel(vehicle.suspension)

    with pytest.raises(
        ValueError,
        match="Rear spring stiffness cannot be negative",
    ):
        model.calculate_spring_force(
            front_displacement=0.010,
            rear_displacement=0.010,
        )


# ---------------------------------------------------------------------------
# M3.5.2 / M3.5.3 — Motion ratio and wheel rate
# ---------------------------------------------------------------------------


def test_front_wheel_rate_is_spring_rate_times_motion_ratio_squared():
    """Front wheel rate must be k * MR²."""

    model = create_test_suspension_model()

    result = model.calculate_wheel_rate()

    expected = 50000.0 * 0.80**2

    assert result.front_wheel_rate == pytest.approx(
        expected
    )


def test_rear_wheel_rate_is_spring_rate_times_motion_ratio_squared():
    """Rear wheel rate must be k * MR²."""

    model = create_test_suspension_model()

    result = model.calculate_wheel_rate()

    expected = 60000.0 * 0.75**2

    assert result.rear_wheel_rate == pytest.approx(
        expected
    )


def test_missing_front_motion_ratio_is_rejected():
    """Missing front motion ratio must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.suspension.front_spring_stiffness.value = 50000.0
    vehicle.suspension.rear_spring_stiffness.value = 60000.0

    vehicle.suspension.front_motion_ratio.value = None
    vehicle.suspension.rear_motion_ratio.value = 0.75

    model = SuspensionModel(vehicle.suspension)

    with pytest.raises(
        ValueError,
        match="Front motion ratio is required",
    ):
        model.calculate_wheel_rate()


def test_missing_rear_motion_ratio_is_rejected():
    """Missing rear motion ratio must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.suspension.front_spring_stiffness.value = 50000.0
    vehicle.suspension.rear_spring_stiffness.value = 60000.0

    vehicle.suspension.front_motion_ratio.value = 0.80
    vehicle.suspension.rear_motion_ratio.value = None

    model = SuspensionModel(vehicle.suspension)

    with pytest.raises(
        ValueError,
        match="Rear motion ratio is required",
    ):
        model.calculate_wheel_rate()


def test_zero_front_motion_ratio_is_rejected():
    """Zero front motion ratio must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.suspension.front_spring_stiffness.value = 50000.0
    vehicle.suspension.rear_spring_stiffness.value = 60000.0

    vehicle.suspension.front_motion_ratio.value = 0.0
    vehicle.suspension.rear_motion_ratio.value = 0.75

    model = SuspensionModel(vehicle.suspension)

    with pytest.raises(
        ValueError,
        match="Front motion ratio must be positive",
    ):
        model.calculate_wheel_rate()


def test_negative_rear_motion_ratio_is_rejected():
    """Negative rear motion ratio must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.suspension.front_spring_stiffness.value = 50000.0
    vehicle.suspension.rear_spring_stiffness.value = 60000.0

    vehicle.suspension.front_motion_ratio.value = 0.80
    vehicle.suspension.rear_motion_ratio.value = -0.75

    model = SuspensionModel(vehicle.suspension)

    with pytest.raises(
        ValueError,
        match="Rear motion ratio must be positive",
    ):
        model.calculate_wheel_rate()


# ---------------------------------------------------------------------------
# Wheel force
# ---------------------------------------------------------------------------


def test_wheel_force_is_wheel_rate_times_displacement():
    """Wheel force must follow F = kw * xw."""

    model = create_test_suspension_model()

    result = model.calculate_wheel_force(
        front_wheel_displacement=0.010,
        rear_wheel_displacement=0.010,
    )

    expected_front = 50000.0 * 0.80**2 * 0.010
    expected_rear = 60000.0 * 0.75**2 * 0.010

    assert result.front_force == pytest.approx(
        expected_front
    )

    assert result.rear_force == pytest.approx(
        expected_rear
    )


def test_wheel_force_scales_linearly_with_displacement():
    """Wheel force must scale linearly with wheel displacement."""

    model = create_test_suspension_model()

    low = model.calculate_wheel_force(
        front_wheel_displacement=0.010,
        rear_wheel_displacement=0.010,
    )

    high = model.calculate_wheel_force(
        front_wheel_displacement=0.020,
        rear_wheel_displacement=0.020,
    )

    assert high.front_force == pytest.approx(
        2.0 * low.front_force
    )

    assert high.rear_force == pytest.approx(
        2.0 * low.rear_force
    )

# ---------------------------------------------------------------------------
# M3.5.5 — Suspension force integration
# ---------------------------------------------------------------------------


def test_wheel_damping_scales_with_motion_ratio():
    """Wheel damping must scale with motion ratio squared."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.suspension.front_damping_compression.value = 3000.0
    vehicle.suspension.front_damping_rebound.value = 4000.0
    vehicle.suspension.rear_damping_compression.value = 3500.0
    vehicle.suspension.rear_damping_rebound.value = 4500.0

    vehicle.suspension.front_motion_ratio.value = 0.80
    vehicle.suspension.rear_motion_ratio.value = 0.75

    model = DamperModel(vehicle.suspension)

    (
        front_compression,
        front_rebound,
        rear_compression,
        rear_rebound,
    ) = model.calculate_wheel_damping()

    assert front_compression == pytest.approx(
        3000.0 * 0.80**2
    )

    assert front_rebound == pytest.approx(
        4000.0 * 0.80**2
    )

    assert rear_compression == pytest.approx(
        3500.0 * 0.75**2
    )

    assert rear_rebound == pytest.approx(
        4500.0 * 0.75**2
    )

def test_total_suspension_force_is_spring_plus_damper():
    """Total suspension force must equal spring plus damper force."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.suspension.front_spring_stiffness.value = 50000.0
    vehicle.suspension.rear_spring_stiffness.value = 60000.0

    vehicle.suspension.front_motion_ratio.value = 0.80
    vehicle.suspension.rear_motion_ratio.value = 0.75

    vehicle.suspension.front_damping_compression.value = 3000.0
    vehicle.suspension.front_damping_rebound.value = 4000.0
    vehicle.suspension.rear_damping_compression.value = 3500.0
    vehicle.suspension.rear_damping_rebound.value = 4500.0

    model = SuspensionModel(vehicle.suspension)

    result = model.calculate_total_force(
        front_displacement=0.010,
        rear_displacement=0.010,
        front_velocity=0.10,
        rear_velocity=0.10,
    )

    expected_front_spring = (
        50000.0 * 0.80**2 * 0.010
    )

    expected_rear_spring = (
        60000.0 * 0.75**2 * 0.010
    )

    expected_front_damper = -3000.0 * 0.10
    expected_rear_damper = -3500.0 * 0.10

    assert result.front_force == pytest.approx(
        expected_front_spring + expected_front_damper
    )

    assert result.rear_force == pytest.approx(
        expected_rear_spring + expected_rear_damper
    )


def test_static_suspension_force_is_only_spring_force():
    """With zero velocity, suspension force must equal spring force."""

    model = create_test_suspension_model()

    result = model.calculate_total_force(
        front_displacement=0.010,
        rear_displacement=0.010,
        front_velocity=0.0,
        rear_velocity=0.0,
    )

    wheel_rate = model.calculate_wheel_rate()

    assert result.front_force == pytest.approx(
        wheel_rate.front_wheel_rate * 0.010
    )

    assert result.rear_force == pytest.approx(
        wheel_rate.rear_wheel_rate * 0.010
    )


def test_damper_changes_total_force_during_compression():
    """Compression damping must reduce total force for positive velocity."""

    model = create_test_suspension_model()

    static = model.calculate_total_force(
        front_displacement=0.010,
        rear_displacement=0.010,
        front_velocity=0.0,
        rear_velocity=0.0,
    )

    dynamic = model.calculate_total_force(
        front_displacement=0.010,
        rear_displacement=0.010,
        front_velocity=0.10,
        rear_velocity=0.10,
    )

    assert dynamic.front_force < static.front_force
    assert dynamic.rear_force < static.rear_force


def test_damper_changes_total_force_during_rebound():
    """Rebound damping must increase force for negative velocity."""

    model = create_test_suspension_model()

    static = model.calculate_total_force(
        front_displacement=0.010,
        rear_displacement=0.010,
        front_velocity=0.0,
        rear_velocity=0.0,
    )

    dynamic = model.calculate_total_force(
        front_displacement=0.010,
        rear_displacement=0.010,
        front_velocity=-0.10,
        rear_velocity=-0.10,
    )

    assert dynamic.front_force > static.front_force
    assert dynamic.rear_force > static.rear_force