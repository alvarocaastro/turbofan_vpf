# Domain Layer

## Purpose

The `domain` folder contains the core physical definitions of the project.
It represents the **conceptual and physical domain** of the problem,
independent of numerical methods, aerodynamic solvers, or CFD tools.

This layer defines *what the problem is*, not *how it is solved*.

In this project, the domain layer provides a rigorous and physically
consistent framework to analyze how **variable blade pitch** affects
aerodynamic incidence and performance in a turbofan fan stage, compared
to a fixed-pitch configuration.

---

## Design Philosophy

The domain layer follows principles commonly adopted in graduate-level and
doctoral research software:

- **Physics-first abstraction**  
  All modules represent real physical concepts used in aerospace
  engineering (flow state, blade kinematics, incidence, operating
  conditions).

- **Separation of concerns**  
  No aerodynamic force models, CFD solvers, or performance calculations
  are implemented here. The domain defines the physical entities that
  higher-level models operate on.

- **Explicit assumptions**  
  All physical quantities are dimensional, and assumptions are made
  explicit to ensure traceability and reproducibility.

- **Solver and model independence**  
  The domain layer is completely independent of CFD, airfoil databases,
  or numerical discretization schemes.

---

## Role in the Variable Pitch Fan Study

The central scientific objective of this project is to evaluate whether
**variable pitch fan blades** can maintain near-optimal aerodynamic
incidence across a wide range of operating conditions.

To enable a rigorous comparison between fixed-pitch and variable-pitch
configurations, the domain layer ensures that:

- Flow conditions are defined consistently for all analyses
- Blade pitch and orientation are introduced explicitly and independently
- Blade incidence is treated as a first-class physical quantity
- Changes in aerodynamic behavior can be directly attributed to pitch
  variation rather than inconsistencies in flow definition

This separation is essential to isolate the aerodynamic benefits of
variable pitch concepts in a scientifically defensible manner.

---

## Module Overview

The `domain` folder currently includes the following modules:

### `atmosphere.py`

Defines atmospheric models and boundary conditions used to derive flow
properties as a function of altitude or flight condition.

This module provides idealized atmospheric representations (e.g. ISA)
and does not perform any aerodynamic or performance calculations.

---

### `flow_state.py`

Defines the **thermodynamic and kinematic state of the airflow**, including
quantities such as pressure, temperature, density, velocity, Mach number,
and Reynolds number.

The flow state is defined independently of blade geometry or pitch and
represents the incoming flow experienced by the fan blade.

---

### `blade_kinematics.py`

Defines the geometric and kinematic orientation of a blade, including
pitch angle, stagger angle, and chord-line orientation.

This module formalizes how blade pitch is represented in the model and
provides the geometric basis for incidence analysis.

---

### `incidence.py`

Provides a formal definition of **blade incidence** as the relative angle
between the incoming flow direction and the blade chord line.

Incidence is treated as a fundamental physical quantity and represents
the key variable through which the aerodynamic impact of variable pitch
is evaluated.

---

### `operating_condition.py`

Defines a complete **operating or flight condition**, linking atmospheric
properties, flow state, and blade kinematics under a consistent physical
context.

This module enables parametric studies across different flight regimes
(e.g. takeoff, climb, cruise) while maintaining a clear separation
between flow definition and blade geometry.

---

### `operating_point.py`

Defines named operating points (e.g. cruise, takeoff, climb) that provide
contextual meaning to operating conditions.

This abstraction is used to label and organize parametric studies without
introducing additional physical modeling assumptions.

---

### `reference_frame.py` (conceptual)

Defines angular reference-frame conventions used in the project. This module
is included for conceptual clarity and future extensibility but is not
actively used in the current 2D sectional analysis.

---
## Typical Use Within the Project

The domain layer is used as the foundation for:

- 2D blade and cascade analyses
- Parametric pitch and incidence sweeps
- Preliminary fan-level studies
- CFD-oriented pre- and post-processing workflows

Higher-level layers of the project consume domain objects to perform
aerodynamic modeling, numerical simulations, and performance evaluation.

---

## What This Layer Does Not Contain

The `domain` folder intentionally excludes:

- Aerodynamic force or moment models
- CFD solvers or turbulence models
- Empirical airfoil databases
- Optimization or performance evaluation routines

These aspects belong to higher-level layers of the project.

---

## Academic Context

This domain structure reflects best practices in scientific and aerospace
engineering software development and is designed to support work at
advanced undergraduate, graduate, and doctoral research levels.
