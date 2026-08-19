from dataclasses import dataclass

from fdt.vehicle.parameters import AerodynamicParameters


@dataclass(frozen=True)
class AeroForceResult:
    """Aerodynamic forces acting on the vehicle."""

    drag_force: float
    downforce: float
    front_downforce: float
    rear_downforce: float


class AeroModel:
    """Simplified quasi-static aerodynamic model."""

    def __init__(
        self,
        parameters: AerodynamicParameters,
    ) -> None:
        self.parameters = parameters

    def _get_parameters(
        self,
    ) -> tuple[float, float, float, float, float]:
        """Return validated aerodynamic parameters."""

        air_density = self.parameters.air_density.value
        frontal_area = self.parameters.frontal_area.value
        drag_coefficient = self.parameters.drag_coefficient.value
        lift_coefficient = self.parameters.lift_coefficient.value
        front_aero_balance = self.parameters.front_aero_balance.value

        if air_density is None:
            raise ValueError("Air density is required.")

        if frontal_area is None:
            raise ValueError("Frontal area is required.")

        if drag_coefficient is None:
            raise ValueError("Drag coefficient is required.")

        if lift_coefficient is None:
            raise ValueError("Lift coefficient is required.")

        if air_density <= 0:
            raise ValueError("Air density must be positive.")

        if frontal_area <= 0:
            raise ValueError("Frontal area must be positive.")

        if drag_coefficient < 0:
            raise ValueError(
                "Drag coefficient cannot be negative."
            )

        if lift_coefficient < 0:
            raise ValueError(
                "Lift coefficient cannot be negative."
            )

        if front_aero_balance is None:
            raise ValueError(
                "Front aero balance is required."
            )

        if not 0.0 <= front_aero_balance <= 1.0:
            raise ValueError(
                "Front aero balance must be between 0 and 1."
            )

        return (
            air_density,
            frontal_area,
            drag_coefficient,
            lift_coefficient,
            front_aero_balance,
        )

    def calculate_forces(
        self,
        velocity: float,
    ) -> AeroForceResult:
        """Calculate aerodynamic drag and downforce."""

        if velocity < 0:
            raise ValueError(
                "Velocity cannot be negative."
            )

        (
            air_density,
            frontal_area,
            drag_coefficient,
            lift_coefficient,
            front_aero_balance,
        ) = self._get_parameters()

        dynamic_pressure = (
            0.5
            * air_density
            * velocity**2
        )

        drag_force = (
            dynamic_pressure
            * drag_coefficient
            * frontal_area
        )

        downforce = (
            dynamic_pressure
            * lift_coefficient
            * frontal_area
        )

        front_downforce =(
            downforce * front_aero_balance
        )

        rear_downforce = (
            downforce * (1.0 - front_aero_balance)
        )

        return AeroForceResult(
            drag_force=drag_force,
            downforce=downforce,
            front_downforce=front_downforce,
            rear_downforce=rear_downforce,
        )