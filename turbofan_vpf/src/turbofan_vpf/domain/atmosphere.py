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

#Imports

from __future__ import annotations
from dataclasses import dataclass
import math

#Physical constants (SI units)
GAMMA_AIR = 1.4              # Ratio of specific heats [-]
R_AIR = 287.05               # Specific gas constant for air [J/(kg·K)]
G0 = 9.80665                 # Gravitational acceleration [m/s^2]

#Definition of dataclass for atmosphere state
@dataclass(frozen=True)      # Immutable dataclass for atmospheric state
class AtmosphereState:
    """

    Dataclass representing the state of the atmosphere at a given altitude.

    Attributes:
        altitude (float): Altitude above sea level [m].
        temperature (float): Temperature [K].
        pressure (float): Pressure [Pa].
        density (float): Density [kg/m^3].

    """
    altitude: float         # [m]
    temperature: float      # [K]
    pressure: float         # [Pa]
    density: float          # [kg/m^3]

#Definition of property to calculate speed of sound. Useful for calculating Mach number.
@property
def speed_of_sound(self) -> float:
    """

    Calculate the speed of sound at the current atmospheric state.

    Returns:
        float: Speed of sound [m/s].

    """
    return math.sqrt(GAMMA_AIR * R_AIR * self.temperature)

#Definition of property to calculate dynamic viscosity using Sutherland's law
@property
def dynamic_viscosity(self) -> float:
    """

    Returns the dynamic viscosity using Sutherland's law.
    
    """
    T_ref = 273.15      # [K]
    mu_ref = 1.716e-5   # [Pa·s]
    S = 110.4           # [K]

    return mu_ref * (self.temperature / T_ref) ** 1.5 * (
        (T_ref + S) / (self.temperature + S)
    )

# Validity limits for the implemented ISA model
TROPOSPHERE_LIMIT = 11_000.0  # [m]

#Definition of ISA atmosphere model
def isa_atmosphere(altitude: float) -> AtmosphereState:
    """

    Computes the International Standard Atmosphere (ISA) porperties for the troposphere (up to 11 km).
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

    # Calculate temperature at altitude using lapse rate
    temperature = T0 + lapse_rate * altitude

    # Calculate pressure using hydrostatic equilibrium
    pressure = p0 * (temperature / T0) ** (-G0 / (lapse_rate * R_AIR))
    
    # Calculate density using ideal gas law
    density = pressure / (R_AIR * temperature)

    return AtmosphereState(
        altitude=altitude,
        temperature=temperature,
        pressure=pressure,
        density=density
    )