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
class Atmosphere(Enum):
    NONE = "Vacuum"
    TRACE = "Trace"
    UNBREATHABLE = "Unbreathable"
    TAINTED = "Tainted"
    BREATHABLE = "Breathable"


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
    gravity: float = 0.0
    radius: float = 0.0
    rotational_period: float = 24.0
    lock: Resonance = Resonance.NONE
    local_day_length: float = 0.0
    days_in_local_year: float = 0.0
    obliquity: int = 0
    unstable_obliquity: bool = False
    black_body_temp: int = 278
    m_number: int = 1
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
    mass_water_vapour: float = 0.0
    world_class: WorldClass = WorldClass.SIX
    albedo: float = 0.1
    abio_vents_occurred: bool = False
    time_to_abio_vents: int | None = None
    abio_surface_occurred: bool = False
    time_to_abio_surface: int | None = None
    carbon_silicate_cycle: bool = False
    multicellular_occurred: bool = False
    time_to_multicellular: int | None = None
    photosynthesis_occurred: bool = False
    time_to_photosynthesis: int | None = None
    oxygen_occurred: bool = False
    time_to_oxygen: int | None = None
    animals_occurred: bool = False
    time_to_animals: int | None = None
    presentients_occurred: bool = False
    time_to_presentients: int | None = None
    surf_temp: int = 278
    methane_present: bool = False
    ozone_present: bool = False
    total_atmospheric_mass: float = 0.0
    atmospheric_pressure: float = 0.0
    partial_oxygen: float = 0.0
    partial_carbon_dioxide: float = 0.0
    partial_nitrogen: float = 0.0
    atmosphere: Atmosphere = Atmosphere.NONE
    scale_height: float = 0.0
    life: str = "Barren"

    def describe(self):
        text = [self.name, f"{self.world_type.value} Age: {self.age:.3f} GYr"]
        if self.world_type == WorldType.SATELLITE:
            text.append(
                f"Mass: {self.satellite_mass:.3f} M♁ Density: {self.density:.3f} K♁ Radius: {self.radius:.0f} km "
                f"Gravity: {self.gravity:.3f} G"
            )
        else:
            text.append(
                f"Mass: {self.planet_mass:.3f} M♁ Density: {self.density:.3f} K♁ Radius: {self.radius:.0f} km "
                f"Gravity: {self.gravity:.3f} G"
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
            f"{self.lithosphere.value} / {self.tectonics.value}"
            f"{' / Episodic Resurfacing' if self.episodic_resurfacing else ''}"
        )
        text.append(f"{self.magnetic_field.value}")
        text.append(
            f"{self.world_class.value}{' CS Cycle present' if self.carbon_silicate_cycle else ''} "
            f"Atmo mass {self.total_atmospheric_mass:.3f} H2: "
            f"{self.mass_hydrogen:.2f} He: {self.mass_helium:.2f} "
            f"N2: {self.mass_nitrogen:.2f} CO2: {self.mass_carbon_dioxide:g} "
            f"O2: {self.mass_oxygen:.2f} H2O vapour: {self.mass_water_vapour:g}"
            f"{' Trace methane' if self.methane_present else ''}"
            f"{' Trace ozone' if self.ozone_present else ''}"
        )
        text.append(
            f"Atmosphere: {self.atmosphere.value} at {self.atmospheric_pressure:.3f} bar ARF: {self.arf} "
            f"pp N2: {self.partial_nitrogen:g} pp CO2: {self.partial_carbon_dioxide:g} "
            f"pp O2: {self.partial_oxygen:g} "
        )
        text.append(f"Albedo: {self.albedo:.2f} Surface Temp: {self.surf_temp:.0f}")
        text.append(
            f"{self.life} [{'Deep sea vents' if self.abio_vents_occurred else ''}"
            f"{' Surface refugia' if self.abio_surface_occurred else ''}"
            f"{' / Multicellular' if self.multicellular_occurred else ''}"
            f"{' / Photosynthetic' if self.photosynthesis_occurred else ''}"
            f"{' / Oxygen Catastrophe' if self.oxygen_occurred else ''}{' / Animals' if self.animals_occurred else ''}"
            f"{' / Pre-sentients' if self.presentients_occurred else ''}]"
        )
        return "\n".join(text)


def _calc_radius(
    wt: WorldType, satellite_mass: float, planet_mass: float, density: float
):
    mass = satellite_mass if wt is WorldType.SATELLITE else planet_mass
    return int(round(6378 * math.pow(mass / density, 1.0 / 3.0), 0))


