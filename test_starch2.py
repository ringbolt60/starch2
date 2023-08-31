# --------------------------------------------------
import pytest

from starch2 import (
    World,
    calc_orbital_period,
    WorldType,
    calc_rotation_period,
    Resonance,
    adjust_for_eccentricity,
)
from utils import Dice


def test_orbital_period():
    """Checks period calculated correctly"""

    lone_input = World(
        world_type=WorldType.LONE, planet_mass=0.93, star_mass=0.94, star_distance=0.892
    )
    period_lone = calc_orbital_period(lone_input)
    assert period_lone == pytest.approx(7617.0, abs=1e-1)

    satellite_input = World(
        world_type=WorldType.SATELLITE,
        satellite_mass=0.023,
        planet_mass=0.876,
        primary_distance=175845,
    )
    period_satellite = calc_orbital_period(satellite_input)
    assert period_satellite == pytest.approx(215.3, abs=1e-1)


# --------------------------------------------------
def test_rotation_period():
    """Checks rotation period calculated correctly"""
    lone_world_1 = World(
        world_type=WorldType.LONE,
        planet_mass=0.93,
        star_mass=0.94,
        star_distance=0.892,
        age=3.225,
        ecc=0.07,
    )
    period, lock = calc_rotation_period(lone_world_1, rand=Dice(mocks=[3, 6, 1]))
    assert 24 <= period <= 40
    assert lock == Resonance.NONE

    lone_world_2 = World(
        world_type=WorldType.LONE,
        planet_mass=0.93,
        star_mass=1.256,
        star_distance=0.892,
        age=9.225,
        ecc=0.37,
        orbital_period=6592.5,
    )
    period, lock = calc_rotation_period(lone_world_2, rand=Dice(mocks=[5, 6, 5]))
    assert period == pytest.approx(2637.0, abs=1e-1)
    assert lock == Resonance.RESONANCE_5_2

    orbited_world = World(
        world_type=WorldType.ORBITED,
        planet_mass=0.93,
        star_mass=0.14,
        star_distance=0.087,
        primary_distance=125687,
        satellite_mass=0.025,
        age=1.225,
        ecc=0.07,
    )
    period, lock = calc_rotation_period(orbited_world, rand=Dice(mocks=[1, 2, 1]))
    assert period == pytest.approx(126.2, abs=1e-1)
    assert lock == Resonance.LOCK_TO_SATELLITE

    satellite_world = World(
        world_type=WorldType.SATELLITE,
        satellite_mass=0.023,
        primary_distance=175845,
        planet_mass=0.876,
        orbital_period=215.3,
    )
    results = calc_rotation_period(satellite_world)
    period, lock = results
    assert period == pytest.approx(215.3, abs=1e-1)
    assert lock == Resonance.LOCK_TO_PRIMARY


# --------------------------------------------------
@pytest.mark.parametrize(
    "e, p, expected_period, expected_lock",
    [
        (0.01, 256.0, 256.0, Resonance.LOCK_TO_STAR),
        (0.08, 478.0, 478.0, Resonance.LOCK_TO_STAR),
        (0.18, 330.0, 220.0, Resonance.RESONANCE_3_2),
        (0.25, 550.0, 275.0, Resonance.RESONANCE_2_1),
        (0.29, 700.0, 350.0, Resonance.RESONANCE_2_1),
        (0.35, 500.0, 200.0, Resonance.RESONANCE_5_2),
        (0.4, 1000.0, 400.0, Resonance.RESONANCE_5_2),
        (0.45, 300.0, 100.0, Resonance.RESONANCE_3_1),
        (0.6, 600.0, 200.0, Resonance.RESONANCE_3_1),
    ],
)
def test_calculate_resonance(e, p, expected_period, expected_lock):
    """Checks resonant orbital periods adjusted for eccentricity"""

    result = adjust_for_eccentricity(ecc=e, period=p)
    lock, period = result
    assert period == expected_period
    assert lock == expected_lock
