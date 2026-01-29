"""
Module: blade_kinematics
-----------------------

This module defines the geometric and kinematic description of a fan blade
representative of the outer fan region of a commercial turbofan engine.

Its purpose is to provide a physically consistent and explicit representation
of blade orientation, including pitch and stagger, independent of aerodynamic
models, performance metrics, or numerical solvers.

Scientific role in this project
-------------------------------
This project aims to quantify the aerodynamic benefit of a Variable Pitch Fan
(VPF) relative to a fixed-pitch concept across multiple operating conditions.
Within that scope, blade pitch is modeled as a controlled rotation of the blade
about its pitch axis, modifying the chord-line orientation and thus the blade
incidence relative to the incoming flow.

Pitch range justification (commercial turbofan outer fan)
---------------------------------------------------------
Pitch variation is intentionally limited to a conservative, realistic range
representative of a large-diameter commercial turbofan fan. The primary intent
of VPF in this context is incidence trimming and off-design efficiency
improvement, not operation at extreme blade angles.

A ±8° pitch variation about a nominal setting is selected because it:
- Provides sufficient authority to compensate off-design incidence shifts
  across typical flight regimes (takeoff/climb/cruise) in preliminary studies.
- Avoids entering operating conditions that would likely be dominated by
  strong separation, large losses, or transonic shock-induced penalties.
- Remains within a defensible mechanical and aeroelastic envelope for an
  outer fan blade, where structural loads and flutter margins are critical.

This module does NOT:
- Define airfoil shape, twist distribution, or 3D blade geometry
- Perform aerodynamic force calculations (CL/CD) or performance evaluation
- Make CFD-specific assumptions

All angles are expressed in radians by design (SI consistency).
"""

#Imports
from __future__ import annotations
from dataclasses import dataclass
import math

# Nominal pitch variation range used throughout the project
min_pitch_deg = -8.0    # Minimum pitch angle [degrees]
max_pitch_deg = 8.0     # Maximum pitch angle [degrees]
min_pitch_rad = math.radians(min_pitch_deg)  # Minimum pitch angle [radians]
max_pitch_rad = math.radians(max_pitch_deg)  # Maximum pitch angle [radians]

#Definition of dataclass for blade kinematics
@dataclass(frozen=True)      # Immutable dataclass for blade kinematics
class BladeKinematics:
    """
    Represents the geometric and kinematic orientation of a fan blade section.

    Attributes:
        - `stagger_angle` represents the nominal geometric setting (design intent).
        - `pitch_angle` represents an additional controllable rotation (VPF action).
        - `r_over_R` is the non-dimensional radial position along the blade span (0 < r/R ≤ 1).
        - The absolute chord-line orientation is defined as:
            chord_angle = stagger_angle + pitch_angle
    """
    pitch_angle: float        # [rad] controllable pitch increment relative to nominal
    stagger_angle: float      # [rad] nominal blade stagger angle (geometry/design)
    r_over_R: float           # [-] non-dimensional radial position (r/R)
    #Definition of a physical consistency check method
    def validate(self) -> None:
        """
        Validate the physical consistency of the blade kinematics.

        Ensures that the pitch angle is within the defined operational range.
        """
        if not (min_pitch_rad <= self.pitch_angle <= max_pitch_rad):
            raise ValueError(
                f"Pitch angle {math.degrees(self.pitch_angle):.2f}° "
                f"out of bounds [{min_pitch_deg}°, {max_pitch_deg}°]."
            )
        
        if not 0.0 < self.r_over_R <= 1.0:
            raise ValueError(
                f"Non-dimensional radial position r/R = {self.r_over_R:.3f} "
                "must be in the range (0, 1]."
            )
        
    #Definition of property to calculate absolute chord angle
    @property
    def chord_angle(self) -> float:
        """
        Calculate the absolute chord-line angle of the blade section.

        Returns:
            float: Absolute chord-line angle [rad].
        """
        return self.stagger_angle + self.pitch_angle
    
    #Definition of property to calculate absolute chord angle in degrees
    @property
    def chord_angle_deg(self) -> float:
        """
        Calculate the absolute chord-line angle of the blade section in degrees.

        Returns:
            float: Absolute chord-line angle [degrees].
        """
        return math.degrees(self.chord_angle)
    
    #Definition of factory method to create BladeKinematics from angles in degrees
    @staticmethod
    def from_degrees(
        *,
        pitch_angle_deg: float,
        stagger_angle_deg: float,
        r_over_R: float,
    ) -> BladeKinematics:
        """
        Factory method to create BladeKinematics from angles in degrees.
        """
        kin = BladeKinematics(
            pitch_angle=math.radians(pitch_angle_deg),
            stagger_angle=math.radians(stagger_angle_deg),
            r_over_R=r_over_R,
        )
        kin.validate()
        return kin
    
    @staticmethod
    def pitch_sweep(
        *,
        stagger_angle: float,
        r_over_R: float,
        pitch_min_rad: float = min_pitch_rad,
        pitch_max_rad: float = max_pitch_rad,
        n_points: int = 17,
    ) -> list[BladeKinematics]:
        """
        Generates a parametric sweep of blade pitch configurations at a fixed
        radial position.

        This method is intended as a study tool for Variable Pitch Fan (VPF)
        analysis. It produces a set of blade kinematic configurations in which
        all parameters (stagger angle and radial position) are held constant,
        while the blade pitch angle is varied within a realistic range.

        The resulting set of BladeKinematics objects can be combined with a
        fixed flow state to:
        - Evaluate the sensitivity of blade incidence to pitch variation
        - Compare fixed-pitch and variable-pitch configurations
        - Identify pitch settings that maintain near-optimal incidence under
          off-design flow conditions

        This method does not perform any aerodynamic or performance calculations;
        it only defines the geometric configurations required for parametric
        analysis.
        """
        if n_points < 2:
            raise ValueError("n_points must be at least 2 to define a sweep.")
        
        step = (pitch_max_rad - pitch_min_rad) / (n_points - 1)
        pitch_values = [pitch_min_rad + i * step for i in range(n_points)]
        
        sweep = [
            BladeKinematics(
                pitch_angle=pitch,
                stagger_angle=stagger_angle,
                r_over_R=r_over_R,
            )
            for pitch in pitch_values
        ]

        for kin in sweep:
            kin.validate()

        return sweep