from dataclasses import dataclass
from math import pi

from fdt.vehicle.parameters import PowertrainParameters


@dataclass(frozen=True)
class EngineOperatingPoint:
    """Engine operating point."""

    engine_speed_rpm: float
    engine_torque: float
    engine_power: float


class PowertrainModel:
    """Simplified engine operating point model."""

    def __init__(
        self,
        parameters: PowertrainParameters,
    ) -> None:
        self.parameters = parameters

    def calculate_engine_power(
        self,
        engine_speed_rpm: float,
        engine_torque: float,
    ) -> float:
        """Calculate engine power from speed and torque."""

        if engine_speed_rpm < 0:
            raise ValueError(
                "Engine speed cannot be negative."
            )

        if engine_torque < 0:
            raise ValueError(
                "Engine torque cannot be negative."
            )

        angular_speed = (
            2.0
            * pi
            * engine_speed_rpm
            / 60.0
        )

        return engine_torque * angular_speed

    def calculate_operating_point(
        self,
        engine_speed_rpm: float,
        engine_torque: float,
    ) -> EngineOperatingPoint:
        """Calculate the engine operating point."""

        engine_power = self.calculate_engine_power(
            engine_speed_rpm=engine_speed_rpm,
            engine_torque=engine_torque,
        )

        return EngineOperatingPoint(
            engine_speed_rpm=engine_speed_rpm,
            engine_torque=engine_torque,
            engine_power=engine_power,
        )
    def limit_engine_operating_point(
    self,
    engine_speed_rpm: float,
    engine_torque: float,
    ) -> EngineOperatingPoint:
        """Limit engine operating point according to powertrain limits."""

        if engine_speed_rpm < 0:
            raise ValueError(
                "Engine speed cannot be negative."
            )

        if engine_torque < 0:
            raise ValueError(
                "Engine torque cannot be negative."
            )

        maximum_torque = self.parameters.maximum_torque.value
        maximum_power = self.parameters.maximum_power.value
        maximum_engine_speed = (
            self.parameters.maximum_engine_speed.value
        )

        if maximum_torque is None:
            raise ValueError(
                "Maximum engine torque is required."
            )

        if maximum_power is None:
            raise ValueError(
                "Maximum engine power is required."
            )

        if maximum_engine_speed is None:
            raise ValueError(
                "Maximum engine speed is required."
            )

        if maximum_torque <= 0:
            raise ValueError(
                "Maximum engine torque must be positive."
            )

        if maximum_power <= 0:
            raise ValueError(
                "Maximum engine power must be positive."
            )

        if maximum_engine_speed <= 0:
            raise ValueError(
                "Maximum engine speed must be positive."
            )

        limited_speed = min(
            engine_speed_rpm,
            maximum_engine_speed,
        )

        torque_limit_from_power = float("inf")

        if limited_speed > 0:
            angular_speed = (
                2.0
                * pi
                * limited_speed
                / 60.0
            )

            torque_limit_from_power = (
                maximum_power
                / angular_speed
            )

        limited_torque = min(
            engine_torque,
            maximum_torque,
            torque_limit_from_power,
        )

        return EngineOperatingPoint(
            engine_speed_rpm=limited_speed,
            engine_torque=limited_torque,
            engine_power=self.calculate_engine_power(
                engine_speed_rpm=limited_speed,
                engine_torque=limited_torque,
            ),
        )
    
    def calculate_gear_ratio(
    self,
    gear: int,
    ) -> float:
        """Return the selected gear ratio."""

        gear_ratios = self.parameters.gear_ratios.value
        number_of_gears = self.parameters.number_of_gears.value

        if not isinstance(gear_ratios, list):
            raise ValueError(
                "Gear ratios must be provided as a list."
            )

        if gear < 1 or gear > number_of_gears:
            raise ValueError(
                "Selected gear is outside the available gears."
            )

        if len(gear_ratios) != number_of_gears:
            raise ValueError(
                "Number of gear ratios must match number of gears."
            )

        return gear_ratios[gear - 1]
    def calculate_wheel_speed(
    self,
    engine_speed_rpm: float,
    gear: int,
    ) -> float:
        """Calculate wheel speed from engine speed and gearing."""

        gear_ratio = self.calculate_gear_ratio(gear)

        final_drive_ratio = self.parameters.final_drive_ratio.value

        if final_drive_ratio is None:
            raise ValueError(
                "Final drive ratio is required."
            )

        if final_drive_ratio <= 0:
            raise ValueError(
                "Final drive ratio must be positive."
            )

        return (
            engine_speed_rpm
            / (gear_ratio * final_drive_ratio)
        )
    def calculate_wheel_torque(
    self,
    engine_torque: float,
    gear: int,
    ) -> float:
        """Calculate wheel torque after gearbox and final drive."""

        gear_ratio = self.calculate_gear_ratio(gear)

        final_drive_ratio = self.parameters.final_drive_ratio.value
        drivetrain_efficiency = (
            self.parameters.drivetrain_efficiency.value
        )

        if final_drive_ratio is None:
            raise ValueError(
                "Final drive ratio is required."
            )

        if final_drive_ratio <= 0:
            raise ValueError(
                "Final drive ratio must be positive."
            )

        if drivetrain_efficiency is None:
            raise ValueError(
                "Drivetrain efficiency is required."
            )

        if not 0 < drivetrain_efficiency <= 1:
            raise ValueError(
                "Drivetrain efficiency must be between 0 and 1."
            )

        return (
            engine_torque
            * gear_ratio
            * final_drive_ratio
            * drivetrain_efficiency
        )
    def calculate_tractive_force(
    self,
    engine_torque: float,
    gear: int,
    wheel_radius: float,
    ) -> float:
        """Calculate longitudinal tractive force at the driven wheels."""

        if wheel_radius <= 0:
            raise ValueError(
                "Wheel radius must be positive."
            )

        wheel_torque = self.calculate_wheel_torque(
            engine_torque=engine_torque,
            gear=gear,
        )

        return wheel_torque / wheel_radius


