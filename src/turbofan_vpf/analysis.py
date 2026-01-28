"""Parametric analysis routines for VPF turbofan studies."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Iterable

import numpy as np

from .config import AnalysisConfig
from .models import (
    drag_coefficient,
    fan_efficiency,
    incidence_adjusted_alpha,
    lift_coefficient,
    specific_thrust,
)


def run_parametric_sweep(
    mach_values: Iterable[float],
    alpha_values_deg: Iterable[float],
    blade_incidence_deg: float,
    config: AnalysisConfig,
) -> dict[str, np.ndarray]:
    """Run a sweep over Mach and angle of attack."""

    mach = np.asarray(list(mach_values), dtype=float)
    alpha = np.asarray(list(alpha_values_deg), dtype=float)
    mach_grid, alpha_grid = np.meshgrid(mach, alpha)

    adjusted_alpha = incidence_adjusted_alpha(alpha_grid, blade_incidence_deg)
    cl = lift_coefficient(
        adjusted_alpha, config.lift_curve_slope_per_deg, config.stall_alpha_deg
    )
    cd = drag_coefficient(cl, config.base_drag_coeff)
    efficiency = fan_efficiency(mach_grid, blade_incidence_deg, config.base_fan_efficiency)
    thrust = specific_thrust(mach_grid, blade_incidence_deg, config.base_specific_thrust_n_per_kg_s)

    drag_reduction = (config.base_drag_coeff - cd) / config.base_drag_coeff

    return {
        "mach": mach_grid,
        "alpha_deg": alpha_grid,
        "adjusted_alpha_deg": adjusted_alpha,
        "cl": cl,
        "cd": cd,
        "drag_reduction": drag_reduction,
        "fan_efficiency": efficiency,
        "specific_thrust": thrust,
    }


def save_results(output_dir: Path, results: dict[str, np.ndarray], config: AnalysisConfig) -> None:
    """Persist results to a NumPy binary for reproducibility."""

    output_dir.mkdir(parents=True, exist_ok=True)
    np.savez(output_dir / "analysis_results.npz", **results, config=asdict(config))
