# FDT-01 Vehicle Baseline

## 1. Purpose

FDT-01 is the baseline vehicle configuration of the FormulaCarDigitalTwin project.

The vehicle is conceptually based on a Formula 4 architecture and is designed to provide a scalable platform for future performance evolution.

The baseline is intended for modelling, simulation, optimization and future physical development.

---

## 2. Vehicle Architecture

### Vehicle type

Formula-style single-seater race car.

### Baseline category

Formula 4 inspired.

### Layout

- Open-wheel
- Single-seat
- Rear-engine/Mid-engine architecture to be defined
- Rear-wheel drive
- Longitudinal powertrain

---

## 3. Target Performance

The initial vehicle is not optimized for maximum performance.

The baseline shall provide a realistic starting point for future development.

Target performance parameters include:

- Vehicle mass
- Power
- Power-to-weight ratio
- Maximum speed
- 0–100 km/h acceleration
- Braking performance
- Cornering performance
- Lap time

Exact target values will be defined after the initial vehicle parameter study.

---

## 4. Vehicle Parameters

The following parameters shall be defined:

### Geometry

- Wheelbase
- Front track
- Rear track
- Overall length
- Overall width
- Overall height
- Tire diameter
- Ground clearance

### Mass properties

- Total mass
- Front/rear weight distribution
- Center of gravity position
- Center of gravity height
- Roll inertia
- Pitch inertia
- Yaw inertia

### Powertrain

- Maximum power
- Maximum torque
- Engine speed range
- Gear ratios
- Final drive ratio
- Differential characteristics

### Tires

- Tire dimensions
- Tire vertical stiffness
- Longitudinal stiffness
- Lateral stiffness
- Friction coefficient
- Load sensitivity

### Aerodynamics

- Drag coefficient
- Lift/downforce coefficient
- Aerodynamic balance
- Reference area

### Suspension

- Suspension type
- Spring stiffness
- Damper characteristics
- Anti-roll bar stiffness
- Motion ratio
- Camber characteristics
- Toe characteristics

---

## 5. Performance Evolution

The FDT-01 architecture shall allow future vehicle configurations to be developed without modifying the fundamental software architecture.

Possible evolution paths include:

### FDT-01 Base

Baseline Formula 4 configuration.

### FDT-01R

Revised mechanical configuration.

Possible changes:

- Suspension
- Tires
- Weight distribution
- Chassis stiffness

### FDT-01A

Aerodynamic development configuration.

Possible changes:

- Front wing
- Rear wing
- Floor
- Diffuser
- Aerodynamic balance

### FDT-01P

Powertrain development configuration.

Possible changes:

- Engine
- Gearbox
- Final drive
- Power delivery

### FDT-01X

High-performance evolution combining multiple developments.
Possible hybrid config

---

## 6. Design Philosophy

The baseline vehicle shall prioritize:

1. Model transparency
2. Physical consistency
3. Modularity
4. Validation capability
5. Manufacturability
6. Performance scalability

The objective is not to create the fastest possible virtual vehicle immediately.

The objective is to create a physically consistent vehicle model that can progressively evolve toward a manufacturable vehicle.