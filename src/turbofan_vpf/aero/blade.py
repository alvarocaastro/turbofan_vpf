"""Simplified blade element analysis placeholders."""

from __future__ import annotations

import numpy as np


def blade_loading_coefficient(
    circulation_m2_s: float,
    blade_speed_m_s: float,
    axial_velocity_m_s: float,
) -> float:
    """Compute a non-dimensional blade loading coefficient.

    Args:
        circulation_m2_s: Section circulation (m^2/s).
        blade_speed_m_s: Tangential blade speed (m/s).
        axial_velocity_m_s: Axial inflow velocity (m/s).

    Returns:
        The loading coefficient based on a simplified expression.
    """

    reference = max(blade_speed_m_s * axial_velocity_m_s, 1e-9)
    return float(2.0 * np.pi * circulation_m2_s / reference)
