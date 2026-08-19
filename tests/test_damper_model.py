import copy

import pytest

from fdt.vehicle.config import FDT01_BASELINE_V1
from fdt.vehicle.damper_model import DamperModel


def create_test_damper_model() -> DamperModel:
    """Create a damper model with valid test parameters."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.suspension.front_damping_compression.value = 3000.0
    vehicle.suspension.front_damping_rebound.value = 4000.0
    vehicle.suspension.rear_damping_compression.value = 3500.0
    vehicle.suspension.rear_damping_rebound.value = 4500.0

    return DamperModel(vehicle.suspension)


# ---------------------------------------------------------------------------
# Basic damper behaviour
# ---------------------------------------------------------------------------


def test_zero_velocity_produces_zero_damper_force():
    """Zero velocity must produce zero damper force."""

    model = create_test_damper_model()

    result = model.calculate_force(
        front_velocity=0.0,
        rear_velocity=0.0,
    )

    assert result.front_force == pytest.approx(0.0)
    assert result.rear_force == pytest.approx(0.0)


def test_front_compression_uses_compression_damping():
    """Positive front velocity must use compression damping."""

    model = create_test_damper_model()

    result = model.calculate_force(
        front_velocity=0.10,
        rear_velocity=0.0,
    )

    assert result.front_force == pytest.approx(-300.0)


def test_front_rebound_uses_rebound_damping():
    """Negative front velocity must use rebound damping."""

    model = create_test_damper_model()

    result = model.calculate_force(
        front_velocity=-0.10,
        rear_velocity=0.0,
    )

    assert result.front_force == pytest.approx(400.0)


def test_rear_compression_uses_compression_damping():
    """Positive rear velocity must use compression damping."""

    model = create_test_damper_model()

    result = model.calculate_force(
        front_velocity=0.0,
        rear_velocity=0.10,
    )

    assert result.rear_force == pytest.approx(-350.0)


def test_rear_rebound_uses_rebound_damping():
    """Negative rear velocity must use rebound damping."""

    model = create_test_damper_model()

    result = model.calculate_force(
        front_velocity=0.0,
        rear_velocity=-0.10,
    )

    assert result.rear_force == pytest.approx(450.0)


def test_damper_force_opposes_velocity():
    """Damper force must oppose suspension velocity."""

    model = create_test_damper_model()

    compression = model.calculate_force(
        front_velocity=0.20,
        rear_velocity=0.20,
    )

    rebound = model.calculate_force(
        front_velocity=-0.20,
        rear_velocity=-0.20,
    )

    assert compression.front_force < 0
    assert compression.rear_force < 0

    assert rebound.front_force > 0
    assert rebound.rear_force > 0


def test_damper_force_scales_linearly_with_velocity():
    """Damper force must scale linearly with velocity."""

    model = create_test_damper_model()

    low = model.calculate_force(
        front_velocity=0.10,
        rear_velocity=0.10,
    )

    high = model.calculate_force(
        front_velocity=0.20,
        rear_velocity=0.20,
    )

    assert high.front_force == pytest.approx(
        2.0 * low.front_force
    )

    assert high.rear_force == pytest.approx(
        2.0 * low.rear_force
    )


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def test_missing_front_compression_damping_is_rejected():
    """Missing front compression damping must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.suspension.front_damping_compression.value = None

    model = DamperModel(vehicle.suspension)

    with pytest.raises(
        ValueError,
        match="Front compression damping is required",
    ):
        model.calculate_force(
            front_velocity=0.10,
            rear_velocity=0.10,
        )


def test_missing_front_rebound_damping_is_rejected():
    """Missing front rebound damping must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.suspension.front_damping_rebound.value = None

    model = DamperModel(vehicle.suspension)

    with pytest.raises(
        ValueError,
        match="Front rebound damping is required",
    ):
        model.calculate_force(
            front_velocity=0.10,
            rear_velocity=0.10,
        )


def test_missing_rear_compression_damping_is_rejected():
    """Missing rear compression damping must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.suspension.rear_damping_compression.value = None

    model = DamperModel(vehicle.suspension)

    with pytest.raises(
        ValueError,
        match="Rear compression damping is required",
    ):
        model.calculate_force(
            front_velocity=0.10,
            rear_velocity=0.10,
        )


def test_missing_rear_rebound_damping_is_rejected():
    """Missing rear rebound damping must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.suspension.rear_damping_rebound.value = None

    model = DamperModel(vehicle.suspension)

    with pytest.raises(
        ValueError,
        match="Rear rebound damping is required",
    ):
        model.calculate_force(
            front_velocity=0.10,
            rear_velocity=0.10,
        )


def test_negative_front_compression_damping_is_rejected():
    """Negative front compression damping must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.suspension.front_damping_compression.value = -1.0

    model = DamperModel(vehicle.suspension)

    with pytest.raises(
        ValueError,
        match="Front compression damping cannot be negative",
    ):
        model.calculate_force(
            front_velocity=0.10,
            rear_velocity=0.10,
        )


def test_negative_front_rebound_damping_is_rejected():
    """Negative front rebound damping must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.suspension.front_damping_rebound.value = -1.0

    model = DamperModel(vehicle.suspension)

    with pytest.raises(
        ValueError,
        match="Front rebound damping cannot be negative",
    ):
        model.calculate_force(
            front_velocity=0.10,
            rear_velocity=0.10,
        )


def test_negative_rear_compression_damping_is_rejected():
    """Negative rear compression damping must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.suspension.rear_damping_compression.value = -1.0

    model = DamperModel(vehicle.suspension)

    with pytest.raises(
        ValueError,
        match="Rear compression damping cannot be negative",
    ):
        model.calculate_force(
            front_velocity=0.10,
            rear_velocity=0.10,
        )


def test_negative_rear_rebound_damping_is_rejected():
    """Negative rear rebound damping must be rejected."""

    vehicle = copy.deepcopy(FDT01_BASELINE_V1)

    vehicle.suspension.rear_damping_rebound.value = -1.0

    model = DamperModel(vehicle.suspension)

    with pytest.raises(
        ValueError,
        match="Rear rebound damping cannot be negative",
    ):
        model.calculate_force(
            front_velocity=0.10,
            rear_velocity=0.10,
        )