#!/usr/bin/env python3
"""
Author : Jon Walters <ringbolt60@gmail.com>
Date   : 2023-08-27
Purpose: Create worlds.
"""

import argparse
import math
import random
from typing import NamedTuple

import tables as t
from utils import Dice


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
        "-l",
        "--luminosity",
        help="Luminosity of star multiples of solar luminosity",
        metavar="float",
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

    parser.add_argument(
        "--metal",
        help="Metallicity of system, with Sol being 1",
        metavar="float",
        type=float,
        default="1.0",
    )

    parser.add_argument(
        "-o",
        "--outside_ice_line",
        help="Is outside formation ice line",
        action="store_true",
    )

    parser.add_argument(
        "-g",
        "--grand_tack",
        help="System has undergone Grand Tack event",
        action="store_true",
    )

    parser.add_argument(
        "-r",
        "--rocky_sat",
        help="World is rocky satellite of gas giant",
        action="store_true",
    )

    parser.add_argument(
        "--oort_cloud",
        help="Planet in Oort cloud",
        action="store_true",
    )

    parser.add_argument(
        "--green_house",
        help="Planet has experienced runaway greenhouse event",
        action="store_true",
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
        "luminosity",
        "metal",
    ):
        a = getattr(args, attr)
        if a <= 0:
            parser.error(f'"{a}" should be a positive float')

    for attr in ("ecc",):
        a = getattr(args, attr)
        if a < 0:
            parser.error(f'"{a}" should be zero or a positive float')

    if args.type == "lone":
        args.type = t.WorldType.LONE
    if args.type == "orbited":
        args.type = t.WorldType.ORBITED
    if args.type == "satellite":
        args.type = t.WorldType.SATELLITE

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
        luminosity=args.luminosity,
        outside_ice_line=args.outside_ice_line,
        grand_tack=args.grand_tack,
        oort_cloud=args.oort_cloud,
        green_house=args.green_house,
        rocky_sat_of_gas_giant=args.rocky_sat,
        metal=args.metal,
    )
    world = world._replace(orbital_period=calc_orbital_period(world))
    rotation_period, lock = calc_rotation_period(world)
    world = world._replace(rotational_period=rotation_period)
    world = world._replace(lock=lock)
    obl, instability = calc_obliquity(world)
    world = world._replace(obliquity=obl, unstable_obliquity=instability)
    water, percent, greenhouse = calc_water(world)
    world = world._replace(
        water_prevalence=water, water_percent=percent, green_house=greenhouse
    )
    lith, tect, epi_resurface, new_water_prev, new_water_percent = calc_geophysics(
        world
    )
    world = world._replace(
        lithosphere=lith,
        tectonics=tect,
        episodic_resurfacing=epi_resurface,
        water_prevalence=new_water_prev,
        water_percent=new_water_percent,
    )
    print(world.describe())


