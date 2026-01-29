"""
Aerodynamics layer for the turbofan VPF project.

This package provides two-dimensional airfoil aerodynamic data (polars) and
associated utilities required to map blade incidence angles to aerodynamic
coefficients.

The aerodynamic layer is intentionally decoupled from blade kinematics and
operating conditions to ensure modularity, traceability, and physical clarity.
"""

from .airfoil_polars import (
    AirfoilPolar,
    PolarMeta,
    XFOILRunner,
)

__all__ = [
    "AirfoilPolar",
    "PolarMeta",
    "XFOILRunner",
]