def _calc_t_number(
    wt: WorldType,
    star_mass: float,
    star_distance: float,
    satellite_mass: float,
    primary_distance: float,
    age: float,
    radius: float,
    planet_mass: float,
) -> float:
    if wt is WorldType.SATELLITE:
        return 0

    if wt is WorldType.LONE:
        const = 9.6e-14
        mass = star_mass
        distance = star_distance
    else:
        const = 1e25
        mass = satellite_mass
        distance = primary_distance

    return (
        const
        * age
        * math.pow(mass, 2)
        * math.pow(radius, 3)
        / planet_mass
        / math.pow(distance, 6)
    )


def _calc_local_day_length(
    lock: Resonance, orbital_period: float, rotational_period: float
) -> float | None:
    if lock == Resonance.LOCK_TO_STAR:
        return None
    return orbital_period * rotational_period / (rotational_period + orbital_period)


def _calc_days_in_local_year(
    lock: Resonance, orbital_period: float, local_day_length: float
) -> float | str:
    if lock == Resonance.LOCK_TO_STAR:
        return "N/A"
    return orbital_period / local_day_length


# TODO Implement synodic month calculations
def synodic_month_length() -> float | str:
    return "TBI"


def _calc_black_body_temp(luminosity, star_distance) -> int:
    bbt = round(278 * math.pow(luminosity, 0.25) / math.sqrt(star_distance), 0)
    return int(bbt)


def _calc_m_number(black_body_temp: int, density: float, radius: float) -> int:
    m = 700000 * black_body_temp / density / math.pow(radius, 2)
    return int(m + 0.99999999)


def _calc_gravity(
    wt: WorldType, satellite_mass: float, planet_mass: float, density: float
) -> float:
    mass = satellite_mass if wt is WorldType.SATELLITE else planet_mass
    return math.pow(mass * math.pow(density, 2), 1.0 / 3.0)


def _calc_carbon_silicate_cycle(
    mass_carbon_dioxide: float,
    black_body_temp: int,
    albedo: float,
    water_prevalence: Water,
) -> bool:
    t_ccs = 0.0
    if mass_carbon_dioxide > 0:
        t_ccs = (
            black_body_temp * math.pow((1 - albedo), 0.25)
            + 8 * math.log10(mass_carbon_dioxide)
            + 36.0
        )

    return bool(water_prevalence in (Water.MODERATE, Water.EXTENSIVE) and t_ccs >= 260)


def _calc_life(
    photosynthesis_occurred, abio_surface_occurred, abio_vents_occurred
) -> str:
    if photosynthesis_occurred:
        return "Aerobic Life"
    if abio_surface_occurred or abio_vents_occurred:
        return "Anaerobic life"
    else:
        return "Barren"


def _calc_photosynthesis_time_scale(star_spectrum: str):
    mult = 100
    if re.match(r"G[89]", star_spectrum):
        mult = 105
    if star_spectrum[0] == "M":
        mult = 300
    if star_spectrum[0] == "K":
        lookup = (110, 115, 120, 130, 145, 160, 180, 210, 240, 240)
        x = int(star_spectrum[1])
        mult = lookup[x]
    return mult


def _calc_partial_pressure(
    total_atmospheric_mass: float, atmospheric_pressure: float, mass_partial: float
):
    if total_atmospheric_mass > 0:
        return atmospheric_pressure * mass_partial / total_atmospheric_mass
    else:
        return 0


def _calc_scale_height(
    mass_hydrogen: float,
    mass_helium: float,
    mass_water_vapour: float,
    mass_nitrogen: float,
    mass_oxygen: float,
    mass_carbon_dioxide: float,
    total_atmospheric_mass: float,
    surf_temp: int,
    gravity: float,
):
    if total_atmospheric_mass == 0:
        return 0
    k = 2 * mass_hydrogen + 4 * mass_helium
    k += 18 * mass_water_vapour + 28 * mass_nitrogen
    k += 32 * mass_oxygen + 44 * mass_carbon_dioxide
    k /= total_atmospheric_mass
    return 0.856 * surf_temp / k / gravity


