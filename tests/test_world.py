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
    calc_albedo,
    calc_mass_carbon_dioxide,
    calc_abio_vents,
    calc_abio_surface,
    calc_multicellular,
    calc_photosynthesis,
    calc_oxygen_cat,
    calc_animals,
    calc_presentients,
    calc_mass_oxygen,
    calc_surface_temp_1,
    adjust_carbon_dioxide,
    calc_water_vapour,
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


def test_calc_albedo(mocker):
    worlds = [mocker.Mock(World) for _ in range(12)]
    worlds[0].configure_mock(
        black_body_temp=342,
        world_class=WorldClass.ONE,
        water_prevalence=Water.TRACE,
        lithosphere=Lithosphere.ANCIENT_PLATE,
        tectonics=Tectonics.FIXED,
    )
    worlds[1].configure_mock(
        black_body_temp=342,
        world_class=WorldClass.TWO,
        water_prevalence=Water.TRACE,
        lithosphere=Lithosphere.ANCIENT_PLATE,
        tectonics=Tectonics.FIXED,
    )
    worlds[2].configure_mock(
        black_body_temp=342,
        world_class=WorldClass.THREE,
        water_prevalence=Water.TRACE,
        lithosphere=Lithosphere.ANCIENT_PLATE,
        tectonics=Tectonics.FIXED,
    )
    worlds[3].configure_mock(
        black_body_temp=342,
        world_class=WorldClass.FOUR,
        water_prevalence=Water.TRACE,
        lithosphere=Lithosphere.ANCIENT_PLATE,
        tectonics=Tectonics.FIXED,
    )
    worlds[4].configure_mock(
        black_body_temp=342,
        world_class=WorldClass.FOUR,
        water_prevalence=Water.MASSIVE,
        lithosphere=Lithosphere.ANCIENT_PLATE,
        tectonics=Tectonics.FIXED,
    )
    worlds[5].configure_mock(
        black_body_temp=342,
        world_class=WorldClass.FIVE,
        water_prevalence=Water.MINIMAL,
        lithosphere=Lithosphere.ANCIENT_PLATE,
        tectonics=Tectonics.FIXED,
    )
    worlds[6].configure_mock(
        black_body_temp=342,
        world_class=WorldClass.FIVE,
        water_prevalence=Water.MODERATE,
        lithosphere=Lithosphere.ANCIENT_PLATE,
        tectonics=Tectonics.FIXED,
    )
    worlds[7].configure_mock(
        black_body_temp=342,
        world_class=WorldClass.FIVE,
        water_prevalence=Water.EXTENSIVE,
        lithosphere=Lithosphere.ANCIENT_PLATE,
        tectonics=Tectonics.FIXED,
    )
    worlds[8].configure_mock(
        black_body_temp=342,
        world_class=WorldClass.SIX,
        water_prevalence=Water.EXTENSIVE,
        lithosphere=Lithosphere.ANCIENT_PLATE,
        tectonics=Tectonics.FIXED,
    )
    worlds[9].configure_mock(
        black_body_temp=342,
        world_class=WorldClass.SIX,
        water_prevalence=Water.MINIMAL,
        lithosphere=Lithosphere.SOLID,
        tectonics=Tectonics.FIXED,
    )
    worlds[10].configure_mock(
        black_body_temp=342,
        world_class=WorldClass.SIX,
        water_prevalence=Water.MODERATE,
        lithosphere=Lithosphere.EARLY_PLATE,
        tectonics=Tectonics.FIXED,
    )
    worlds[11].configure_mock(
        black_body_temp=70,
        world_class=WorldClass.SIX,
        water_prevalence=Water.MASSIVE,
        lithosphere=Lithosphere.SOLID,
        tectonics=Tectonics.NONE,
    )
    randoms = (
        Dice(mocks=[3, 4, 5]),
        Dice(mocks=[3, 4, 3, 6, 6, 6]),
        Dice(mocks=[1, 5, 5, 6, 1, 5, 4]),
        Dice(mocks=[5, 6, 4, 5, 6, 6]),
        Dice(mocks=[3, 3, 3]),
        Dice(mocks=[2, 2, 1]),
        Dice(mocks=[2, 5, 4]),
        Dice(mocks=[3, 3, 3]),
        Dice(mocks=[2, 5, 4]),
        Dice(mocks=[2, 2, 1]),
        Dice(mocks=[2, 5, 4]),
        Dice(mocks=[3, 3, 3]),
    )
    expected = (0.77, 0.3, 0.21, 0.3, 0.34, 0.21, 0.3, 0.31, 0.55, 0.07, 0.49, 0.59)
    for n, world in enumerate(worlds):
        albedo = calc_albedo(world, randoms[n])

        assert albedo == pytest.approx(expected[n]), f"Case {n}"


