#!/usr/bin/env python3
"""
Author : Jon Walters <ringbolt60@gmail.com>
Date   : 2023-08-27
Purpose: Create worlds.
"""

# import argparse
import math
import random
import re
from enum import Enum
from typing import NamedTuple

import tables as t  # type: ignore
from utils import Dice, look_up


class Water(Enum):
    TRACE = "Trace"
    MINIMAL = "Minimal"
    MODERATE = "Moderate"
    EXTENSIVE = "Extensive"
    MASSIVE = "Massive"

    @classmethod
    def from_text(cls, text):
        lookup = {
            "trace": cls.TRACE,
            "minimal": cls.MINIMAL,
            "moderate": cls.MODERATE,
            "extensive": cls.EXTENSIVE,
            "massive": cls.MASSIVE,
        }
        return lookup[text]


# --------------------------------------------------
class Lithosphere(Enum):
    MOLTEN = "Molten Lithosphere"
    SOFT = "Soft Lithosphere"
    EARLY_PLATE = "Early Plate Lithosphere"
    MATURE_PLATE = "Mature Plate Lithosphere"
    ANCIENT_PLATE = "Ancient Plate Lithosphere"
    SOLID = "Solid Plate Lithosphere"

    @classmethod
    def from_text(cls, text):
        lookup = {
            "molten": cls.MOLTEN,
            "soft": cls.SOFT,
            "early_plate": cls.EARLY_PLATE,
            "mature_plate": cls.MATURE_PLATE,
            "ancient_plate": cls.ANCIENT_PLATE,
            "solid": cls.SOLID,
        }
        return lookup[text]


# --------------------------------------------------
class WorldType(Enum):
    LONE = "Lone Planet"
    ORBITED = "Planet with Satellite"
    SATELLITE = "Satellite"


# --------------------------------------------------
class WorldClass(Enum):
    ONE = "Class 1 (Venus-type)"
    TWO = "Class 2 (Dulcinea-type)"
    THREE = "Class 3 (Titan-type)"
    FOUR = "Class 4 (Earth-type)"
    FIVE = "Class 5 (Mars-type)"
    SIX = "Class 6 (Luna-type)"


# --------------------------------------------------
class Tectonics(Enum):
    NONE = "No plate tectonics"
    MOBILE = "Mobile plate tectonics"
    FIXED = "Fixed Plate Tectonics"


# --------------------------------------------------
class Resonance(Enum):
    NONE = "None"
    LOCK_TO_SATELLITE = "1:1 tidal lock with satellite"
    LOCK_TO_PRIMARY = "1:1 tidal lock with planet"
    LOCK_TO_STAR = "1:1 tidal lock with star"
    RESONANCE_3_2 = "3:2 resonance with star"
    RESONANCE_2_1 = "2:1 resonance with star"
    RESONANCE_5_2 = "5:2 resonance with star"
    RESONANCE_3_1 = "3:1 resonance with star"


# --------------------------------------------------
class MagneticField(Enum):
    NONE = "No magnetic field"
    WEAK = "Weak magnetic field"
    MODERATE = "Moderate Magnetic Field"
    STRONG = "Strong Magnetic Field"


