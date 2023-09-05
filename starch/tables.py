# --------------------------------------------------


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
    (-5, (0, 0, "trace")),
    (-1, (0, 1, "minimal")),
    (0, (0, 2, "minimal")),
    (1, (1, 3, "minimal")),
    (2, (2, 5, "minimal")),
    (3, (3, 7.5, "minimal")),
    (4, (5, 10, "moderate")),
    (5, (7.5, 20, "moderate")),
    (6, (10, 30, "moderate")),
    (7, (20, 40, "moderate")),
    (8, (30, 50, "moderate")),
    (9, (40, 55, "moderate")),
    (10, (50, 60, "moderate")),
    (11, (55, 65, "moderate")),
    (12, (60, 70, "extensive")),
    (13, (65, 75, "extensive")),
    (14, (70, 80, "extensive")),
    (15, (75, 85, "extensive")),
    (16, (80, 90, "extensive")),
    (17, (85, 95, "extensive")),
    (18, (90, 97.5, "extensive")),
    (19, (95, 100, "extensive")),
    (20, (100, 100, "massive")),
]

# Deternines the status of the lithosphere
# Random selection by 3d6 with h as modifier
# result is Lithosphere enum
lithosphere = [
    (15, ("molten", 1)),
    (23, ("soft", 2)),
    (31, ("early_plate", 3)),
    (63, ("mature_plate", 4)),
    (87, ("ancient_plate", 5)),
    (88, ("solid", 6)),
]

# Determines the status of the lithosphere for tidally stressed planet
# Random selection by f
# result is Lithosphere enum
lithosphere_stressed = [
    (200, ("solid", 6)),
    (630, ("ancient_plate", 5)),
    (2000, ("mature_plate", 4)),
    (6300, ("early_plate", 3)),
    (20000, ("soft", 2)),
    (20001, ("molten", 1)),
]


# Determine greenhouse effect and mass of water vapour in atmosphere
# Look up from t2
# result is greenhouse effect for moderate water amounts
water_vapour = [
    (259, 0),
    (260, 16),
    (262, 17),
    (265, 18),
    (268, 19),
    (270, 20),
    (273, 21),
    (276, 22),
    (279, 23),
    (282, 24),
    (286, 25),
    (289, 26),
    (293, 27),
    (296, 28),
    (300, 29),
    (304, 30),
    (309, 31),
    (313, 32),
    (318, 33),
    (323, 34),
    (328, 35),
    (333, 36),
    (100000, 37),
]
