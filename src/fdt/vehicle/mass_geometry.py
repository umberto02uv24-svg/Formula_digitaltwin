from dataclasses import dataclass

from fdt.vehicle.parameters import VehicleParameters


GRAVITY = 9.81


@dataclass(frozen=True)
class StaticLoadResult:
    """Static vertical loads acting on the front and rear axles."""

    front_axle_load: float
    rear_axle_load: float
    total_load: float

    @property
    def front_load_distribution(self) -> float:
        """Return the fraction of static load carried by the front axle."""

        return self.front_axle_load / self.total_load

    @property
    def rear_load_distribution(self) -> float:
        """Return the fraction of static load carried by the rear axle."""

        return self.rear_axle_load / self.total_load


class MassGeometryModel:
    """Static mass and geometry model of the vehicle."""

    def __init__(self, vehicle: VehicleParameters) -> None:
        self.vehicle = vehicle

    def calculate_static_loads(self) -> StaticLoadResult:
        """Calculate the static vertical loads on the front and rear axles."""

        mass = self.vehicle.mass.mass.value
        wheelbase = self.vehicle.geometry.wheelbase.value
        cg_position = self.vehicle.mass.cg_longitudinal_position.value

        if mass is None:
            raise ValueError("Vehicle mass is required.")

        if wheelbase is None:
            raise ValueError("Wheelbase is required.")

        if cg_position is None:
            raise ValueError(
            "CG longitudinal position is required."
        )

        if mass <= 0:
            raise ValueError("Vehicle mass must be positive.")

        if wheelbase <= 0:
            raise ValueError("Wheelbase must be positive.")

        if cg_position < 0 or cg_position > wheelbase:
            raise ValueError(
            "CG longitudinal position must lie between the front "
            "and rear axles."
        )

        total_load = mass * GRAVITY

        front_axle_load = (
            total_load * (wheelbase - cg_position) / wheelbase
        )

        rear_axle_load = (
        total_load * cg_position / wheelbase
        )

        return StaticLoadResult(
            front_axle_load=front_axle_load,
            rear_axle_load=rear_axle_load,
            total_load=total_load,
    )