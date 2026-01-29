"""
Domain layer for the turbofan Variable Pitch Fan (VPF) project.

This package defines the physical and geometric abstractions used to describe
the operating conditions of the fan at a conceptual level.
"""

from .atmosphere import AtmosphereState, isa_atmosphere
from .flow_state import FlowState
from .blade_kinematics import BladeKinematics
from .incidence import compute_incidence
from .operating_condition import OperatingCondition

__all__ = [
    "AtmosphereState",
    "isa_atmosphere",
    "FlowState",
    "BladeKinematics",
    "compute_incidence",
    "OperatingCondition",
]
