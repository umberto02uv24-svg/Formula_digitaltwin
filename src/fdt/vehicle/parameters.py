from dataclasses import dataclass

from fdt.vehicle.parameter import EngineeringParameter


@dataclass
class VehicleGeometry:
    """Geometric parameters of the vehicle."""

    wheelbase: EngineeringParameter
    front_track: EngineeringParameter
    rear_track: EngineeringParameter
    ground_clearance: EngineeringParameter
    tire_radius: EngineeringParameter


@dataclass
class MassProperties:
    """Mass and inertia properties of the vehicle."""

    mass: EngineeringParameter
    front_mass_distribution: EngineeringParameter
    cg_height: EngineeringParameter
    cg_longitudinal_position: EngineeringParameter
    cg_lateral_position: EngineeringParameter
    roll_inertia: EngineeringParameter
    pitch_inertia: EngineeringParameter
    yaw_inertia: EngineeringParameter


@dataclass
class PowertrainParameters:
    """Powertrain parameters."""

    maximum_power: EngineeringParameter
    maximum_torque: EngineeringParameter
    maximum_engine_speed: EngineeringParameter
    number_of_gears: EngineeringParameter
    final_drive_ratio: EngineeringParameter
    drivetrain_efficiency: EngineeringParameter


@dataclass
class AerodynamicParameters:
    """Aerodynamic parameters."""

    reference_area: EngineeringParameter
    drag_coefficient: EngineeringParameter
    lift_coefficient: EngineeringParameter
    aero_balance: EngineeringParameter


@dataclass
class TireParameters:
    """Tire parameters."""

    front_width: EngineeringParameter
    rear_width: EngineeringParameter
    diameter: EngineeringParameter
    vertical_stiffness: EngineeringParameter
    longitudinal_stiffness: EngineeringParameter
    lateral_stiffness: EngineeringParameter
    friction_coefficient: EngineeringParameter


@dataclass
class SuspensionParameters:
    """Suspension parameters."""

    front_type: EngineeringParameter
    rear_type: EngineeringParameter
    front_spring_stiffness: EngineeringParameter
    rear_spring_stiffness: EngineeringParameter
    front_motion_ratio: EngineeringParameter
    rear_motion_ratio: EngineeringParameter


@dataclass
class BrakeParameters:
    """Brake system parameters."""

    front_brake_torque: EngineeringParameter
    rear_brake_torque: EngineeringParameter
    brake_bias: EngineeringParameter


@dataclass
class VehicleParameters:
    """Complete parameter set defining a vehicle configuration."""

    geometry: VehicleGeometry
    mass: MassProperties
    powertrain: PowertrainParameters
    aerodynamics: AerodynamicParameters
    tires: TireParameters
    suspension: SuspensionParameters
    brakes: BrakeParameters