def create_world(args, rand: Dice = Dice()) -> World:
    """Creates a new world from the seed parameters."""

    orbital_period = _calc_orbital_period(
        args.type,
        args.distance_primary,
        args.mass,
        args.satellite_mass,
        args.mass_star,
        args.distance_star,
    )
    radius = _calc_radius(args.type, args.satellite_mass, args.mass, args.density)
    t_number = _calc_t_number(
        args.type,
        args.mass_star,
        args.distance_star,
        args.satellite_mass,
        args.distance_primary,
        args.age,
        radius,
        args.mass,
    )
    t_adj = int(round(t_number * 12, 0))

    rotation_period, lock = _calc_rotation_period(
        args.type,
        t_number,
        t_adj,
        orbital_period,
        args.ecc,
        args.distance_primary,
        args.satellite_mass,
        args.mass,
        rand,
    )
    local_day_length = _calc_local_day_length(lock, orbital_period, rotation_period)
    days_in_local_year = _calc_days_in_local_year(
        lock, orbital_period, local_day_length
    )
    obl, instability = _calc_obliquity(args.type, t_adj, lock, rand)
    black_body_temp = _calc_black_body_temp(args.luminosity, args.distance_star)
    m_number = _calc_m_number(black_body_temp, args.density, radius)
    water, water_percent, greenhouse = _calc_water(
        m_number,
        black_body_temp,
        args.rocky_sat,
        args.outside_ice_line,
        args.grand_tack,
        args.oort_cloud,
        rand,
    )
    gravity = _calc_gravity(args.type, args.satellite_mass, args.mass, args.density)
    lith, tect, epi_resurface, water, water_percent = _calc_geophysics(
        args.type,
        args.age,
        gravity,
        args.metal,
        False,
        args.mass,
        radius,
        args.distance_primary,
        lock,
        args.ecc,
        args.mass_star,
        args.distance_star,
        water,
        water_percent,
        rand,
    )
    magnetic_field = _calc_magnetic_field(lith, tect, rand)
    arf = _calc_arf(water, greenhouse, lith, magnetic_field, rand)
    mass_hydrogen = _calc_mass_hydrogen(m_number, arf)
    mass_helium = _calc_mass_helium(m_number, arf)
    mass_nitrogen = _calc_mass_nitrogen(m_number, black_body_temp, arf, water)
    world_class = _calc_world_class(
        greenhouse, mass_hydrogen, mass_nitrogen, black_body_temp, mass_helium, m_number
    )
    albedo = _calc_albedo(world_class, water, lith, tect, black_body_temp, rand)
    mass_carbon_dioxide = _calc_mass_carbon_dioxide(
        world_class, arf, m_number, black_body_temp
    )
    abio_vent, abio_vent_time = _calc_abio_vents(
        world_class, water, lith, tect, args.age, rand
    )
    carbon_silicate_cycle = _calc_carbon_silicate_cycle(
        mass_carbon_dioxide, black_body_temp, albedo, water
    )
    abio_surf, abio_surf_time = _calc_abio_surface(
        world_class,
        carbon_silicate_cycle,
        lith,
        tect,
        abio_vent,
        abio_vent_time,
        args.age,
        rand,
    )
    multi, multi_time = _calc_multicellular(
        abio_vent, abio_surf, abio_vent_time, abio_surf_time, args.age
    )
    photo_time_scale = _calc_photosynthesis_time_scale(args.spectral_type)
    photo, photo_time = _calc_photosynthesis(
        abio_surf, args.spectral_type, photo_time_scale, abio_surf_time, args.age
    )
    oxy, oxy_time = _calc_oxygen_cat(
        photo, photo_time_scale, photo_time, args.age, rand
    )
    anim, anim_time = _calc_animals(multi, multi_time, oxy, oxy_time, args.age, rand)
    pre, pre_time = _calc_presentients(anim, water, anim_time, args.age, rand)
    mass_oxygen = _calc_mass_oxygen(photo, oxy, arf)
    surf_temp, methane, ozone = _calc_base_surf_temp(
        black_body_temp,
        albedo,
        world_class,
        mass_carbon_dioxide,
        arf,
        abio_surf,
        abio_vent,
        m_number,
        oxy,
        carbon_silicate_cycle,
    )
    surf_temp, mass_carbon_dioxide = _adjust_for_carbon_dioxide(
        surf_temp, mass_carbon_dioxide, carbon_silicate_cycle, rand
    )
    surf_temp, mass_water_vapour = _calc_water_vapour(
        surf_temp, m_number, black_body_temp, water
    )
    total_atmospheric_mass = (
        mass_oxygen
        + mass_helium
        + mass_nitrogen
        + mass_carbon_dioxide
        + mass_water_vapour
        + mass_hydrogen
    )
    atmospheric_pressure = gravity * total_atmospheric_mass
    partial_oxygen = _calc_partial_pressure(
        total_atmospheric_mass, atmospheric_pressure, mass_oxygen
    )
    partial_carbon_dioxide = _calc_partial_pressure(
        total_atmospheric_mass, atmospheric_pressure, mass_carbon_dioxide
    )
    partial_nitrogen = _calc_partial_pressure(
        total_atmospheric_mass, atmospheric_pressure, mass_nitrogen
    )
    breathability = _calc_breathability(
        atmospheric_pressure,
        partial_oxygen,
        partial_carbon_dioxide,
        partial_nitrogen,
        total_atmospheric_mass,
        arf,
    )
    scale_height = _calc_scale_height(
        mass_hydrogen,
        mass_helium,
        mass_water_vapour,
        mass_nitrogen,
        mass_oxygen,
        mass_carbon_dioxide,
        total_atmospheric_mass,
        surf_temp,
        gravity,
    )
    life = _calc_life(photo, abio_surf, abio_vent)

    return World(
        name=args.name,
        world_type=args.type,
        planet_mass=args.mass,
        star_spectrum=args.spectral_type,
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
        orbital_period=orbital_period,
        gravity=gravity,
        radius=radius,
        rotational_period=rotation_period,
        lock=lock,
        local_day_length=local_day_length,
        days_in_local_year=days_in_local_year,
        obliquity=obl,
        unstable_obliquity=instability,
        black_body_temp=black_body_temp,
        m_number=m_number,
        water_prevalence=water,
        water_percent=water_percent,
        lithosphere=lith,
        tectonics=tect,
        episodic_resurfacing=epi_resurface,
        orbital_tidal_heating=False,
        magnetic_field=magnetic_field,
        arf=arf,
        mass_hydrogen=mass_hydrogen,
        mass_helium=mass_helium,
        mass_nitrogen=mass_nitrogen,
        mass_carbon_dioxide=mass_carbon_dioxide,
        mass_oxygen=mass_oxygen,
        mass_water_vapour=mass_water_vapour,
        world_class=world_class,
        albedo=albedo,
        abio_vents_occurred=abio_vent,
        time_to_abio_vents=abio_vent_time,
        abio_surface_occurred=abio_surf,
        time_to_abio_surface=abio_surf_time,
        carbon_silicate_cycle=carbon_silicate_cycle,
        multicellular_occurred=multi,
        time_to_multicellular=multi_time,
        photosynthesis_occurred=photo,
        time_to_photosynthesis=photo_time,
        oxygen_occurred=oxy,
        time_to_oxygen=oxy_time,
        animals_occurred=anim,
        time_to_animals=anim_time,
        presentients_occurred=pre,
        time_to_presentients=pre_time,
        surf_temp=surf_temp,
        methane_present=methane,
        ozone_present=ozone,
        total_atmospheric_mass=total_atmospheric_mass,
        atmospheric_pressure=atmospheric_pressure,
        partial_oxygen=partial_oxygen,
        partial_carbon_dioxide=partial_carbon_dioxide,
        partial_nitrogen=partial_nitrogen,
        atmosphere=breathability,
        scale_height=scale_height,
        life=life,
    )


