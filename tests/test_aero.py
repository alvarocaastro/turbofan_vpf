import numpy as np
import pytest

from turbofan_vpf.aero import blade_loading_coefficient, incidence_delta_deg


def test_blade_loading_coefficient_positive():
    coefficient = blade_loading_coefficient(0.25, 200.0, 150.0)
    assert coefficient == pytest.approx(2.0 * np.pi * 0.25 / (200.0 * 150.0))


def test_incidence_delta_deg():
    assert incidence_delta_deg(2.0, -0.5) == 1.5
