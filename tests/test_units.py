from fdt.units.registry import ureg


def test_mass_unit_conversion():
    """Check that mass units can be converted."""

    mass = 530 * ureg.kg

    mass_in_grams = mass.to("g")

    assert mass_in_grams.magnitude == 530000