# --------------------------------------------------
class World(NamedTuple):
    name: str = "DEFAULT"
    world_type: WorldType = WorldType.ORBITED
    planet_mass: float = 1.0
    star_spectrum: str = "G2"
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
    obliquity: int = 0
    unstable_obliquity: bool = False
    luminosity: float = 1.0
    outside_ice_line: bool = False
    grand_tack: bool = False
    oort_cloud: bool = False
    green_house: bool = False
    rocky_sat_of_gas_giant: bool = False
    water_prevalence: Water = Water.TRACE
    water_percent: float = 0.0
    metal: float = 1.0
    lithosphere: Lithosphere = Lithosphere.SOLID
    tectonics: Tectonics = Tectonics.NONE
    episodic_resurfacing: bool = False
    orbital_tidal_heating: bool = False
    magnetic_field: MagneticField = MagneticField.NONE
    arf: float = 0.0
    mass_hydrogen: float = 0.0
    mass_helium: float = 0.0
    mass_nitrogen: float = 0.0
    mass_carbon_dioxide: float = 0.0
    mass_oxygen: float = 0.0
    world_class: WorldClass = WorldClass.SIX
    albedo: float = 0.1
    abio_vents_occurred: bool = False
    time_to_abio_vents: int | None = None
    abio_surface_occurred: bool = False
    time_to_abio_surface: int | None = None
    multicellular_occured: bool = False
    time_to_multicellular: int | None = None
    photosynthesis_occurred: bool = False
    time_to_photosynthesis: int | None = None
    oxygen_occurred: bool = False
    time_to_oxygen: int | None = None
    animals_occurred: bool = False
    time_to_animals: int | None = None
    presentients_occurred: bool = False
    time_to_presentients: int | None = None

    @property
    def radius(self):
        mass = (
            self.satellite_mass
            if self.world_type == WorldType.SATELLITE
            else self.planet_mass
        )
        return int(round(6378 * math.pow(mass / self.density, 1.0 / 3.0), 0))

    @property
    def t_number(self) -> float:
        if self.world_type == WorldType.SATELLITE:
            return 0

        if self.world_type == WorldType.LONE:
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
        if self.lock == Resonance.LOCK_TO_STAR:
            return None
        return (
            self.orbital_period
            * self.rotational_period
            / (self.rotational_period + self.orbital_period)
        )

    @property
    def days_in_local_year(self) -> float | str:
        if self.lock == Resonance.LOCK_TO_STAR:
            return "N/A"
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
            if self.world_type == WorldType.SATELLITE
            else self.planet_mass
        )
        return math.pow(mass * math.pow(self.density, 2), 1.0 / 3.0)

    @property
    def carbon_silicate_cycle(self) -> bool:
        if self.mass_carbon_dioxide > 0:
            t_ccs = (
                self.black_body_temp * math.pow((1 - self.albedo), 0.25)
                + 8 * math.log10(self.mass_carbon_dioxide)
                + 36.0
            )
        else:
            t_ccs = 0
        if self.water_prevalence in (Water.MODERATE, Water.EXTENSIVE) and t_ccs >= 260:
            return True
        else:
            return False

    @property
    def life(self) -> str:
        if self.photosynthesis_occurred:
            return "Aerobic Life"
        if self.abio_surface_occurred or self.abio_vents_occurred:
            return "Anaerobic life"
        else:
            return "Lifeless"

    @property
    def photosynthesis_time_scale(self):
        mult = 100
        if re.match(r"G[89]", self.star_spectrum):
            mult = 105
        if self.star_spectrum[0] == "M":
            mult = 300
        if self.star_spectrum[0] == "K":
            lookup = (110, 115, 120, 130, 145, 160, 180, 210, 240, 240)
            x = int(self.star_spectrum[1])
            mult = lookup[x]
        return mult

    def describe(self):
        text = [self.name, f"{self.world_type.value} Age: {self.age:.3f} GYr"]
        if self.world_type == WorldType.SATELLITE:
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
        if self.world_type == WorldType.ORBITED:
            text.append(
                f"Satellite Mass: {self.satellite_mass:.3f} M♁ Distance: {self.primary_distance:.0f} km"
            )
        elif self.world_type == WorldType.SATELLITE:
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
        text.append(
            f"{self.world_class.value}{' CS Cycle present' if self.carbon_silicate_cycle else ''} ARF: {self.arf} H2: "
            f"{self.mass_hydrogen:.2f} He: {self.mass_helium:.2f} "
            f"N2: {self.mass_nitrogen:.2f} CO2: {self.mass_carbon_dioxide:.2f} "
            f"O2: {self.mass_oxygen:.2f}"
        )
        text.append(f"Albedo: {self.albedo:.2f}")
        text.append(
            f"{self.life} [{'Deep sea vents' if self.abio_vents_occurred else ''}{' Surface refugia' if self.abio_surface_occurred else ''}"
            f"{' / Multicellular' if self.multicellular_occured else ''}{' / Photosynthetic' if self.photosynthesis_occurred else ''}"
            f"{' / Oxygen Catastrophe' if self.oxygen_occurred else ''}{' / Animals' if self.animals_occurred else ''}{' / Pre-sentients' if self.presentients_occurred else ''}]"
        )
        return "\n".join(text)


# --------------------------------------------------
def calc_orbital_period(w: World) -> float:
    """
    Returns orbital period around primary in hours.

    Implements Step 18 pp 92,93. Constants tweaked to make earth and Luna exact.
    """
    if w.world_type == WorldType.SATELLITE:
        return 2.768e-6 * math.sqrt(
            math.pow(w.primary_distance, 3) / (w.satellite_mass + w.planet_mass)
        )
    return 8766.0 * math.sqrt(math.pow(w.star_distance, 3) / w.star_mass)


