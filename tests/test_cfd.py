import pytest

from turbofan_vpf.cfd import mesh_resolution_hint


def test_mesh_resolution_hint():
    assert mesh_resolution_hint(1.2, target_y_plus=1.0) == pytest.approx(1.2e-4)


def test_mesh_resolution_hint_requires_positive_radius():
    with pytest.raises(ValueError):
        mesh_resolution_hint(0.0)
