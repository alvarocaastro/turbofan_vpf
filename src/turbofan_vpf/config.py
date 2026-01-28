"""Configuration models for the VPF turbofan study."""

from dataclasses import dataclass


@dataclass(frozen=True)
class VPFConfig:
    """Top-level configuration values for baseline studies."""

    reference_radius_m: float = 0.75
    reference_turbofan_mass_flow_kg_s: float = 180.0
    design_altitude_m: float = 11000.0
    design_mach: float = 0.78
