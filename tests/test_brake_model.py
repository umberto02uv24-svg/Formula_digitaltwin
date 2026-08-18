import copy

import pytest

from fdt.vehicle.brake_model import BrakeModel
from fdt.vehicle.config import FDT01_BASELINE_V1


def create_test_brake_model() -> BrakeModel:
    """Create a brake model with valid test parameters."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.brakes.brake_bias.value = 0.60

    return BrakeModel(vehicle.brakes)


# ---------------------------------------------------------------------------
# M3.4.1 — Brake torque distribution
# ---------------------------------------------------------------------------


def test_brake_torque_is_distributed_according_to_bias():
    """Brake torque must be distributed according to brake bias."""

    model = create_test_brake_model()

    result = model.calculate_brake_torque(
        total_brake_torque=4000.0,
    )

    assert result.front_torque == pytest.approx(2400.0)
    assert result.rear_torque == pytest.approx(1600.0)


def test_front_and_rear_torque_sum_to_total():
    """Front and rear axle torque must sum to total requested torque."""

    model = create_test_brake_model()

    result = model.calculate_brake_torque(
        total_brake_torque=4000.0,
    )

    assert (
        result.front_torque + result.rear_torque
        == pytest.approx(4000.0)
    )


def test_zero_brake_torque_produces_zero_forces():
    """Zero brake torque must produce zero axle torque."""

    model = create_test_brake_model()

    result = model.calculate_brake_torque(
        total_brake_torque=0.0,
    )

    assert result.front_torque == pytest.approx(0.0)
    assert result.rear_torque == pytest.approx(0.0)


def test_negative_total_brake_torque_is_rejected():
    """Negative total brake torque must be rejected."""

    model = create_test_brake_model()

    with pytest.raises(
        ValueError,
        match="cannot be negative",
    ):
        model.calculate_brake_torque(
            total_brake_torque=-100.0,
        )


def test_missing_brake_bias_is_rejected():
    """Missing brake bias must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.brakes.brake_bias.value = None

    model = BrakeModel(vehicle.brakes)

    with pytest.raises(
        ValueError,
        match="Brake bias is required",
    ):
        model.calculate_brake_torque(
            total_brake_torque=4000.0,
        )


def test_brake_bias_below_zero_is_rejected():
    """Brake bias below zero must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.brakes.brake_bias.value = -0.1

    model = BrakeModel(vehicle.brakes)

    with pytest.raises(
        ValueError,
        match="between 0 and 1",
    ):
        model.calculate_brake_torque(
            total_brake_torque=4000.0,
        )


def test_brake_bias_above_one_is_rejected():
    """Brake bias above one must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.brakes.brake_bias.value = 1.1

    model = BrakeModel(vehicle.brakes)

    with pytest.raises(
        ValueError,
        match="between 0 and 1",
    ):
        model.calculate_brake_torque(
            total_brake_torque=4000.0,
        )


# ---------------------------------------------------------------------------
# M3.4.2 — Wheel brake torque
# ---------------------------------------------------------------------------


def test_wheel_brake_torque_is_half_of_axle_torque():
    """Each wheel receives half of its axle brake torque."""

    model = create_test_brake_model()

    front_wheel_torque, rear_wheel_torque = (
        model.calculate_wheel_brake_torque(
            total_brake_torque=4000.0,
        )
    )

    assert front_wheel_torque == pytest.approx(1200.0)
    assert rear_wheel_torque == pytest.approx(800.0)


def test_wheel_brake_torques_sum_to_half_total():
    """One front and one rear wheel represent half the total axle torque."""

    model = create_test_brake_model()

    front_wheel_torque, rear_wheel_torque = (
        model.calculate_wheel_brake_torque(
            total_brake_torque=4000.0,
        )
    )

    assert (
        front_wheel_torque + rear_wheel_torque
        == pytest.approx(2000.0)
    )


def test_wheel_brake_torque_rejects_negative_total_torque():
    """Wheel brake torque must reject negative total torque."""

    model = create_test_brake_model()

    with pytest.raises(
        ValueError,
        match="cannot be negative",
    ):
        model.calculate_wheel_brake_torque(
            total_brake_torque=-100.0,
        )


# ---------------------------------------------------------------------------
# M3.4.3 — Braking force
# ---------------------------------------------------------------------------


