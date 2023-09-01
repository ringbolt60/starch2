#!/usr/bin/env python3
"""tests for main.py"""

import os
import random
import re
import sys
from subprocess import getstatusoutput

sys.path.append(os.path.abspath("../starch2"))

PRG = "../starch2/main.py"


# --------------------------------------------------
def test_exists():
    """exists"""

    assert os.path.isfile(PRG)


# --------------------------------------------------
def test_usage():
    """usage"""

    for flag in ["-h", "--help"]:
        rv, out = getstatusoutput(f"{PRG} {flag}")
        assert rv == 0
        assert re.match("usage", out, re.IGNORECASE)


# --------------------------------------------------
def test_negative_numeric_inputs():
    """Reject numeric inputs that are negative."""

    for arg in ("-m", "-M", "-D", "-s", "-d", "-a", "-k", "-e"):
        bad = (random.random() + 0.1) * -10
        rv, out = getstatusoutput(f"{PRG} NovaTerra lone {arg} {bad}")
        assert rv != 0
        if arg == "-e":
            assert re.search(f'"{bad}" should be zero or a positive float', out)
        else:
            assert re.search(f'"{bad}" should be a positive float', out)


# --------------------------------------------------
def test_zero_numeric_inputs():
    """Reject numeric inputs that are zero."""

    for arg in ("-m", "-M", "-D", "-s", "-d", "-a", "-k"):
        rv, out = getstatusoutput(f"{PRG} NovaTerra lone {arg} 0.0")
        assert rv != 0
        assert re.search('"0.0" should be a positive float', out)


# --------------------------------------------------
def test_bad_numeric_inputs():
    """Reject inputs that cannot be converted to float."""

    bad = "kjahgfdaj"
    for arg in (
        "--mass",
        "--mass_star",
        "--distance_star",
        "--satellite_mass",
        "--distance_primary",
        "--age",
        "--density",
        "--ecc",
    ):
        rv, out = getstatusoutput(f"{PRG} NovaTerra lone {arg} {bad}")
        assert rv != 0
        assert re.search(f"argument ../{arg}: invalid float value: '{bad}'", out)


# --------------------------------------------------
def test_orbited_default_case():
    """Reject incorrect output for orbited case when using default values"""

    rv, out = getstatusoutput(f"{PRG} NovaTerra orbited")
    assert rv == 0
    assert re.match(
        """NovaTerra
Planet with Satellite Age: 4.568 GYr
Mass: 1.000 M♁ Density: 1.000 K♁ Radius: 6378 km
Star Mass: 1.000 M☉ Distance: 1.000 AU Lumin: 1.000 L☉
Satellite Mass: 0.012 M♁ Distance: 384400 km
---
Orbital Period = 8766.0 hours""",
        out,
    )
    assert re.search(r"Rotation Period = \d{1,5}\.\d hours", out)


# --------------------------------------------------
def test_lone_default_case():
    """Reject incorrect output for lone case when using default values"""

    rv, out = getstatusoutput(f"{PRG} NovaTerra lone -l 0.678")
    assert rv == 0
    assert re.match(
        """NovaTerra
Lone Planet Age: 4.568 GYr
Mass: 1.000 M♁ Density: 1.000 K♁ Radius: 6378 km
Star Mass: 1.000 M☉ Distance: 1.000 AU Lumin: 0.678 L☉
---
Orbital Period = 8766.0 hours""",
        out,
    )
    assert re.search(r"Rotation Period = \d{1,5}\.\d hours", out)


# --------------------------------------------------
def test_satellite_default_case():
    """Reject incorrect output for satellite case when using default values"""

    rv, out = getstatusoutput(f"{PRG} Luna satellite")
    assert rv == 0
    assert re.match(
        """Luna
Satellite Age: 4.568 GYr
Mass: 0.012 M♁ Density: 1.000 K♁ Radius: 1472 km
Star Mass: 1.000 M☉ Distance: 1.000 AU Lumin: 1.000 L☉
Primary Mass: 1.000 M♁ Distance: 384400 km
---
Orbital Period = 655.7 hours""",
        out,
    )
    assert re.search(r"Rotation Period = \d{1,5}\.\d hours", out)


# --------------------------------------------------
def test_arcadia_case():
    """Reject incorrect output for lone planet with varied mass, stellar mass and orbital distance"""

    rv, out = getstatusoutput(f"{PRG} Arcadia lone -m 0.93 -M 0.94 -D 0.892 -k 0.879")
    assert rv == 0
    assert re.match(
        """Arcadia
Lone Planet Age: 4.568 GYr
Mass: 0.930 M♁ Density: 0.879 K♁ Radius: 6499 km
Star Mass: 0.940 M☉ Distance: 0.892 AU Lumin: 1.000 L☉
---
Orbital Period = 7617.0 hours""",
        out,
    )
    assert re.search(r"Rotation Period = \d{1,5}\.\d hours", out)


# --------------------------------------------------
def test_new_luna_case():
    """Reject incorrect output for satellite with varied planet mass and satellite mass"""

    rv, out = getstatusoutput(
        f"{PRG} 'New Luna' satellite -s 0.023 -m 0.876 -d 175845 -k 0.519 -l 0.235"
    )
    assert rv == 0
    assert re.match(
        """New Luna
Satellite Age: 4.568 GYr
Mass: 0.023 M♁ Density: 0.519 K♁ Radius: 2257 km
Star Mass: 1.000 M☉ Distance: 1.000 AU Lumin: 0.235 L☉
Primary Mass: 0.876 M♁ Distance: 175845 km
---
Orbital Period = 215.3 hours""",
        out,
    )
    assert re.search(r"Rotation Period = \d{1,5}\.\d hours", out)


def test_lorelei_case():
    """Reject incorrect output for planet with varied planet mass and satellite mass"""

    rv, out = getstatusoutput(
        f"{PRG} Lorelei orbited -m 1.175 -s 0.023 -d 457897 -M 0.138 -D 0.078 -k 0.905"
    )
    assert rv == 0
    assert re.match(
        """Lorelei
Planet with Satellite Age: 4.568 GYr
Mass: 1.175 M♁ Density: 0.905 K♁ Radius: 6958 km
Star Mass: 0.138 M☉ Distance: 0.078 AU Lumin: 1.000 L☉
Satellite Mass: 0.023 M♁ Distance: 457897 km
---
Orbital Period = 514.0 hours""",
        out,
    )
    assert re.search(r"Rotation Period = \d{1,5}\.\d hours", out)
