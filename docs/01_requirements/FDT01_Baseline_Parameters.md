# FDT-01 Baseline Parameters

## 1. Purpose

This document defines the baseline physical parameters of the FDT-01 vehicle.

Each parameter is associated with:

- value
- unit
- source
- confidence level
- status

The objective is to maintain traceability between requirements, assumptions, models and future experimental data.

---

## 2. Parameter Status

The following status categories are used:

- TBD: value not yet defined
- Estimated: engineering estimate
- Benchmark: derived from reference vehicles
- Calculated: obtained from another model or parameter
- Validated: supported by experimental data

---

## 3. Vehicle Geometry

| Parameter | Symbol | Value | Unit | Source | Confidence | Status |
|---|---|---:|---|---|---|---|
| Wheelbase | L | 2.70 | m | F4 benchmark | Medium | TBD |
| Front track | Tf | 1.50 | m | F4 benchmark | Medium | TBD |
| Rear track | Tr | 1.48 | m | F4 benchmark | Medium | TBD |
| Overall length | Ltot | TBD | m | F4 benchmark | Medium | TBD |
| Overall width | Wtot | TBD | m | F4 benchmark | Medium | TBD |
| Overall height | Htot | TBD | m | F4 benchmark | Medium | TBD |
| Ground clearance | hGC | 0.05 | m | Engineering estimate | Low | TBD |
| Tire radius | Rw | TBD | m | Tire specification | Medium | TBD |

---

## 4. Mass Properties

| Parameter | Symbol | Value | Unit | Source | Confidence | Status |
|---|---|---:|---|---|---|---|
| Vehicle mass | m | 530 | kg | Requirement | Medium | TBD |
| Front mass distribution | λf | 0.45 | - | Engineering estimate | Medium | TBD |
| CG height | 0.3 | TBD | m | Engineering estimate | Low | TBD |
| CG longitudinal position | xCG | TBD | m | Calculated | Low | TBD |
| CG lateral position | yCG | TBD | m | Assumption | High | TBD |
| Roll inertia | Ixx | TBD | kg m² | Calculated | Low | TBD |
| Pitch inertia | Iyy | TBD | kg m² | Calculated | Low | TBD |
| Yaw inertia | Izz | TBD | kg m² | Calculated | Low | TBD |

---

## 5. Powertrain

| Parameter | Symbol | Value | Unit | Source | Confidence | Status |
|---|---|---:|---|---|---|---|
| Maximum power | Pmax | 130 | kW | F4 benchmark | Medium | TBD |
| Maximum torque | Tmax | 220 | Nm | F4 benchmark | Medium | TBD |
| Maximum engine speed | nmax | TBD | rpm | Engine specification | Medium | TBD |
| Number of gears | Ngear | 6 | - | Architecture | High | TBD |
| Final drive ratio | if | TBD | - | Engineering estimate | Low | TBD |
| Drivetrain efficiency | η | TBD | - | Engineering estimate | Low | TBD |

---

## 6. Aerodynamics

| Parameter | Symbol | Value | Unit | Source | Confidence | Status |
|---|---|---:|---|---|---|---|
| Reference area | A | TBD | m² | Geometry | Medium | TBD |
| Drag coefficient | Cd | TBD | - | Aero estimate | Low | TBD |
| Lift coefficient | Cl | TBD | - | Aero estimate | Low | TBD |
| Aero balance | BA | TBD | % | Aero estimate | Low | TBD |

---

## 7. Tires

| Parameter | Symbol | Value | Unit | Source | Confidence | Status |
|---|---|---:|---|---|---|---|
| Front tire width | Wf | 220 | mm | Tire specification | Medium | TBD |
| Rear tire width | Wr | 260 | mm | Tire specification | Medium | TBD |
| Tire diameter | D | 330.2 | mm | Tire specification | Medium | TBD |
| Tire vertical stiffness | Cz | TBD | N/m | Estimate | Low | TBD |
| Longitudinal stiffness | Cx | TBD | N | Estimate | Low | TBD |
| Lateral stiffness | Cy | TBD | N/rad | Estimate | Low | TBD |
| Friction coefficient | μ | TBD | - | Estimate | Low | TBD |

---

## 8. Suspension

| Parameter | Symbol | Value | Unit | Source | Confidence | Status |
|---|---|---:|---|---|---|---|
| Front suspension type | - | TBD | - | Architecture | High | TBD |
| Rear suspension type | - | TBD | - | Architecture | High | TBD |
| Front spring stiffness | Ksf | TBD | N/m | Estimate | Low | TBD |
| Rear spring stiffness | Ksr | TBD | N/m | Estimate | Low | TBD |
| Front motion ratio | MRf | TBD | - | Geometry | Medium | TBD |
| Rear motion ratio | MRr | TBD | - | Geometry | Medium | TBD |

---

## 9. Brakes

| Parameter | Symbol | Value | Unit | Source | Confidence | Status |
|---|---|---:|---|---|---|---|
| Front brake torque limit | Tbf | TBD | Nm | Estimate | Low | TBD |
| Rear brake torque limit | Tbr | TBD | Nm | Estimate | Low | TBD |
| Brake bias | β | TBD | % | Architecture | Medium | TBD |

---

## 10. Validation Priority

Parameters shall be progressively upgraded from estimated to validated values.

Priority shall be given to parameters with the highest influence on vehicle performance.

Initial validation priority:

1. Vehicle mass
2. Center of gravity position
3. Tire characteristics
4. Powertrain torque curve
5. Aerodynamic coefficients
6. Suspension characteristics
7. Vehicle inertias

---

## 11. Traceability

Every parameter used by the simulation shall ultimately be traceable to one of the following:

- Design requirement
- Manufacturer specification
- Reference vehicle
- Engineering calculation
- Experimental measurement
- Validated simulation