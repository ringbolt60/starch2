#!/usr/bin/env python3
"""
Author : Jon Walters <ringbolt60@gmail.com>
Date   : 2023-08-27
Purpose: Create worlds.
"""

import argparse
import itertools
import math
import random
from enum import Enum
from typing import Tuple

import pytest


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Create worlds.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("name", metavar="str", help="The name of the world")

    parser.add_argument(
        "type",
        metavar="str",
        help="The type of the world",
        choices=["lone", "orbited", "satellite"],
    )

    parser.add_argument(
        "-m",
        "--mass",
        help="Mass of primary in Earth masses",
        metavar="mass",
        type=float,
        default="1.0",
    )

    parser.add_argument(
        "-M",
        "--mass_star",
        help="Mass of star in Sol masses",
        metavar="mass",
        type=float,
        default="1.0",
    )

    parser.add_argument(
        "-D",
        "--distance_star",
        help="Distance of star in AU",
        metavar="distance",
        type=float,
        default="1.0",
    )

    parser.add_argument(
        "-s",
        "--satellite_mass",
        help="Mass of satellite in Earth masses",
        metavar="distance au",
        type=float,
        default="0.0123",
    )

    parser.add_argument(
        "-d",
        "--distance_primary",
        help="Distance of satellite in km",
        metavar="distance km",
        type=float,
        default="384400",
    )

    parser.add_argument(
        "-a",
        "--age",
        help="Age of system in billions of years",
        metavar="float",
        type=float,
        default="4.568",
    )

    parser.add_argument(
        "-k",
        "--density",
        help="Density of world in earth densities",
        metavar="float",
        type=float,
        default="1.0",
    )

    parser.add_argument(
        "-e",
        "--ecc",
        help="Eccentricity of orbit",
        metavar="float",
        type=float,
        default="0.01",
    )

    args = parser.parse_args()

    for attr in (
        "mass",
        "mass_star",
        "distance_star",
        "satellite_mass",
        "distance_primary",
        "age",
        "density",
        "ecc",
    ):
        a = getattr(args, attr)
        if a <= 0:
            parser.error(f'"{a}" should be a positive float')

    if args.type == "lone":
        args.type = WorldType.LONE
    if args.type == "orbited":
        args.type = WorldType.ORBITED
    if args.type == "satellite":
        args.type = WorldType.SATELLITE

    return args


# --------------------------------------------------
def main():
    """Start doing stuff here."""

    args = get_args()
    name = args.name
    world_type = args.type
    planet_mass = args.mass
    star_mass = args.mass_star
    star_distance = args.distance_star
    satellite_mass = args.satellite_mass
    primary_distance = args.distance_primary
    age = args.age
    density = args.density
    if world_type == WorldType.SATELLITE:
        radius = calculate_radius(density, satellite_mass)
    else:
        radius = calculate_radius(density, planet_mass)
    period = calc_orbital_period(
        world_type,
        star_mass=star_mass,
        star_distance=star_distance,
        planet_mass=planet_mass,
        satellite_mass=satellite_mass,
        primary_distance=primary_distance,
    )
    ecc = args.ecc
    rotation_period, lock = calc_rotation_period(
        world_type,
        star_mass=star_mass,
        star_distance=star_distance,
        planet_mass=planet_mass,
        satellite_mass=satellite_mass,
        primary_distance=primary_distance,
        orbital_period=period,
        radius=radius,
        age=age,
        ecc=ecc,
    )

    match world_type:
        case WorldType.LONE:
            print(
                f"{name}\n"
                f"{world_type.value} Age: {age:.3f} GYr\n"
                f"Mass: {planet_mass:.3f} M♁ Density: {density:.3f} K♁ Radius: {radius:.0f} km\n"
                f"Star Mass: {star_mass:.3f} M☉ Distance: {star_distance:.3f} AU\n"
                f"---\n"
                f"Orbital Period = {period:.1f} hours\n"
                f"Rotation Period = {rotation_period:.1f} hours ({lock})"
            )
        case WorldType.ORBITED:
            print(
                f"{name}\n"
                f"{world_type.value} Age: {age:.3f} GYr\n"
                f"Mass: {planet_mass:.3f} M♁ Density: {density:.3f} K♁ Radius: {radius:.0f} km\n"
                f"Star Mass: {star_mass:.3f} M☉ Distance: {star_distance:.3f} AU\n"
                f"Satellite Mass: {satellite_mass:.3f} M♁ Distance: {primary_distance:.0f} km\n"
                f"---\n"
                f"Orbital Period = {period:.1f} hours\n"
                f"Rotation Period = {rotation_period:.1f} hours ({lock})"
            )
        case WorldType.SATELLITE:
            print(
                f"{name}\n"
                f"{world_type.value} Age: {age:.3f} GYr\n"
                f"Mass: {satellite_mass:.3f} M♁ Density: {density:.3f} K♁ Radius: {radius:.0f} km\n"
                f"Star Mass: {star_mass:.3f} M☉ Distance: {star_distance:.3f} AU\n"
                f"Primary Mass: {planet_mass:.3f} M♁ Distance: {primary_distance:.0f} km\n"
                f"---\n"
                f"Orbital Period = {period:.1f} hours\n"
                f"Rotation Period = {rotation_period:.1f} hours ({lock})"
            )


