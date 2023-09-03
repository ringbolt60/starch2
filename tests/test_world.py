"""Tests for world.py."""
import os
import sys

import pytest

from starch.world import (
    World,
    calc_orbital_period,
    calc_rotation_period,
    calc_obliquity,
    calc_geophysics,
    adjust_for_eccentricity,
    calc_water,
    calc_magnetic_field,
    calc_arf,
    calc_mass_hydrogen,
    calc_mass_helium,
    calc_mass_nitrogen,
    WorldClass,
    calc_world_class,
)
from starch.world import (
    Water,
    Lithosphere,
    WorldType,
    Resonance,
    Tectonics,
    MagneticField,
)
from utils import Dice  # type: ignore

# sys.path.append(os.path.abspath("../starch"))


@pytest.fixture
def worlds_to_use():
    """Pre-defined worlds to use in tests cases."""

    return (
        # t_number-adj is 3
        World(
            world_type=WorldType.LONE,
            planet_mass=0.93,
            star_mass=0.94,
            star_distance=0.892,
            metal=1.21,
        ),
        World(
            world_type=WorldType.SATELLITE,
            satellite_mass=0.023,
            planet_mass=0.876,
            primary_distance=175845,
        ),
        # t_adj is 2   radius planet is 6225.7
        World(
            world_type=WorldType.LONE,
            planet_mass=0.93,
            star_mass=0.94,
            star_distance=0.892,
            age=3.225,
            ecc=0.07,
            grand_tack=True,
            density=0.87,
            metal=0.56,
        ),
        World(
            world_type=WorldType.LONE,
            planet_mass=0.93,
            star_mass=1.256,
            star_distance=0.892,
            age=9.225,
            ecc=0.37,
            orbital_period=6592.5,
            grand_tack=True,
            oort_cloud=True,
            orbital_tidal_heating=True,
        ),
        World(
            world_type=WorldType.ORBITED,
            planet_mass=0.93,
            star_mass=0.14,
            star_distance=0.087,
            primary_distance=125687,
            satellite_mass=0.025,
            age=1.225,
            ecc=0.07,
            grand_tack=True,
            density=1.03,
            metal=0.76,
        ),
        World(
            world_type=WorldType.SATELLITE,
            satellite_mass=0.023,
            primary_distance=175845,
            planet_mass=0.876,
            orbital_period=215.3,
            outside_ice_line=True,
            density=0.567,
            orbital_tidal_heating=True,
        ),
    )


def test_orbital_period(worlds_to_use):
    """Checks period calculated correctly"""
    expected = (
        7617.0,
        215.3,
        7617.0,
        6589.5,
        601.2,
        215.3,
    )
    for n, world in enumerate(worlds_to_use):
        period = calc_orbital_period(world)
        assert period == pytest.approx(expected[n], abs=1e-1), f"Case {n}"


# --------------------------------------------------
def test_rotation_period(worlds_to_use):
    """Checks rotation period calculated correctly"""
    period, lock = calc_rotation_period(worlds_to_use[2], rand=Dice(mocks=[3, 6, 1]))
    assert 24 <= period <= 40
    assert lock.value == Resonance.NONE.value

    period, lock = calc_rotation_period(worlds_to_use[3], rand=Dice(mocks=[5, 6, 5]))
    assert period == pytest.approx(2637.0, abs=1e-1)
    assert lock.value == Resonance.RESONANCE_5_2.value

    period, lock = calc_rotation_period(worlds_to_use[4], rand=Dice(mocks=[1, 2, 1]))
    assert period == pytest.approx(126.2, abs=1e-1)
    assert lock.value == Resonance.LOCK_TO_SATELLITE.value

    period, lock = calc_rotation_period(worlds_to_use[5])
    assert period == pytest.approx(215.3, abs=1e-1)
    assert lock.value == Resonance.LOCK_TO_PRIMARY.value


# --------------------------------------------------
def test_obliquity(worlds_to_use):
    randoms = (
        Dice(mocks=[3, 4, 3]),
        Dice(mocks=[3, 4, 3]),
        Dice(mocks=[2, 2, 1, 1, 1, 5, 4]),
        Dice(mocks=[1, 1, 1, 5, 6, 4]),
        Dice(mocks=[6, 6, 6]),
        Dice(mocks=[2, 2, 1]),
    )
    expected = (
        (32, 36, False),
        (2, 2, False),
        (60, 80, True),
        (46, 49, True),
        (10, 10, False),
        (0, 0, False),
    )
    for n, world in enumerate(worlds_to_use):
        obliquity, instability = calc_obliquity(world, randoms[n])
        lower, upper, expected_instability = expected[n]
        assert lower <= obliquity <= upper, f"Case {n}"
        assert instability is expected_instability, f"Case {n}"


