<h1 align="center">
  VVSPY - VVS API Wrapper 🚆
</h1>

<h4 align="center">
  Fully object-oriented library to integrate the VVS API into your project.
</h4>

<div align="center">
  <img src="https://img.shields.io/pypi/pyversions/vvspy" />
  <img src="https://img.shields.io/pypi/v/vvspy" />
  <a href="https://vvspy.readthedocs.io/en/latest/" target="_blank">
    <img src="https://img.shields.io/readthedocs/vvspy" />
  </a>
  <img src="https://github.com/zaanposni/vvspy/workflows/BasicCheckup/badge.svg" alt="Checkup status"/>
  <img src="https://github.com/zaanposni/vvspy/workflows/Unittests/badge.svg" alt="Checkup status"/>
  <img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat"/>
  <a href="https://github.com/zaanposni/vvspy/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/zaanposni/vvs.svg"/>
  </a>
</div>
<br>

<!-- TODO: Add description -->

Excepteur fugiat laborum nostrud officia ad fugiat. Do magna dolor ullamco sint ut reprehenderit enim elit cillum. Quis officia cupidatat nostrud non aute consectetur ullamco cupidatat mollit esse eu. Laborum ullamco non voluptate eiusmod qui.

## Installation

> :arrow_up: Python 3.8 or higher required.

This repository is available over [PyPI](https://pypi.org/project/vvspy/). Therefore you can simply install the module with the following command:

```bash
pip install vvspy
```

## Usage

> :warning: To use the library you need to obtain station id's for the VVS endpoints. Regarding this, please see the issue: [#12](https://github.com/zaanposni/vvspy/issues/12#issuecomment-568175314).

<br>

The first function provided by _vvspy_ is `get_trip()` and `get_trips()`. This function **gets complete trip information's between two stations**. This functions returns not only the start and end station, but also the intermediate stations and the departure and arrival times.

```python
from vvspy import get_trip  # also usable: get_trips

trip = get_trip("5000355", "5005600")  # Stuttgart main station

print(f"Duration: {trip.duration / 60} minutes")
for connect in trip.connections:
    print(f"From: {connect.origin.name} - To: {connect.destination.name}")
```

```text
# Output:
Duration: 58 minutes
From: Wallgraben - To: Hauptbf (A.-Klett-Pl.)
From: Hauptbf (Arnulf-Klett-Platz) - To: Stuttgart Hauptbahnhof (tief)
From: Stuttgart Hauptbahnhof (tief) - To: Marbach (N)
From: Marbach (N) Bf - To: Murr Hardtlinde
```

<br>

The following code snippet will **filter the requested departures** for a specific train number.

```python
from vvspy import get_departures

departures = get_departures("5006118")  # Stuttgart main station (lower)
for depart in departures:
    if depart.serving_line.symbol == "S4":
        print(f"Departure of S4 at {depart.real_datetime}")
```

<br>

When requesting departure times the object includes a attribute storing the delay a connection has. As shown in the code below you can access this attribute using `connection.delay`.

```python
from vvspy import get_departures

departures = get_departures("5006115", limit=3)  # Stuttgart main station
for depart in departures:
    if depart.delay > 0:
        print("Alarm! Delay detected.")
        print(depart)  # [Delayed] [11:47] [RB17]: Stuttgart Hauptbahnhof (oben) - Pforzheim Hauptbahnhof
    else:
        print("Train on time")
        print(depart)  # [11:47] [RB17]: Stuttgart Hauptbahnhof (oben) - Pforzheim Hauptbahnhof
```

## Features

- :sparkles: Departures, arrivals, trips, station info, upcoming events, maintenance work
- :white_check_mark: Parsing all available info into result obj
- :wrench: Full customizable requests and parameters
- :test_tube: Well tested

> See [issues](https://github.com/zaanposni/vvspy/issues) on GitHub for upcoming features and requests.

## Contribution

Thanks to all who have already contributed to this project!

<div>
  <a href="https://github.com/zaanposni">
    <img src="https://avatars3.githubusercontent.com/u/24491035?s=460&v=4" height=90px, width=90px style="border-radius: 50%" />
  </a>
  <a href="https://github.com/ArPiiX">
    <img src="https://avatars1.githubusercontent.com/u/48033823?s=460&v=4" height=90px, width=90px style="border-radius: 50%" />
  </a>
  <a href="https://github.com/Monkmitrad">
    <img src="https://avatars1.githubusercontent.com/u/33026966?s=460&v=4" height=90px, width=90px style="border-radius: 50%" />
  </a>
  <a href="https://github.com/chrrel">
    <img src="https://avatars.githubusercontent.com/u/7842385?v=4" height=90px, width=90px style="border-radius: 50%" />
  </a>
  <a href="https://github.com/mhorst00">
    <img src="https://avatars.githubusercontent.com/u/36167515?v=4" height=90px, width=90px style="border-radius: 50%" />
  </a>
</div>

## Projects using _vvspy_

- <a href="https://github.com/aschuma/vvs_direct_connect">vvs_direct_connect</a> is a dockerized REST service providing departure data by @[aschuma](https://github.com/aschuma).

## License

This project is licensed under MIT.
