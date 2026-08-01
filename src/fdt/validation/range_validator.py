from fdt.database.models import ParameterRecord
from fdt.units.registry import ureg

from fdt.validation.parameter_ranges import PARAMETER_RANGES


def validate_parameter_range(parameter: ParameterRecord) -> None:
    """Validate that an engineering parameter is within its defined range."""

    if parameter.value is None:
        return

    parameter_range = PARAMETER_RANGES.get(parameter.name)

    if parameter_range is None:
        return

    quantity = parameter.value * ureg(parameter.unit)

    minimum = parameter_range["min"] * ureg(parameter_range["unit"])
    maximum = parameter_range["max"] * ureg(parameter_range["unit"])

    try:
        quantity = quantity.to(minimum.units)
    except Exception as exc:
        raise ValueError(
            f"Parameter '{parameter.name}' has incompatible unit "
            f"'{parameter.unit}'. Expected unit dimension: "
            f"'{parameter_range['unit']}'."
        ) from exc

    if quantity < minimum or quantity > maximum:
        raise ValueError(
            f"Parameter '{parameter.name}' is outside the allowed range. "
            f"Value: {quantity}, "
            f"allowed range: {minimum} to {maximum}."
        )