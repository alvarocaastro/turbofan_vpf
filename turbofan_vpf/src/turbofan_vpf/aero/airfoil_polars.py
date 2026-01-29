"""
Module: airfoil_polars
----------------------

This module defines a clean aerodynamic interface for 2D airfoil polars.

Its purpose is to provide aerodynamic coefficients (CL, CD, optionally CM)
as functions of angle of attack (alpha) for specified Reynolds and Mach
conditions. These polars will later be used to quantify the aerodynamic
benefit of incidence control enabled by Variable Pitch Fan (VPF) kinematics.

Design goals
------------
- Separate aerodynamic data from kinematics/geometry (domain layer)
- Provide reproducible, cacheable polars (CSV export/import)
- Offer an optional XFOIL-based generator (if XFOIL is available)
- Provide robust interpolation utilities for analysis scripts

This module does NOT:
- Model turbomachinery performance or fan-level thrust
- Perform CFD or loss modeling
- Depend on blade geometry or pitch models directly
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import subprocess
import tempfile

import numpy as np


# Definition of metadata describing a polar generation context
@dataclass(frozen=True)
class PolarMeta:
    airfoil_id: str                 # e.g., "NACA0012" or "CUSTOM:myfoil"
    reynolds: float                 # Reynolds number [-]
    mach: float                     # Mach number [-]
    ncrit: float = 9.0              # Ncrit for XFOIL transition model [-] (typical 7-9)
    source: str = "unknown"         # Source of the polar data (e.g., "xfoil", "experiment")
    notes: str = ""                 # Optional additional notes about the polar


# Definition of an airfoil polar container with interpolation utilities
@dataclass(frozen=True)
class AirfoilPolar:
    """
    Immutable container for a 2D airfoil polar.

    Arrays must be strictly monotonic in alpha_deg and of equal length.
    """

    meta: PolarMeta
    alpha_deg: np.ndarray           # Angle of attack array [deg]
    cl: np.ndarray                  # Lift coefficient array [-]
    cd: np.ndarray                  # Drag coefficient array [-]
    cm: Optional[np.ndarray] = None # Pitching moment coefficient array [-], optional

    # Definition of basic consistency checks for polar data
    def validate(self) -> None:
        """
        Validates the internal consistency of the polar data.
        Raises ValueError if inconsistencies are found.
        """
        if self.meta.reynolds <= 0.0:
            raise ValueError("Reynolds number must be positive.")
        if self.meta.mach < 0.0:
            raise ValueError("Mach number cannot be negative.")

        if self.alpha_deg.ndim != 1:
            raise ValueError("alpha_deg must be a 1D array.")
        n = self.alpha_deg.size
        if n < 3:
            raise ValueError("Polar data must contain at least 3 points.")

        if self.cl.shape != (n,) or self.cd.shape != (n,):
            raise ValueError("alpha_deg, cl, cd must have the same length.")

        if self.cm is not None and self.cm.shape != (n,):
            raise ValueError("cm must have the same length as alpha_deg if provided.")

        if not np.all(np.isfinite(self.alpha_deg)):
            raise ValueError("alpha_deg contains non-finite values.")
        if not np.all(np.isfinite(self.cl)) or not np.all(np.isfinite(self.cd)):
            raise ValueError("cl/cd contain non-finite values.")
        if np.any(self.cd < 0.0):
            raise ValueError("cd contains negative values (invalid).")

        # Require strict monotonicity in alpha_deg for reliable interpolation
        diff = np.diff(self.alpha_deg)
        if not (np.all(diff > 0.0) or np.all(diff < 0.0)):
            raise ValueError("alpha_deg must be strictly monotonic for interpolation.")

    # Definition of alpha bounds for safe interpolation
    @property
    def alpha_min_deg(self) -> float:
        """Minimum angle of attack in the polar [deg]."""
        return float(np.min(self.alpha_deg))

    @property
    def alpha_max_deg(self) -> float:
        """Maximum angle of attack in the polar [deg]."""
        return float(np.max(self.alpha_deg))

    # Definition of a safe linear interpolation helper (clamped or strict)
    def _interp(
        self,
        x_deg: float,
        y: np.ndarray,
        *,
        clamp: bool,
    ) -> float:
        xmin = self.alpha_min_deg
        xmax = self.alpha_max_deg

        if clamp:
            xq = float(np.clip(x_deg, xmin, xmax))
        else:
            if not (xmin <= x_deg <= xmax):
                raise ValueError(
                    f"alpha={x_deg:.3f} deg outside polar range "
                    f"[{xmin:.3f}, {xmax:.3f}] deg."
                )
            xq = x_deg

        return float(np.interp(xq, self.alpha_deg, y))

    # Definition of CL(alpha) interpolation
    def cl_at(self, alpha_deg: float, *, clamp: bool = True) -> float:
        return self._interp(alpha_deg, self.cl, clamp=clamp)

    # Definition of CD(alpha) interpolation
    def cd_at(self, alpha_deg: float, *, clamp: bool = True) -> float:
        return self._interp(alpha_deg, self.cd, clamp=clamp)

    # Definition of CM(alpha) interpolation
    def cm_at(self, alpha_deg: float, *, clamp: bool = True) -> float:
        if self.cm is None:
            raise ValueError("This polar does not contain CM data.")
        return self._interp(alpha_deg, self.cm, clamp=clamp)

    # Definition of L/D computation (with safe CD handling)
    def ld_at(self, alpha_deg: float, *, clamp: bool = True) -> float:
        cd = self.cd_at(alpha_deg, clamp=clamp)
        if cd <= 0.0:
            raise ValueError("CD is non-positive; cannot compute L/D.")
        return self.cl_at(alpha_deg, clamp=clamp) / cd

    # Definition of CSV export for reproducibility
    def to_csv(self, path: Path) -> None:
        self.validate()
        path.parent.mkdir(parents=True, exist_ok=True)

        lines: list[str] = []
        lines.append(f"# airfoil_id: {self.meta.airfoil_id}")
        lines.append(f"# reynolds: {self.meta.reynolds}")
        lines.append(f"# mach: {self.meta.mach}")
        lines.append(f"# ncrit: {self.meta.ncrit}")
        lines.append(f"# source: {self.meta.source}")
        if self.meta.notes:
            lines.append(f"# notes: {self.meta.notes}")

        header = "alpha_deg,cl,cd" + (",cm" if self.cm is not None else "")
        lines.append(header)

        if self.cm is None:
            data = np.column_stack((self.alpha_deg, self.cl, self.cd))
        else:
            data = np.column_stack((self.alpha_deg, self.cl, self.cd, self.cm))

        with path.open("w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
            np.savetxt(f, data, delimiter=",", fmt="%.8e")

    # Definition of CSV import for reproducibility
    @staticmethod
    def from_csv(path: Path) -> AirfoilPolar:
        meta_dict: dict[str, str] = {}
        data_lines: list[str] = []

        with path.open("r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if not s:
                    continue
                if s.startswith("#"):
                    parts = s[1:].strip().split(":", maxsplit=1)
                    if len(parts) == 2:
                        meta_dict[parts[0].strip()] = parts[1].strip()
                    continue
                data_lines.append(line)

        if len(data_lines) < 2:
            raise ValueError("CSV contains no data rows.")

        header = data_lines[0].strip().split(",")
        arr = np.loadtxt(data_lines[1:], delimiter=",")

        if arr.ndim == 1:
            arr = arr.reshape(1, -1)

        cols = {name: arr[:, i] for i, name in enumerate(header)}
        alpha_deg = cols["alpha_deg"]
        cl = cols["cl"]
        cd = cols["cd"]
        cm = cols.get("cm", None)

        meta = PolarMeta(
            airfoil_id=meta_dict.get("airfoil_id", path.stem),
            reynolds=float(meta_dict.get("reynolds", "0.0")),
            mach=float(meta_dict.get("mach", "0.0")),
            ncrit=float(meta_dict.get("ncrit", "9.0")),
            source=meta_dict.get("source", "csv"),
            notes=meta_dict.get("notes", ""),
        )

        polar = AirfoilPolar(meta=meta, alpha_deg=alpha_deg, cl=cl, cd=cd, cm=cm)
        polar.validate()
        return polar


# Definition of an optional XFOIL runner for polar generation
class XFOILRunner:
    """
    Minimal XFOIL runner that generates polars via subprocess.
    """

    def __init__(self, xfoil_exe: str = "xfoil") -> None:
        self.xfoil_exe = xfoil_exe

    # Definition of a polar generation method using XFOIL
    def generate_polar(
        self,
        *,
        airfoil: str,
        reynolds: float,
        mach: float,
        alpha_start_deg: float,
        alpha_end_deg: float,
        alpha_step_deg: float,
        ncrit: float = 9.0,
        max_iter: int = 100,
    ) -> AirfoilPolar:
        if reynolds <= 0.0:
            raise ValueError("Reynolds must be positive for XFOIL.")
        if mach < 0.0:
            raise ValueError("Mach must be non-negative for XFOIL.")
        if alpha_step_deg <= 0.0:
            raise ValueError("alpha_step_deg must be positive.")
        if alpha_end_deg <= alpha_start_deg:
            raise ValueError("alpha_end_deg must be greater than alpha_start_deg.")

        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            polar_file = td_path / "polar.txt"
            xfoil_in = td_path / "xfoil.in"

            lines: list[str] = []
            lines.append("PLop")
            lines.append("G")
            lines.append("")

            if airfoil.upper().startswith("NACA"):
                digits = airfoil.upper().replace("NACA", "").replace(" ", "")
                if not digits.isdigit():
                    raise ValueError(f"Invalid NACA spec: {airfoil}")
                lines.append(f"NACA {digits}")
            else:
                coord_path = Path(airfoil)
                if not coord_path.exists():
                    raise ValueError(f"Airfoil file not found: {coord_path}")
                lines.append(f"LOAD {coord_path}")
                lines.append("")

            lines.append("OPER")
            lines.append(f"VISC {reynolds:.8e}")
            lines.append(f"MACH {mach:.6f}")
            lines.append(f"ITER {max_iter}")
            lines.append("VPAR")
            lines.append(f"N {ncrit:.3f}")
            lines.append("")

            lines.append("PACC")
            lines.append(str(polar_file))
            lines.append("")

            lines.append(f"ASEQ {alpha_start_deg:.3f} {alpha_end_deg:.3f} {alpha_step_deg:.3f}")
            lines.append("PACC")
            lines.append("")

            lines.append("QUIT")

            xfoil_in.write_text("\n".join(lines) + "\n", encoding="utf-8")

            try:
                proc = subprocess.run(
                    [self.xfoil_exe],
                    input=xfoil_in.read_text(encoding="utf-8"),
                    text=True,
                    capture_output=True,
                    check=False,
                    timeout=60,
                )
            except FileNotFoundError as e:
                raise RuntimeError(
                    "XFOIL executable not found. Install XFOIL or provide xfoil_exe path."
                ) from e

            if proc.returncode != 0 or not polar_file.exists():
                raise RuntimeError(
                    "XFOIL polar generation failed.\n"
                    f"Return code: {proc.returncode}\n"
                    f"STDOUT (tail): {proc.stdout[-400:]}\n"
                    f"STDERR (tail): {proc.stderr[-400:]}\n"
                )

            alpha_list: list[float] = []
            cl_list: list[float] = []
            cd_list: list[float] = []
            cm_list: list[float] = []

            for line in polar_file.read_text(encoding="utf-8", errors="ignore").splitlines():
                parts = line.strip().split()
                if len(parts) < 6:
                    continue
                try:
                    a = float(parts[0])
                    clv = float(parts[1])
                    cdv = float(parts[2])
                    cmv = float(parts[4])
                except ValueError:
                    continue
                alpha_list.append(a)
                cl_list.append(clv)
                cd_list.append(cdv)
                cm_list.append(cmv)

            if len(alpha_list) < 5:
                raise RuntimeError("XFOIL returned insufficient polar points.")

            meta = PolarMeta(
                airfoil_id=airfoil,
                reynolds=float(reynolds),
                mach=float(mach),
                ncrit=float(ncrit),
                source="xfoil",
                notes=f"ASEQ {alpha_start_deg} {alpha_end_deg} {alpha_step_deg}, ITER {max_iter}",
            )

            polar = AirfoilPolar(
                meta=meta,
                alpha_deg=np.asarray(alpha_list, dtype=float),
                cl=np.asarray(cl_list, dtype=float),
                cd=np.asarray(cd_list, dtype=float),
                cm=np.asarray(cm_list, dtype=float),
            )
            polar.validate()
            return polar