# --------------------------------------------------
def calc_rotation_period(w: World, rand: Dice = Dice()) -> (float, Resonance):
    """
    Returns sidereal rotation period of world.

    Implements Step 19 pp 93-95. Constants tweaked to make earth and Luna exact.
    """
    roll = sum(rand.next() for _ in range(3))
    if w.world_type == WorldType.SATELLITE:
        return w.orbital_period, Resonance.LOCK_TO_PRIMARY

    t_adjusted = w.t_adj + roll
    if w.t_number >= 2 or t_adjusted >= 24:
        if w.world_type == WorldType.LONE:
            period = w.orbital_period
            lock, period = adjust_for_eccentricity(w.ecc, period)
            return period, lock
        return (
            2.768e-6
            * math.sqrt(
                math.pow(w.primary_distance, 3) / (w.satellite_mass + w.planet_mass)
            ),
            Resonance.LOCK_TO_SATELLITE,
        )

    p = look_up(t.planet_rotation_rate, t_adjusted)
    lower, upper = p
    period = random.uniform(lower, upper)
    lock = Resonance.NONE
    if period >= w.orbital_period:
        period = w.orbital_period
        lock, period = adjust_for_eccentricity(w.ecc, period)
    return period, lock


# --------------------------------------------------
def calc_water(w: World, rand: Dice = Dice()) -> (Water, int, bool):
    """
    Returns the water prevalence and percentage.

    Implements Step 23 pp 101-103.
    """
    water = Water.TRACE
    percentage = 0
    gh = False

    if w.m_number <= 2:
        water = Water.MASSIVE
        percentage = 100
    elif w.m_number >= 29:
        if w.black_body_temp >= 125 or w.rocky_sat_of_gas_giant:
            water = Water.TRACE
            percentage = 0
        else:
            water = Water.MASSIVE
            percentage = 100
    else:
        mod = 0
        if w.outside_ice_line:
            water = Water.MASSIVE
            percentage = 100
        else:
            mod = -w.m_number
            if w.grand_tack:
                mod += 6
            if w.oort_cloud:
                mod += 3
        look_up_value = sum(rand.next() for _ in range(3)) + mod
        lower, upper, water = look_up(t.hydro_cover, look_up_value)
        water = Water.from_text(water)
        percentage = random.uniform(lower, upper)

    if w.m_number > 2 and w.black_body_temp >= 300:
        if water == Water.MINIMAL:
            if sum(rand.next() for _ in range(3)) + w.black_body_temp >= 318:
                water = Water.TRACE
                percentage = 0
        if water in [
            Water.MODERATE,
            Water.EXTENSIVE,
            Water.MASSIVE,
        ]:
            if sum(rand.next() for _ in range(3)) + w.black_body_temp >= 318:
                water = Water.TRACE
                percentage = 0
                gh = True

    return water, percentage, gh


# --------------------------------------------------
def adjust_for_eccentricity(ecc=0.0, period=1.0):
    """Check for eccentricity induced orbital resonance."""
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
def calc_obliquity(world: World, rand: Dice = Dice()) -> (int, bool):
    """
    Calculate planet obliquity.

    Step 20, pp 96-97
    """
    roll = sum(rand.next() for _ in range(3))
    instability = False
    mod = 0

    if world.world_type == WorldType.SATELLITE or world.lock != Resonance.NONE:
        obl = roll - 8 if roll > 8 else 0
        return obl, instability

    if world.world_type == WorldType.LONE:
        roll2 = sum(rand.next() for _ in range(3))
        if not 8 <= roll2 <= 13:
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
            lower, upper = look_up(t.planet_extreme_obliquity_table, roll3)
            obl = random.randint(lower, upper)
    else:
        lower, upper = look_up(t.planet_obliquity_table, look_up_value)
        obl = random.randint(lower, upper)

    return obl, instability


