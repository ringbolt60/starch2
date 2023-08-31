# Starch2

Creates a world using defaults based on own Earth.

Worlds can be of three types: 
### Planet with Satellite
```
$ ./starch2.py "New Earth" orbited
New Earth
Planet with Satellite 
Mass: 1.000 M♁ Density: 1.000 K♁ Radius: 6738 km
Star Mass: 1.000 M☉ Distance: 1.000 AU
Satellite Mass: 0.0123 M♁ Distance: 384400 km
---
Orbital Period = 8766.0 hours
..... and so forth
```
### Lone Planet
```
$ ./starch2.py "New Earth" lone
New Earth
Lone Planet 
Mass: 1.000 M♁ Density: 1.000 K♁ Radius: 6738 km
Star Mass: 1.000 M☉ Distance: 1.000 AU
---
Orbital Period = 8766.0 hours
..... and so forth
```
### Satellite
```
$ ./starch2.py Luna satellite
Luna
Satellite 
Mass: 0.0123 M♁ Density: 0.606 K♁ Radius: 1737 km
Star Mass: 1.000 M☉ Distance: 1.000 AU
Primary Mass: 1.000 M♁ Distance: 384400 km
---
Orbital Period = 655.7 hours
..... and so forth
```
### Options
Star mass `-M` and distance `-D` can be varied

Planet (`-m`) or satellite (`-s`) mass can be varied 

Satellite orbital (`-d`) distance can be supplied

For example (partial outputs shown - extra data will appear after Orbital Period:
```
$ ./starch2.py Arcadia lone -m 0.93 -M 0.94 -D 0.892
Arcadia
Lone Planet
Mass: 0.93 M♁ Density: 0.879 K♁ Radius: 6468 km
Star Mass: 0.94 M☉ Distance: 0.892 AU
---
Orbital Period = 7620.5 hours
..... and so forth
```
```
$ ./starch2.py "New Luna" satellite -s 0.023 -m 0.876 -d 175845
New Luna
Satellite
Mass: 0.023 M♁ Density: 0.519 K♁ Radius: 2246 km
Star Mass: 1.000 M☉ Distance: 1.000 AU
Primary Mass: 0.876 M♁ Distance: 175845 km
---
Orbital Period = 215.4 hours
..... and so forth
```
```
$ ./starch2.py Lorelei orbited -m 1.175 -s 0.023 -d 457897 -M 0.138 -D 0.078
Lorelie
Planet with Satellite
Mass: 1.175 M♁ Density: 0.905 K♁ Radius: 7351 km
Star Mass: 0.138 M☉ Distance: 0.078 AU
Satellite Mass: 0.023 M♁ Distance: 457897 km
---
Orbital Period = 514.3 hours
..... and so forth
```
### Help

Responds to `-h` and `--help` with a usage:

```
$ ./starch2 -h
usage: starch2.py [-h] [-m float] [-M float] [-D float] [-s float] [-d float] [-a float] [-k float] str str

Create world

positional arguments:
  str         Name
  str         Type (choice 'lone' 'orbited' 'satellite')

optional arguments:
  -h, --help            show this help message and exit
  -m float, --mass float
                        Mass of primary in Earth masses (default: 1.0)
  -M float, --mass_star float
                        Mass of star in Sol masses (default: 1.0)
  -D float, --distance_star float
                        Distance of star in AU (default: 1.0)
  -s float, --satellite_mass float
                        Mass of satellite in Earth masses (default: 0.0123)
  -d float, --distance_primary float
                        Distance of satellite in km (default: 384400)
  -a float, --age float
                        Age of system in billions of years (default: 4.568)
  -k density float, --density float
                        Density of world in Earth densities (default: 1.0)
  -e eccentricity float, --ecc float
                        Eccentricity of orbit (default: 0.0)
```
### Tests
Run the test suite to ensure your program is correct:

```
$ make test
pytest -xv test.py
============================= test session starts ==============================
collecting ... collected 11 items

test.py::test_exists PASSED                                              [  9%]
test.py::test_usage PASSED                                               [ 18%]
test.py::test_negative_numeric_inputs PASSED                             [ 27%]
test.py::test_zero_numeric_inputs PASSED                                 [ 36%]
test.py::test_bad_numeric_inputs PASSED                                  [ 45%]
test.py::test_orbited_default_case PASSED                                [ 54%]
test.py::test_lone_default_case PASSED                                   [ 63%]
test.py::test_satellite_default_case PASSED                              [ 72%]
test.py::test_arcadia_case PASSED                                        [ 81%]
test.py::test_new_luna_case PASSED                                       [ 90%]
test.py::test_lorelei_case PASSED                                        [100%]

============================== 11 passed in 2.79s ==============================
```