# --------------------------------------------------
def _calc_orbital_period(
    wt: WorldType,
    prime_dist: float,
    pl_mass: float,
    sat_mass: float,
    star_mass: float,
    star_distance: float,
) -> float:
    """
    Returns orbital period around primary in hours.

    Implements Step 18 pp 92,93. Constants tweaked to make earth and Luna exact.
    """
    if prime_dist <= 0:
        raise ValueError("prime_dist must be positive")
    if pl_mass <= 0:
        raise ValueError("pl_mass must be positive")
    if sat_mass <= 0:
        raise ValueError("sat_mass must be positive")
    if star_mass <= 0:
        raise ValueError("star_mass must be positive")
    if star_distance <= 0:
        raise ValueError("star_distance must be positive")

    if wt == WorldType.SATELLITE:
        return 2.768e-6 * math.sqrt(math.pow(prime_dist, 3) / (sat_mass + pl_mass))
    return 8766.0 * math.sqrt(math.pow(star_distance, 3) / star_mass)


# --------------------------------------------------
def _calc_rotation_period(
    wt: WorldType,
    t_number: float,
    t_adj: int,
    orbital_period: float,
    ecc: float,
    primary_distance: float,
    satellite_mass: float,
    planet_mass: float,
    rand: Dice = Dice(),
) -> (float, Resonance):
    """
    Returns sidereal rotation period of world.

    Implements Step 19 pp 93-95. Constants tweaked to make earth and Luna exact.
    """
    roll = sum(rand.next() for _ in range(3)) + t_adj
    if wt == WorldType.SATELLITE:
        return orbital_period, Resonance.LOCK_TO_PRIMARY

    if t_number >= 2 or roll >= 24:
        if wt == WorldType.LONE:
            period = orbital_period
            lock, period = _adjust_for_eccentricity(ecc, period)
            return period, lock
        return (
            2.768e-6
            * math.sqrt(math.pow(primary_distance, 3) / (satellite_mass + planet_mass)),
            Resonance.LOCK_TO_SATELLITE,
        )

    p = look_up(t.planet_rotation_rate, roll)
    lower, upper = p
    period = random.uniform(lower, upper)
    lock = Resonance.NONE
    if period >= orbital_period:
        period = orbital_period
        lock, period = _adjust_for_eccentricity(ecc, period)
    return period, lock


