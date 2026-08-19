from dataclasses import dataclass

from fdt.vehicle.damper_model import DamperModel
from fdt.vehicle.parameters import SuspensionParameters


@dataclass(frozen=True)
class SpringForceResult:
    """Suspension spring forces at the front and rear axle."""

    front_force: float
    rear_force: float


@dataclass(frozen=True)
class WheelRateResult:
    """Effective wheel rates at the front and rear axle."""

    front_wheel_rate: float
    rear_wheel_rate: float


@dataclass(frozen=True)
class SuspensionForceResult:
    """Total suspension force at the front and rear axle."""

    front_force: float
    rear_force: float


class SuspensionModel:
    """Simplified suspension spring and damper model."""

    def __init__(
        self,
        parameters: SuspensionParameters,
    ) -> None:
        self.parameters = parameters

    def calculate_spring_force(
        self,
        front_displacement: float,
        rear_displacement: float,
    ) -> SpringForceResult:
        """Calculate spring forces from suspension displacement."""

        front_stiffness = (
            self.parameters.front_spring_stiffness.value
        )
        rear_stiffness = (
            self.parameters.rear_spring_stiffness.value
        )

        if front_stiffness is None:
            raise ValueError(
                "Front spring stiffness is required."
            )

        if rear_stiffness is None:
            raise ValueError(
                "Rear spring stiffness is required."
            )

        if front_stiffness < 0:
            raise ValueError(
                "Front spring stiffness cannot be negative."
            )

        if rear_stiffness < 0:
            raise ValueError(
                "Rear spring stiffness cannot be negative."
            )

        return SpringForceResult(
            front_force=front_stiffness * front_displacement,
            rear_force=rear_stiffness * rear_displacement,
        )

    def calculate_wheel_rate(
        self,
    ) -> WheelRateResult:
        """Calculate effective wheel rates."""

        front_stiffness = (
            self.parameters.front_spring_stiffness.value
        )
        rear_stiffness = (
            self.parameters.rear_spring_stiffness.value
        )

        front_motion_ratio = (
            self.parameters.front_motion_ratio.value
        )
        rear_motion_ratio = (
            self.parameters.rear_motion_ratio.value
        )

        if front_stiffness is None:
            raise ValueError(
                "Front spring stiffness is required."
            )

        if rear_stiffness is None:
            raise ValueError(
                "Rear spring stiffness is required."
            )

        if front_motion_ratio is None:
            raise ValueError(
                "Front motion ratio is required."
            )

        if rear_motion_ratio is None:
            raise ValueError(
                "Rear motion ratio is required."
            )

        if front_stiffness < 0:
            raise ValueError(
                "Front spring stiffness cannot be negative."
            )

        if rear_stiffness < 0:
            raise ValueError(
                "Rear spring stiffness cannot be negative."
            )

        if front_motion_ratio <= 0:
            raise ValueError(
                "Front motion ratio must be positive."
            )

        if rear_motion_ratio <= 0:
            raise ValueError(
                "Rear motion ratio must be positive."
            )

        return WheelRateResult(
            front_wheel_rate=(
                front_stiffness * front_motion_ratio**2
            ),
            rear_wheel_rate=(
                rear_stiffness * rear_motion_ratio**2
            ),
        )

    def calculate_wheel_force(
        self,
        front_wheel_displacement: float,
        rear_wheel_displacement: float,
    ) -> SpringForceResult:
        """Calculate spring force at the wheels."""

        wheel_rates = self.calculate_wheel_rate()

        return SpringForceResult(
            front_force=(
                wheel_rates.front_wheel_rate
                * front_wheel_displacement
            ),
            rear_force=(
                wheel_rates.rear_wheel_rate
                * rear_wheel_displacement
            ),
        )

    def calculate_total_force(
        self,
        front_displacement: float,
        rear_displacement: float,
        front_velocity: float,
        rear_velocity: float,
    ) -> SuspensionForceResult:
        """Calculate total spring and damper force."""

        spring_force = self.calculate_wheel_force(
            front_wheel_displacement=front_displacement,
            rear_wheel_displacement=rear_displacement,
        )

        damper_model = DamperModel(self.parameters)

        damper_force = damper_model.calculate_force(
            front_velocity=front_velocity,
            rear_velocity=rear_velocity,
        )

        return SuspensionForceResult(
            front_force=(
                spring_force.front_force
                + damper_force.front_force
            ),
            rear_force=(
                spring_force.rear_force
                + damper_force.rear_force
            ),
        )