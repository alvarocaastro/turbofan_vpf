import pytest

from turbofan_vpf.cycle import estimate_specific_thrust


def test_estimate_specific_thrust():
    result = estimate_specific_thrust(450.0, 250.0, 200.0)
    assert result == pytest.approx(1.0)


def test_estimate_specific_thrust_rejects_nonpositive_flow():
    with pytest.raises(ValueError):
        estimate_specific_thrust(450.0, 250.0, 0.0)
