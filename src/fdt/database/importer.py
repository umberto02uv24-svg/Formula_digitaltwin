from dataclasses import fields, is_dataclass

from fdt.vehicle.parameter import EngineeringParameter
from fdt.vehicle.parameters import VehicleParameters

from .models import ParameterRecord
from .repository import initialize_database, insert_parameter


def _extract_parameters(
    obj,
    prefix: str = "",
) -> list[tuple[str, EngineeringParameter]]:
    """Recursively extract EngineeringParameter objects."""

    parameters = []

    if isinstance(obj, EngineeringParameter):
        parameters.append((prefix, obj))
        return parameters

    if not is_dataclass(obj):
        return parameters

    for field in fields(obj):
        value = getattr(obj, field.name)

        field_name = (
            f"{prefix}.{field.name}"
            if prefix
            else field.name
        )

        parameters.extend(
            _extract_parameters(value, field_name)
        )

    return parameters


def import_vehicle_parameters(
    vehicle: VehicleParameters,
    vehicle_id: str,
) -> None:
    """Import all engineering parameters of a vehicle into SQLite."""

    initialize_database()

    parameters = _extract_parameters(vehicle)

    for name, parameter in parameters:
        record = ParameterRecord(
            name=name,
            value=parameter.value,
            unit=parameter.unit,
            source=parameter.source,
            confidence=parameter.confidence.value,
            status=parameter.status.value,
            vehicle_id=vehicle_id,
        )

        insert_parameter(record)