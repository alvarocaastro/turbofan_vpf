"""Analytical models for a Variable Pitch Fan turbofan."""

from __future__ import annotations

import numpy as np


def incidence_adjusted_alpha(alpha_deg: np.ndarray, blade_incidence_deg: float) -> np.ndarray:
    """Combine flow incidence with blade pitch variation."""

    return alpha_deg + blade_incidence_deg


def lift_coefficient(
    alpha_deg: np.ndarray,
    lift_curve_slope_per_deg: float,
    stall_alpha_deg: float,
) -> np.ndarray:
    """Simplified CL(alpha) with soft-stall behavior."""

    linear = lift_curve_slope_per_deg * alpha_deg
    stall_factor = 1.0 / (1.0 + np.exp((np.abs(alpha_deg) - stall_alpha_deg) / 1.5))
    return linear * stall_factor


def drag_coefficient(
    cl: np.ndarray,
    base_drag_coeff: float,
    induced_drag_factor: float = 0.08,
) -> np.ndarray:
    """Synthetic drag polar: CD = CD0 + k * CL^2."""

    return base_drag_coeff + induced_drag_factor * cl**2


def fan_efficiency(
    mach: np.ndarray,
    blade_incidence_deg: float,
    base_efficiency: float,
) -> np.ndarray:
    """Estimate efficiency degradation with Mach and incidence."""

    mach_penalty = 0.04 * (mach - 0.7) ** 2
    incidence_penalty = 0.0025 * blade_incidence_deg**2
    efficiency = base_efficiency - mach_penalty - incidence_penalty
    return np.clip(efficiency, 0.6, 0.95)


def specific_thrust(
    mach: np.ndarray,
    blade_incidence_deg: float,
    base_specific_thrust: float,
) -> np.ndarray:
    """Estimate specific thrust as a function of Mach and incidence."""

    mach_factor = 1.0 - 0.15 * (mach - 0.75)
    incidence_factor = 1.0 - 0.01 * np.abs(blade_incidence_deg)
    return base_specific_thrust * mach_factor * incidence_factor
