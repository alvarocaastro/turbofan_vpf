"""
Module: reference_frame
-----------------------

This module defines angular reference frames used in the project.

The purpose of this module is to make explicit the reference frames in which
flow angles and blade orientations are defined, ensuring clarity and
consistency across the domain layer.
"""

from enum import Enum


class ReferenceFrame(Enum):
    """
    Enumeration of angular reference frames used in the project.
    """

    AXIAL = "axial"
    RELATIVE = "relative"
