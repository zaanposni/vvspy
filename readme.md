<h1 align="center">VVS API Wrapper</h1>
<p align="center">
<img src="https://img.shields.io/pypi/pyversions/vvspy" />
<img src="https://img.shields.io/pypi/v/vvspy" />
<a href="https://vvspy.readthedocs.io/en/latest/" target="_blank"><img src="https://img.shields.io/readthedocs/vvspy" /></a>
<img src="https://github.com/FI18-Trainees/vvspy/workflows/BasicCheckup/badge.svg" alt="Checkup status"/>
<img src="https://github.com/FI18-Trainees/vvspy/workflows/Unittests/badge.svg" alt="Checkup status"/>
<a href="https://github.com/zaanposni/vvs/blob/dev/LICENSE"><img src="https://img.shields.io/github/license/zaanposni/vvs.svg"/></a>
</p>

**Fully object-oriented library** to integrate the **VVS API** into your project.

- <a href="https://vvspy.readthedocs.io/en/latest/" target="_blank">readthedocs</a>

## Installation

**Python 3.6 or higher required**
```
pip install vvspy
```

## Examples
- Detect delay in upcoming departures:
```python
from vvspy import get_departures

deps = get_departures("5006115", limit=3)  # Stuttgart main station
for dep in deps:
    if dep.delay > 0:
        print("Alarm! Delay detected.")
        print(dep)  # [Delayed] [11:47] [RB17]: Stuttgart Hauptbahnhof (oben) - Pforzheim Hauptbahnhof

    else:
        print("Train on time")
        print(dep)  # [11:47] [RB17]: Stuttgart Hauptbahnhof (oben) - Pforzheim Hauptbahnhof
```
- Get complete trip info between two stations (including interchanges):
```python
from vvspy import get_trip  # also usable: get_trips

trip = get_trip("5000355", "5005600")  # Stuttgart main station

print(f"Duration: {trip.duration / 60} minutes")
for connection in trip.connections:
    print(f"From: {connection.origin.name} - To: {connection.destination.name}")
```
```text
# Output:
Duration: 58 minutes
From: Wallgraben - To: Hauptbf (A.-Klett-Pl.)
From: Hauptbf (Arnulf-Klett-Platz) - To: Stuttgart Hauptbahnhof (tief)
From: Stuttgart Hauptbahnhof (tief) - To: Marbach (N)
From: Marbach (N) Bf - To: Murr Hardtlinde
```
- Filter for specific lines:
```python
from vvspy import get_departures

deps = get_departures("5006118")  # Stuttgart main station (lower)
for dep in deps:
    if dep.serving_line.symbol == "S4":
        print(f"Departure of S4 at {dep.real_datetime}")
```

## Get your station id

See: <a href="https://github.com/FI18-Trainees/vvspy/issues/12#issuecomment-568175314">https://github.com/FI18-Trainees/vvspy/issues/12#issuecomment-568175314</a>


## Features

- [x] full customizable requests and parameters
- [x] parsing all available info into result obj
- [x] Well tested and maintained
- [x] Departures, Arrivals, Trips, Station info, Upcoming events, Maintenance work

- See issues/projects on GitHub for upcoming features

## Contributors <img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat"/>

<a href="https://github.com/zaanposni"><img src="https://avatars3.githubusercontent.com/u/24491035?s=460&v=4"
                                            height=90px, width=90px style="border-radius: 50%" /></a>
<a href="https://github.com/ArPiiX"><img src="https://avatars1.githubusercontent.com/u/48033823?s=460&v=4"
                                         height=90px, width=90px style="border-radius: 50%" /></a>
<a href="https://github.com/Monkmitrad"><img src="https://avatars1.githubusercontent.com/u/33026966?s=460&v=4"
                                             height=90px, width=90px style="border-radius: 50%" /></a>
<a href="https://github.com/chrrel"><img src="https://avatars.githubusercontent.com/u/7842385?v=4"
                                             height=90px, width=90px style="border-radius: 50%" /></a>

## Projects using vvspy

- <a href="https://github.com/aschuma/vvs_direct_connect">vvs_direct_connect</a> is a dockerized REST service providing departure data by @[aschuma](https://github.com/aschuma).

## License:

This project is licensed under MIT.
