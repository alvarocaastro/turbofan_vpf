"""
Module: incidence
-----------------

This module provides a formal definition of blade incidence for sectional
fan-blade analysis.

Incidence is defined as the relative angle between the incoming flow
direction and the blade chord-line direction. In this project, incidence is
the primary variable through which the aerodynamic benefit of Variable Pitch
Fan (VPF) concepts is evaluated.

Sign convention
---------------
Incidence is defined as:

    incidence = flow_angle - chord_angle

where:
- flow_angle is the absolute flow direction (from FlowState) [rad]
- chord_angle is the absolute chord-line direction (from BladeKinematics) [rad]

The returned incidence is wrapped to the interval [-pi, pi] to ensure a
continuous representation.

This module does NOT:
- Perform aerodynamic force calculations (CL/CD)
- Compute losses, efficiency, or performance metrics
- Depend on CFD solvers or numerical discretization
"""
#Imports
from __future__ import annotations
import math

from turbofan_vpf.domain.flow_state import FlowState
from turbofan_vpf.domain.blade_kinematics import BladeKinematics

#Definition of an angular normalization utility mapping angles to [-pi, pi]
def wrap_to_pi(angle_rad:float) -> float:
    """
    Wraps an angle in radians to the interval [-pi, pi].

    This prevents discontinuities when dealing with angular quantities.
    (e.g., avoiding 359 deg instead of -1 deg).
    Parameters:
    -----------
    angle_rad : float
        Angle in radians to be wrapped.

    Returns:
    --------
    float
        Angle wrapped to the interval [-pi, pi].
    """
    wrapped = (angle_rad + math.pi) % (2.0 * math.pi) - math.pi
    return wrapped

# Definition of blade incidence as the relative angle between flow direction and blade chord line
def compute_incidence(flow:FlowState, blade:BladeKinematics) -> float:
    """
    Computes blade incidence [rad] using the project sign convention:

        incidence = flow_angle - chord_angle

    Args:
        flow: FlowState containing absolute flow direction (flow_angle).
        blade: BladeKinematics defining the chord-line direction (chord_angle).

    Returns:
        Incidence angle in radians, wrapped to [-pi, pi].

    Notes:
        - Positive incidence means the flow approaches the blade chord line with
          a positive relative angle according to the sign convention above.
        - Incidence is a geometric quantity. Aerodynamic models may later map
          incidence to CL/CD, losses, etc., but that is outside the domain layer.
    """

    flow.validate()
    blade.validate()

    raw_incidence = flow.flow_angle - blade.chord_angle
    return wrap_to_pi(raw_incidence)

# Definition of a convenience wrapper returning blade incidence in degrees
def incidence_deg(flow:FlowState, blade:BladeKinematics) -> float:
    """
    Computes blade incidence in degrees.

    Args:
        flow: FlowState containing absolute flow direction (flow_angle).
        blade: BladeKinematics defining the chord-line direction (chord_angle).

    Useful for plotting, logs and reporting
    """

    return math.degrees(compute_incidence(flow, blade))
