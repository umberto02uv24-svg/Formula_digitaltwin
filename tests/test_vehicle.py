from fdt.vehicle.config import FDT01_BASELINE


def test_fdt01_baseline_exists():
    vehicle = FDT01_BASELINE

    assert vehicle.mass > 0
    assert vehicle.wheelbase > 0
    assert vehicle.front_track > 0
    assert vehicle.rear_track > 0


def test_fdt01_mass_distribution():
    vehicle = FDT01_BASELINE

    assert 0.0 < vehicle.front_mass_distribution < 1.0