def test_braking_force_is_brake_torque_divided_by_radius():
    """Braking force must equal wheel torque divided by wheel radius."""

    model = create_test_brake_model()

    front_force, rear_force = model.calculate_braking_force(
        total_brake_torque=4000.0,
        wheel_radius=0.25,
    )

    assert front_force == pytest.approx(4800.0)
    assert rear_force == pytest.approx(3200.0)


def test_braking_force_scales_with_brake_torque():
    """Braking force must scale linearly with brake torque."""

    model = create_test_brake_model()

    low_front, low_rear = model.calculate_braking_force(
        total_brake_torque=2000.0,
        wheel_radius=0.25,
    )

    high_front, high_rear = model.calculate_braking_force(
        total_brake_torque=4000.0,
        wheel_radius=0.25,
    )

    assert high_front == pytest.approx(
        2.0 * low_front
    )

    assert high_rear == pytest.approx(
        2.0 * low_rear
    )


def test_zero_wheel_radius_is_rejected_for_braking_force():
    """Zero wheel radius must be rejected."""

    model = create_test_brake_model()

    with pytest.raises(
        ValueError,
        match="Wheel radius must be positive",
    ):
        model.calculate_braking_force(
            total_brake_torque=4000.0,
            wheel_radius=0.0,
        )


def test_negative_wheel_radius_is_rejected_for_braking_force():
    """Negative wheel radius must be rejected."""

    model = create_test_brake_model()

    with pytest.raises(
        ValueError,
        match="Wheel radius must be positive",
    ):
        model.calculate_braking_force(
            total_brake_torque=4000.0,
            wheel_radius=-0.25,
        )


# ---------------------------------------------------------------------------
# M3.4.4 — Brake torque limits
# ---------------------------------------------------------------------------


def create_limited_test_brake_model() -> BrakeModel:
    """Create a brake model with explicit axle torque limits."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.brakes.brake_bias.value = 0.60
    vehicle.brakes.front_brake_torque.value = 3000.0
    vehicle.brakes.rear_brake_torque.value = 2000.0

    return BrakeModel(vehicle.brakes)


def test_brake_torque_is_limited_by_front_and_rear_capacity():
    """Brake torque must not exceed axle torque capacity."""

    model = create_limited_test_brake_model()

    result = model.calculate_limited_brake_torque(
        total_brake_torque=6000.0,
    )

    assert result.front_torque == pytest.approx(3000.0)
    assert result.rear_torque == pytest.approx(2000.0)


def test_front_brake_torque_limit_is_applied_independently():
    """Front brake capacity must be applied independently."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.brakes.brake_bias.value = 0.70
    vehicle.brakes.front_brake_torque.value = 2000.0
    vehicle.brakes.rear_brake_torque.value = 3000.0

    model = BrakeModel(vehicle.brakes)

    result = model.calculate_limited_brake_torque(
        total_brake_torque=4000.0,
    )

    assert result.front_torque == pytest.approx(2000.0)
    assert result.rear_torque == pytest.approx(1200.0)


def test_rear_brake_torque_limit_is_applied_independently():
    """Rear brake capacity must be applied independently."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.brakes.brake_bias.value = 0.40
    vehicle.brakes.front_brake_torque.value = 3000.0
    vehicle.brakes.rear_brake_torque.value = 1000.0

    model = BrakeModel(vehicle.brakes)

    result = model.calculate_limited_brake_torque(
        total_brake_torque=4000.0,
    )

    assert result.front_torque == pytest.approx(1600.0)
    assert result.rear_torque == pytest.approx(1000.0)


def test_missing_front_brake_torque_limit_is_rejected():
    """Missing front brake torque capacity must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.brakes.brake_bias.value = 0.60
    vehicle.brakes.front_brake_torque.value = None
    vehicle.brakes.rear_brake_torque.value = 2000.0

    model = BrakeModel(vehicle.brakes)

    with pytest.raises(
        ValueError,
        match="Front brake torque limit is required",
    ):
        model.calculate_limited_brake_torque(
            total_brake_torque=4000.0,
        )


def test_missing_rear_brake_torque_limit_is_rejected():
    """Missing rear brake torque capacity must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.brakes.brake_bias.value = 0.60
    vehicle.brakes.front_brake_torque.value = 3000.0
    vehicle.brakes.rear_brake_torque.value = None

    model = BrakeModel(vehicle.brakes)

    with pytest.raises(
        ValueError,
        match="Rear brake torque limit is required",
    ):
        model.calculate_limited_brake_torque(
            total_brake_torque=4000.0,
        )


def test_negative_front_brake_torque_limit_is_rejected():
    """Negative front brake torque capacity must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.brakes.brake_bias.value = 0.60
    vehicle.brakes.front_brake_torque.value = -100.0
    vehicle.brakes.rear_brake_torque.value = 2000.0

    model = BrakeModel(vehicle.brakes)

    with pytest.raises(
        ValueError,
        match="Front brake torque limit cannot be negative",
    ):
        model.calculate_limited_brake_torque(
            total_brake_torque=4000.0,
        )