def test_calc_mass_carbon_dioxide(mocker):
    worlds = [mocker.Mock(World) for _ in range(6)]
    worlds[0].configure_mock(
        arf=2.7, m_number=7, black_body_temp=167, world_class=WorldClass.ONE
    )
    worlds[1].configure_mock(
        arf=1.7, m_number=7, black_body_temp=200, world_class=WorldClass.TWO
    )
    worlds[2].configure_mock(
        arf=2.7, m_number=7, black_body_temp=167, world_class=WorldClass.THREE
    )
    worlds[3].configure_mock(
        arf=2.7, m_number=55, black_body_temp=254, world_class=WorldClass.FOUR
    )
    worlds[4].configure_mock(
        arf=0.5, m_number=42, black_body_temp=254, world_class=WorldClass.FIVE
    )
    worlds[5].configure_mock(
        arf=2.4, m_number=7, black_body_temp=200, world_class=WorldClass.SIX
    )

    expected = (
        (243.0, 297.0),
        (15.3, 18.7),
        (0.0, 0.0),
        (0.0, 0.0),
        (4.5, 5.5),
        (0.0, 0.0),
    )
    for n, world in enumerate(worlds):
        field = calc_mass_carbon_dioxide(world)
        lower, upper = expected[n]
        assert lower <= field <= upper, f"Case {n}"


def test_calc_ccs():
    worlds = [World() for _ in range(6)]
    worlds[0] = worlds[0]._replace(
        albedo=0.27,
        luminosity=1.776,
        mass_carbon_dioxide=5.3,
        water_prevalence=Water.MODERATE,
    )
    worlds[1] = worlds[1]._replace(
        albedo=0.27,
        luminosity=1.776,
        mass_carbon_dioxide=5.3,
        water_prevalence=Water.EXTENSIVE,
    )
    worlds[2] = worlds[2]._replace(
        albedo=0.27,
        luminosity=0.035889,
        mass_carbon_dioxide=5.3,
        water_prevalence=Water.EXTENSIVE,
    )
    worlds[3] = worlds[3]._replace(
        albedo=0.27,
        luminosity=1.776,
        mass_carbon_dioxide=5.3,
        water_prevalence=Water.MASSIVE,
    )
    worlds[4] = worlds[4]._replace(
        albedo=0.27,
        luminosity=1.776,
        mass_carbon_dioxide=5.3,
        water_prevalence=Water.TRACE,
    )
    worlds[5] = worlds[5]._replace(
        albedo=0.27,
        luminosity=1.776,
        mass_carbon_dioxide=0.0,
        water_prevalence=Water.EXTENSIVE,
    )

    expected = (
        True,
        True,
        False,
        False,
        False,
        False,
    )
    for n, world in enumerate(worlds):
        assert world.carbon_silicate_cycle is expected[n], f"Case {n}"


