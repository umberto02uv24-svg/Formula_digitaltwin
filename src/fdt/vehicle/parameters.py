from dataclasses import dataclass


@dataclass
class VehicleParameters:
    """Physical parameters defining the FDT-01 vehicle."""

    # Mass properties
    mass: float
    cg_height: float
    front_mass_distribution: float

    # Geometry
    wheelbase: float
    front_track: float
    rear_track: float

    # Aerodynamics
    reference_area: float
    drag_coefficient: float
    lift_coefficient: float

    # Powertrain
    maximum_power: float
    maximum_torque: float