def test_negative_rear_brake_torque_limit_is_rejected():
    """Negative rear brake torque capacity must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.brakes.brake_bias.value = 0.60
    vehicle.brakes.front_brake_torque.value = 3000.0
    vehicle.brakes.rear_brake_torque.value = -100.0

    model = BrakeModel(vehicle.brakes)

    with pytest.raises(
        ValueError,
        match="Rear brake torque limit cannot be negative",
    ):
        model.calculate_limited_brake_torque(
            total_brake_torque=4000.0,
        )

# ---------------------------------------------------------------------------
# M3.4.5 — Brake model validation
# ---------------------------------------------------------------------------


def test_brake_bias_distribution_is_conserved():
    """Unrestricted brake torque must be conserved."""

    model = create_test_brake_model()

    total_torque = 5000.0

    result = model.calculate_brake_torque(
        total_brake_torque=total_torque,
    )

    reconstructed_torque = (
        result.front_torque
        + result.rear_torque
    )

    assert reconstructed_torque == pytest.approx(
        total_torque
    )


def test_wheel_torque_distribution_is_conserved():
    """Wheel torque must be consistent with axle torque."""

    model = create_test_brake_model()

    total_torque = 5000.0

    axle_result = model.calculate_brake_torque(
        total_brake_torque=total_torque,
    )

    front_wheel, rear_wheel = (
        model.calculate_wheel_brake_torque(
            total_brake_torque=total_torque,
        )
    )

    assert front_wheel * 2.0 == pytest.approx(
        axle_result.front_torque
    )

    assert rear_wheel * 2.0 == pytest.approx(
        axle_result.rear_torque
    )


def test_braking_force_is_consistent_with_wheel_torque():
    """Braking force must be consistent with wheel torque."""

    model = create_test_brake_model()

    wheel_radius = 0.25
    total_torque = 4000.0

    front_wheel_torque, rear_wheel_torque = (
        model.calculate_wheel_brake_torque(
            total_brake_torque=total_torque,
        )
    )

    front_force, rear_force = (
        model.calculate_braking_force(
            total_brake_torque=total_torque,
            wheel_radius=wheel_radius,
        )
    )

    assert front_force == pytest.approx(
        front_wheel_torque / wheel_radius
    )

    assert rear_force == pytest.approx(
        rear_wheel_torque / wheel_radius
    )


def test_limited_brake_torque_never_exceeds_system_capacity():
    """Limited axle torque must never exceed brake capacity."""

    model = create_limited_test_brake_model()

    result = model.calculate_limited_brake_torque(
        total_brake_torque=10000.0,
    )

    front_limit = (
        model.parameters.front_brake_torque.value
    )

    rear_limit = (
        model.parameters.rear_brake_torque.value
    )

    assert front_limit is not None
    assert rear_limit is not None

    assert result.front_torque <= front_limit
    assert result.rear_torque <= rear_limit


def test_zero_brake_demand_is_zero_after_limiting():
    """Zero brake demand must remain zero after limiting."""

    model = create_limited_test_brake_model()

    result = model.calculate_limited_brake_torque(
        total_brake_torque=0.0,
    )

    assert result.front_torque == pytest.approx(0.0)
    assert result.rear_torque == pytest.approx(0.0)


def test_braking_force_decreases_with_larger_wheel_radius():
    """For the same torque, larger radius produces lower force."""

    model = create_test_brake_model()

    total_torque = 4000.0

    small_radius_front, small_radius_rear = (
        model.calculate_braking_force(
            total_brake_torque=total_torque,
            wheel_radius=0.20,
        )
    )

    large_radius_front, large_radius_rear = (
        model.calculate_braking_force(
            total_brake_torque=total_torque,
            wheel_radius=0.40,
        )
    )

    assert large_radius_front < small_radius_front
    assert large_radius_rear < small_radius_rear

    assert large_radius_front == pytest.approx(
        small_radius_front / 2.0
    )

    assert large_radius_rear == pytest.approx(
        small_radius_rear / 2.0
    )