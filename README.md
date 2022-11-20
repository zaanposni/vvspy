<h1 align="center">
  VVSPY - Python API Wrapper 🚆
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
  <a href="https://github.com/zaanposni/vvspy/actions/workflows/pytest.yaml">
    <img src="https://github.com/zaanposni/vvspy/actions/workflows/pytest.yaml/badge.svg?branch=master" alt="Status: Pytest"/>
  </a>
  <img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat"/>
  <a href="https://github.com/zaanposni/vvspy/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/zaanposni/vvs.svg"/>
  </a>
</div>
<br>

## Motivation

I always wanted to get some insights into public transport, and as I am very programming affine, I started investigating the VVS API. However, I noticed quickly that the EFA system is not programmer-friendly, at least if you are still getting into it. I saw some projects from CodeOfGermany and various others, but as they are way out of date, I figured I wanted to publish my solution. For example, I use this library to track my daily connections and send push notifications on my mobile device if one is delayed. But you can do various other things, for example, a simple dashboard displaying upcoming departures at a nearby station.

## Installation

> :arrow_up: Python 3.7 or higher required.

This repository is available over [PyPI](https://pypi.org/project/vvspy/). Therefore you can simply install the module with the following command:

```bash linenums="0"
pip install vvspy
```

### Features

- :sparkles: Departures, arrivals, trips, station info, upcoming events, maintenance work
- :white_check_mark: Parsing all available info into result obj
- :wrench: Full customizable requests and parameters
- :test_tube: Well tested

> See [issues](https://github.com/zaanposni/vvspy/issues) on GitHub for upcoming features and requests.

### Usage

> :warning: To use the library you need to obtain station id's for the VVS endpoints. Regarding this, please see the issue: [#12](https://github.com/zaanposni/vvspy/issues/12#issuecomment-568175314).

<br>

The first function provided by _vvspy_ is `get_trip()` and `get_trips()`. This function **gets complete trip information's between two stations**. This functions returns not only the start and end station, but also the intermediate stations and the departure and arrival times.

```python
from vvspy import get_trip  # alternative: get_trips

trip = get_trip("5000355", "5005600")  # Stuttgart main station

print(f"Duration: {trip.duration / 60} minutes")
for connection in trip.connections:
    print(f"From: {connection.origin.name} - To: {connection.destination.name}")
```

```text linenums="0"
# Output:
Duration: 58 minutes
From: Wallgraben - To: Hauptbf (A.-Klett-Pl.)
From: Hauptbf (Arnulf-Klett-Platz) - To: Stuttgart Hauptbahnhof (tief)
From: Stuttgart Hauptbahnhof (tief) - To: Marbach (N)
From: Marbach (N) Bf - To: Murr Hardtlinde
```

During the following code we first get depatures from a specific station. Next we iterate over the results and check if the train is of type `S4`. If so, we print the departure time. In the second example we only check if the train is delayed. If thats the case, we print the delay time.

```python
from vvspy import get_departures # alternative: get_departure

departures = get_departures("5006118", limit=3)  # Stuttgart main station (lower)

# Example 1: Filter by train number
for departure in departures:
    if departure.serving_line.symbol == "S4":
        print(f"Departure of S4 at {departure.real_datetime}")

# Example 2: Check for delay
for departure in departures:
    if departure.delay > 0:
        print("Alarm! Delay detected.")
        print(departure)  # [Delayed] [11:47] [RB17]: Stuttgart Hauptbahnhof (oben) - Pforzheim Hauptbahnhof
    else:
        print("Train on time")
        print(departure)  # [11:47] [RB17]: Stuttgart Hauptbahnhof (oben) - Pforzheim Hauptbahnhof
```

<br>

> This was only a small selection of examples. For more please check out our [examples](https://vvspy.readthedocs.io/en/latest/examples/) tab.

## Projects using _vvspy_

- <a href="https://github.com/aschuma/vvs_direct_connect">vvs_direct_connect</a> is a dockerized REST service providing departure data by [@aschuma](https://github.com/aschuma).

## Contributors

<!-- TODO: Add description on how to contribute -->

Thanks to all who have already contributed to this project!

<!-- TODO: Update the CI badges -->

<div>
  <a href="https://github.com/zaanposni">
    <img src="https://avatars3.githubusercontent.com/u/24491035?s=460&v=4" height=75px, width=75px style="border-radius: 50%" />
  </a>
  <a href="https://github.com/ArPiiX">
    <img src="https://avatars1.githubusercontent.com/u/48033823?s=460&v=4" height=75px, width=75px style="border-radius: 50%" />
  </a>
  <a href="https://github.com/Monkmitrad">
    <img src="https://avatars1.githubusercontent.com/u/33026966?s=460&v=4" height=75px, width=75px style="border-radius: 50%" />
  </a>
  <a href="https://github.com/chrrel">
    <img src="https://avatars.githubusercontent.com/u/7842385?v=4" height=75px, width=75px style="border-radius: 50%" />
  </a>
  <a href="https://github.com/mhorst00">
    <img src="https://avatars.githubusercontent.com/u/36167515?v=4" height=75px, width=75px style="border-radius: 50%" />
  </a>
</div>

## License

This project is licensed under [MIT](https://github.com/zaanposni/vvspy).
