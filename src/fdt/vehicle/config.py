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
    wheelbase=EngineeringParameter(
        value=2.70,
        unit="m",
        source="F4 benchmark",
        confidence=ConfidenceLevel.MEDIUM,
        status=ParameterStatus.BENCHMARK,
    ),
    front_track=EngineeringParameter(
        value=1.50,
        unit="m",
        source="F4 benchmark",
        confidence=ConfidenceLevel.MEDIUM,
        status=ParameterStatus.BENCHMARK,
    ),
    rear_track=EngineeringParameter(
        value=1.48,
        unit="m",
        source="F4 benchmark",
        confidence=ConfidenceLevel.MEDIUM,
        status=ParameterStatus.BENCHMARK,
    ),
    ground_clearance=EngineeringParameter(
        value=0.050,
        unit="m",
        source="Engineering estimate",
        confidence=ConfidenceLevel.LOW,
        status=ParameterStatus.ESTIMATED,
    ),
    tire_radius=EngineeringParameter(
        value=0.280,
        unit="m",
        source="Engineering estimate",
        confidence=ConfidenceLevel.LOW,
        status=ParameterStatus.ESTIMATED,
    ),
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
    maximum_power=EngineeringParameter(
        value=130000.0,
        unit="W",
        source="F4 benchmark",
        confidence=ConfidenceLevel.MEDIUM,
        status=ParameterStatus.BENCHMARK,
    ),
    maximum_torque=EngineeringParameter(
        value=220.0,
        unit="N*m",
        source="F4 benchmark",
        confidence=ConfidenceLevel.MEDIUM,
        status=ParameterStatus.BENCHMARK,
    ),
    maximum_engine_speed=EngineeringParameter(
        value=10000.0,
        unit="rpm",
        source="Engineering estimate",
        confidence=ConfidenceLevel.LOW,
        status=ParameterStatus.ESTIMATED,
    ),
    number_of_gears=EngineeringParameter(
        value=6,
        unit="-",
        source="F4 benchmark",
        confidence=ConfidenceLevel.HIGH,
        status=ParameterStatus.BENCHMARK,
    ),
    final_drive_ratio=EngineeringParameter(
        value=None,
        unit="-",
        source="TBD",
        confidence=ConfidenceLevel.LOW,
        status=ParameterStatus.TBD,
    ),
    drivetrain_efficiency=EngineeringParameter(
        value=0.90,
        unit="-",
        source="Engineering estimate",
        confidence=ConfidenceLevel.LOW,
        status=ParameterStatus.ESTIMATED,
    ),
),
   aerodynamics=AerodynamicParameters(
    reference_area=EngineeringParameter(
        value=None,
        unit="m^2",
        source="TBD",
        confidence=ConfidenceLevel.LOW,
        status=ParameterStatus.TBD,
    ),
    drag_coefficient=EngineeringParameter(
        value=None,
        unit="-",
        source="TBD",
        confidence=ConfidenceLevel.LOW,
        status=ParameterStatus.TBD,
    ),
    lift_coefficient=EngineeringParameter(
        value=None,
        unit="-",
        source="TBD",
        confidence=ConfidenceLevel.LOW,
        status=ParameterStatus.TBD,
    ),
    aero_balance=EngineeringParameter(
        value=None,
        unit="%",
        source="TBD",
        confidence=ConfidenceLevel.LOW,
        status=ParameterStatus.TBD,
    ),
),

    tires=TireParameters(
    front_width=EngineeringParameter(
        value=0.220,
        unit="m",
        source="FIA F4 technical envelope",
        confidence=ConfidenceLevel.MEDIUM,
        status=ParameterStatus.BENCHMARK,
    ),
    rear_width=EngineeringParameter(
        value=0.260,
        unit="m",
        source="FIA F4 technical envelope",
        confidence=ConfidenceLevel.MEDIUM,
        status=ParameterStatus.BENCHMARK,
    ),
    diameter=EngineeringParameter(
        value=0.660,
        unit="m",
        source="Engineering estimate",
        confidence=ConfidenceLevel.LOW,
        status=ParameterStatus.ESTIMATED,
    ),
    vertical_stiffness=EngineeringParameter(
        value=None,
        unit="N/m",
        source="TBD",
        confidence=ConfidenceLevel.LOW,
        status=ParameterStatus.TBD,
    ),
    longitudinal_stiffness=EngineeringParameter(
        value=None,
        unit="N",
        source="TBD",
        confidence=ConfidenceLevel.LOW,
        status=ParameterStatus.TBD,
    ),
    lateral_stiffness=EngineeringParameter(
        value=None,
        unit="N/rad",
        source="TBD",
        confidence=ConfidenceLevel.LOW,
        status=ParameterStatus.TBD,
    ),
    friction_coefficient=EngineeringParameter(
        value=None,
        unit="-",
        source="TBD",
        confidence=ConfidenceLevel.LOW,
        status=ParameterStatus.TBD,
    ),
),

    suspension=SuspensionParameters(
    front_type=EngineeringParameter(
        value="Double wishbone / pushrod",
        unit="-",
        source="F4 architecture benchmark",
        confidence=ConfidenceLevel.HIGH,
        status=ParameterStatus.BENCHMARK,
    ),
    rear_type=EngineeringParameter(
        value="Double wishbone / pushrod",
        unit="-",
        source="F4 architecture benchmark",
        confidence=ConfidenceLevel.HIGH,
        status=ParameterStatus.BENCHMARK,
    ),
    front_spring_stiffness=EngineeringParameter(
        value=None,
        unit="N/m",
        source="TBD",
        confidence=ConfidenceLevel.LOW,
        status=ParameterStatus.TBD,
    ),
    rear_spring_stiffness=EngineeringParameter(
        value=None,
        unit="N/m",
        source="TBD",
        confidence=ConfidenceLevel.LOW,
        status=ParameterStatus.TBD,
    ),
    front_motion_ratio=EngineeringParameter(
        value=None,
        unit="-",
        source="TBD",
        confidence=ConfidenceLevel.LOW,
        status=ParameterStatus.TBD,
    ),
    rear_motion_ratio=EngineeringParameter(
        value=None,
        unit="-",
        source="TBD",
        confidence=ConfidenceLevel.LOW,
        status=ParameterStatus.TBD,
    ),
),

    brakes=BrakeParameters(
    front_brake_torque=EngineeringParameter(
        value=None,
        unit="N*m",
        source="TBD",
        confidence=ConfidenceLevel.LOW,
        status=ParameterStatus.TBD,
    ),
    rear_brake_torque=EngineeringParameter(
        value=None,
        unit="N*m",
        source="TBD",
        confidence=ConfidenceLevel.LOW,
        status=ParameterStatus.TBD,
    ),
    brake_bias=EngineeringParameter(
        value=0.60,
        unit="-",
        source="Engineering estimate",
        confidence=ConfidenceLevel.MEDIUM,
        status=ParameterStatus.ESTIMATED,
    ),
),
)