# --------------------------------------------------
class World(NamedTuple):
    name: str = "DEFAULT"
    world_type: t.WorldType = t.WorldType.ORBITED
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
    lock: t.Resonance = t.Resonance.NONE
    obliquity: int = 0
    unstable_obliquity: bool = False
    luminosity: float = 1.0
    outside_ice_line: bool = False
    grand_tack: bool = False
    oort_cloud: bool = False
    green_house: bool = False
    rocky_sat_of_gas_giant: bool = False
    water_prevalence: t.Water = t.Water.TRACE
    water_percent: float = 0.0
    metal: float = 1.0
    lithosphere: t.Lithosphere = t.Lithosphere.SOLID
    tectonics: t.Tectonics = t.Tectonics.NONE
    episodic_resurfacing: bool = False
    orbital_tidal_heating: bool = False

    @property
    def radius(self):
        mass = (
            self.satellite_mass
            if self.world_type.value == t.WorldType.SATELLITE.value
            else self.planet_mass
        )
        return int(round(6378 * math.pow(mass / self.density, 1.0 / 3.0), 0))

    @property
    def t_number(self) -> float:
        if self.world_type.value == t.WorldType.SATELLITE.value:
            return 0

        if self.world_type.value == t.WorldType.LONE.value:
            const = 9.6e-14
            mass = self.star_mass
            distance = self.star_distance
        else:
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

    @property
    def t_adj(self) -> int:
        ta = round(self.t_number * 12, 0)
        return int(ta)

    @property
    def local_day_length(self) -> float | None:
        if self.lock.value == t.Resonance.LOCK_TO_STAR.value:
            return None
        else:
            return (
                self.orbital_period
                * self.rotational_period
                / (self.rotational_period + self.orbital_period)
            )

    @property
    def days_in_local_year(self) -> float | str:
        if self.lock.value == t.Resonance.LOCK_TO_STAR.value:
            return "N/A"
        else:
            return self.orbital_period / self.local_day_length

    # TODO Implement synodic month calculations
    @property
    def synodic_month_length(self) -> float | str:
        return "TBI"

    @property
    def black_body_temp(self) -> int:
        bbt = round(
            278 * math.pow(self.luminosity, 0.25) / math.sqrt(self.star_distance), 0
        )
        return int(bbt)

    @property
    def m_number(self) -> int:
        m = 700000 * self.black_body_temp / self.density / math.pow(self.radius, 2)
        return int(m + 0.99999999)

    @property
    def gravity(self) -> float:
        mass = (
            self.satellite_mass
            if self.world_type.value == t.WorldType.SATELLITE.value
            else self.planet_mass
        )
        return math.pow(mass * math.pow(self.density, 2), 1.0 / 3.0)

    def describe(self):
        text = [self.name, f"{self.world_type.value} Age: {self.age:.3f} GYr"]
        if self.world_type.value == t.WorldType.SATELLITE.value:
            text.append(
                f"Mass: {self.satellite_mass:.3f} M♁ Density: {self.density:.3f} K♁ Radius: {self.radius:.0f} km "
                f"Gravity: {self.gravity:.3f} G"
            )
        else:
            text.append(
                f"Mass: {self.planet_mass:.3f} M♁ Density: {self.density:.3f} K♁ Radius: {self.radius:.0f} km Gravity: {self.gravity:.3f} G"
            )
        text.append(
            f"Star Mass: {self.star_mass:.3f} M☉ Distance: {self.star_distance:.3f} AU Lumin: {self.luminosity:.3f} L☉"
        )
        if self.world_type.value == t.WorldType.ORBITED.value:
            text.append(
                f"Satellite Mass: {self.satellite_mass:.3f} M♁ Distance: {self.primary_distance:.0f} km"
            )
        elif self.world_type.value == t.WorldType.SATELLITE.value:
            text.append(
                f"Primary Mass: {self.planet_mass:.3f} M♁ Distance: {self.primary_distance:.0f} km"
            )
        text.append("---")
        text.append(f"Orbital Period = {self.orbital_period:.1f} hours")
        text.append(
            f"Rotation Period = {self.rotational_period:.1f} hours {self.lock.value}"
        )
        text.append(
            f"Obliquity = {self.obliquity}° {'Unstable' if self.unstable_obliquity else ''}"
        )
        if self.local_day_length:
            text.append(
                f"Day length = {self.local_day_length:.1f} hours {self.days_in_local_year:.2f} days in year"
            )
        else:
            text.append("Day length: not applicable")
        text.append(
            f"Black body temperature = {self.black_body_temp} K {'Runaway Greenhouse' if self.green_house else ''}"
        )
        text.append(f"M number = {self.m_number}")
        text.append(
            f"Water prevalence: {self.water_prevalence.value} {self.water_percent:5.1f}%"
        )

        text.append(
            f"{self.lithosphere.value} / {self.tectonics.value}{' / Episodic Resurfacing' if self.episodic_resurfacing else ''}"
        )
        return "\n".join(text)


# --------------------------------------------------
def calc_orbital_period(w: World) -> float:
    """
    Returns orbital period around primary in hours.

    Implements Step 18 pp 92,93. Constants tweaked to make earth and Luna exact.
    """
    if w.world_type.value == t.WorldType.SATELLITE.value:
        return 2.768e-6 * math.sqrt(
            math.pow(w.primary_distance, 3) / (w.satellite_mass + w.planet_mass)
        )
    return 8766.0 * math.sqrt(math.pow(w.star_distance, 3) / w.star_mass)