def test_calc_abio_vents(mocker):
    worlds = [mocker.Mock(World) for _ in range(7)]
    worlds[0].configure_mock(
        water_prevalence=Water.EXTENSIVE,
        world_class=WorldClass.TWO,
        lithosphere=Lithosphere.SOFT,
        tectonics=Tectonics.MOBILE,
        age=4.5,
    )
    worlds[1].configure_mock(
        water_prevalence=Water.MODERATE,
        world_class=WorldClass.TWO,
        lithosphere=Lithosphere.SOFT,
        tectonics=Tectonics.MOBILE,
        age=4.5,
    )
    worlds[2].configure_mock(
        water_prevalence=Water.EXTENSIVE,
        world_class=WorldClass.ONE,
        lithosphere=Lithosphere.SOFT,
        tectonics=Tectonics.MOBILE,
        age=4.5,
    )
    worlds[3].configure_mock(
        water_prevalence=Water.EXTENSIVE,
        world_class=WorldClass.TWO,
        lithosphere=Lithosphere.SOFT,
        tectonics=Tectonics.MOBILE,
        age=0.2,
    )
    worlds[4].configure_mock(
        water_prevalence=Water.EXTENSIVE,
        world_class=WorldClass.TWO,
        lithosphere=Lithosphere.SOLID,
        tectonics=Tectonics.MOBILE,
        age=4.5,
    )
    worlds[5].configure_mock(
        water_prevalence=Water.EXTENSIVE,
        world_class=WorldClass.TWO,
        lithosphere=Lithosphere.SOFT,
        tectonics=Tectonics.FIXED,
        age=4.5,
    )
    worlds[6].configure_mock(
        water_prevalence=Water.EXTENSIVE,
        world_class=WorldClass.TWO,
        lithosphere=Lithosphere.SOFT,
        tectonics=Tectonics.NONE,
        age=4.5,
    )

    randoms = (
        Dice(mocks=[3, 4, 5]),
        Dice(mocks=[3, 4, 3, 6, 6, 6]),
        Dice(mocks=[1, 5, 5, 6, 1, 5, 4]),
        Dice(mocks=[5, 6, 4, 5, 6, 6]),
        Dice(mocks=[3, 3, 3]),
        Dice(mocks=[2, 2, 1]),
        Dice(mocks=[2, 5, 4]),
    )

    expected = (
        (True, 360),
        (True, 300),
        (False, None),
        (False, None),
        (False, None),
        (False, None),
        (True, 330),
    )

    for n, world in enumerate(worlds):
        present, time = calc_abio_vents(world, randoms[n])
        exp_present, exp_time = expected[n]
        assert present is exp_present, f"Case {n}"
        assert time == exp_time, f"Case {n}"


def test_calc_abio_surface():
    worlds = [World() for _ in range(6)]
    worlds[0] = worlds[0]._replace(
        albedo=0.27,
        luminosity=1.776,
        mass_carbon_dioxide=5.3,
        water_prevalence=Water.MODERATE,
        lithosphere=Lithosphere.SOFT,
        world_class=WorldClass.TWO,
        abio_vents_occurred=True,
        time_to_abio_vents=180,
    )
    worlds[1] = worlds[1]._replace(
        albedo=0.27,
        luminosity=1.776,
        mass_carbon_dioxide=5.3,
        water_prevalence=Water.MODERATE,
        lithosphere=Lithosphere.EARLY_PLATE,
        world_class=WorldClass.FOUR,
        abio_vents_occurred=True,
        time_to_abio_vents=30,
    )
    worlds[2] = worlds[2]._replace(
        albedo=0.27,
        luminosity=0.035889,
        mass_carbon_dioxide=5.3,
        water_prevalence=Water.MODERATE,
        lithosphere=Lithosphere.SOFT,
        world_class=WorldClass.TWO,
    )
    worlds[3] = worlds[3]._replace(
        albedo=0.27,
        luminosity=1.776,
        mass_carbon_dioxide=5.3,
        water_prevalence=Water.MODERATE,
        lithosphere=Lithosphere.SOFT,
        world_class=WorldClass.ONE,
    )
    worlds[4] = worlds[4]._replace(
        albedo=0.27,
        luminosity=1.776,
        mass_carbon_dioxide=5.3,
        water_prevalence=Water.MODERATE,
        lithosphere=Lithosphere.SOFT,
        world_class=WorldClass.THREE,
    )
    worlds[5] = worlds[5]._replace(
        albedo=0.27,
        luminosity=1.776,
        mass_carbon_dioxide=5.3,
        water_prevalence=Water.MODERATE,
        lithosphere=Lithosphere.SOFT,
        world_class=WorldClass.SIX,
    )

    expected = (
        (True, 1200),
        (True, 2250),
        (False, None),
        (False, None),
        (False, None),
        (False, None),
    )

    randoms = (
        Dice(mocks=[3, 4, 5]),
        Dice(mocks=[6, 5, 6, 6, 6, 6]),
        Dice(mocks=[1, 5, 5, 6, 1, 5, 4]),
        Dice(mocks=[5, 6, 4, 5, 6, 6]),
        Dice(mocks=[3, 3, 3]),
        Dice(mocks=[2, 2, 1]),
    )

    for n, world in enumerate(worlds):
        present, time = calc_abio_surface(world, randoms[n])
        exp_present, exp_time = expected[n]
        assert present is exp_present, f"Case {n}"
        assert time == exp_time, f"Case {n}"


