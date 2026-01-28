"""CFD mesh planning helpers."""

from __future__ import annotations


def mesh_resolution_hint(radius_m: float, target_y_plus: float = 1.0) -> float:
    """Provide a rough wall-normal spacing estimate.

    Args:
        radius_m: Fan radius (m).
        target_y_plus: Desired non-dimensional wall spacing.

    Returns:
        Suggested first cell height (m).
    """

    if radius_m <= 0:
        raise ValueError("Radius must be positive.")
    return radius_m * target_y_plus * 1e-4
