import pytest

from fdt.database.models import ParameterRecord
from fdt.validation.range_validator import validate_parameter_range


def test_valid_parameter_range():
    """Check that a parameter inside its allowed range is accepted."""

    parameter = ParameterRecord(
        name="mass.mass",
        value=530.0,
        unit="kg",
        source="F4 benchmark",
        confidence="Medium",
        status="Benchmark",
        vehicle_id="FDT01",
        configuration_version="1.0",
    )

    validate_parameter_range(parameter)


def test_parameter_below_minimum_is_rejected():
    """Check that a parameter below its minimum is rejected."""

    parameter = ParameterRecord(
        name="mass.mass",
        value=300.0,
        unit="kg",
        source="Test",
        confidence="Low",
        status="Test",
        vehicle_id="FDT01",
        configuration_version="1.0",
    )

    with pytest.raises(ValueError):
        validate_parameter_range(parameter)


def test_parameter_above_maximum_is_rejected():
    """Check that a parameter above its maximum is rejected."""

    parameter = ParameterRecord(
        name="mass.mass",
        value=900.0,
        unit="kg",
        source="Test",
        confidence="Low",
        status="Test",
        vehicle_id="FDT01",
        configuration_version="1.0",
    )

    with pytest.raises(ValueError):
        validate_parameter_range(parameter)


def test_unknown_parameter_is_ignored():
    """Check that parameters without a defined range are accepted."""

    parameter = ParameterRecord(
        name="unknown.parameter",
        value=123.0,
        unit="-",
        source="Test",
        confidence="Low",
        status="Test",
        vehicle_id="FDT01",
        configuration_version="1.0",
    )

    validate_parameter_range(parameter)


def test_none_value_is_ignored():
    """Check that TBD parameters are accepted."""

    parameter = ParameterRecord(
        name="mass.mass",
        value=None,
        unit="kg",
        source="TBD",
        confidence="Low",
        status="TBD",
        vehicle_id="FDT01",
        configuration_version="1.0",
    )

    validate_parameter_range(parameter)