def test_calc_time_to_multicellular(mocker):
    worlds = [mocker.Mock(World) for _ in range(6)]
    worlds[0].configure_mock(
        abio_vents_occurred=True,
        time_to_abio_vents=30,
        abio_surface_occurred=True,
        time_to_abio_surface=3000,
        age=4.5,
    )
    worlds[1].configure_mock(
        abio_vents_occurred=True,
        time_to_abio_vents=2020,
        abio_surface_occurred=True,
        time_to_abio_surface=2000,
        age=4.5,
    )
    worlds[2].configure_mock(
        abio_vents_occurred=False,
        time_to_abio_vents=None,
        abio_surface_occurred=True,
        time_to_abio_surface=2000,
        age=4.5,
    )
    worlds[3].configure_mock(
        abio_vents_occurred=True,
        time_to_abio_vents=180,
        abio_surface_occurred=False,
        time_to_abio_surface=None,
        age=4.5,
    )
    worlds[4].configure_mock(
        abio_vents_occurred=False,
        time_to_abio_vents=None,
        abio_surface_occurred=False,
        time_to_abio_surface=None,
        age=4.5,
    )
    worlds[5].configure_mock(
        abio_vents_occurred=True,
        time_to_abio_vents=2020,
        abio_surface_occurred=True,
        time_to_abio_surface=2000,
        age=2.1,
    )

    randoms = (
        Dice(mocks=[3, 4, 5]),
        Dice(mocks=[3, 4, 3, 6, 6, 6]),
        Dice(mocks=[1, 5, 5, 6, 1, 5, 4]),
        Dice(mocks=[5, 6, 4, 5, 6, 6]),
        Dice(mocks=[3, 3, 3]),
        Dice(mocks=[3, 3, 3]),
    )

    expected = (
        (True, 930),
        (True, 2750),
        (True, 2825),
        (True, 1305),
        (False, None),
        (False, None),
    )

    for n, world in enumerate(worlds):
        present, time = calc_multicellular(world, randoms[n])
        exp_present, exp_time = expected[n]
        assert present is exp_present, f"Case {n}"
        assert time == exp_time, f"Case {n}"


def test_calc_photosynthesis(mocker):
    worlds = [World() for _ in range(6)]
    worlds[0] = worlds[0]._replace(
        abio_surface_occurred=True,
        time_to_abio_surface=3000,
        star_spectrum="G2",
        age=4.5,
    )
    worlds[1] = worlds[1]._replace(
        abio_surface_occurred=True,
        time_to_abio_surface=2000,
        star_spectrum="G8",
        age=4.5,
    )
    worlds[2] = worlds[2]._replace(
        abio_surface_occurred=True,
        time_to_abio_surface=1000,
        star_spectrum="K5",
        age=4.5,
    )
    worlds[3] = worlds[3]._replace(
        abio_surface_occurred=False,
        time_to_abio_surface=None,
        star_spectrum="G2",
        age=4.5,
    )
    worlds[4] = worlds[4]._replace(
        abio_surface_occurred=True,
        time_to_abio_surface=None,
        star_spectrum="BD",
        age=4.5,
    )
    worlds[5] = worlds[5]._replace(
        abio_surface_occurred=True,
        time_to_abio_surface=2000,
        star_spectrum="G2",
        age=1.9,
    )

    randoms = (
        Dice(mocks=[3, 4, 5]),
        Dice(mocks=[3, 4, 3, 6, 6, 6]),
        Dice(mocks=[1, 5, 5, 6, 1, 5, 4]),
        Dice(mocks=[5, 6, 4, 5, 6, 6]),
        Dice(mocks=[3, 3, 3]),
        Dice(mocks=[3, 3, 3]),
    )

    expected = (
        (True, 4200),
        (True, 3050),
        (True, 2760),
        (False, None),
        (False, None),
        (False, None),
    )

    for n, world in enumerate(worlds):
        present, time = calc_photosynthesis(world, randoms[n])
        exp_present, exp_time = expected[n]
        assert present is exp_present, f"Case {n}"
        assert time == exp_time, f"Case {n}"


