"""
Module: flow_state
------------------

This module defines the thermodynamic and kinematic state of a compressible
flow as experienced by an aerodynamic component.

The purpose of this module is to represent the flow conditions independently
of blade geometry, pitch setting, or aerodynamic models. It provides a clean
and physically consistent description of velocity, Mach number, Reynolds
number, and total flow properties.

In the context of this project, the flow state acts as an intermediate layer
between the atmospheric environment and blade-level analyses. This separation
is essential to isolate the aerodynamic effects of variable blade pitch from
changes in external flow conditions.

This module follows standard aerospace engineering conventions and is intended
for preliminary and conceptual analyses.

This module does NOT:
- Define blade geometry or pitch
- Perform aerodynamic force calculations
- Depend on CFD solvers or numerical discretization
"""

#Imports
from __future__ import annotations
from dataclasses import dataclass
import math
from turtle import speed

from turbofan_vpf.src.turbofan_vpf.domain.atmosphere import speed_of_sound

#Physical constants (SI units)
GAMMA_AIR = 1.4              # Ratio of specific heats [-]
R_AIR = 287.05               # Specific gas constant for air [J/(kg·K)]

#Definition of dataclass for flow state
@dataclass(frozen=True)      # Immutable dataclass for flow state
class FlowState:
    """
    Dataclass representing the state of a compressible flow.

    Attributes:
        velocity (float): Flow speed magnitude [m/s].
        flow_angle (float): Absolute flow direction [rad].
        static_pressure (float): Static pressure [Pa].
        static_temperature (float): Static temperature [K].
        density (float): Flow density [kg/m^3].
    """
    velocity: float              # [m/s]
    flow_angle: float            # [rad]
    static_pressure: float       # [Pa]
    static_temperature: float    # [K]
    density: float               # [kg/m^3]

#Definition of a physical validation for flow state
def validate(self) -> None:
    """
    Validate the physical consistency of the flow state.

    Raises:
        ValueError: If any physical property is out of realistic bounds.
    """
    if self.velocity < 0.0:
        raise ValueError("Velocity must be non-negative.")
    if self.static_pressure <= 0.0:
        raise ValueError("Static pressure must be positive.")
    if self.static_temperature <= 0.0:
        raise ValueError("Static temperature must be positive.")
    if self.density <= 0:
        raise ValueError("Density must be positive.")
    
#Definition of property to calculate Mach number
@property
def mach_number(self) -> float:
    """
    Calculate the Mach number of the flow.

    Returns:
        float: Mach number [-].
    """
    speed_of_sound = math.sqrt(GAMMA_AIR * R_AIR * self.static_temperature)
    return self.velocity / speed_of_sound

#Definition of property to calculate total temperature
@property
def total_temperature(self) -> float:
    """
    Calculate the total (stagnation) temperature assuming isoentropic flow.

    Returns:
        float: Total temperature [K].
    """
    return self.static_temperature * (
        1.0 + (GAMMA_AIR - 1.0) / 2.0 * self.mach_number ** 2
    )

#Definition of property to calculate total pressure
@property
def total_pressure(self) -> float:
    """
    Calculate the total (stagnation) pressure assuming isoentropic flow.

    Returns:
        float: Total pressure [Pa].
    """
    return self.static_pressure * (
        1.0 + (GAMMA_AIR - 1.0) / 2.0 * self.mach_number ** 2
    ) ** (GAMMA_AIR / (GAMMA_AIR - 1.0))

#Definition of property to calculate Reynolds number based on a characteristic length
@property
def reynolds_number(self, characteristic_length: float, dynamic_viscosity: float) -> float:
    """
    Calculate the Reynolds number based on a characteristic length.

    Args:
        characteristic_length (float): Characteristic length [m].

    Returns:
        float: Reynolds number [-].
    """
    if characteristic_length <= 0.0:
        raise ValueError("Characteristic length must be positive.")

    return (self.density * self.velocity * characteristic_length / dynamic_viscosity)