# --------------------------------------------------
def calc_rotation_period(w: World, rand: Dice = Dice()) -> (float, t.Resonance):
    """
    Returns sidereal rotation period of world.

    Implements Step 19 pp 93-95. Constants tweaked to make earth and Luna exact.
    """
    roll = sum(rand.next() for _ in range(3))
    if w.world_type.value == t.WorldType.SATELLITE.value:
        return w.orbital_period, t.Resonance.LOCK_TO_PRIMARY

    t_adjusted = w.t_adj + roll
    if w.t_number >= 2 or t_adjusted >= 24:
        if w.world_type.value == t.WorldType.LONE.value:
            period = w.orbital_period
            lock, period = adjust_for_eccentricity(w.ecc, period)
            return period, lock
        return (
            2.768e-6
            * math.sqrt(
                math.pow(w.primary_distance, 3) / (w.satellite_mass + w.planet_mass)
            ),
            t.Resonance.LOCK_TO_SATELLITE,
        )

    p = t.look_up(t.planet_rotation_rate, t_adjusted)
    lower, upper = p
    period = random.uniform(lower, upper)
    lock = t.Resonance.NONE
    if period >= w.orbital_period:
        period = w.orbital_period
        lock, period = adjust_for_eccentricity(w.ecc, period)
    return period, lock


# --------------------------------------------------
def calc_water(w: World, rand: Dice = Dice()) -> (t.Water, int, bool):
    """
    Returns the water prevalence and percentage.

    Implements Step 23 pp 101-103.
    """
    water = t.Water.TRACE
    percentage = 0
    gh = False

    if w.m_number <= 2:
        water = t.Water.MASSIVE
        percentage = 100
    elif w.m_number >= 29:
        if w.black_body_temp >= 125 or w.rocky_sat_of_gas_giant:
            water = t.Water.TRACE
            percentage = 0
        else:
            water = t.Water.MASSIVE
            percentage = 100
    else:
        if w.outside_ice_line:
            water = t.Water.MASSIVE
            percentage = 100
        else:
            mod = -w.m_number
            if w.grand_tack:
                mod += 6
            if w.oort_cloud:
                mod += 3
        look_up_value = sum(rand.next() for _ in range(3)) + mod
        lower, upper, water = t.look_up(t.hydro_cover, look_up_value)
        percentage = random.uniform(lower, upper)

    if w.m_number > 2 and w.black_body_temp >= 300:
        if water.value == t.Water.MINIMAL.value:
            if sum(rand.next() for _ in range(3)) + w.black_body_temp >= 318:
                water = t.Water.TRACE
                percentage = 0
        if water.value in [
            e.value
            for e in [
                t.Water.MODERATE,
                t.Water.EXTENSIVE,
                t.Water.MASSIVE,
            ]
        ]:
            if sum(rand.next() for _ in range(3)) + w.black_body_temp >= 318:
                water = t.Water.TRACE
                percentage = 0
                gh = True

    return water, percentage, gh


# --------------------------------------------------
def adjust_for_eccentricity(ecc=0.0, period=1.0):
    """Check for eccentricity induced orbital resonance."""
    multiplier = 1
    lock = ""
    if ecc <= 0.12:
        lock = t.Resonance.LOCK_TO_STAR
    elif 0.12 < ecc < 0.25:
        multiplier = 2.0 / 3.0
        lock = t.Resonance.RESONANCE_3_2
    elif 0.25 <= ecc < 0.35:
        multiplier = 0.5
        lock = t.Resonance.RESONANCE_2_1
    elif 0.35 <= ecc < 0.45:
        multiplier = 0.4
        lock = t.Resonance.RESONANCE_5_2
    else:
        lock = t.Resonance.RESONANCE_3_1
        multiplier = 1.0 / 3.0
    return lock, period * multiplier


# --------------------------------------------------
def calc_obliquity(world: World, rand: Dice = Dice()) -> (int, bool):
    """
    Calculate planet obliquity.

    Step 20, pp 96-97
    """
    roll = sum(rand.next() for _ in range(3))
    instability = False
    mod = 0

    if (
        world.world_type.value == t.WorldType.SATELLITE.value
        or world.lock != t.Resonance.NONE
    ):
        obl = roll - 8 if roll > 8 else 0
        return obl, instability

    if world.world_type.value == t.WorldType.LONE.value:
        roll2 = sum(rand.next() for _ in range(3))
        if not (8 <= roll2 <= 13):
            mod = -7
            instability = True

    look_up_value = world.t_adj + roll + mod
    if look_up_value >= 25:
        obl = roll - 8 if roll > 8 else 0
    elif look_up_value <= 4:
        roll3 = rand.next()
        if roll3 == 6:
            roll4 = sum(rand.next() for _ in range(3))
            obl = 90 - roll4 if roll4 > 7 else 90
        else:
            lower, upper = t.look_up(t.planet_extreme_obliquity_table, roll3)
            obl = random.randint(lower, upper)
    else:
        lower, upper = t.look_up(t.planet_obliquity_table, look_up_value)
        obl = random.randint(lower, upper)

    return obl, instability