def test_calc_oxygen_present(mocker):
    worlds = [World() for _ in range(6)]
    worlds[0] = worlds[0]._replace(
        photosynthesis_occurred=True,
        time_to_photosynthesis=2000,
        star_spectrum="G2",
        age=4.5,
    )
    worlds[1] = worlds[1]._replace(
        photosynthesis_occurred=True,
        time_to_photosynthesis=3000,
        star_spectrum="G8",
        age=4.8,
    )
    worlds[2] = worlds[2]._replace(
        photosynthesis_occurred=True,
        time_to_photosynthesis=3000,
        star_spectrum="K5",
        age=6.5,
    )
    worlds[3] = worlds[3]._replace(
        photosynthesis_occurred=False,
        time_to_photosynthesis=3000,
        star_spectrum="G2",
        age=4.8,
    )
    worlds[4] = worlds[4]._replace(
        photosynthesis_occurred=True,
        time_to_photosynthesis=2000,
        star_spectrum="M2",
        age=7.0,
    )
    worlds[5] = worlds[5]._replace(
        photosynthesis_occurred=True,
        time_to_photosynthesis=3000,
        star_spectrum="G2",
        age=1.9,
    )

    randoms = (
        Dice(mocks=[3, 4, 5]),
        Dice(mocks=[3, 4, 3, 6, 6, 6]),
        Dice(mocks=[1, 5, 5, 6, 1, 5, 4]),
        Dice(mocks=[5, 6, 4, 5, 6, 6]),
        Dice(mocks=[3, 3, 3]),
        Dice(mocks=[3, 3, 3]),
    )

    expected = (
        (True, 3800),
        (True, 4575),
        (True, 5640),
        (False, None),
        (True, 6050),
        (False, None),
    )

    for n, world in enumerate(worlds):
        present, time = calc_oxygen_cat(world, randoms[n])
        exp_present, exp_time = expected[n]
        assert present is exp_present, f"Case {n}"
        assert time == exp_time, f"Case {n}"


def test_calc_animals(mocker):
    worlds = [World() for _ in range(6)]
    worlds[0] = worlds[0]._replace(
        multicellular_occured=True,
        time_to_multicellular=2000,
        time_to_oxygen=3100,
        oxygen_occurred=True,
        age=4.5,
    )
    worlds[1] = worlds[1]._replace(
        multicellular_occured=True,
        time_to_multicellular=2000,
        time_to_oxygen=3100,
        oxygen_occurred=True,
        age=3.25,
    )
    worlds[2] = worlds[2]._replace(
        multicellular_occured=True,
        time_to_multicellular=700,
        time_to_oxygen=6100,
        oxygen_occurred=True,
        age=4.5,
    )
    worlds[3] = worlds[3]._replace(
        multicellular_occured=True,
        time_to_multicellular=700,
        time_to_oxygen=6100,
        oxygen_occurred=True,
        age=4.5,
    )
    worlds[4] = worlds[4]._replace(
        multicellular_occured=True,
        time_to_multicellular=700,
        time_to_oxygen=None,
        oxygen_occurred=False,
        age=4.5,
    )
    worlds[5] = worlds[5]._replace(
        multicellular_occured=True,
        time_to_multicellular=700,
        time_to_oxygen=6100,
        oxygen_occurred=True,
        age=1.5,
    )

    randoms = (
        Dice(mocks=[3, 4, 5]),
        Dice(mocks=[3, 4, 3, 6, 6, 6]),
        Dice(mocks=[1, 5, 5, 6, 1, 5, 4]),
        Dice(mocks=[5, 6, 4, 5, 6, 6]),
        Dice(mocks=[3, 3, 3]),
        Dice(mocks=[3, 3, 3]),
    )

    expected = (
        (True, 4350),
        (False, None),
        (True, 4000),
        (False, None),
        (True, 3400),
        (False, None),
    )

    for n, world in enumerate(worlds):
        present, time = calc_animals(world, randoms[n])
        exp_present, exp_time = expected[n]
        assert present is exp_present, f"Case {n}"
        assert time == exp_time, f"Case {n}"