# --------------------------------------------------
def _calc_water(
    m_number: int,
    black_body_temp: int,
    rocky_sat: bool,
    outside_ice_line: bool,
    grand_tack: bool,
    oort_cloud: bool,
    rand: Dice = Dice(),
) -> (Water, int, bool):
    """
    Returns the water prevalence and percentage.

    Implements Step 23 pp 101-103.
    """
    water = Water.TRACE
    percentage = 0
    gh = False

    if m_number <= 2:
        water = Water.MASSIVE
        percentage = 100
    elif m_number >= 29:
        if black_body_temp >= 125 or rocky_sat:
            water = Water.TRACE
            percentage = 0
        else:
            water = Water.MASSIVE
            percentage = 100
    else:
        mod = 0
        if outside_ice_line:
            water = Water.MASSIVE
            percentage = 100
        else:
            mod = -m_number
            if grand_tack:
                mod += 6
            if oort_cloud:
                mod += 3
        look_up_value = sum(rand.next() for _ in range(3)) + mod
        lower, upper, water = look_up(t.hydro_cover, look_up_value)
        water = Water.from_text(water)
        percentage = random.uniform(lower, upper)

    if m_number > 2 and black_body_temp >= 300:
        if water == Water.MINIMAL:
            if sum(rand.next() for _ in range(3)) + black_body_temp >= 318:
                water = Water.TRACE
                percentage = 0
        if water in [
            Water.MODERATE,
            Water.EXTENSIVE,
            Water.MASSIVE,
        ]:
            if sum(rand.next() for _ in range(3)) + black_body_temp >= 318:
                water = Water.TRACE
                percentage = 0
                gh = True

    return water, percentage, gh


# --------------------------------------------------
def _adjust_for_eccentricity(ecc=0.0, period=1.0):
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
def _calc_obliquity(
    wt: WorldType, t_adj: int, lock: Resonance, rand: Dice = Dice()
) -> (int, bool):
    """
    Calculate planet obliquity.

    Step 20, pp 96-97
    """
    roll = sum(rand.next() for _ in range(3))
    instability = False
    mod = 0

    if wt is WorldType.SATELLITE or lock != Resonance.NONE:
        obl = roll - 8 if roll > 8 else 0
        return obl, instability

    if wt is WorldType.LONE:
        roll2 = sum(rand.next() for _ in range(3))
        if not 8 <= roll2 <= 13:
            mod = -7
            instability = True

    look_up_value = t_adj + roll + mod
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
def _calc_geophysics(
    wt: WorldType,
    age: float,
    gravity: float,
    metal: float,
    orbital_tidal_heating: bool,
    planet_mass: float,
    radius: float,
    primary_distance: float,
    lock: Resonance,
    ecc: float,
    star_mass: float,
    star_distance: float,
    water_prevalence: Water,
    water_percent: float,
    rand: Dice = Dice(),
) -> (Lithosphere, Tectonics, bool, Water, float):
    """Calculate planet geophysical parameters

    Implements Step 24, pp 104-108
    """
    lith, tect, ep_resurf, new_water, new_percent = (
        Lithosphere.SOLID,
        Tectonics.NONE,
        False,
        water_prevalence,
        water_percent,
    )
    age_mod = int(round(8 * age, 0))
    primordial_heat_mod = int(round(-60 * math.log10(gravity), 0))
    radiogenic_heat_mod = int(round(-10 * math.log10(metal), 0))
    roll1 = sum(rand.next() for _ in range(3))
    lookup = age_mod + primordial_heat_mod + radiogenic_heat_mod + roll1
    lith, ordinal = look_up(t.lithosphere, lookup)
    lith = Lithosphere.from_text(lith)

    f = 0
    if orbital_tidal_heating and wt is WorldType.SATELLITE:
        f = 1.59e15 * planet_mass * radius / math.pow(primary_distance, 3)

    if (lock is not Resonance.NONE) and (wt is not WorldType.SATELLITE):
        if (
            ecc >= 0.05
            or lock
            in (
                Resonance.RESONANCE_5_2,
                Resonance.RESONANCE_2_1,
                Resonance.RESONANCE_3_2,
                Resonance.RESONANCE_3_1,
            )
            or orbital_tidal_heating
        ):
            f = 1.57e-4 * star_mass * radius / math.pow(star_distance, 3)

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
        if water_prevalence in (Water.EXTENSIVE, Water.MASSIVE):
            roll2 += 6
        if water_prevalence in (Water.MINIMAL, Water.TRACE):
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

    if lith is Lithosphere.MOLTEN and new_water is not Water.MASSIVE:
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
def _calc_magnetic_field(
    lithosphere: Lithosphere, tectonics: Tectonics, rand: Dice = Dice()
) -> MagneticField:
    roll = sum(rand.next() for _ in range(3))
    if lithosphere is Lithosphere.SOFT:
        roll += 4
    if tectonics is Tectonics.MOBILE and lithosphere in (
        Lithosphere.EARLY_PLATE,
        Lithosphere.ANCIENT_PLATE,
    ):
        roll += 8
    if lithosphere == Lithosphere.MATURE_PLATE and tectonics == Tectonics.MOBILE:
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
def _calc_arf(
    water_prevalence: Water,
    green_house: bool,
    lithosphere: Lithosphere,
    magnetic_field: MagneticField,
    rand: Dice = Dice(),
) -> float:
    roll = sum(rand.next() for _ in range(3))
    if water_prevalence == Water.MASSIVE:
        roll += 6
    if green_house:
        roll += 6
    if lithosphere == Lithosphere.MOLTEN:
        roll += 6
    if lithosphere == Lithosphere.SOFT:
        roll += 4
    if lithosphere == Lithosphere.EARLY_PLATE:
        roll += 2
    if lithosphere == Lithosphere.ANCIENT_PLATE:
        roll -= 2
    if lithosphere == Lithosphere.SOLID:
        roll -= 4
    if magnetic_field == MagneticField.MODERATE:
        roll -= 2
    if magnetic_field == MagneticField.WEAK:
        roll -= 4
    if magnetic_field == MagneticField.NONE:
        roll -= 6
    if roll < 0:
        roll = 0
    return roll / 10.0


