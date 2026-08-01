from fdt.validation.parameter_ranges import PARAMETER_RANGES


def test_mass_range_exists():
    """Check that the vehicle mass has a defined engineering range."""

    assert "mass.mass" in PARAMETER_RANGES

    mass_range = PARAMETER_RANGES["mass.mass"]

    assert mass_range["min"] < mass_range["max"]
    assert mass_range["unit"] == "kg"


def test_wheelbase_range_exists():
    """Check that the wheelbase has a defined engineering range."""

    assert "geometry.wheelbase" in PARAMETER_RANGES

    wheelbase_range = PARAMETER_RANGES["geometry.wheelbase"]

    assert wheelbase_range["min"] < wheelbase_range["max"]
    assert wheelbase_range["unit"] == "m"


def test_all_ranges_are_valid():
    """Check that all defined parameter ranges are internally consistent."""

    for name, parameter_range in PARAMETER_RANGES.items():
        assert "min" in parameter_range
        assert "max" in parameter_range
        assert "unit" in parameter_range

        assert parameter_range["min"] < parameter_range["max"]