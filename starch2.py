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

from tables import look_up, planet_rotation_rate
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
        default="0.0",
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
    ):
        a = getattr(args, attr)
        if a <= 0:
            parser.error(f'"{a}" should be a positive float')

    for attr in ("ecc",):
        a = getattr(args, attr)
        if a < 0:
            parser.error(f'"{a}" should be zero or a positive float')

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
    print(world.describe())


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
    world_type: WorldType = WorldType.ORBITED
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
        return int(round(6378 * math.pow(mass / self.density, 1.0 / 3.0), 0))

    @property
    def t(self) -> float:
        if self.world_type is WorldType.SATELLITE:
            return 0

        match self.world_type:
            case WorldType.LONE:
                const = 9.6e-14
                mass = self.star_mass
                distance = self.star_distance
            case WorldType.ORBITED:
                const = 1e25
                mass = self.satellite_mass
                distance = self.primary_distance

        return (
            const
            * self.age
            * math.pow(mass, 2)
            * math.pow(self.radius, 3)
            / self.planet_mass
            / math.pow(distance, 6)
        )

    def describe(self):
        text = [self.name, f"{self.world_type.value} Age: {self.age:.3f} GYr"]
        if self.world_type is WorldType.SATELLITE:
            text.append(
                f"Mass: {self.satellite_mass:.3f} M♁ Density: {self.density:.3f} K♁ Radius: {self.radius:.0f} km"
            )
        else:
            text.append(
                f"Mass: {self.planet_mass:.3f} M♁ Density: {self.density:.3f} K♁ Radius: {self.radius:.0f} km"
            )
        text.append(
            f"Star Mass: {self.star_mass:.3f} M☉ Distance: {self.star_distance:.3f} AU"
        )
        if self.world_type is WorldType.ORBITED:
            text.append(
                f"Satellite Mass: {self.satellite_mass:.3f} M♁ Distance: {self.primary_distance:.0f} km"
            )
        elif self.world_type is WorldType.SATELLITE:
            text.append(
                f"Primary Mass: {self.planet_mass:.3f} M♁ Distance: {self.primary_distance:.0f} km"
            )
        text.append("---")
        text.append(f"Orbital Period = {self.orbital_period:.1f} hours")
        text.append(
            f"Rotation Period = {self.rotational_period:.1f} hours {self.lock.value}"
        )
        return "\n".join(text)


# --------------------------------------------------
def calc_orbital_period(w: World) -> float:
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
if __name__ == "__main__":
    main()
