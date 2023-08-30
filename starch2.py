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
from typing import NamedTuple
from utils import Dice

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
        metavar="mass",
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
    world = World(
        name=args.name,
        world_type=args.type,
        planet_mass=args.mass,
        star_mass=args.mass_star,
        star_distance=args.distance_star,
        satellite_mass=args.satellite_mass,
        primary_distance=args.distance_primary,
        age=args.age,
        ecc=args.ecc,
        density=args.density,
    )
    world = world._replace(orbital_period=calc_orbital_period(world))
    rotation_period, lock = calc_rotation_period(world)
    world = world._replace(rotational_period=rotation_period)
    world = world._replace(lock=lock)

    match world.world_type:
        case WorldType.LONE:
            print(
                f"{world.name}\n"
                f"{world.world_type.value} Age: {world.age:.3f} GYr\n"
                f"Mass: {world.planet_mass:.3f} M♁ Density: {world.density:.3f} K♁ Radius: {world.radius:.0f} km\n"
                f"Star Mass: {world.star_mass:.3f} M☉ Distance: {world.star_distance:.3f} AU\n"
                f"---\n"
                f"Orbital Period = {world.orbital_period:.1f} hours\n"
                f"Rotation Period = {world.rotational_period:.1f} hours {world.lock.value}"
            )
        case WorldType.ORBITED:
            print(
                f"{world.name}\n"
                f"{world.world_type.value} Age: {world.age:.3f} GYr\n"
                f"Mass: {world.planet_mass:.3f} M♁ Density: {world.density:.3f} K♁ Radius: {world.radius:.0f} km\n"
                f"Star Mass: {world.star_mass:.3f} M☉ Distance: {world.star_distance:.3f} AU\n"
                f"Satellite Mass: {world.satellite_mass:.3f} M♁ Distance: {world.primary_distance:.0f} km\n"
                f"---\n"
                f"Orbital Period = {world.orbital_period:.1f} hours\n"
                f"Rotation Period = {world.rotational_period:.1f} hours {world.lock.value}"
            )
        case WorldType.SATELLITE:
            print(
                f"{world.name}\n"
                f"{world.world_type.value} Age: {world.age:.3f} GYr\n"
                f"Mass: {world.satellite_mass:.3f} M♁ Density: {world.density:.3f} K♁ Radius: {world.radius:.0f} km\n"
                f"Star Mass: {world.star_mass:.3f} M☉ Distance: {world.star_distance:.3f} AU\n"
                f"Primary Mass: {world.planet_mass:.3f} M♁ Distance: {world.primary_distance:.0f} km\n"
                f"---\n"
                f"Orbital Period = {world.orbital_period:.1f} hours\n"
                f"Rotation Period = {world.rotational_period:.1f} hours {world.lock.value}"
            )


# --------------------------------------------------
class WorldType(Enum):
    LONE = "Lone Planet"
    ORBITED = "Planet with Satellite"
    SATELLITE = "Satellite"


class Resonance(Enum):
    NONE = ""
    LOCK_TO_SATELLITE = "1:1 tidal lock with satellite"
    LOCK_TO_PRIMARY = "1:1 tidal lock with planet"
    LOCK_TO_STAR = "1:1 tidal lock with star"
    RESONANCE_3_2 = "3:2 resonance with star"
    RESONANCE_2_1 = "2:1 resonance with star"
    RESONANCE_5_2 = "5:2 resonance with star"
    RESONANCE_3_1 = "3:1 resonance with star"


# --------------------------------------------------
class World(NamedTuple):
    name: str = "DEFAULT"
    world_type: WorldType = WorldType.LONE
    planet_mass: float = 1.0
    star_mass: float = 1.0
    star_distance: float = 1.0
    satellite_mass: float = 0.0123
    primary_distance: float = 384400
    age: float = 4.568
    ecc: float = 0.07
    orbital_period: float = 7617.0
    density: float = 1.0
    rotational_period: float = 24.0
    lock: Resonance = Resonance.NONE

    @property
    def radius(self):
        mass = (
            self.satellite_mass
            if self.world_type is WorldType.SATELLITE
            else self.planet_mass
        )
        return int(round(6738 * math.pow(mass / self.density, 1.0 / 3.0), 0))

    @property
    def t(self) -> float:
        t = 0
        if self.world_type is WorldType.LONE:
            t = (
                9.6e-14
                * self.age
                * math.pow(self.star_mass, 2)
                * math.pow(self.radius, 3)
                / self.planet_mass
                / math.pow(self.star_distance, 6)
            )
        elif self.world_type is WorldType.ORBITED:
            t = (
                1e25
                * self.age
                * math.pow(self.satellite_mass, 2)
                * math.pow(self.radius, 3)
                / self.planet_mass
                / math.pow(self.primary_distance, 6)
            )
        return t


# --------------------------------------------------
def calc_orbital_period(w: "World") -> float:
    """
    Returns orbital period around primary in hours.

    Implements Step 18 pp 92,93. Constants tweaked to make earth and Luna exact.
    """
    if w.world_type is WorldType.SATELLITE:
        return 2.768e-6 * math.sqrt(
            math.pow(w.primary_distance, 3) / (w.satellite_mass + w.planet_mass)
        )
    else:
        return 8766.0 * math.sqrt(math.pow(w.star_distance, 3) / w.star_mass)


# --------------------------------------------------
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
def calc_rotation_period(w: World, rand: Dice = Dice()) -> (float, Resonance):
    """
    Returns sidereal rotation period of world.

    Implements Step 19 pp 93-95. Constants tweaked to make earth and Luna exact.
    """
    roll = sum([rand.next() for _ in range(3)])
    if w.world_type is WorldType.SATELLITE:
        return w.orbital_period, Resonance.LOCK_TO_PRIMARY

    t_adjusted = int(round(w.t * 12, 0) + roll)
    if w.t >= 2 or t_adjusted >= 24:
        if w.world_type is WorldType.LONE:
            period = w.orbital_period
            lock, period = adjust_for_eccentricity(w.ecc, period)
            return period, lock
        else:
            return (
                2.768e-6
                * math.sqrt(
                    math.pow(w.primary_distance, 3) / (w.satellite_mass + w.planet_mass)
                ),
                Resonance.LOCK_TO_SATELLITE,
            )
    else:
        p = look_up(planet_rotation_rate, t_adjusted)
        lower, upper = p
        period = random.uniform(lower, upper)
        lock = Resonance.NONE
        if period >= w.orbital_period:
            period = w.orbital_period
            lock, period = adjust_for_eccentricity(w.ecc, period)
        return period, lock


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
        orbital_period=6589.5,
    )
    period, lock = calc_rotation_period(lone_world_2, rand=Dice(mocks=[3, 6, 5]))
    assert period == pytest.approx(2635.8, abs=1e-1)
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
def adjust_for_eccentricity(ecc=0.0, period=1.0):
    multiplier = 1
    lock = ""
    if ecc <= 0.12:
        lock = Resonance.LOCK_TO_STAR
    elif 0.12 < ecc < 0.25:
        multiplier = 2.0 / 3.0
        lock = Resonance.RESONANCE_3_2
    elif 0.25 <= ecc < 0.35:
        multiplier = 0.5
        lock = Resonance.RESONANCE_2_1
    elif 0.35 <= ecc < 0.45:
        multiplier = 0.4
        lock = Resonance.RESONANCE_5_2
    else:
        lock = Resonance.RESONANCE_3_1
        multiplier = 1.0 / 3.0
    return lock, period * multiplier


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
