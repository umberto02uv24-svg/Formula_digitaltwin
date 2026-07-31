from fdt.vehicle.config import FDT01_BASELINE_V1
from fdt.vehicle.parameter import ParameterStatus


def test_fdt01_baseline_exists():
    """Check that the main FDT-01 baseline parameters are valid."""

    vehicle = FDT01_BASELINE_V1

    assert vehicle.mass.mass.value > 0
    assert vehicle.geometry.wheelbase.value > 0
    assert vehicle.geometry.front_track.value > 0
    assert vehicle.geometry.rear_track.value > 0


def test_fdt01_mass_distribution():
    """Check that the front mass distribution is physically valid."""

    vehicle = FDT01_BASELINE_V1

    distribution = vehicle.mass.front_mass_distribution.value

    assert 0.0 < distribution < 1.0


def test_fdt01_mass_traceability():
    """Check traceability information for vehicle mass."""

    vehicle = FDT01_BASELINE_V1
    mass = vehicle.mass.mass

    assert mass.value == 530.0
    assert mass.unit == "kg"
    assert mass.status == ParameterStatus.BENCHMARK
    assert mass.source != ""


def test_fdt01_geometry_traceability():
    """Check traceability information for wheelbase."""

    vehicle = FDT01_BASELINE_V1
    wheelbase = vehicle.geometry.wheelbase

    assert wheelbase.value == 2.70
    assert wheelbase.unit == "m"
    assert wheelbase.source != ""
    assert wheelbase.status == ParameterStatus.BENCHMARK


def test_fdt01_powertrain_traceability():
    """Check traceability information for maximum power."""

    vehicle = FDT01_BASELINE_V1
    power = vehicle.powertrain.maximum_power

    assert power.value > 0
    assert power.unit == "W"
    assert power.status == ParameterStatus.BENCHMARK