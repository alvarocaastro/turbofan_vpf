"""
Module: operating_point
-----------------------

This module defines operating points representing named flight or operating
conditions (e.g., cruise, takeoff, climb) used for parametric studies.

An operating point provides contextual meaning to an operating condition but
does not perform any physical calculations.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class OperatingPoint:
    """
    Represents a named operating point for analysis purposes.
    """

    name: str
    altitude: float        # [m]
    mach: float            # [-]
    description: str = ""
