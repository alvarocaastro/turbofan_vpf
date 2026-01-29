"""
Domain layer for the turbofan Variable Pitch Fan (VPF) project.

This package defines the physical, geometric, and contextual abstractions used
to describe operating conditions at a conceptual level.
"""

from .atmosphere import AtmosphereState, isa_atmosphere
from .flow_state import FlowState
from .blade_kinematics import BladeKinematics
from .incidence import compute_incidence
from .operating_condition import OperatingCondition
from .operating_point import OperatingPoint
from .reference_frame import ReferenceFrame

__all__ = [
    "AtmosphereState",
    "isa_atmosphere",
    "FlowState",
    "BladeKinematics",
    "compute_incidence",
    "OperatingCondition",
    "OperatingPoint",
    "ReferenceFrame",
]

