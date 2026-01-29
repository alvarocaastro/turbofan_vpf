# Domain Layer

## Purpose

The `domain` folder contains the core physical and conceptual definitions
of the project. It represents the **problem domain**, independent of any
numerical method, aerodynamic model, or CFD implementation.

This layer defines *what the problem is*, not *how it is solved*.

In the context of this project, the domain layer provides a rigorous and
consistent physical framework to study the aerodynamic implications of
Variable Pitch Fan (VPF) concepts compared to fixed-pitch configurations.

---

## Design Philosophy

The domain layer follows these fundamental principles:

- **Physics-first design**  
  All entities represent real physical concepts used in aerospace
  engineering (flow state, blade kinematics, incidence).

- **Separation of concerns**  
  Domain objects do not perform detailed aerodynamic or CFD calculations.
  They define the physical state and relationships required by higher-level
  models.

- **Immutability and clarity**  
  Domain objects are designed to be immutable or explicitly transformed,
  ensuring reproducibility and traceability of results.

- **Solver independence**  
  No dependency on CFD solvers, meshing tools, or numerical discretization
  schemes is allowed in this layer.

---

## Role in the Variable Pitch Fan Study

The central scientific objective of this project is to evaluate how
variable blade pitch can maintain optimal aerodynamic incidence across
different flight conditions.

To achieve this, the domain layer ensures that:

- The **flow conditions** are defined consistently for all analyses
- The **blade pitch variation** is introduced explicitly and independently
- Changes in aerodynamic performance can be directly linked to variations
  in blade incidence rather than changes in flow definition

This approach enables a rigorous comparison between fixed-pitch and
variable-pitch fan configurations under identical operating conditions.

---

## Typical Contents

The `domain` folder typically includes:

- `flow_state.py`  
  Definition of the thermodynamic and kinematic state of the airflow.

- `blade_kinematics.py`  
  Description of blade pitch, stagger, and geometric orientation.

- `reference_frames.py` (future extension)  
  Definitions for absolute and relative frames of reference.

Each module is designed to be reusable across multiple analyses, including
2D blade studies, cascade analyses, and preliminary fan-level models.

---

## What This Layer Does Not Contain

- CFD solvers or turbulence models
- Empirical airfoil data
- Numerical optimization routines
- Geometry generation

These aspects are intentionally delegated to higher-level layers of the
project.

---

## Academic Context

This structure reflects best practices in scientific software development
and is commonly adopted in graduate-level and doctoral research to ensure
clarity, extensibility, and physical rigor.