# --------------------------------------------------
class WorldType(Enum):
    LONE = "Lone Planet"
    ORBITED = "Planet with Satellite"
    SATELLITE = "Satellite"


# --------------------------------------------------
def calc_orbital_period(
    world_type: WorldType,
    planet_mass: float = 1.0,
    star_mass: float = 1.0,
    star_distance: float = 1.0,
    satellite_mass: float = 0.0123,
    primary_distance: float = 384400.0,
) -> float:
    """
    Returns orbital period around primary in hours.

    Implements Step 18 pp 92,93. Constants tweaked to make earth and Luna exact.
    """
    if world_type is WorldType.SATELLITE:
        return 2.768e-6 * math.sqrt(
            math.pow(primary_distance, 3) / (satellite_mass + planet_mass)
        )
    else:
        return 8766.0 * math.sqrt(math.pow(star_distance, 3) / star_mass)


# --------------------------------------------------
def test_orbital_period():
    """Checks period calculated correctly"""
    period_lone = calc_orbital_period(
        world_type=WorldType.LONE, planet_mass=0.93, star_mass=0.94, star_distance=0.892
    )
    assert period_lone == pytest.approx(7617.0, abs=1e-1)

    period_satellite = calc_orbital_period(
        world_type=WorldType.SATELLITE,
        satellite_mass=0.023,
        primary_distance=175845,
        planet_mass=0.876,
    )
    assert period_satellite == pytest.approx(215.3, abs=1e-1)


# --------------------------------------------------
class Dice:
    """Generator producing a stream of six sided dice rolls."""

    def __init__(self, seed: int | None = None, mocks=None):
        self.seed: int | None = seed
        if mocks:
            self.mocks = itertools.cycle(mocks)
        else:
            self.mocks = None  # type: ignore
        self.generator = random.Random(self.seed)

    def next(self):
        if self.mocks:
            return self.mocks.__next__()
        else:
            return self.generator.randint(1, 6)


# --------------------------------------------------
def test_dice():
    d6 = Dice()
    total = 0
    for _ in range(1000):
        roll = d6.next()
        assert 1 <= roll <= 6
        total += roll
    assert 1000 <= total <= 6000
    assert total / 1000 == pytest.approx(3.5, abs=0.5)

    d6_seeded = Dice(seed=1)
    expected = [2, 5, 1, 3, 1, 4, 4, 4, 6, 4]
    actual = []
    for _ in range(10):
        actual.append(d6_seeded.next())
    assert actual == expected

    d6_mock = Dice(mocks=[1, 2, 3])
    expected = [1, 2, 3, 1, 2, 3, 1]
    actual = []
    for _ in range(7):
        actual.append(d6_mock.next())
    assert actual == expected


# --------------------------------------------------
def calc_rotation_period(
    world_type: WorldType,
    planet_mass: float = 1.0,
    star_mass: float = 1.0,
    star_distance: float = 1.0,
    satellite_mass: float = 0.0123,
    primary_distance: float = 384400.0,
    orbital_period: float = 7617.0,
    age: float = 4.568,
    radius: float = 6378.1,
    ecc: float = 0.0,
    rand: Dice = Dice(),
) -> (float, str):
    """
    Returns sidereal rotation period of world.

    Implements Step 19 pp 93-95. Constants tweaked to make earth and Luna exact.
    """
    roll = sum([rand.next() for _ in range(3)])
    if world_type is WorldType.SATELLITE:
        return orbital_period, "1:1 tidal lock with primary"

    if world_type is WorldType.LONE:
        t = (
            9.6e-14
            * age
            * math.pow(star_mass, 2)
            * math.pow(radius, 3)
            / planet_mass
            / math.pow(star_distance, 6)
        )
    elif world_type is WorldType.ORBITED:
        t = (
            1e25
            * age
            * math.pow(satellite_mass, 2)
            * math.pow(radius, 3)
            / planet_mass
            / math.pow(primary_distance, 6)
        )
    t_adjusted = int(round(t * 12, 0) + roll)
    if t >= 2 or t_adjusted >= 24:
        if world_type is WorldType.LONE:
            period = orbital_period
            lock, period = adjust_for_eccentricity(ecc, period)
            return period, lock
        else:
            return (
                2.768e-6
                * math.sqrt(
                    math.pow(primary_distance, 3) / (satellite_mass + planet_mass)
                ),
                "1:1 tidal lock with satellite",
            )
    else:
        p = look_up(planet_rotation_rate, t_adjusted)
        lower, upper = p
        period = random.uniform(lower, upper)
        lock = ""
        if period >= orbital_period:
            period = orbital_period
            lock, period = adjust_for_eccentricity(ecc, period)
        return period, lock


