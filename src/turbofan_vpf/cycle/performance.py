"""Preliminary cycle performance estimators."""

from __future__ import annotations


def estimate_specific_thrust(
    jet_velocity_m_s: float,
    flight_velocity_m_s: float,
    total_mass_flow_kg_s: float,
) -> float:
    """Estimate specific thrust for a single-stream turbofan.

    Args:
        jet_velocity_m_s: Effective exhaust velocity (m/s).
        flight_velocity_m_s: Flight speed (m/s).
        total_mass_flow_kg_s: Total engine mass flow (kg/s).

    Returns:
        Specific thrust in N/(kg/s).
    """

    if total_mass_flow_kg_s <= 0:
        raise ValueError("Total mass flow must be positive.")
    return (jet_velocity_m_s - flight_velocity_m_s) / total_mass_flow_kg_s
