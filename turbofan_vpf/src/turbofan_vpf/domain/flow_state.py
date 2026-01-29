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

#Physical constants (SI units)
GAMMA_AIR = 1.4              # Ratio of specific heats [-]
R_AIR = 287.05               # Specific gas constant for air [J/(kg·K)]

#Definition of dataclass for flow state
@dataclass(frozen=True)
class FlowState:
    """
    Dataclass representing the state of a compressible flow.
    """

    velocity: float              # [m/s]
    flow_angle: float            # [rad]
    static_pressure: float       # [Pa]
    static_temperature: float    # [K]
    density: float               # [kg/m^3]

    #Definition of method to validate physical consistency
    def validate(self) -> None:
        """
        Validate the physical consistency of the flow state.
        """
        if self.velocity < 0.0:
            raise ValueError("Velocity must be non-negative.")
        if self.static_pressure <= 0.0:
            raise ValueError("Static pressure must be positive.")
        if self.static_temperature <= 0.0:
            raise ValueError("Static temperature must be positive.")
        if self.density <= 0.0:
            raise ValueError("Density must be positive.")

    #Definition of property to calculate Mach number
    @property
    def mach_number(self) -> float:
        """
        Returns the Mach number of the flow.
        """
        speed_of_sound = math.sqrt(GAMMA_AIR * R_AIR * self.static_temperature)
        return self.velocity / speed_of_sound

    #Definition of property to calculate total temperature
    @property
    def total_temperature(self) -> float:
        """
        Returns the total (stagnation) temperature assuming isentropic flow.
        """
        return self.static_temperature * (
            1.0 + (GAMMA_AIR - 1.0) / 2.0 * self.mach_number**2
        )

    #Definition of property to calculate total pressure
    @property
    def total_pressure(self) -> float:
        """
        Returns the total (stagnation) pressure assuming isentropic flow.
        """
        return self.static_pressure * (
            1.0 + (GAMMA_AIR - 1.0) / 2.0 * self.mach_number**2
        ) ** (GAMMA_AIR / (GAMMA_AIR - 1.0))

    def reynolds_number(
        self,
        characteristic_length: float,
        dynamic_viscosity: float,
    ) -> float:
        """
        Computes the Reynolds number based on a characteristic length.

        Args:
            characteristic_length: Reference length [m].
            dynamic_viscosity: Dynamic viscosity [Pa·s].

        Returns:
            Reynolds number [-].
        """
        if characteristic_length <= 0.0:
            raise ValueError("Characteristic length must be positive.")
        if dynamic_viscosity <= 0.0:
            raise ValueError("Dynamic viscosity must be positive.")

        return (
            self.density * self.velocity * characteristic_length
            / dynamic_viscosity
        )