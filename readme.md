<h1 align="center">VVS API Wrapper</h1>
<p align="center">
<a href="https://github.com/zaanposni/vvs"><img alt="star this repo" src="https://img.shields.io/github/stars/zaanposni/vvs" /></a>
<a href="https://github.com/zaanposni/vvs/fork"><img alt="fork this repo" src="https://img.shields.io/github/forks/zaanposni/vvs" /></a>
<img src="https://img.shields.io/badge/api-vvs-orange" />
<img src="https://img.shields.io/pypi/pyversions/vvspy" />
<img src="https://img.shields.io/pypi/v/vvspy" />
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
        print("Line number: " + dep.serving_line.symbol)
```
- Get complete trip info between two stations:
```python
from vvspy import get_trip

# TODO
```

## Features

- [x] fully object oriented results
- [ ] full customizable requests and parameters  # coming soon
- [x] parsing all available info into result obj
- [x] Well tested and maintained
- [x] Departures, Arrivals, Trips, Station info, Upcoming events, Maintenance work

See issues/projects on GitHub for upcoming features

## Contributors <img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat"/>

- <a href="https://github.com/zaanposni">Zaanposni</a>
- <a href="https://github.com/Monkmitrad">Monkmitrad</a>
<hr />

### License:

This project is licensed under MIT.