# --------------------------------------------------
def test_day_length(worlds_to_use):
    expected = (23.92, 23.92, 23.92, 23.91, 23.92, 21.59)

    for n, world in enumerate(worlds_to_use):
        assert world.local_day_length == pytest.approx(
            expected[n], abs=1e-2
        ), f"Case {n}"


# --------------------------------------------------
def test_year_length(worlds_to_use):
    expected = (318.375, 318.375, 318.375, 275.687, 318.375, 9.971)

    for n, world in enumerate(worlds_to_use):
        assert world.days_in_local_year == pytest.approx(
            expected[n], abs=1e-3
        ), f"Case {n}"


# --------------------------------------------------
def test_black_body_temp(worlds_to_use):
    expected = (294, 278, 294, 294, 943, 278)

    for n, world in enumerate(worlds_to_use):
        assert world.black_body_temp == expected[n], f"Case {n}"


# --------------------------------------------------
def test_m_number(worlds_to_use):
    expected = (6, 60, 6, 6, 17, 72)

    for n, world in enumerate(worlds_to_use):
        assert world.m_number == expected[n], f"Case {n}"


# --------------------------------------------------
def test_gravity(worlds_to_use):
    expected = (0.976, 0.284, 0.890, 0.976, 0.996, 0.195)

    for n, world in enumerate(worlds_to_use):
        assert world.gravity == pytest.approx(expected[n], abs=1e-3), f"Case {n}"


# --------------------------------------------------
def test_water(worlds_to_use):
    randoms = (
        Dice(mocks=[3, 4, 3]),
        Dice(mocks=[3, 4, 3]),
        Dice(mocks=[1, 5, 5, 1, 1, 5, 4]),
        Dice(mocks=[5, 6, 1, 5, 6, 4]),
        Dice(mocks=[6, 6, 6]),
        Dice(mocks=[2, 2, 1]),
    )
    expected = (
        (Water.MODERATE, 5, 10, False),
        (Water.TRACE, 0, 0, False),
        (Water.MODERATE, 55, 65, False),
        (Water.EXTENSIVE, 75, 85, False),
        (Water.TRACE, 0, 0, True),
        (Water.TRACE, 0, 0, False),
    )
    for n, world in enumerate(worlds_to_use):
        water, percentage, greenhouse = calc_water(world, randoms[n])
        exp_water, lower, upper, exp_greenhouse = expected[n]
        assert water.value == exp_water.value, f"Case {n}"
        assert lower <= percentage <= upper, f"Case {n}"
        assert greenhouse is exp_greenhouse, f"Case {n}"


# --------------------------------------------------
def test_geophysics(worlds_to_use):
    worlds_to_use = list(worlds_to_use)
    worlds_to_use[0] = worlds_to_use[0]._replace(water_percent=5.7)
    worlds_to_use[0] = worlds_to_use[0]._replace(water_prevalence=Water.MODERATE)
    worlds_to_use[2] = worlds_to_use[2]._replace(water_percent=61.0)
    worlds_to_use[2] = worlds_to_use[2]._replace(water_prevalence=Water.MODERATE)
    worlds_to_use[3] = worlds_to_use[3]._replace(water_percent=84.9)
    worlds_to_use[3] = worlds_to_use[3]._replace(water_prevalence=Water.EXTENSIVE)
    worlds_to_use[3] = worlds_to_use[3]._replace(lock=Resonance.RESONANCE_5_2)
    worlds_to_use[5] = worlds_to_use[5]._replace(planet_mass=97.5)
    randoms = (
        Dice(mocks=[3, 4, 3]),
        Dice(mocks=[3, 4, 3, 6, 6, 6]),
        Dice(mocks=[1, 5, 5, 6, 1, 5, 4]),
        Dice(mocks=[5, 6, 4, 5, 6, 6]),
        Dice(mocks=[3, 3, 3]),
        Dice(mocks=[2, 2, 1]),
    )
    expected = (
        (
            Lithosphere.MATURE_PLATE,
            Tectonics.FIXED,
            True,
            Water.MODERATE,
            5.7,
        ),
        (
            Lithosphere.ANCIENT_PLATE,
            Tectonics.FIXED,
            False,
            Water.TRACE,
            0,
        ),
        (
            Lithosphere.MATURE_PLATE,
            Tectonics.MOBILE,
            False,
            Water.MODERATE,
            61.0,
        ),
        (
            Lithosphere.SOLID,
            Tectonics.NONE,
            False,
            Water.EXTENSIVE,
            100,
        ),
        (
            Lithosphere.SOFT,
            Tectonics.NONE,
            False,
            Water.TRACE,
            0,
        ),
        (
            Lithosphere.MOLTEN,
            Tectonics.NONE,
            False,
            Water.TRACE,
            0,
        ),
    )
    for n, world in enumerate(worlds_to_use):
        (
            lithosphere,
            tectonics,
            episodic_resurfacing,
            new_water,
            new_percent,
        ) = calc_geophysics(world, randoms[n])
        exp_litho, exp_tect, exp_episodic, exp_new_water, exp_new_percent = expected[n]
        assert lithosphere == exp_litho, f"Case {n}"
        assert tectonics == exp_tect, f"Case {n}"
        assert episodic_resurfacing is exp_episodic, f"Case {n}"
        assert new_water == exp_new_water, f"Case {n}"
        assert new_percent == pytest.approx(exp_new_percent, abs=1e-1), f"Case {n}"


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
# --------------------------------------------------
def test_calculate_resonance(e, p, expected_period, expected_lock):
    """Checks resonant orbital periods adjusted for eccentricity"""

    result = adjust_for_eccentricity(ecc=e, period=p)
    lock, period = result
    assert period == expected_period
    assert lock.value == expected_lock.value


