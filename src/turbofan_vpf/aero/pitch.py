"""Incidence and pitch variation utilities."""

from __future__ import annotations


def incidence_delta_deg(design_incidence_deg: float, pitch_offset_deg: float) -> float:
    """Estimate the change in incidence due to pitch variation.

    Args:
        design_incidence_deg: Baseline incidence angle at design (deg).
        pitch_offset_deg: Commanded pitch change (deg).

    Returns:
        Updated incidence in degrees.
    """

    return design_incidence_deg + pitch_offset_deg
