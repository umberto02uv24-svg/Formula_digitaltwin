import pytest

from fdt.database.models import ParameterRecord
from fdt.validation.parameters import validate_parameter


def test_positive_parameter_is_valid():
    """Check that a positive parameter is accepted."""

    parameter = ParameterRecord(
        name="mass.mass",
        value=530.0,
        unit="kg",
        source="Test",
        confidence="High",
        status="Validated",
        vehicle_id="TEST",
        configuration_version="1.0",
    )

    validate_parameter(parameter)


def test_negative_parameter_is_rejected():
    """Check that a negative parameter is rejected."""

    parameter = ParameterRecord(
        name="mass.mass",
        value=-530.0,
        unit="kg",
        source="Test",
        confidence="High",
        status="Validated",
        vehicle_id="TEST",
        configuration_version="1.0",
    )

    with pytest.raises(ValueError):
        validate_parameter(parameter)


def test_tbd_parameter_is_accepted():
    """Check that TBD parameters can be validated."""

    parameter = ParameterRecord(
        name="aerodynamics.drag_coefficient",
        value=None,
        unit="-",
        source="TBD",
        confidence="Low",
        status="TBD",
        vehicle_id="TEST",
        configuration_version="1.0",
    )

    validate_parameter(parameter)

def test_invalid_mass_unit_is_rejected():
    """Check that mass cannot be expressed as a length."""

    parameter = ParameterRecord(
        name="mass.mass",
        value=530.0,
        unit="m",
        source="Test",
        confidence="High",
        status="Validated",
        vehicle_id="TEST",
        configuration_version="1.0",
    )

    with pytest.raises(ValueError):
        validate_parameter(parameter)


def test_power_unit_is_valid():
    """Check that power accepts equivalent power units."""

    parameter = ParameterRecord(
        name="powertrain.maximum_power",
        value=130.0,
        unit="kW",
        source="Test",
        confidence="High",
        status="Validated",
        vehicle_id="TEST",
        configuration_version="1.0",
    )

    validate_parameter(parameter)

import pytest

from fdt.database.models import ParameterRecord
from fdt.validation.parameters import validate_parameter


def make_parameter(
    name: str,
    value: float | None,
    unit: str,
) -> ParameterRecord:
    """Create a test parameter."""

    return ParameterRecord(
        name=name,
        value=value,
        unit=unit,
        source="Test",
        confidence="Low",
        status="Test",
        vehicle_id="FDT01",
        configuration_version="1.0",
    )


def test_valid_parameter_passes_full_validation():
    """A physically correct parameter inside its range is accepted."""

    parameter = make_parameter(
        name="mass.mass",
        value=530.0,
        unit="kg",
    )

    validate_parameter(parameter)


def test_parameter_above_range_is_rejected():
    """A parameter above its engineering range is rejected."""

    parameter = make_parameter(
        name="mass.mass",
        value=900.0,
        unit="kg",
    )

    with pytest.raises(ValueError):
        validate_parameter(parameter)


def test_parameter_below_range_is_rejected():
    """A parameter below its engineering range is rejected."""

    parameter = make_parameter(
        name="mass.mass",
        value=300.0,
        unit="kg",
    )

    with pytest.raises(ValueError):
        validate_parameter(parameter)


def test_invalid_unit_is_rejected_by_full_validation():
    """A physically incompatible unit is rejected."""

    parameter = make_parameter(
        name="mass.mass",
        value=530.0,
        unit="m",
    )

    with pytest.raises(ValueError):
        validate_parameter(parameter)


def test_none_value_is_accepted():
    """A TBD parameter with no value is accepted."""

    parameter = make_parameter(
        name="mass.mass",
        value=None,
        unit="kg",
    )

    validate_parameter(parameter)