# --------------------------------------------------
def _calc_mass_hydrogen(m_number, arf) -> float:
    if m_number <= 2:
        mass = arf * 100
    else:
        mass = 0
    return random.uniform(mass * 0.9, mass * 1.1)


# --------------------------------------------------
def _calc_mass_helium(m_number, arf) -> float:
    if m_number <= 2:
        mass = arf * 25
    elif m_number == 3:
        mass = arf * 5
    elif m_number == 4:
        mass = arf
    else:
        mass = 0
    return random.uniform(mass * 0.9, mass * 1.1)


# --------------------------------------------------
def _calc_mass_nitrogen(m_number, black_body_temp, arf, water_prevalence) -> float:
    if m_number <= 28 and black_body_temp >= 80:
        mass = arf * 0.7
        if black_body_temp <= 125 and water_prevalence is Water.MASSIVE:
            mass *= 15
    else:
        mass = 0
    return random.uniform(mass * 0.9, mass * 1.1)


# --------------------------------------------------
def _calc_world_class(
    green_house: bool,
    mass_hydrogen: float,
    mass_nitrogen: float,
    black_body_temp: int,
    mass_helium: float,
    m_number: int,
) -> WorldClass:
    if green_house:
        return WorldClass.ONE
    if mass_hydrogen > 0.0:
        return WorldClass.TWO
    if mass_hydrogen == 0.0 and mass_nitrogen > 0.0 and (80 <= black_body_temp <= 125):
        return WorldClass.THREE
    if mass_hydrogen == 0.0 and mass_nitrogen > 0.0 and black_body_temp > 125:
        return WorldClass.FOUR
    if (
        mass_hydrogen == 0.0
        and mass_helium == 0.0
        and mass_nitrogen == 0.0
        and m_number <= 44
        and black_body_temp > 195
    ):
        return WorldClass.FIVE
    return WorldClass.SIX


# --------------------------------------------------
def _calc_albedo(
    wc: WorldClass,
    water_prevalence: Water,
    lithosphere: Lithosphere,
    tectonics: Tectonics,
    black_body_temp: int,
    rand: Dice = Dice(),
) -> float:
    roll = sum(rand.next() for _ in range(3)) / 100
    if wc is WorldClass.ONE:
        return 0.65 + roll
    if wc is WorldClass.TWO:
        return 0.2 + roll
    if wc is WorldClass.THREE:
        return 0.1 + roll
    if wc in (WorldClass.FOUR, WorldClass.FIVE):
        lookup = {
            Water.TRACE: 0.15,
            Water.MINIMAL: 0.16,
            Water.MODERATE: 0.19,
            Water.EXTENSIVE: 0.22,
            Water.MASSIVE: 0.25,
        }
        return lookup[water_prevalence] + roll
    if wc is WorldClass.SIX:
        lookup = {
            Water.TRACE: 0.01,
            Water.MINIMAL: 0.02,
            Water.MODERATE: 0.08,
            Water.EXTENSIVE: 0.14,
            Water.MASSIVE: 0.20,
        }
        a = lookup[water_prevalence] + roll
        if lithosphere in (Lithosphere.SOFT, Lithosphere.MOLTEN):
            a += 0.5
        if lithosphere in (Lithosphere.EARLY_PLATE, Lithosphere.MATURE_PLATE):
            a += 0.3
        if lithosphere == Lithosphere.ANCIENT_PLATE and tectonics == Tectonics.MOBILE:
            a += 0.3
        if lithosphere == Lithosphere.ANCIENT_PLATE and tectonics == Tectonics.FIXED:
            a += 0.3
        if lithosphere == Lithosphere.SOLID and black_body_temp < 80:
            a += 0.3
        return a


