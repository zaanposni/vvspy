<h1 align="center">VVS API Wrapper</h1>
<p align="center">
<img src="https://img.shields.io/badge/api-vvs-orange" />
<img src="https://img.shields.io/pypi/pyversions/vvspy" />
<img src="https://img.shields.io/pypi/v/vvspy" />
<img src="https://github.com/FI18-Trainees/vvspy/workflows/BasicCheckup/badge.svg" alt="Checkup status"/>
<a href="https://github.com/zaanposni/vvs/blob/dev/LICENSE"><img src="https://img.shields.io/github/license/zaanposni/vvs.svg"/></a>
</p>
<h2 align="center">Note: This is still work in progress</h2><br />

**Fully object-oriented library** to integrate the **VVS API** into your project.


## Installation

```
pip install vvspy
```

## Requirements

Python 3.6 or higher

## Examples
- Detect delay in upcoming departures:
```python
from vvspy import get_departures

deps = get_departures("5006115", limit=3)  # Stuttgart main station
for dep in deps:
    if dep.delay > 0:
        print("Alarm! Delay detected.")
        print(dep)  # Station @ Timestamp: Train: Origin - Destination
```
- Get complete trip info between two stations:
```python
from vvspy import get_trip

# TODO
```
- Filter for specific lines:
```python
from vvspy import get_departures

deps = get_departures("5006118")  # Stuttgart main station (lower)
for dep in deps:
    if dep.serving_line.symbol == "S4":
        print(f"Departure of S4 at {dep.real_datetime}")
```
## Features

- [x] fully object oriented results
- [ ] full customizable requests and parameters  # coming soon
- [x] parsing all available info into result obj
- [x] Well tested and maintained
- [x] Departures, Arrivals, Trips, Station info, Upcoming events, Maintenance work

See issues/projects on GitHub for upcoming features

## Contributors <img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat"/>

<a href="https://github.com/zaanposni"><img src="https://avatars3.githubusercontent.com/u/24491035?s=460&v=4"
                                            height=90px, width=90px style="border-radius: 50%" /></a>
<a href="https://github.com/Monkmitrad"><img src="https://avatars1.githubusercontent.com/u/48033823?s=460&v=4"
                                            height=90px, width=90px style="border-radius: 50%" /></a>
<a href="https://github.com/Monkmitrad"><img src="https://avatars1.githubusercontent.com/u/33026966?s=460&v=4"
                                            height=90px, width=90px style="border-radius: 50%" /></a>

## License:

This project is licensed under MIT.