# --------------------------------------------------
def calc_geophysics(
    w: World, rand: Dice = Dice()
) -> (Lithosphere, Tectonics, bool, Water, float):
    """Calculate planet geophysical parameters

    Implements Step 24, pp 104-108
    """
    lith, tect, ep_resurf, new_water, new_percent = (
        Lithosphere.SOLID,
        Tectonics.NONE,
        False,
        w.water_prevalence,
        w.water_percent,
    )
    age_mod = int(round(8 * w.age, 0))
    primordial_heat_mod = int(round(-60 * math.log10(w.gravity), 0))
    radiogenic_heat_mod = int(round(-10 * math.log10(w.metal), 0))
    roll1 = sum(rand.next() for _ in range(3))
    lookup = age_mod + primordial_heat_mod + radiogenic_heat_mod + roll1
    lith, ordinal = look_up(t.lithosphere, lookup)
    lith = Lithosphere.from_text(lith)

    f = 0
    if w.orbital_tidal_heating and w.world_type == WorldType.SATELLITE:
        f = 1.59e15 * w.planet_mass * w.radius / math.pow(w.primary_distance, 3)

    if (w.lock != Resonance.NONE) and (w.world_type != WorldType.SATELLITE):
        if (
            w.ecc >= 0.05
            or w.lock
            in (
                Resonance.RESONANCE_5_2,
                Resonance.RESONANCE_2_1,
                Resonance.RESONANCE_3_2,
                Resonance.RESONANCE_3_1,
            )
            or w.orbital_tidal_heating
        ):
            f = 1.57e-4 * w.star_mass * w.radius / math.pow(w.star_distance, 3)

    if f > 0:
        new_lith, new_ordinal = look_up(t.lithosphere_stressed, f)
        new_lith = Lithosphere.from_text(new_lith)
        if new_ordinal < ordinal:
            lith = new_lith

    if lith in [
        Lithosphere.EARLY_PLATE,
        Lithosphere.MATURE_PLATE,
        Lithosphere.ANCIENT_PLATE,
    ]:
        roll2 = sum(rand.next() for _ in range(3))
        if w.water_prevalence in (Water.EXTENSIVE, Water.MASSIVE):
            roll2 += 6
        if w.water_prevalence in (Water.MINIMAL, Water.TRACE):
            roll2 -= 6
        if lith == Lithosphere.EARLY_PLATE:
            roll2 += 2
        if lith == Lithosphere.ANCIENT_PLATE:
            roll2 -= 2
        tect = Tectonics.MOBILE if roll2 >= 11 else Tectonics.FIXED

    if (
        lith in (Lithosphere.EARLY_PLATE, Lithosphere.MATURE_PLATE)
        and tect == Tectonics.FIXED
    ):
        ep_resurf = True

    if lith == Lithosphere.MOLTEN and new_water != Water.MASSIVE:
        new_water = Water.TRACE
        new_percent = 0

    if new_water == Water.EXTENSIVE:
        roll3 = sum(rand.next() for _ in range(3))
        if lith in [Lithosphere.SOFT, Lithosphere.SOLID]:
            # if lith in (Lithosphere.SOFT, Lithosphere.SOLID):
            new_percent += roll3 + 10
        if lith in [Lithosphere.EARLY_PLATE, Lithosphere.ANCIENT_PLATE]:
            new_percent += roll3
        if new_percent > 100:
            new_percent = 100

    return lith, tect, ep_resurf, new_water, new_percent


# --------------------------------------------------
def calc_magnetic_field(w: World, rand: Dice = Dice()) -> MagneticField:
    roll = sum(rand.next() for _ in range(3))
    if w.lithosphere == Lithosphere.SOFT:
        roll += 4
    if w.tectonics == Tectonics.MOBILE and w.lithosphere in (
        Lithosphere.EARLY_PLATE,
        Lithosphere.ANCIENT_PLATE,
    ):
        roll += 8
    if w.lithosphere == Lithosphere.MATURE_PLATE and w.tectonics == Tectonics.MOBILE:
        roll += 12

    if roll <= 14:
        return MagneticField.NONE
    if 15 <= roll <= 17:
        return MagneticField.WEAK
    if 18 <= roll <= 19:
        return MagneticField.MODERATE
    else:
        return MagneticField.STRONG


