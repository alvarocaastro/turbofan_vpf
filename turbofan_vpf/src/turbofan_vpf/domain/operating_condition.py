"""
Module: operating_condition
----------------------------

This module defines an operating condition as the combination of atmospheric
environment, flow state, and blade kinematics.

An operating condition represents a complete and self-consistent case for
sectional fan-blade analysis, serving as the reference point for incidence
evaluation and subsequent aerodynamic studies.

This module does NOT perform aerodynamic or performance calculations.
"""

from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Optional

from .atmosphere import AtmosphereState
from .flow_state import FlowState
from .blade_kinematics import BladeKinematics
from .incidence import compute_incidence
from .operating_point import OperatingPoint

@dataclass(frozen=True)
class OperatingCondition:
    """
    Represents a complete operating condition for sectional fan-blade analysis.

    Attributes:
    -----------
    atmosphere : AtmosphereState
        The atmospheric environment state.
    flow_state : FlowState
        The flow state at the blade.
    blade_kinematics : BladeKinematics
        The kinematic properties of the blade.
    """

    atmosphere: AtmosphereState
    flow_state: FlowState
    blade_kinematics: BladeKinematics

    # Optional association to a named operating point
    operating_point: Optional[OperatingPoint] = None

    # Definition of a global physical consistency check for the operating
    # condition
    def validate(self) -> None:
        """
        Validates the physical consistency of the operating condition.

        Raises:
        -------
        ValueError
            If any of the attributes are not physically consistent.
        """
        self.atmosphere.validate()
        self.flow_state.validate()
        self.blade_kinematics.validate()

    # Definitio of blade incidence for the current operating condition
    @property
    def incidence(self) -> float:
        """
        Computes the blade incidence angle for the current operating condition.

        Returns:
        --------
        float
            The blade incidence angle in radians.
        """
        return compute_incidence(self.flow_state, self.blade_kinematics)

    # Definition of blade incidence in degrees
    @property
    def incidence_deg(self) -> float:
        """
        Computes the blade incidence angle for the current operating condition in degrees.

        Returns:
        --------
        float
            The blade incidence angle in degrees.
        """
        return math.degrees(self.incidence)
    
    #Definition of the local mach number for the operating condition
    @property
    def mach_number(self) -> float:
        """
        Computes the local Mach number for the current operating condition.

        Returns:
        --------
        float
            The local Mach number.
        """
        return self.flow_state.mach_number

    #Definition of the Reynolds number based on a characteristic length
    def reynolds_number(self, characteristic_length: float) -> float:
        """
        Computes the Reynolds number for the current operating condition.

        Returns:
        --------
        float
            The Reynolds number.
        """
        return self.flow_state.reynolds_number(
            characteristic_length=characteristic_length,
            dynamic_viscosity=self.atmosphere.dynamic_viscosity
        )