def test_calc_presentient(mocker):
    worlds = [World() for _ in range(6)]
    worlds[0] = worlds[0]._replace(
        animals_occurred=True,
        time_to_animals=4300,
        water_prevalence=Water.EXTENSIVE,
        age=5.5,
    )
    worlds[1] = worlds[1]._replace(
        animals_occurred=True,
        time_to_animals=4300,
        water_prevalence=Water.EXTENSIVE,
        age=4.0,
    )
    worlds[2] = worlds[2]._replace(
        animals_occurred=True,
        time_to_animals=4300,
        water_prevalence=Water.MASSIVE,
        age=6.2,
    )
    worlds[3] = worlds[3]._replace(
        animals_occurred=True,
        time_to_animals=4300,
        water_prevalence=Water.MASSIVE,
        age=3.2,
    )
    worlds[4] = worlds[4]._replace(
        animals_occurred=True,
        time_to_animals=3300,
        water_prevalence=Water.MODERATE,
        age=4.3,
    )
    worlds[5] = worlds[5]._replace(
        animals_occurred=False,
        time_to_animals=3300,
        water_prevalence=Water.MODERATE,
        age=4.3,
    )

    randoms = (
        Dice(mocks=[3, 4, 5]),
        Dice(mocks=[3, 4, 3, 6, 6, 6]),
        Dice(mocks=[1, 5, 5, 6, 1, 5, 4]),
        Dice(mocks=[5, 6, 4, 5, 6, 6]),
        Dice(mocks=[3, 3, 3]),
        Dice(mocks=[3, 3, 3]),
    )

    expected = (
        (True, 4900),
        (False, None),
        (True, 5400),
        (False, None),
        (True, 3750),
        (False, None),
    )

    for n, world in enumerate(worlds):
        present, time = calc_presentients(world, randoms[n])
        exp_present, exp_time = expected[n]
        assert present is exp_present, f"Case {n}"
        assert time == exp_time, f"Case {n}"


def test_calc_mass_oxygen(mocker):
    worlds = [mocker.Mock(World) for _ in range(4)]
    worlds[0].configure_mock(
        arf=2.7, photosynthesis_occurred=True, oxygen_occurred=False
    )
    worlds[1].configure_mock(
        arf=1.7,
        photosynthesis_occurred=False,
        oxygen_occurred=False,
    )
    worlds[2].configure_mock(
        arf=2.4,
        photosynthesis_occurred=True,
        oxygen_ocurred=True,
    )
    worlds[3].configure_mock(
        arf=1.7,
        photosynthesis_occurred=True,
        oxygen_ocurred=True,
    )
    randoms = (
        Dice(mocks=[3, 4, 5]),
        Dice(mocks=[3, 4, 3, 6, 6, 6]),
        Dice(mocks=[1, 5, 5, 6, 1, 5, 4]),
        Dice(mocks=[5, 6, 4, 5, 6, 6]),
    )
    expected = (
        0.024,
        0.0,
        0.624,
        0.51,
    )
    for n, world in enumerate(worlds):
        assert calc_mass_oxygen(world, randoms[n]) == expected[n], f"Case {n}"


def test_calc_surface_temp():
    worlds = [World() for _ in range(6)]
    worlds[0] = worlds[0]._replace(
        world_class=WorldClass.ONE,
        mass_carbon_dioxide=65.3,
        albedo=0.75,
    )
    worlds[1] = worlds[1]._replace(
        world_class=WorldClass.SIX,
        albedo=0.3,
    )
    worlds[2] = worlds[2]._replace(
        world_class=WorldClass.TWO,
        arf=0.0,
        albedo=0.25,
    )
    worlds[3] = worlds[3]._replace(
        world_class=WorldClass.FOUR,
        abio_vents_occurred=True,
        arf=1.2,
        tectonics=Tectonics.FIXED,
        water_prevalence=Water.MINIMAL,
        albedo=0.25,
    )
    worlds[4] = worlds[4]._replace(
        world_class=WorldClass.TWO,
        arf=1.2,
        tectonics=Tectonics.FIXED,
        water_prevalence=Water.MINIMAL,
        albedo=0.25,
    )
    worlds[5] = worlds[5]._replace(
        world_class=WorldClass.FOUR,
        arf=0.9,
        oxygen_occurred=True,
        albedo=0.25,
        abio_vents_occurred=True,
    )

    expected = (
        (650, False, False),
        (254, False, False),
        (259, False, False),
        (261, True, False),
        (261, True, False),
        (261, True, True),
    )
    for n, world in enumerate(worlds):
        temp, trace_methane, trace_ozone = calc_surface_temp_1(world)
        exp_temp, exp_methane, exp_ozone = expected[n]
        assert temp == exp_temp, f"Case {n} temp"
        assert trace_methane == exp_methane, f"Case {n} methane"
        assert trace_ozone == exp_ozone, f"Case {n} methane"


