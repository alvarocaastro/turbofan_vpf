"""Plotting helpers for the VPF turbofan study."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def plot_contour(
    x_grid: np.ndarray,
    y_grid: np.ndarray,
    z_grid: np.ndarray,
    title: str,
    x_label: str,
    y_label: str,
    colorbar_label: str,
    output_path: Path,
) -> None:
    """Generate and save a contour plot."""

    fig, ax = plt.subplots(figsize=(7, 5))
    contour = ax.contourf(x_grid, y_grid, z_grid, levels=20, cmap="viridis")
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    fig.colorbar(contour, ax=ax, label=colorbar_label)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def plot_lift_curve(
    alpha_deg: np.ndarray,
    cl: np.ndarray,
    output_path: Path,
) -> None:
    """Plot CL vs alpha for a representative Mach slice."""

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(alpha_deg, cl, marker="o")
    ax.set_title("Curva de sustentación CL vs α")
    ax.set_xlabel("Ángulo de ataque α (deg)")
    ax.set_ylabel("CL")
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
