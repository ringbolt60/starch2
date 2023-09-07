#!/usr/bin/env python3
"""
Author : Jon Walters <ringbolt60@gmail.com>
Date   : 2023-08-27
Purpose: Create worlds.
"""

import argparse
import re

from world import (
    WorldType,
    create_world,
)


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
        "--spectral_type",
        help="Spectral type of primary star",
        metavar="str",
        type=str,
        default="G2",
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

    sp = args.spectral_type
    if not re.match(r"[AGKM][0123456789]$|BD$", sp):
        parser.error(f'"{sp}" should be valid spectral type')

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
    world = create_world(args)
    print(world.describe())


# --------------------------------------------------
if __name__ == "__main__":
    main()
