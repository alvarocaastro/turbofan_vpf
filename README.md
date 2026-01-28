# Variable Pitch Fan (VPF) Turbofan — TFG Repository

## Project context
This repository supports a Final Degree Project (TFG) in Aerospace Engineering focused on
variable pitch fan (VPF) turbofan analysis. It is intended for academic research, exploratory
analysis, and reproducible documentation of assumptions, models, and results.

## Purpose
The codebase provides a lightweight Python toolchain for:
- Aerodynamic blade loading estimates
- Incidence and pitch variation sweeps
- Preliminary cycle performance calculations
- CFD pre-processing placeholders

## Scope and limitations
- Models are intentionally simplified for early-stage research and educational use.
- Results are not validated for certification or industrial design decisions.
- CFD workflows are placeholders and require dedicated solvers and meshes.

## Tools and technologies
- Python 3.10+
- NumPy for numerical routines
- Pytest, Ruff, and MyPy for development hygiene
- GitHub Actions for continuous integration

## Constraints
- The repository is organized with separate branches for stable code (`main`) and
  documentation/configuration (`settings`).
- Documentation lives only in the `settings` branch.
- Data and results are tracked only as empty placeholders to preserve structure.

## Usage
Clone the repository and switch branches depending on the content you need:

```bash
git switch main       # Code and tests
```

```bash
git switch settings   # Documentation and repository setup
```
