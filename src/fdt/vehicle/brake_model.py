from dataclasses import dataclass

from fdt.vehicle.parameters import BrakeParameters


@dataclass(frozen=True)
class BrakeTorqueResult:
    """Brake torque distributed between front and rear axles."""

    front_torque: float
    rear_torque: float


class BrakeModel:
    """Simplified brake torque distribution and limitation model."""

    def __init__(self, parameters: BrakeParameters) -> None:
        self.parameters = parameters

    def calculate_brake_torque(
        self,
        total_brake_torque: float,
    ) -> BrakeTorqueResult:
        """Distribute total brake torque according to brake bias."""

        if total_brake_torque < 0:
            raise ValueError(
                "Total brake torque cannot be negative."
            )

        brake_bias = self.parameters.brake_bias.value

        if brake_bias is None:
            raise ValueError(
                "Brake bias is required."
            )

        if not 0.0 <= brake_bias <= 1.0:
            raise ValueError(
                "Brake bias must be between 0 and 1."
            )

        front_torque = (
            total_brake_torque * brake_bias
        )

        rear_torque = (
            total_brake_torque * (1.0 - brake_bias)
        )

        return BrakeTorqueResult(
            front_torque=front_torque,
            rear_torque=rear_torque,
        )

    def calculate_limited_brake_torque(
        self,
        total_brake_torque: float,
    ) -> BrakeTorqueResult:
        """Distribute brake torque and apply system torque limits."""

        result = self.calculate_brake_torque(
            total_brake_torque=total_brake_torque,
        )

        front_brake_torque = (
            self.parameters.front_brake_torque.value
        )

        rear_brake_torque = (
            self.parameters.rear_brake_torque.value
        )

        if front_brake_torque is None:
            raise ValueError(
                "Front brake torque limit is required."
            )

        if rear_brake_torque is None:
            raise ValueError(
                "Rear brake torque limit is required."
            )

        if front_brake_torque < 0:
            raise ValueError(
                "Front brake torque limit cannot be negative."
            )

        if rear_brake_torque < 0:
            raise ValueError(
                "Rear brake torque limit cannot be negative."
            )

        return BrakeTorqueResult(
            front_torque=min(
                result.front_torque,
                front_brake_torque,
            ),
            rear_torque=min(
                result.rear_torque,
                rear_brake_torque,
            ),
        )

    def calculate_wheel_brake_torque(
        self,
        total_brake_torque: float,
    ) -> tuple[float, float]:
        """Calculate brake torque acting on each front and rear wheel."""

        axle_torque = self.calculate_brake_torque(
            total_brake_torque=total_brake_torque,
        )

        front_wheel_torque = (
            axle_torque.front_torque / 2.0
        )

        rear_wheel_torque = (
            axle_torque.rear_torque / 2.0
        )

        return (
            front_wheel_torque,
            rear_wheel_torque,
        )

    def calculate_braking_force(
        self,
        total_brake_torque: float,
        wheel_radius: float,
    ) -> tuple[float, float]:
        """Calculate longitudinal braking force at front and rear wheels."""

        if wheel_radius <= 0:
            raise ValueError(
                "Wheel radius must be positive."
            )

        front_wheel_torque, rear_wheel_torque = (
            self.calculate_wheel_brake_torque(
                total_brake_torque=total_brake_torque,
            )
        )

        front_force = (
            front_wheel_torque / wheel_radius
        )

        rear_force = (
            rear_wheel_torque / wheel_radius
        )

        return front_force, rear_force