# --------------------------------------------------
def test_calculate_magnetic_field(worlds_to_use):
    worlds_to_use = list(worlds_to_use)
    worlds_to_use[0] = worlds_to_use[0]._replace(lithosphere=Lithosphere.SOFT)
    worlds_to_use[2] = worlds_to_use[2]._replace(lithosphere=Lithosphere.EARLY_PLATE)
    worlds_to_use[2] = worlds_to_use[2]._replace(tectonics=Tectonics.MOBILE)
    worlds_to_use[3] = worlds_to_use[3]._replace(lithosphere=Lithosphere.ANCIENT_PLATE)
    worlds_to_use[3] = worlds_to_use[3]._replace(tectonics=Tectonics.MOBILE)
    worlds_to_use[5] = worlds_to_use[5]._replace(lithosphere=Lithosphere.MATURE_PLATE)
    worlds_to_use[5] = worlds_to_use[5]._replace(tectonics=Tectonics.MOBILE)
    randoms = (
        Dice(mocks=[3, 4, 5]),
        Dice(mocks=[3, 4, 3, 6, 6, 6]),
        Dice(mocks=[1, 5, 5, 6, 1, 5, 4]),
        Dice(mocks=[5, 6, 4, 5, 6, 6]),
        Dice(mocks=[3, 3, 3]),
        Dice(mocks=[2, 2, 1]),
    )
    expected = (
        MagneticField.WEAK,
        MagneticField.NONE,
        MagneticField.MODERATE,
        MagneticField.STRONG,
        MagneticField.NONE,
        MagneticField.WEAK,
    )
    for n, world in enumerate(worlds_to_use):
        field = calc_magnetic_field(world, randoms[n])
        assert field == expected[n], f"Case {n}"


def test_calculate_arf(worlds_to_use):
    worlds_to_use = list(worlds_to_use)
    worlds_to_use[0] = worlds_to_use[0]._replace(lithosphere=Lithosphere.SOFT)
    worlds_to_use[2] = worlds_to_use[2]._replace(lithosphere=Lithosphere.EARLY_PLATE)
    worlds_to_use[2] = worlds_to_use[2]._replace(water_prevalence=Water.MASSIVE)
    worlds_to_use[2] = worlds_to_use[2]._replace(magnetic_field=MagneticField.STRONG)
    worlds_to_use[3] = worlds_to_use[3]._replace(lithosphere=Lithosphere.ANCIENT_PLATE)
    worlds_to_use[4] = worlds_to_use[4]._replace(green_house=True)
    worlds_to_use[4] = worlds_to_use[4]._replace(magnetic_field=MagneticField.MODERATE)
    worlds_to_use[5] = worlds_to_use[5]._replace(lithosphere=Lithosphere.SOLID)
    worlds_to_use[5] = worlds_to_use[5]._replace(magnetic_field=MagneticField.WEAK)
    randoms = (
        Dice(mocks=[3, 4, 5]),
        Dice(mocks=[3, 4, 3, 6, 6, 6]),
        Dice(mocks=[1, 5, 5, 6, 1, 5, 4]),
        Dice(mocks=[5, 6, 4, 5, 6, 6]),
        Dice(mocks=[3, 3, 3]),
        Dice(mocks=[2, 2, 1]),
    )
    expected = (
        1.0,
        0.0,
        1.9,
        0.7,
        0.9,
        0.0,
    )
    for n, world in enumerate(worlds_to_use):
        field = calc_arf(world, randoms[n])
        assert field == expected[n], f"Case {n}"