# --------------------------------------------------
def calc_arf(w: World, rand: Dice = Dice()) -> float:
    roll = sum(rand.next() for _ in range(3))
    if w.water_prevalence == Water.MASSIVE:
        roll += 6
    if w.green_house:
        roll += 6
    if w.lithosphere == Lithosphere.MOLTEN:
        roll += 6
    if w.lithosphere == Lithosphere.SOFT:
        roll += 4
    if w.lithosphere == Lithosphere.EARLY_PLATE:
        roll += 2
    if w.lithosphere == Lithosphere.ANCIENT_PLATE:
        roll -= 2
    if w.lithosphere == Lithosphere.SOLID:
        roll -= 4
    if w.magnetic_field == MagneticField.MODERATE:
        roll -= 2
    if w.magnetic_field == MagneticField.WEAK:
        roll -= 4
    if w.magnetic_field == MagneticField.NONE:
        roll -= 6
    if roll < 0:
        roll = 0
    return roll / 10.0


# --------------------------------------------------
def calc_mass_hydrogen(w: World) -> float:
    if w.m_number <= 2:
        mass = w.arf * 100
    else:
        mass = 0
    return random.uniform(mass * 0.9, mass * 1.1)


# --------------------------------------------------
def calc_mass_helium(w: World) -> float:
    if w.m_number <= 2:
        mass = w.arf * 25
    elif w.m_number == 3:
        mass = w.arf * 5
    elif w.m_number == 4:
        mass = w.arf
    else:
        mass = 0
    return random.uniform(mass * 0.9, mass * 1.1)


# --------------------------------------------------
def calc_mass_nitrogen(w: World) -> float:
    if w.m_number <= 28 and w.black_body_temp >= 80:
        mass = w.arf * 0.7
        if w.black_body_temp <= 125 and w.water_prevalence == Water.MASSIVE:
            mass *= 15
    else:
        mass = 0
    return random.uniform(mass * 0.9, mass * 1.1)


# --------------------------------------------------
def calc_world_class(w: World) -> WorldClass:
    if w.green_house:
        return WorldClass.ONE
    if w.mass_hydrogen > 0.0:
        return WorldClass.TWO
    if (
        w.mass_hydrogen == 0.0
        and w.mass_nitrogen > 0.0
        and (80 <= w.black_body_temp <= 125)
    ):
        return WorldClass.THREE
    if w.mass_hydrogen == 0.0 and w.mass_nitrogen > 0.0 and w.black_body_temp > 125:
        return WorldClass.FOUR
    if (
        w.mass_hydrogen == 0.0
        and w.mass_helium == 0.0
        and w.mass_nitrogen == 0.0
        and w.m_number <= 44
        and w.black_body_temp > 195
    ):
        return WorldClass.FIVE
    return WorldClass.SIX


# --------------------------------------------------
def calc_albedo(w: World, rand: Dice = Dice()) -> float:
    roll = sum(rand.next() for _ in range(3)) / 100
    if w.world_class == WorldClass.ONE:
        return 0.65 + roll
    if w.world_class == WorldClass.TWO:
        return 0.2 + roll
    if w.world_class == WorldClass.THREE:
        return 0.1 + roll
    if w.world_class in (WorldClass.FOUR, WorldClass.FIVE):
        lookup = {
            Water.TRACE: 0.15,
            Water.MINIMAL: 0.16,
            Water.MODERATE: 0.19,
            Water.EXTENSIVE: 0.22,
            Water.MASSIVE: 0.25,
        }
        return lookup[w.water_prevalence] + roll
    if w.world_class == WorldClass.SIX:
        lookup = {
            Water.TRACE: 0.01,
            Water.MINIMAL: 0.02,
            Water.MODERATE: 0.08,
            Water.EXTENSIVE: 0.14,
            Water.MASSIVE: 0.20,
        }
        a = lookup[w.water_prevalence] + roll
        if w.lithosphere in (Lithosphere.SOFT, Lithosphere.MOLTEN):
            a += 0.5
        if w.lithosphere in (Lithosphere.EARLY_PLATE, Lithosphere.MATURE_PLATE):
            a += 0.3
        if (
            w.lithosphere == Lithosphere.ANCIENT_PLATE
            and w.tectonics == Tectonics.MOBILE
        ):
            a += 0.3
        if (
            w.lithosphere == Lithosphere.ANCIENT_PLATE
            and w.tectonics == Tectonics.FIXED
        ):
            a += 0.3
        if w.lithosphere == Lithosphere.SOLID and w.black_body_temp < 80:
            a += 0.3
        return a


