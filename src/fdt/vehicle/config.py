from .parameters import (
    AerodynamicParameters,
    BrakeParameters,
    MassProperties,
    PowertrainParameters,
    SuspensionParameters,
    TireParameters,
    VehicleGeometry,
    VehicleParameters,
)
from .parameter import ConfidenceLevel, EngineeringParameter, ParameterStatus

FDT01_BASELINE_V1 = VehicleParameters(
    geometry=VehicleGeometry(
        wheelbase=2.70,
        front_track=1.50,
        rear_track=1.48,
        ground_clearance=0.050,
        tire_radius=0.280,
    ),

   mass=MassProperties(
    mass=EngineeringParameter(
        value=530.0,
        unit="kg",
        source="F4 benchmark",
        confidence=ConfidenceLevel.MEDIUM,
        status=ParameterStatus.BENCHMARK,
    ),

    front_mass_distribution=EngineeringParameter(
        value=0.45,
        unit="-",
        source="Engineering estimate",
        confidence=ConfidenceLevel.MEDIUM,
        status=ParameterStatus.ESTIMATED,
    ),

    cg_height=EngineeringParameter(
        value=0.300,
        unit="m",
        source="Engineering estimate",
        confidence=ConfidenceLevel.LOW,
        status=ParameterStatus.ESTIMATED,
    ),

    cg_longitudinal_position=EngineeringParameter(
        value=1.485,
        unit="m",
        source="Calculated from wheelbase and mass distribution",
        confidence=ConfidenceLevel.MEDIUM,
        status=ParameterStatus.CALCULATED,
    ),

    cg_lateral_position=EngineeringParameter(
        value=0.0,
        unit="m",
        source="Vehicle symmetry assumption",
        confidence=ConfidenceLevel.HIGH,
        status=ParameterStatus.ESTIMATED,
    ),

    roll_inertia=EngineeringParameter(
        value=None,
        unit="kg*m^2",
        source="TBD",
        confidence=ConfidenceLevel.LOW,
        status=ParameterStatus.TBD,
    ),

    pitch_inertia=EngineeringParameter(
        value=None,
        unit="kg*m^2",
        source="TBD",
        confidence=ConfidenceLevel.LOW,
        status=ParameterStatus.TBD,
    ),

    yaw_inertia=EngineeringParameter(
        value=None,
        unit="kg*m^2",
        source="TBD",
        confidence=ConfidenceLevel.LOW,
        status=ParameterStatus.TBD,
    ),
),

    powertrain=PowertrainParameters(
        maximum_power=130000.0,
        maximum_torque=220.0,
        maximum_engine_speed=10000.0,
        number_of_gears=6,
        final_drive_ratio=3.8,
        drivetrain_efficiency=0.90,
    ),

    aerodynamics=AerodynamicParameters(
        reference_area=0.0,
        drag_coefficient=0.0,
        lift_coefficient=0.0,
        aero_balance=0.0,
    ),

    tires=TireParameters(
        front_width=0.220,
        rear_width=0.260,
        diameter=0.660,
        vertical_stiffness=0.0,
        longitudinal_stiffness=0.0,
        lateral_stiffness=0.0,
        friction_coefficient=0.0,
    ),

    suspension=SuspensionParameters(
        front_type="Double wishbone / pushrod",
        rear_type="Double wishbone / pushrod",
        front_spring_stiffness=0.0,
        rear_spring_stiffness=0.0,
        front_motion_ratio=0.0,
        rear_motion_ratio=0.0,
    ),

    brakes=BrakeParameters(
        front_brake_torque=0.0,
        rear_brake_torque=0.0,
        brake_bias=0.60,
    ),
)