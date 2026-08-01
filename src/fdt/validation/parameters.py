from fdt.database.models import ParameterRecord
from fdt.units.registry import ureg

from fdt.validation.parameter_dimensions import PARAMETER_DIMENSIONS
from fdt.validation.range_validator import validate_parameter_range


EXPECTED_UNITS = {
    "mass": ureg.kg,
    "length": ureg.m,
    "power": ureg.W,
    "torque": ureg.N * ureg.m,
    "angular_speed": ureg.rpm,
    "spring_stiffness": ureg.N / ureg.m,
    "lateral_stiffness": ureg.N / ureg.radian,
    "longitudinal_stiffness": ureg.N,
}


def validate_parameter(parameter: ParameterRecord) -> None:
    """Validate the physical consistency of an engineering parameter."""

    if parameter.value is None:
        return

    quantity = parameter.value * ureg(parameter.unit)

    if quantity.magnitude < 0:
        raise ValueError(
            f"Parameter '{parameter.name}' cannot be negative."
        )

    expected_dimension = PARAMETER_DIMENSIONS.get(parameter.name)

    if expected_dimension is None:
        return

    expected_unit = EXPECTED_UNITS[expected_dimension]

    if quantity.dimensionality != expected_unit.dimensionality:
        raise ValueError(
            f"Parameter '{parameter.name}' has invalid unit "
            f"'{parameter.unit}'. Expected dimension: "
            f"{expected_dimension}."
        )

    validate_parameter_range(parameter)