# --------------------------------------------------
def test_rotation_period():
    """Checks rotation period calculated correctly"""
    period_lone = calc_rotation_period(
        world_type=WorldType.LONE,
        planet_mass=0.93,
        star_mass=0.94,
        star_distance=0.892,
        age=3.225,
        radius=6584.0,
        ecc=0.07,
        rand=Dice(mocks=[3, 6, 1]),
    )
    assert 24 <= period_lone[0] <= 40

    period_orbited = calc_rotation_period(
        world_type=WorldType.ORBITED,
        planet_mass=0.93,
        star_mass=0.14,
        star_distance=0.087,
        primary_distance=125687,
        satellite_mass=0.025,
        age=1.225,
        radius=6584.0,
        ecc=0.07,
        rand=Dice(mocks=[1, 2, 1]),
    )
    period, lock = period_orbited
    assert period == pytest.approx(126.2, abs=1e-1)
    assert lock == "1:1 tidal lock with satellite"

    results = calc_rotation_period(
        world_type=WorldType.SATELLITE,
        satellite_mass=0.023,
        primary_distance=175845,
        planet_mass=0.876,
        orbital_period=215.3,
    )
    period, lock = results
    assert period == pytest.approx(215.3, abs=1e-1)
    assert lock == "1:1 tidal lock with primary"


# --------------------------------------------------
def calculate_radius(density: float = 1.0, mass: float = 1) -> int:
    """Calculates world radius from mass and density"""
    return int(round(6738 * math.pow(mass / density, 1.0 / 3.0), 0))


# --------------------------------------------------
def test_calculate_radius():
    """Checks world radius calculated correctly from mass and density"""
    radius = calculate_radius(mass=0.931, density=1.122)
    assert radius == 6332


# --------------------------------------------------
def adjust_for_eccentricity(ecc=0.0, period=1.0):
    multiplier = 1
    text = ""
    if ecc <= 0.12:
        text = "1:1 tidal lock with star"
    elif 0.12 < ecc < 0.25:
        multiplier = 2.0 / 3.0
        text = "3:2 spin resonance with star"
    elif 0.25 <= ecc < 0.35:
        multiplier = 0.5
        text = "2:1 spin resonance with star"
    elif 0.35 <= ecc < 0.45:
        multiplier = 0.4
        text = "5:2 spin resonance with star"
    else:
        text = "3:1 spin resonance with star"
        multiplier = 1.0 / 3.0
    return text, period * multiplier


# --------------------------------------------------
@pytest.mark.parametrize(
    "e, p, expected_period, expected_text",
    [
        (0.01, 256.0, 256.0, "1:1 tidal lock with star"),
        (0.08, 478.0, 478.0, "1:1 tidal lock with star"),
        (0.18, 330.0, 220.0, "3:2 spin resonance with star"),
        (0.25, 550.0, 275.0, "2:1 spin resonance with star"),
        (0.29, 700.0, 350.0, "2:1 spin resonance with star"),
        (0.35, 500.0, 200.0, "5:2 spin resonance with star"),
        (0.4, 1000.0, 400.0, "5:2 spin resonance with star"),
        (0.45, 300.0, 100.0, "3:1 spin resonance with star"),
        (0.6, 600.0, 200.0, "3:1 spin resonance with star"),
    ],
)
def test_calculate_resonance(e, p, expected_period, expected_text):
    """Checks resonant orbital periods adjusted for eccentricity"""

    result = adjust_for_eccentricity(ecc=e, period=p)
    text, period = result
    assert period == expected_period
    assert text == expected_text


# --------------------------------------------------
def look_up(table, selection_value):
    result = table[-1][1]
    for row in table:
        score, entry = row
        if selection_value <= score:
            result = entry
            break
    return result


# --------------------------------------------------
# Determines rotation rate of planet
# Random selection by 3d6 + T value
# Tuple is (dice roll, result)
# Result is (minumum period, maximum period)
# Highest result is "Resonant"
planet_rotation_rate = [
    (3, (4, 5)),
    (4, (4, 6)),
    (5, (5, 8)),
    (6, (6, 10)),
    (7, (8, 12)),
    (8, (10, 16)),
    (9, (12, 20)),
    (10, (16, 24)),
    (11, (20, 32)),
    (12, (24, 40)),
    (13, (32, 48)),
    (14, (40, 64)),
    (15, (48, 80)),
    (16, (64, 96)),
    (17, (80, 128)),
    (18, (96, 160)),
    (19, (128, 192)),
    (20, (160, 256)),
    (21, (192, 320)),
    (22, (256, 384)),
    (23, (320, 384)),
    (24, "Resonant"),
]
# --------------------------------------------------
if __name__ == "__main__":
    main()
