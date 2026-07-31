from .parameters import VehicleParameters


FDT01_BASELINE = VehicleParameters(
    mass=500.0,
    cg_height=0.30,
    front_mass_distribution=0.45,

    wheelbase=2.60,
    front_track=1.50,
    rear_track=1.45,

    reference_area=1.20,
    drag_coefficient=0.80,
    lift_coefficient=-1.50,

    maximum_power=118000.0,
    maximum_torque=190.0,
)