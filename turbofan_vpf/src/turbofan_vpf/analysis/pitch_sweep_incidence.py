"""
Script: pitch_sweep_incidence
-----------------------------

This analysis script performs a parametric sweep of blade pitch and evaluates
the resulting blade incidence under one nominal and one off-design flow angle.

Its purpose is to demonstrate, at a purely kinematic/geometric level, the core
mechanism behind Variable Pitch Fan (VPF) concepts: pitch variation allows the
blade to compensate changes in incoming flow direction by controlling incidence.

No aerodynamic polars, CL/CD, losses, or CFD are used here.
"""
from __future__ import annotations

import math
import os
from pathlib import Path

import matplotlib # pylint: disable=wrong-import-position,import-error

# Configure a robust Matplotlib backend before importing pyplot.
# If running headless (no display), force the non-interactive 'Agg' backend.
if os.environ.get("DISPLAY", "") == "":
    matplotlib.use("Agg")

import matplotlib.pyplot as plt # pylint: disable=wrong-import-position,import-error

from turbofan_vpf.domain.atmosphere import isa_atmosphere 
from turbofan_vpf.domain.flow_state import FlowState
from turbofan_vpf.domain.blade_kinematics import BladeKinematics 
from turbofan_vpf.domain.incidence import compute_incidence 



# Definition of a helper function to build a FlowState from ISA + Mach + flow angle
def build_flow_state_from_isa(
    *,
    altitude_m: float,
    mach: float,
    flow_angle_rad: float,
) -> FlowState:
    """
    Constructs a FlowState from ISA atmospheric conditions, flight Mach number,
    and local flow direction.
    """
    atmosphere = isa_atmosphere(altitude_m)
    velocity = mach * atmosphere.speed_of_sound

    return FlowState(
        velocity=velocity,
        flow_angle=flow_angle_rad,
        static_pressure=atmosphere.pressure,
        static_temperature=atmosphere.temperature,
        density=atmosphere.density,
    )


# Definition of the output directory resolver for plots and artifacts
def get_results_dir() -> Path:
    """
    Returns the project-level results directory: <repo_root>/data/results.
    Assumes this script is located at: <repo_root>/src/turbofan_vpf/analysis/.
    """
    repo_root = Path(__file__).resolve().parents[3]
    out_dir = repo_root / "data" / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


# Definition of the main analysis routine for pitch sweep incidence evaluation
def main() -> None:
    # -- 1) Define operating environment (ISA) and flight condition --
    altitude_m = 11_000.0
    mach = 0.78

    # Local flow angles (representing the local inlet flow direction at the blade)
    flow_angle_nominal_deg = 30.0
    flow_angle_off_design_deg = 35.0  # +5 deg off-design shift

    flow_nominal = build_flow_state_from_isa(
        altitude_m=altitude_m,
        mach=mach,
        flow_angle_rad=math.radians(flow_angle_nominal_deg),
    )

    flow_off_design = build_flow_state_from_isa(
        altitude_m=altitude_m,
        mach=mach,
        flow_angle_rad=math.radians(flow_angle_off_design_deg),
    )

    # -- 2) Define a representative blade section (outer fan region) --
    r_over_R = 0.90

    # Choose stagger so that incidence is 0 deg at nominal when pitch = 0 deg:
    # incidence = flow_angle - (stagger + pitch)
    # set pitch=0 and incidence=0 => stagger = flow_angle_nominal
    stagger_angle_rad = math.radians(flow_angle_nominal_deg)

    # -- 3) Generate pitch sweep configurations --
    sweep = BladeKinematics.pitch_sweep(
        stagger_angle=stagger_angle_rad,
        r_over_R=r_over_R,
        n_points=33,
    )

    # -- 4) Compute incidence for each pitch setting at both flow angles --
    pitch_deg = [math.degrees(k.pitch_angle) for k in sweep]

    incidence_nominal_deg = [
        math.degrees(compute_incidence(flow_nominal, k)) for k in sweep
    ]
    incidence_off_design_deg = [
        math.degrees(compute_incidence(flow_off_design, k)) for k in sweep
    ]

    # -- 5) Compute pitch required to recover zero-incidence in off-design --
    # incidence = flow - (stagger + pitch) -> set incidence = 0 => pitch = flow - stagger
    pitch_to_zero_off_design_rad = flow_off_design.flow_angle - stagger_angle_rad
    pitch_to_zero_off_design_deg = math.degrees(pitch_to_zero_off_design_rad)

    # Check feasibility within the defined ±8° pitch authority
    feasible = -8.0 <= pitch_to_zero_off_design_deg <= 8.0

    print("=== Pitch Sweep Incidence Analysis ===")
    print(f"Altitude: {altitude_m:.0f} m (ISA), Mach: {mach:.2f}")
    print(f"Nominal flow angle: {flow_angle_nominal_deg:.2f} deg")
    print(f"Off-design flow angle: {flow_angle_off_design_deg:.2f} deg")
    print(f"Blade stagger angle: {math.degrees(stagger_angle_rad):.2f} deg")
    print(
        f"Pitch required to recover i=0 (off-design): {pitch_to_zero_off_design_deg:.2f} deg"
    )
    if feasible:
        print("Result: Compensation is feasible within the selected ±8° pitch authority.")
    else:
        print(
            "Result: Required pitch exceeds ±8° -> compensation not feasible within this pitch authority."
        )

    # -- 6) Plot results --
    plt.figure()
    plt.plot(pitch_deg, incidence_nominal_deg, label="Nominal flow angle")
    plt.plot(pitch_deg, incidence_off_design_deg, label="Off-design flow angle (+5°)")

    plt.axhline(0.0, linewidth=1.0)
    plt.axvline(0.0, linewidth=1.0)

    # Mark the pitch that recovers i = 0 under off-design flow
    plt.scatter([pitch_to_zero_off_design_deg], [0.0], marker="o", label="Pitch for i=0 (off-design)")

    plt.xlabel("Blade pitch angle [deg]")
    plt.ylabel("Blade incidence angle [deg]")
    plt.title("Incidence vs Pitch (Nominal vs Off-design Flow Angles)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Always save results (reproducibility), and show if possible.
    out_dir = get_results_dir()
    out_file = out_dir / "pitch_sweep_incidence.png"
    plt.savefig(out_file, dpi=200)
    print(f"Plot saved to: {out_file}")

    # Show only if a GUI backend is available
    try:
        plt.show()
    except Exception:
        pass


if __name__ == "__main__":
    main()
