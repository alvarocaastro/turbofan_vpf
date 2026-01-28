"""Configuration objects for the analytical turbofan study."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AnalysisConfig:
    """Baseline configuration for parametric studies."""

    reference_area_m2: float = 2.5
    reference_radius_m: float = 0.75
    base_drag_coeff: float = 0.03
    lift_curve_slope_per_deg: float = 0.1
    stall_alpha_deg: float = 12.0
    base_fan_efficiency: float = 0.88
    base_specific_thrust_n_per_kg_s: float = 65.0