def test_calc_mass_hydrogen(mocker):
    worlds = [mocker.Mock(World) for _ in range(3)]
    worlds[0].configure_mock(arf=1.2, m_number=2)
    worlds[1].configure_mock(arf=1.1, m_number=22)
    worlds[2].configure_mock(arf=0.0, m_number=1)

    expected = (
        (108.0, 132.0),
        (0.0, 0.0),
        (0.0, 0.0),
    )
    for n, world in enumerate(worlds):
        field = calc_mass_hydrogen(world)
        lower, upper = expected[n]
        assert lower <= field <= upper, f"Case {n}"


def test_calc_mass_helium(mocker):
    worlds = [mocker.Mock(World) for _ in range(6)]
    worlds[0].configure_mock(arf=0.7, m_number=2)
    worlds[1].configure_mock(arf=0.9, m_number=3)
    worlds[2].configure_mock(arf=2.1, m_number=4)
    worlds[3].configure_mock(arf=0.0, m_number=3)
    worlds[4].configure_mock(arf=2.0, m_number=5)
    worlds[5].configure_mock(arf=1.7, m_number=1)

    expected = (
        (15.75, 19.25),
        (4.05, 4.95),
        (1.89, 2.31),
        (0.0, 0.0),
        (0.0, 0.0),
        (38.25, 46.75),
    )
    for n, world in enumerate(worlds):
        field = calc_mass_helium(world)
        lower, upper = expected[n]
        assert lower <= field <= upper, f"Case {n}"


def test_calc_mass_nitrogen(mocker):
    worlds = [mocker.Mock(World) for _ in range(6)]
    worlds[0].configure_mock(
        arf=2.7, m_number=2, black_body_temp=167, water_prevalence=Water.TRACE
    )
    worlds[1].configure_mock(
        arf=1.0, m_number=14, black_body_temp=85, water_prevalence=Water.MASSIVE
    )
    worlds[2].configure_mock(
        arf=1.0, m_number=8, black_body_temp=278, water_prevalence=Water.EXTENSIVE
    )
    worlds[3].configure_mock(
        arf=0.0, m_number=25, black_body_temp=124, water_prevalence=Water.MASSIVE
    )
    worlds[4].configure_mock(
        arf=2.7, m_number=32, black_body_temp=167, water_prevalence=Water.TRACE
    )
    worlds[5].configure_mock(
        arf=1.6, m_number=1, black_body_temp=77, water_prevalence=Water.TRACE
    )

    expected = (
        (1.701, 2.079),
        (9.45, 11.55),
        (0.63, 0.77),
        (0.0, 0.0),
        (0.0, 0.0),
        (0.0, 0.0),
    )
    for n, world in enumerate(worlds):
        field = calc_mass_nitrogen(world)
        lower, upper = expected[n]
        assert lower <= field <= upper, f"Case {n}"


def test_calc_world_class(mocker):
    worlds = [mocker.Mock(World) for _ in range(6)]
    worlds[0].configure_mock(
        green_house=True,
        black_body_temp=85,
        mass_hydrogen=55.3,
        mass_helium=23.0,
        mass_nitrogen=0.0,
        m_number=7,
    )
    worlds[1].configure_mock(
        green_house=False,
        black_body_temp=105,
        mass_hydrogen=70.0,
        mass_helium=23.0,
        mass_nitrogen=2.0,
        m_number=2,
    )
    worlds[2].configure_mock(
        green_house=False,
        black_body_temp=105,
        mass_hydrogen=0.0,
        mass_helium=23.0,
        mass_nitrogen=2.0,
        m_number=3,
    )
    worlds[3].configure_mock(
        green_house=False,
        black_body_temp=278,
        mass_hydrogen=0.0,
        mass_helium=2.2,
        mass_nitrogen=1.2,
        m_number=8,
    )
    worlds[4].configure_mock(
        green_house=False,
        black_body_temp=205,
        mass_hydrogen=0.0,
        mass_helium=0.0,
        mass_nitrogen=0.0,
        m_number=32,
    )
    worlds[5].configure_mock(
        green_house=False,
        black_body_temp=85,
        mass_hydrogen=0.0,
        mass_helium=0.0,
        mass_nitrogen=0.0,
        m_number=55,
    )

    expected = (
        WorldClass.ONE,
        WorldClass.TWO,
        WorldClass.THREE,
        WorldClass.FOUR,
        WorldClass.FIVE,
        WorldClass.SIX,
    )
    for n, world in enumerate(worlds):
        world_class = calc_world_class(world)

        assert world_class == expected[n], f"Case {n}"
