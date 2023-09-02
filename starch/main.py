#!/usr/bin/env python3
"""
Author : Jon Walters <ringbolt60@gmail.com>
Date   : 2023-08-27
Purpose: Create worlds.
"""

import argparse

from starch import (
    World,
    calc_orbital_period,
    calc_rotation_period,
    calc_obliquity,
    calc_water,
    calc_geophysics,
    calc_magnetic_field,
)
from tables import WorldType


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
        args.type = WorldType.LONE
    elif args.type == "orbited":
        args.type = WorldType.ORBITED
    else:
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
    world = world._replace(magnetic_field=calc_magnetic_field(world))
    print(world.describe())


# --------------------------------------------------
if __name__ == "__main__":
    main()
