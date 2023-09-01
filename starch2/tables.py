# --------------------------------------------------
import main


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
    (-5, (0, 0, main.Water.TRACE)),
    (-1, (0, 1, main.Water.MINIMAL)),
    (0, (0, 2, main.Water.MINIMAL)),
    (1, (1, 3, main.Water.MINIMAL)),
    (2, (2, 5, main.Water.MINIMAL)),
    (3, (3, 7.5, main.Water.MINIMAL)),
    (4, (5, 10, main.Water.MODERATE)),
    (5, (7.5, 20, main.Water.MODERATE)),
    (6, (10, 30, main.Water.MODERATE)),
    (7, (20, 40, main.Water.MODERATE)),
    (8, (30, 50, main.Water.MODERATE)),
    (9, (40, 55, main.Water.MODERATE)),
    (10, (50, 60, main.Water.MODERATE)),
    (11, (55, 65, main.Water.MODERATE)),
    (12, (60, 70, main.Water.EXTENSIVE)),
    (13, (65, 75, main.Water.EXTENSIVE)),
    (14, (70, 80, main.Water.EXTENSIVE)),
    (15, (75, 85, main.Water.EXTENSIVE)),
    (16, (80, 90, main.Water.EXTENSIVE)),
    (17, (85, 95, main.Water.EXTENSIVE)),
    (18, (90, 97.5, main.Water.EXTENSIVE)),
    (19, (95, 100, main.Water.EXTENSIVE)),
    (20, (100, 100, main.Water.MASSIVE)),
]

# Deternines the status of the lithosphere
# Random selection by 3d6 with h as modifier
# result is Lithosphere enum
lithosphere = [
    (15, (main.Lithosphere.MOLTEN, 1)),
    (23, (main.Lithosphere.SOFT, 2)),
    (31, (main.Lithosphere.EARLY_PLATE, 3)),
    (63, (main.Lithosphere.MATURE_PLATE, 4)),
    (87, (main.Lithosphere.ANCIENT_PLATE, 5)),
    (88, (main.Lithosphere.SOLID, 6)),
]

# Determines the status of the lithosphere for tidally stressed planet
# Random selection by f
# result is Lithosphere enum
lithosphere_stressed = [
    (200, (main.Lithosphere.SOLID, 6)),
    (630, (main.Lithosphere.ANCIENT_PLATE, 5)),
    (2000, (main.Lithosphere.MATURE_PLATE, 4)),
    (6300, (main.Lithosphere.EARLY_PLATE, 3)),
    (20000, (main.Lithosphere.SOFT, 2)),
    (20001, (main.Lithosphere.MOLTEN, 1)),
]