# --------------------------------------------------
def calc_mass_carbon_dioxide(w: World) -> float:
    if w.world_class is WorldClass.ONE:
        mass = 100 * w.arf
    elif w.world_class is WorldClass.SIX:
        mass = 0
    else:
        if w.m_number <= 44 and w.black_body_temp >= 195:
            mass = 10 * w.arf
        else:
            mass = 0
    return random.uniform(mass * 0.9, mass * 1.1)


# --------------------------------------------------
def calc_abio_vents(w: World, rand: Dice = Dice()) -> (bool, int | None):
    if w.world_class == WorldClass.ONE:
        return False, None
    if w.water_prevalence in (Water.TRACE, Water.MINIMAL):
        return False, None
    if w.lithosphere in (Lithosphere.MOLTEN, Lithosphere.SOLID):
        return False, None
    if w.tectonics == Tectonics.FIXED:
        return False, None
    time = 30 * sum(rand.next() for _ in range(3))
    if w.age > time / 1000:
        return True, time
    else:
        return False, None


# --------------------------------------------------
def calc_abio_surface(w: World, rand: Dice = Dice()) -> (bool, int | None):
    if w.world_class in (
        WorldClass.ONE,
        WorldClass.THREE,
        WorldClass.FIVE,
        WorldClass.SIX,
    ):
        return False, None
    if not w.carbon_silicate_cycle:
        return False, None
    if w.lithosphere in (Lithosphere.MOLTEN, Lithosphere.SOLID):
        return False, None

    if w.lithosphere == Lithosphere.SOFT or w.tectonics == Tectonics.MOBILE:
        time_mult = 100
    else:
        time_mult = 200
    time = time_mult * sum(rand.next() for _ in range(3))
    if w.abio_vents_occurred:
        time = min(time, w.time_to_abio_vents * 75)

    if w.age > time / 1000:
        return True, time
    else:
        return False, None


# --------------------------------------------------
def calc_multicellular(w: World, rand: Dice = Dice()) -> (bool, int | None):
    if w.abio_vents_occurred is False and w.abio_surface_occurred is False:
        return False, None

    time = 75 * sum(rand.next() for _ in range(3))
    if w.abio_vents_occurred is True:
        ttav = w.time_to_abio_vents
    else:
        ttav = 50000
    if w.abio_surface_occurred is True:
        ttas = w.time_to_abio_surface
    else:
        ttas = 50000
    time += min(ttav, ttas)

    if w.age > time / 1000:
        return True, time
    else:
        return False, None


def calc_photosynthesis(w: World, rand: Dice = Dice()) -> (bool, int | None):
    if w.abio_surface_occurred is False or w.star_spectrum == "BD":
        return False, None

    time = sum(rand.next() for _ in range(3)) * w.photosynthesis_time_scale
    time += w.time_to_abio_surface

    if w.age > time / 1000:
        return True, time
    else:
        return False, None


def calc_oxygen_cat(w: World, rand: Dice = Dice()) -> (bool, int | None):
    if w.photosynthesis_occurred is False:
        return False, None

    time = sum(rand.next() for _ in range(3)) * w.photosynthesis_time_scale * 1.5
    time += w.time_to_photosynthesis

    if w.age > time / 1000:
        return True, time
    else:
        return False, None


def calc_animals(w: World, rand: Dice = Dice()) -> (bool, int | None):
    if w.multicellular_occured is False:
        return False, None

    time = 300 * sum(rand.next() for _ in range(3))
    time += w.time_to_multicellular
    if w.oxygen_occurred and time > w.time_to_oxygen:
        time -= (time - w.time_to_oxygen) / 2

    if w.age > time / 1000:
        return True, time
    else:
        return False, None


def calc_presentients(w: World, rand: Dice = Dice()) -> (bool, int | None):
    if w.animals_occurred is False:
        return False, None
    mult = 50
    if w.water_prevalence == Water.MASSIVE:
        mult = 100
    time = mult * sum(rand.next() for _ in range(3))
    time += w.time_to_animals

    if w.age > time / 1000:
        return True, time
    else:
        return False, None


# --------------------------------------------------
def calc_mass_oxygen(w: World, rand: Dice = Dice()) -> float:
    if w.photosynthesis_occurred is False and w.oxygen_occurred is False:
        return 0.0
    roll = sum(rand.next() for _ in range(3))
    if w.oxygen_occurred:
        roll += 15
        return w.arf * roll / 100
    return roll * 0.002
