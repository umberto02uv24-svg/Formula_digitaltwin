from fdt.vehicle.config import FDT01_BASELINE_V1
from fdt.vehicle.parameter import ParameterStatus


def test_fdt01_baseline_exists():
    vehicle = FDT01_BASELINE_V1

    assert vehicle.mass.mass.value > 0
    assert vehicle.geometry.wheelbase > 0
    assert vehicle.geometry.front_track > 0
    assert vehicle.geometry.rear_track > 0


def test_fdt01_mass_distribution():
    vehicle = FDT01_BASELINE_V1

    distribution = vehicle.mass.front_mass_distribution.value

    assert 0.0 < distribution < 1.0


def test_fdt01_mass_traceability():
    vehicle = FDT01_BASELINE_V1

    mass = vehicle.mass.mass

    assert mass.value == 530.0
    assert mass.unit == "kg"
    assert mass.status == ParameterStatus.BENCHMARK
    assert mass.source != ""