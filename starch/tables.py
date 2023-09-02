# --------------------------------------------------
from enum import Enum


def look_up(table, selection_value):
    result = table[-1][1]
    for row in table:
        score, entry = row
        if selection_value <= score:
            result = entry
            break
    return result


class Water(Enum):
    TRACE = "Trace"
    MINIMAL = "Minimal"
    MODERATE = "Moderate"
    EXTENSIVE = "Extensive"
    MASSIVE = "Massive"


class Lithosphere(Enum):
    MOLTEN = "Molten Lithosphere"
    SOFT = "Soft Lithosphere"
    EARLY_PLATE = "Early Plate Lithosphere"
    MATURE_PLATE = "Mature Plate Lithosphere"
    ANCIENT_PLATE = "Ancient Plate Lithosphere"
    SOLID = "Solid Plate Lithosphere"


# --------------------------------------------------
class WorldType(Enum):
    LONE = "Lone Planet"
    ORBITED = "Planet with Satellite"
    SATELLITE = "Satellite"


# --------------------------------------------------


# --------------------------------------------------
class Tectonics(Enum):
    NONE = "No plate tectonics"
    MOBILE = "Mobile plate tectonics"
    FIXED = "Fixed Plate Tectonics"


# --------------------------------------------------


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
# Determines rotation rate of planet
# Random selection by 3d6 + T value
# Tuple is (dice roll, result)
# Result is (minimum period, maximum period)
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

# Determines obliquity of planet
# Random selection by d6 + T value
# Tuple is (dice roll, result)
# Result is (minimum obliquity, obliquity period) except
# Lowest result is "Extreme"
# Highest result is "Minimal"
planet_obliquity_table = [
    (4, "Extreme"),
    (5, (46, 49)),
    (6, (44, 48)),
    (7, (42, 46)),
    (8, (40, 44)),
    (9, (38, 42)),
    (10, (36, 40)),
    (11, (34, 38)),
    (12, (32, 36)),
    (13, (30, 34)),
    (14, (28, 32)),
    (15, (26, 30)),
    (16, (24, 28)),
    (17, (22, 26)),
    (18, (20, 24)),
    (19, (18, 22)),
    (20, (16, 20)),
    (21, (14, 18)),
    (22, (12, 16)),
    (23, (10, 14)),
    (24, (10, 12)),
    (25, "Minimal"),
]

# Determines extreme obliquity of planet
# Random selection by d6
# Tuple is (dice roll, result)
# Result is (minimum obliquity, maximum obliquity) except
# Highest result is "Roll more"
planet_extreme_obliquity_table = [
    (2, (50, 60)),
    (3, (50, 70)),
    (4, (60, 80)),
    (5, (70, 80)),
    (6, "Roll more"),
]

# Determines the percentage coverage of water on a planet
# Look up table
# Result is (minimum cover, maximum cover, prevalence)
hydro_cover = [
    (-5, (0, 0, Water.TRACE)),
    (-1, (0, 1, Water.MINIMAL)),
    (0, (0, 2, Water.MINIMAL)),
    (1, (1, 3, Water.MINIMAL)),
    (2, (2, 5, Water.MINIMAL)),
    (3, (3, 7.5, Water.MINIMAL)),
    (4, (5, 10, Water.MODERATE)),
    (5, (7.5, 20, Water.MODERATE)),
    (6, (10, 30, Water.MODERATE)),
    (7, (20, 40, Water.MODERATE)),
    (8, (30, 50, Water.MODERATE)),
    (9, (40, 55, Water.MODERATE)),
    (10, (50, 60, Water.MODERATE)),
    (11, (55, 65, Water.MODERATE)),
    (12, (60, 70, Water.EXTENSIVE)),
    (13, (65, 75, Water.EXTENSIVE)),
    (14, (70, 80, Water.EXTENSIVE)),
    (15, (75, 85, Water.EXTENSIVE)),
    (16, (80, 90, Water.EXTENSIVE)),
    (17, (85, 95, Water.EXTENSIVE)),
    (18, (90, 97.5, Water.EXTENSIVE)),
    (19, (95, 100, Water.EXTENSIVE)),
    (20, (100, 100, Water.MASSIVE)),
]

# Deternines the status of the lithosphere
# Random selection by 3d6 with h as modifier
# result is Lithosphere enum
lithosphere = [
    (15, (Lithosphere.MOLTEN, 1)),
    (23, (Lithosphere.SOFT, 2)),
    (31, (Lithosphere.EARLY_PLATE, 3)),
    (63, (Lithosphere.MATURE_PLATE, 4)),
    (87, (Lithosphere.ANCIENT_PLATE, 5)),
    (88, (Lithosphere.SOLID, 6)),
]

# Determines the status of the lithosphere for tidally stressed planet
# Random selection by f
# result is Lithosphere enum
lithosphere_stressed = [
    (200, (Lithosphere.SOLID, 6)),
    (630, (Lithosphere.ANCIENT_PLATE, 5)),
    (2000, (Lithosphere.MATURE_PLATE, 4)),
    (6300, (Lithosphere.EARLY_PLATE, 3)),
    (20000, (Lithosphere.SOFT, 2)),
    (20001, (Lithosphere.MOLTEN, 1)),
]
