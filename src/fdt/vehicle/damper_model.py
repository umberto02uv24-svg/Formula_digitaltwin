from dataclasses import dataclass

from fdt.vehicle.parameters import SuspensionParameters


@dataclass(frozen=True)
class DamperForceResult:
    """Damper forces at the front and rear axle."""

    front_force: float
    rear_force: float


class DamperModel:
    """Simplified linear damper model."""

    def __init__(
        self,
        parameters: SuspensionParameters,
    ) -> None:
        self.parameters = parameters

    def _get_damping_coefficients(
        self,
    ) -> tuple[float, float, float, float]:
        """Return front/rear compression and rebound damping."""

        front_compression = (
            self.parameters.front_damping_compression.value
        )
        front_rebound = (
            self.parameters.front_damping_rebound.value
        )
        rear_compression = (
            self.parameters.rear_damping_compression.value
        )
        rear_rebound = (
            self.parameters.rear_damping_rebound.value
        )

        if front_compression is None:
            raise ValueError(
                "Front compression damping is required."
            )

        if front_rebound is None:
            raise ValueError(
                "Front rebound damping is required."
            )

        if rear_compression is None:
            raise ValueError(
                "Rear compression damping is required."
            )

        if rear_rebound is None:
            raise ValueError(
                "Rear rebound damping is required."
            )

        if front_compression < 0:
            raise ValueError(
                "Front compression damping cannot be negative."
            )

        if front_rebound < 0:
            raise ValueError(
                "Front rebound damping cannot be negative."
            )

        if rear_compression < 0:
            raise ValueError(
                "Rear compression damping cannot be negative."
            )

        if rear_rebound < 0:
            raise ValueError(
                "Rear rebound damping cannot be negative."
            )

        return (
            front_compression,
            front_rebound,
            rear_compression,
            rear_rebound,
        )

    def calculate_force(
        self,
        front_velocity: float,
        rear_velocity: float,
    ) -> DamperForceResult:
        """Calculate damper forces from damper velocities."""

        (
            front_compression,
            front_rebound,
            rear_compression,
            rear_rebound,
        ) = self._get_damping_coefficients()

        front_coefficient = (
            front_compression
            if front_velocity >= 0
            else front_rebound
        )

        rear_coefficient = (
            rear_compression
            if rear_velocity >= 0
            else rear_rebound
        )

        front_force = -front_coefficient * front_velocity
        rear_force = -rear_coefficient * rear_velocity

        return DamperForceResult(
            front_force=front_force,
            rear_force=rear_force,
        )

    def calculate_wheel_damping(
        self,
    ) -> tuple[float, float, float, float]:
        """Calculate effective damping coefficients at the wheels."""

        (
            front_compression,
            front_rebound,
            rear_compression,
            rear_rebound,
        ) = self._get_damping_coefficients()

        front_motion_ratio = (
            self.parameters.front_motion_ratio.value
        )
        rear_motion_ratio = (
            self.parameters.rear_motion_ratio.value
        )

        if front_motion_ratio is None:
            raise ValueError(
                "Front motion ratio is required."
            )

        if rear_motion_ratio is None:
            raise ValueError(
                "Rear motion ratio is required."
            )

        if front_motion_ratio <= 0:
            raise ValueError(
                "Front motion ratio must be positive."
            )

        if rear_motion_ratio <= 0:
            raise ValueError(
                "Rear motion ratio must be positive."
            )

        front_ratio_squared = front_motion_ratio**2
        rear_ratio_squared = rear_motion_ratio**2

        return (
            front_compression * front_ratio_squared,
            front_rebound * front_ratio_squared,
            rear_compression * rear_ratio_squared,
            rear_rebound * rear_ratio_squared,
        )