# --------------------------------------------------
def calc_geophysics(
    w: World, rand: Dice = Dice()
) -> (t.Lithosphere, t.Tectonics, bool, t.Water, float):
    """Calculate planet geophysical parameters

    Implements Step 24, pp 104-108
    """
    lith, tect, ep_resurf, new_water, new_percent = (
        t.Lithosphere.SOLID,
        t.Tectonics.NONE,
        False,
        w.water_prevalence,
        w.water_percent,
    )
    age_mod = int(round(8 * w.age, 0))
    primordial_heat_mod = int(round(-60 * math.log10(w.gravity), 0))
    radiogenic_heat_mod = int(round(-10 * math.log10(w.metal), 0))
    roll1 = sum(rand.next() for _ in range(3))
    lookup = age_mod + primordial_heat_mod + radiogenic_heat_mod + roll1
    lith, ordinal = t.look_up(t.lithosphere, lookup)

    f = 0
    if w.orbital_tidal_heating and w.world_type.value == t.WorldType.SATELLITE.value:
        f = 1.59e15 * w.planet_mass * w.radius / math.pow(w.primary_distance, 3)

    if (w.lock.value != t.Resonance.NONE.value) and (
        w.world_type.value != t.WorldType.SATELLITE.value
    ):
        if (
            w.ecc >= 0.05
            or w.lock
            in (
                t.Resonance.RESONANCE_5_2,
                t.Resonance.RESONANCE_2_1,
                t.Resonance.RESONANCE_3_2,
                t.Resonance.RESONANCE_3_1,
            )
            or w.orbital_tidal_heating
        ):
            f = 1.57e-4 * w.star_mass * w.radius / math.pow(w.star_distance, 3)

    if f > 0:
        new_lith, new_ordinal = t.look_up(t.lithosphere_stressed, f)
        if new_ordinal < ordinal:
            lith = new_lith

    if lith.value in [
        e.value
        for e in (
            t.Lithosphere.EARLY_PLATE,
            t.Lithosphere.MATURE_PLATE,
            t.Lithosphere.ANCIENT_PLATE,
        )
    ]:
        roll2 = sum(rand.next() for _ in range(3))
        if w.water_prevalence in (t.Water.EXTENSIVE, t.Water.MASSIVE):
            roll2 += 6
        if w.water_prevalence in (t.Water.MINIMAL, t.Water.TRACE):
            roll2 -= 6
        if lith.value == t.Lithosphere.EARLY_PLATE.value:
            roll2 += 2
        if lith.value == t.Lithosphere.ANCIENT_PLATE.value:
            roll2 -= 2
        tect = t.Tectonics.MOBILE if roll2 >= 11 else t.Tectonics.FIXED

    if (
        lith.value
        in (e.value for e in (t.Lithosphere.EARLY_PLATE, t.Lithosphere.MATURE_PLATE))
        and tect.value == t.Tectonics.FIXED.value
    ):
        ep_resurf = True

    if (
        lith.value == t.Lithosphere.MOLTEN.value
        and new_water.value != t.Water.MASSIVE.value
    ):
        new_water = t.Water.TRACE
        new_percent = 0

    if new_water.value == t.Water.EXTENSIVE.value:
        roll3 = sum(rand.next() for _ in range(3))
        if lith.value in [e.value for e in [t.Lithosphere.SOFT, t.Lithosphere.SOLID]]:
            # if lith in (t.Lithosphere.SOFT, t.Lithosphere.SOLID):
            new_percent += roll3 + 10
        if lith.value in [
            e.value for e in [t.Lithosphere.EARLY_PLATE, t.Lithosphere.ANCIENT_PLATE]
        ]:
            new_percent += roll3
        if new_percent > 100:
            new_percent = 100

    return lith, tect, ep_resurf, new_water, new_percent


# --------------------------------------------------
if __name__ == "__main__":
    main()
