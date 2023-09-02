#!/usr/bin/env python3
"""
Author : Jon Walters <ringbolt60@gmail.com>
Date   : 2023-08-27
Purpose: Create worlds.
"""

# import argparse
import math
import random
from typing import NamedTuple

import tables as t
from utils import Dice


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
    magnetic_field: t.MagneticField = t.MagneticField.NONE

    @property
    def radius(self):
        mass = (
            self.satellite_mass
            if self.world_type == t.WorldType.SATELLITE
            else self.planet_mass
        )
        return int(round(6378 * math.pow(mass / self.density, 1.0 / 3.0), 0))

    @property
    def t_number(self) -> float:
        if self.world_type == t.WorldType.SATELLITE:
            return 0

        if self.world_type == t.WorldType.LONE:
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
        if self.lock == t.Resonance.LOCK_TO_STAR:
            return None
        else:
            return (
                self.orbital_period
                * self.rotational_period
                / (self.rotational_period + self.orbital_period)
            )

    @property
    def days_in_local_year(self) -> float | str:
        if self.lock == t.Resonance.LOCK_TO_STAR:
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
            if self.world_type == t.WorldType.SATELLITE
            else self.planet_mass
        )
        return math.pow(mass * math.pow(self.density, 2), 1.0 / 3.0)

    def describe(self):
        text = [self.name, f"{self.world_type.value} Age: {self.age:.3f} GYr"]
        if self.world_type == t.WorldType.SATELLITE:
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
        if self.world_type == t.WorldType.ORBITED:
            text.append(
                f"Satellite Mass: {self.satellite_mass:.3f} M♁ Distance: {self.primary_distance:.0f} km"
            )
        elif self.world_type == t.WorldType.SATELLITE:
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
        text.append(f"{self.magnetic_field.value}")
        return "\n".join(text)


# --------------------------------------------------
def calc_orbital_period(w: World) -> float:
    """
    Returns orbital period around primary in hours.

    Implements Step 18 pp 92,93. Constants tweaked to make earth and Luna exact.
    """
    if w.world_type == t.WorldType.SATELLITE:
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
    if w.world_type == t.WorldType.SATELLITE:
        return w.orbital_period, t.Resonance.LOCK_TO_PRIMARY

    t_adjusted = w.t_adj + roll
    if w.t_number >= 2 or t_adjusted >= 24:
        if w.world_type == t.WorldType.LONE:
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
        if water == t.Water.MINIMAL:
            if sum(rand.next() for _ in range(3)) + w.black_body_temp >= 318:
                water = t.Water.TRACE
                percentage = 0
        if water in [
            t.Water.MODERATE,
            t.Water.EXTENSIVE,
            t.Water.MASSIVE,
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

    if world.world_type == t.WorldType.SATELLITE or world.lock != t.Resonance.NONE:
        obl = roll - 8 if roll > 8 else 0
        return obl, instability

    if world.world_type == t.WorldType.LONE:
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
    if w.orbital_tidal_heating and w.world_type == t.WorldType.SATELLITE:
        f = 1.59e15 * w.planet_mass * w.radius / math.pow(w.primary_distance, 3)

    if (w.lock != t.Resonance.NONE) and (w.world_type != t.WorldType.SATELLITE):
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

    if lith in [
        t.Lithosphere.EARLY_PLATE,
        t.Lithosphere.MATURE_PLATE,
        t.Lithosphere.ANCIENT_PLATE,
    ]:
        roll2 = sum(rand.next() for _ in range(3))
        if w.water_prevalence in (t.Water.EXTENSIVE, t.Water.MASSIVE):
            roll2 += 6
        if w.water_prevalence in (t.Water.MINIMAL, t.Water.TRACE):
            roll2 -= 6
        if lith == t.Lithosphere.EARLY_PLATE:
            roll2 += 2
        if lith == t.Lithosphere.ANCIENT_PLATE:
            roll2 -= 2
        tect = t.Tectonics.MOBILE if roll2 >= 11 else t.Tectonics.FIXED

    if (
        lith in (t.Lithosphere.EARLY_PLATE, t.Lithosphere.MATURE_PLATE)
        and tect == t.Tectonics.FIXED
    ):
        ep_resurf = True

    if lith == t.Lithosphere.MOLTEN and new_water != t.Water.MASSIVE:
        new_water = t.Water.TRACE
        new_percent = 0

    if new_water == t.Water.EXTENSIVE:
        roll3 = sum(rand.next() for _ in range(3))
        if lith in [t.Lithosphere.SOFT, t.Lithosphere.SOLID]:
            # if lith in (t.Lithosphere.SOFT, t.Lithosphere.SOLID):
            new_percent += roll3 + 10
        if lith in [t.Lithosphere.EARLY_PLATE, t.Lithosphere.ANCIENT_PLATE]:
            new_percent += roll3
        if new_percent > 100:
            new_percent = 100

    return lith, tect, ep_resurf, new_water, new_percent


# --------------------------------------------------
def calc_magnetic_field(w: World, rand: Dice = Dice()) -> t.MagneticField:
    roll = sum(rand.next() for _ in range(3))
    if w.lithosphere == t.Lithosphere.SOFT:
        roll += 4
    if w.tectonics == t.Tectonics.MOBILE and w.lithosphere in (
        t.Lithosphere.EARLY_PLATE,
        t.Lithosphere.ANCIENT_PLATE,
    ):
        roll += 8
    if (
        w.lithosphere == t.Lithosphere.MATURE_PLATE
        and w.tectonics == t.Tectonics.MOBILE
    ):
        roll += 12

    if roll <= 14:
        return t.MagneticField.NONE
    elif 15 <= roll <= 17:
        return t.MagneticField.WEAK
    elif 18 <= roll <= 19:
        return t.MagneticField.MODERATE
    else:
        return t.MagneticField.STRONG
