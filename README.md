# FDT01 — Formula Digital Twin

A physics-based digital twin of a formula-style race car, built to simulate static and dynamic vehicle. The project targets a **14-DOF vehicle model** as the fidelity level — detailed enough to capture load transfer, tire slip dynamics, and yaw response, without the complexity (and opacity) of a full commercial multibody solver.

> **Status: active development.** The dynamic solver core is functional and validated; suspension-coupled roll/pitch dynamics and a proper differential model are the next milestones. This README reflects the current state honestly, including known simplifications — see [Roadmap](#roadmap).

---

## Why this project

Most of what's publicly written about vehicle dynamics simulation either stays at the level of the simple bicycle model, or jumps straight to "buy CarSim/VI-CarRealTime." This project is an attempt to build the space in between from first principles: a fully modular, from-scratch Python implementation of the physics that a formula car's handling actually depends on — tire slip, load transfer, rigid-body dynamics — with every parameter's source and confidence level tracked explicitly, and every subsystem unit-tested and cross-validated before being wired into the next one.

The end goal is a tool that can answer concrete engineering questions before the car turns a wheel on track: how does brake bias affect corner entry stability, how sensitive is the car to a given aero balance, what does a given suspension stiffness change actually do to load transfer — grounded in a model whose assumptions are visible and traceable, not a black box.

---

## What's implemented

The codebase is organized as one small, focused module per physical subsystem, each independently testable, orchestrated by a top-level dynamic solver.

| Subsystem | Module | What it does |
|---|---|---|
| Aerodynamics | `aero_model.py` | Drag and downforce (front/rear split) from a quasi-static drag/lift coefficient model |
| Powertrain | `powertrain_model.py` | Engine operating point, gear/final-drive ratios, tractive force, power/torque/speed limiting |
| Braking | `brake_model.py` | Brake torque distribution by bias, per-axle and per-wheel torque, system torque limits |
| Tire | `tyre_model.py` | Combined-slip tire model (longitudinal/lateral stiffness, load-sensitive friction, friction-circle saturation) |
| Load transfer | `axle_load_model.py` | Static + acceleration-based dynamic vertical load transfer, front/rear |
| Suspension | `suspension_model.py`, `damper_model.py` | Spring/damper force from wheel displacement and velocity, motion-ratio-corrected wheel rates |
| Wheel kinematics | `wheel_kinematics_model.py` | Per-wheel slip angle and contact-patch velocity from rigid-body motion + steer angle |
| Wheel dynamics | `wheel_dynamics_model.py` | Wheel rotational equation of motion (own angular velocity DOF) and resulting slip ratio |
| Rigid body | `newton_euler_model.py` | Full 6-DOF equations of motion, body-fixed frame |
| Force aggregation | `chassis_loads_model.py` | Combines tire, aero and gravity forces/moments into the net force/moment driving the rigid body |
| **Solver** | `dynamic_vehicle_model.py` | Unifies all of the above into one integrable state vector and closes the simulation loop via `scipy.integrate.solve_ivp` |

Every physical constant lives in `config.py` as an `EngineeringParameter` — value, unit, source, confidence level, and status (estimated / benchmark / calculated / validated). This is a deliberate choice: a simulation is only as trustworthy as its inputs, and it should always be possible to tell, at a glance, which numbers are measured and which are still placeholders.

---

## Architecture

```
Driver inputs (steer, throttle, brake)
            │
            ▼
 ┌─────────────────────────────────────────────────────────┐
 │                 DynamicVehicleModel                      │
 │                                                           │
 │  state → wheel kinematics → slip angle/contact velocity  │
 │        → slip ratio (from wheel spin state)               │
 │        → tire forces (per wheel)                          │
 │        → [fixed-point loop] axle load ↔ longitudinal accel│
 │        → chassis load aggregation (tire + aero + gravity) │
 │        → Newton-Euler 6-DOF → accelerations                │
 │        → wheel spin dynamics → angular accelerations       │
 └─────────────────────────────────────────────────────────┘
            │
            ▼
   scipy.integrate.solve_ivp → integrated vehicle state
```

State vector: `[u, v, r, x, y, yaw, ω_fl, ω_fr, ω_rl, ω_rr]` — body-frame velocities, inertial-frame pose, and the four wheel spin rates.

---

## Roadmap

- [ ] Suspension kinematics module (camber gain, non-linear roll centre) — unlocks active roll/pitch DOF
- [ ] Differential model (open / locked / LSD) — currently a fixed 50/50 rear torque split
- [ ] Ackermann steering geometry — currently both front wheels share one steer angle
- [ ] Quasi-static solver (equilibrium/trim conditions) built on the same subsystem modules
- [ ] Automated test suite (pytest) covering every module
- [ ] Replace placeholder tire, suspension and inertia parameters with test/CAD-derived data

---

## Tech stack

- **Python** — pure standard-library `dataclasses` for typed, immutable data models
- **SciPy** (`solve_ivp`) — numerical integration (RK45 / Radau)
- **NumPy** — array/vector operations in the solver layer
- **FreeCAD** - CAD program with included FEM/CAM workspace
- **OpenFOAM** - Industry standard CFD software
- **Lotus Shark** - Suspension kinematic Tool
---


## About

Built by Umberto as an independent engineering project applying vehicle dynamics theory (Milliken & Milliken, Rajamani) to a from-scratch simulation of a real formula-style car.

Feedback and contributions welcome — open an issue or reach out directly.