# --------------------------------------------------
def _calc_mass_carbon_dioxide(
    wc: WorldClass, arf: float, m_number: float, black_body_temp: float
) -> float:
    if wc is WorldClass.ONE:
        mass = 100 * arf
    elif wc is WorldClass.SIX:
        mass = 0
    else:
        if m_number <= 44 and black_body_temp >= 195:
            mass = 10 * arf
        else:
            mass = 0
    return random.uniform(mass * 0.9, mass * 1.1)


# --------------------------------------------------
def _calc_abio_vents(
    wc: WorldClass,
    water_prevalence: Water,
    lithosphere: Lithosphere,
    tectonics: Tectonics,
    age: float,
    rand: Dice = Dice(),
) -> (bool, int | None):
    if wc is WorldClass.ONE:
        return False, None
    if water_prevalence in (Water.TRACE, Water.MINIMAL):
        return False, None
    if lithosphere in (Lithosphere.MOLTEN, Lithosphere.SOLID):
        return False, None
    if tectonics is Tectonics.FIXED:
        return False, None
    time = 30 * sum(rand.next() for _ in range(3))
    if age > time / 1000:
        return True, time
    else:
        return False, None


# --------------------------------------------------
def _calc_abio_surface(
    wc: WorldClass,
    carbon_silicate_cycle: bool,
    lithosphere: Lithosphere,
    tectonics: Tectonics,
    abio_vents_occurred: bool,
    time_to_abio_vents: float,
    age: float,
    rand: Dice = Dice(),
) -> (bool, int | None):
    if wc in (
        WorldClass.ONE,
        WorldClass.THREE,
        WorldClass.FIVE,
        WorldClass.SIX,
    ):
        return False, None
    if not carbon_silicate_cycle:
        return False, None
    if lithosphere in (Lithosphere.MOLTEN, Lithosphere.SOLID):
        return False, None

    if lithosphere == Lithosphere.SOFT or tectonics == Tectonics.MOBILE:
        time_mult = 100
    else:
        time_mult = 200
    time = time_mult * sum(rand.next() for _ in range(3))
    if abio_vents_occurred:
        time = min(time, time_to_abio_vents * 75)

    if age > time / 1000:
        return True, time
    else:
        return False, None


# --------------------------------------------------
def _calc_multicellular(
    abio_vents_occurred: bool,
    abio_surface_occurred: bool,
    time_to_abio_vents: int,
    time_to_abio_surface: int,
    age: float,
    rand: Dice = Dice(),
) -> (bool, int | None):
    if abio_vents_occurred is False and abio_surface_occurred is False:
        return False, None

    time = 75 * sum(rand.next() for _ in range(3))
    if abio_vents_occurred is True:
        ttav = time_to_abio_vents
    else:
        ttav = 50000
    if abio_surface_occurred is True:
        ttas = time_to_abio_surface
    else:
        ttas = 50000
    time += min(ttav, ttas)

    if age > time / 1000:
        return True, time
    else:
        return False, None


def _calc_photosynthesis(
    abio_surface_occurred: bool,
    star_spectrum: str,
    photosynthesis_time_scale: float,
    time_to_abio_surface: int,
    age: float,
    rand: Dice = Dice(),
) -> (bool, int | None):
    if abio_surface_occurred is False or star_spectrum == "BD":
        return False, None

    time = sum(rand.next() for _ in range(3)) * photosynthesis_time_scale
    time += time_to_abio_surface

    if age > time / 1000:
        return True, time
    else:
        return False, None


def _calc_oxygen_cat(
    photosynthesis_occurred: bool,
    photosynthesis_time_scale: float,
    time_to_photosynthesis: float,
    age: float,
    rand: Dice = Dice(),
) -> (bool, int | None):
    if photosynthesis_occurred is False:
        return False, None

    time = sum(rand.next() for _ in range(3)) * photosynthesis_time_scale * 1.5
    time += time_to_photosynthesis

    if age > time / 1000:
        return True, time
    else:
        return False, None


def _calc_animals(
    multicellular_occurred: bool,
    time_to_multicellular: float,
    oxygen_occurred: bool,
    time_to_oxygen: float,
    age: float,
    rand: Dice = Dice(),
) -> (bool, int | None):
    if multicellular_occurred is False:
        return False, None

    time = 300 * sum(rand.next() for _ in range(3))
    time += time_to_multicellular
    if oxygen_occurred and time > time_to_oxygen:
        time -= (time - time_to_oxygen) / 2

    if age > time / 1000:
        return True, time
    else:
        return False, None