def test_adjust_carbon_dioxide():
    worlds = [World() for _ in range(4)]
    worlds[0] = worlds[0]._replace(
        world_class=WorldClass.ONE,
        mass_carbon_dioxide=65.3,
        surf_temp=240,
    )
    worlds[1] = worlds[1]._replace(
        world_class=WorldClass.FOUR,
        mass_carbon_dioxide=4.0,
        water_prevalence=Water.MINIMAL,
        surf_temp=278,
    )
    worlds[2] = worlds[2]._replace(
        world_class=WorldClass.FOUR,
        mass_carbon_dioxide=7.2,
        water_prevalence=Water.MODERATE,
        surf_temp=278,
    )
    worlds[3] = worlds[3]._replace(
        world_class=WorldClass.FOUR,
        mass_carbon_dioxide=6.7,
        water_prevalence=Water.MODERATE,
        surf_temp=240,
    )

    randoms = (
        Dice(mocks=[3, 4, 5]),
        Dice(mocks=[3, 4, 3, 6, 6, 6]),
        Dice(mocks=[1, 5, 5, 6, 1, 5, 4]),
        Dice(mocks=[5, 6, 4, 5, 6, 6]),
    )
    expected = (
        (291, 65.3),
        (319, 4.0),
        (290, 9.95e-4),
        (268, 0.09884),
    )
    for n, world in enumerate(worlds):
        new_temp, new_mass_co2 = adjust_carbon_dioxide(world, randoms[n])
        exp_temp, exp_mass_co2 = expected[n]
        assert new_temp == exp_temp, f"Case {n} temp"
        assert new_mass_co2 == pytest.approx(
            exp_mass_co2, abs=1e-6
        ), f"Case {n} carbon dioxide"


def test_calc_water_vapour():
    worlds = [World() for _ in range(6)]
    worlds[0] = worlds[0]._replace(
        world_class=WorldClass.FOUR,
        water_prevalence=Water.TRACE,
        surf_temp=240,
    )
    worlds[1] = worlds[1]._replace(
        world_class=WorldClass.FOUR,
        water_prevalence=Water.EXTENSIVE,
        surf_temp=278,
    )
    worlds[2] = worlds[2]._replace(
        world_class=WorldClass.FOUR,
        water_prevalence=Water.MASSIVE,
        surf_temp=265,
    )
    worlds[3] = worlds[3]._replace(
        world_class=WorldClass.FOUR,
        water_prevalence=Water.MODERATE,
        surf_temp=315,
    )
    worlds[4] = worlds[4]._replace(
        world_class=WorldClass.FOUR,
        water_prevalence=Water.MODERATE,
        surf_temp=328,
    )
    worlds[5] = worlds[5]._replace(
        world_class=WorldClass.FOUR,
        water_prevalence=Water.MODERATE,
        surf_temp=259,
    )

    expected = (
        (240, 0.0),
        (304, 0.031333),
        (287, 0.009924),
        (348, 0.234323),
        (363, 0.416366),
        (259, 1.78e-5),
    )
    for n, world in enumerate(worlds):
        new_temp, mass_vapour = calc_water_vapour(world)
        exp_temp, exp_mass_vapour = expected[n]
        assert new_temp == exp_temp, f"Case {n} temp"
        assert mass_vapour == pytest.approx(
            exp_mass_vapour, abs=1e-6
        ), f"Case {n} carbon dioxide"
