# FDT-01 System Architecture

## 1. Purpose

This document defines the software and data architecture of the FormulaCarDigitalTwin project.

The architecture is designed to support the progressive development of a complete digital twin of a Formula-style race car.

---

## 2. Design Principles

The system follows the following principles:

- Modularity
- Reusability
- Separation of data and models
- Testability
- Traceability
- Scalability
- Validation-driven development

---

## 3. System Layers

### 3.1 Data Layer

The data layer contains all physical and configuration parameters required by the models.

Examples:

- Vehicle parameters
- Tire data
- Engine data
- Track data
- Material properties

---

### 3.2 Model Layer

The model layer implements the physical models of the vehicle.

Main subsystems:

- Vehicle
- Tires
- Powertrain
- Suspension
- Aerodynamics
- Vehicle Dynamics

---

### 3.3 Simulation Layer

The simulation layer combines the physical models to perform vehicle-level simulations.

Main simulations:

- Acceleration
- Braking
- Steady-state cornering
- Transient handling
- Lap time

---

### 3.4 Optimization Layer

The optimization layer modifies vehicle parameters to improve selected performance metrics.

Examples:

- Lap time
- Vehicle mass
- Downforce
- Tire utilization
- Powertrain efficiency

---

### 3.5 Validation Layer

The validation layer compares simulation results against:

- Analytical solutions
- Published data
- Benchmark vehicles
- Experimental measurements

---

## 4. Data Flow

The general data flow is:

Data
→ Vehicle Model
→ Subsystem Models
→ Vehicle Dynamics
→ Simulation
→ Results
→ Validation

---

## 5. Software Architecture

The main Python package is:

`src/fdt`

with the following modules:

- `vehicle`
- `tires`
- `powertrain`
- `suspension`
- `aerodynamics`
- `dynamics`
- `simulation`
- `optimization`
- `io`
- `utils`

---

## 6. Versioning

The baseline vehicle is identified as:

FDT-01 Base

Future configurations include:

- FDT-01R
- FDT-01A
- FDT-01X

---

## 7. Development Strategy

Development will proceed from low-complexity models toward progressively more detailed models.

The initial implementation will use simplified analytical models.

These models will progressively be replaced or extended with higher-fidelity models as validation data becomes available.