def _calc_presentients(
    animals_occurred: bool,
    water_prevalence: Water,
    time_to_animals: float,
    age: float,
    rand: Dice = Dice(),
) -> (bool, int | None):
    if animals_occurred is False:
        return False, None
    mult = 50
    if water_prevalence == Water.MASSIVE:
        mult = 100
    time = mult * sum(rand.next() for _ in range(3))
    time += time_to_animals

    if age > time / 1000:
        return True, time
    else:
        return False, None


# --------------------------------------------------
def _calc_mass_oxygen(
    photosynthesis_occurred: bool,
    oxygen_occurred: bool,
    arf: float,
    rand: Dice = Dice(),
) -> float:
    if photosynthesis_occurred is False and oxygen_occurred is False:
        return 0.0
    roll = sum(rand.next() for _ in range(3))
    if oxygen_occurred:
        roll += 15
        return arf * roll / 100
    return roll * 0.002


def _calc_base_surf_temp(
    black_body_temp: int,
    albedo: float,
    wc: WorldClass,
    mass_carbon_dioxide,
    arf: float,
    abio_surface_occurred: bool,
    abio_vents_occurred: bool,
    m_number: int,
    oxygen_occurred: bool,
    carbon_silicate_cycle: bool,
) -> (int, bool, bool):
    """Step 30 first half"""
    base_temp = black_body_temp * math.pow((1 - albedo), 0.25)
    temp = 278.45
    methane_present = False
    ozone_present = False
    if wc is WorldClass.ONE:
        if mass_carbon_dioxide > 0:
            temp = base_temp + 250 * math.log10(mass_carbon_dioxide)
    elif wc is WorldClass.SIX:
        temp = base_temp
    elif arf == 0.0:
        temp = base_temp
    else:
        temp = base_temp
        if wc in (WorldClass.TWO, WorldClass.THREE) or (
            wc is WorldClass.FOUR and (abio_surface_occurred or abio_vents_occurred)
        ):
            if black_body_temp >= 110 and m_number <= 16:
                temp += int(2.1 + 8 * math.log10(arf))
                methane_present = True
        if oxygen_occurred:
            temp += int(1.7 + 8 * math.log10(arf))
            ozone_present = True
        if carbon_silicate_cycle:
            pass

    return int(round(temp, 0)), methane_present, ozone_present


# --------------------------------------------------
def _adjust_for_carbon_dioxide(
    surf_temp: int,
    mass_carbon_dioxide: float,
    carbon_silicate_cycle: bool,
    rand: Dice = Dice(),
) -> (int, float):
    new_temp = surf_temp
    new_mass_carbon_dioxide = mass_carbon_dioxide
    if carbon_silicate_cycle:
        temp_mod = max(8, 260 - surf_temp)
        temp_mod += sum(rand.next() for _ in range(3)) - 7
        new_temp += temp_mod
        new_mass_carbon_dioxide = 3.16e-5 * math.pow(1.333, temp_mod)
    else:
        if mass_carbon_dioxide > 0.0:
            new_temp = surf_temp + 36 + 8 * math.log10(mass_carbon_dioxide)

    return int(round(new_temp, 0)), new_mass_carbon_dioxide


# --------------------------------------------------
def _calc_water_vapour(
    surf_temp: int, m_number: int, black_body_temp: int, water_prevalence: Water
) -> (int, float):
    new_temp = surf_temp
    mass_water_vapour = 0.0
    if (
        m_number <= 18
        and black_body_temp >= 260
        and water_prevalence in (Water.MODERATE, Water.EXTENSIVE, Water.MASSIVE)
    ):
        temp_add = look_up(t.water_vapour, new_temp)
        if new_temp > 333:
            temp_add += int((new_temp - 333) / 5 + 0.99999)
        if water_prevalence is Water.EXTENSIVE:
            temp_add += 3
        if water_prevalence is Water.MASSIVE:
            temp_add += 4
        new_temp += temp_add
        mass_water_vapour = 1.78e-5 * math.pow(1.333, temp_add)

    return int(round(new_temp, 0)), mass_water_vapour


def _calc_breathability(
    atmospheric_pressure: float,
    partial_oxygen: float,
    partial_carbon_dioxide: float,
    partial_nitrogen: float,
    total_atmospheric_mass: float,
    arf: float,
) -> Atmosphere:
    if (
        atmospheric_pressure >= 0.1
        and 0.12 <= partial_oxygen <= 0.3
        and partial_carbon_dioxide <= 0.015
        and partial_nitrogen <= 4.0
    ):
        return Atmosphere.BREATHABLE
    if partial_oxygen > 0:
        return Atmosphere.TAINTED
    if arf > 0 and total_atmospheric_mass == 0:
        return Atmosphere.TRACE
    if arf == 0:
        return Atmosphere.NONE
    return Atmosphere.UNBREATHABLE
