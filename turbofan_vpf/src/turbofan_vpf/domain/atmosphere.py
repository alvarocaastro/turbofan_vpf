"""
Module: atmosphere
------------------

This module defines idealized atmospheric models used to describe the
external environment in which the aerodynamic analysis is performed.

Its purpose is to provide physically consistent atmospheric properties
(temperature, pressure, density, speed of sound) as a function of altitude,
independent of any aerodynamic body, blade geometry, or propulsion model.

In the context of this project, the atmosphere represents a boundary
condition from which the flow state is derived. This separation ensures
that changes in aerodynamic behavior can be traced back to blade pitch
variation rather than inconsistencies in environmental assumptions.

This module follows standard aerospace engineering conventions and is
intended for preliminary and conceptual analyses, not for high-fidelity
atmospheric modeling.

This module does NOT:
- Perform aerodynamic or performance calculations
- Depend on blade geometry or pitch
- Include CFD-specific assumptions
"""

from __future__ import annotations
from dataclasses import dataclass
import math


# Physical constants (SI units)
GAMMA_AIR = 1.4              # Ratio of specific heats [-]
R_AIR = 287.05               # Specific gas constant for air [J/(kg·K)]
G0 = 9.80665                 # Gravitational acceleration [m/s^2]

# Validity limits for the implemented ISA model
TROPOSPHERE_LIMIT = 11_000.0  # [m]


@dataclass(frozen=True)
class AtmosphereState:
    """
    Dataclass representing the state of the atmosphere at a given altitude.
    """

    altitude: float         # [m]
    temperature: float      # [K]
    pressure: float         # [Pa]
    density: float          # [kg/m^3]

    # Definition of physical consistency validation
    def validate(self) -> None:
        if self.altitude < 0.0:
            raise ValueError("Altitude must be non-negative.")
        if self.temperature <= 0.0:
            raise ValueError("Temperature must be positive.")
        if self.pressure <= 0.0:
            raise ValueError("Pressure must be positive.")
        if self.density <= 0.0:
            raise ValueError("Density must be positive.")

    # Definition of speed of sound
    @property
    def speed_of_sound(self) -> float:
        return math.sqrt(GAMMA_AIR * R_AIR * self.temperature)

    # Definition of dynamic viscosity using Sutherland's law
    @property
    def dynamic_viscosity(self) -> float:
        T_ref = 273.15      # [K]
        mu_ref = 1.716e-5   # [Pa·s]
        S = 110.4           # [K]

        return mu_ref * (self.temperature / T_ref) ** 1.5 * (
            (T_ref + S) / (self.temperature + S)
        )


# Definition of ISA atmosphere model (troposphere only)
def isa_atmosphere(altitude: float) -> AtmosphereState:
    """
    Computes the International Standard Atmosphere (ISA) properties for the
    troposphere (up to 11 km).

    References:
    - ISO 2533:1975: Standard Atmosphere
    - Anderson, J.D., Introduction to Flight, 7th Edition, McGraw-Hill, 2005.
    """
    if not 0.0 <= altitude <= TROPOSPHERE_LIMIT:
        raise ValueError(
            "ISA model implemented is valid only for altitudes between "
            "0 m and 11 km (troposphere)."
        )

    # Troposphere parameters
    T0 = 288.15               # Sea level standard temperature [K]
    p0 = 101325.0             # Sea level standard pressure [Pa]
    lapse_rate = -0.0065      # Temperature lapse rate [K/m]

    # Temperature at altitude
    temperature = T0 + lapse_rate * altitude

    # Pressure from hydrostatic equilibrium
    pressure = p0 * (temperature / T0) ** (-G0 / (lapse_rate * R_AIR))

    # Density from ideal gas law
    density = pressure / (R_AIR * temperature)

    state = AtmosphereState(
        altitude=altitude,
        temperature=temperature,
        pressure=pressure,
        density=density,
    )
    state.validate()

    return state
