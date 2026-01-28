"""Run analytical parametric sweeps for the VPF turbofan study."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from turbofan_vpf.analysis import run_parametric_sweep, save_results
from turbofan_vpf.config import AnalysisConfig
from turbofan_vpf.plots import plot_contour, plot_lift_curve


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="VPF turbofan analytical study")
    parser.add_argument("--mach", nargs="+", type=float, default=[0.6, 0.8, 1.0])
    parser.add_argument("--alpha", nargs="+", type=float, default=[-2, 0, 2, 6, 10])
    parser.add_argument("--incidence", type=float, default=2.0, help="Blade incidence (deg)")
    parser.add_argument("--output", type=Path, default=Path("results"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = AnalysisConfig()

    results = run_parametric_sweep(args.mach, args.alpha, args.incidence, config)
    save_results(args.output, results, config)

    plot_contour(
        results["mach"],
        results["alpha_deg"],
        results["fan_efficiency"],
        "Eficiencia del fan vs Mach y α",
        "Mach",
        "Ángulo de ataque α (deg)",
        "Eficiencia",
        args.output / "fan_efficiency.png",
    )

    plot_contour(
        results["mach"],
        results["alpha_deg"],
        results["specific_thrust"],
        "Empuje específico vs Mach y α",
        "Mach",
        "Ángulo de ataque α (deg)",
        "Empuje específico (N/kg/s)",
        args.output / "specific_thrust.png",
    )

    plot_contour(
        results["mach"],
        results["alpha_deg"],
        results["drag_reduction"],
        "Reducción sintética de drag vs Mach y α",
        "Mach",
        "Ángulo de ataque α (deg)",
        "ΔCD/CD0",
        args.output / "drag_reduction.png",
    )

    mach_values = np.unique(results["mach"])
    mid_index = len(mach_values) // 2
    cl_slice = results["cl"][:, mid_index]
    plot_lift_curve(results["alpha_deg"][:, mid_index], cl_slice, args.output / "cl_alpha.png")


if __name__ == "__main__":
    main()
