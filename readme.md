# 🚂 VVS API Wrapper

[![PackageVersion][package_version_img]][package_version_img]
[![PythonVersions][python_versions_img]][python_versions_img]
[![License][repo_license_img]][repo_license_url]

**Fully object-oriented library** to integrate the **VVS API** into your project.

## Installation

Python 3.6 or higher required

```bash
pip install vvspy
```

## Examples

- Detect delay in upcoming departures:

```python
from vvspy import get_departures
from vvspy.enums.stations import Station

deps = get_departures(Station.HAUPTBAHNHOF__TIEF, limit=3)
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
from vvspy.enums.stations import Station

trip = get_trip(Station.HAUPTBAHNHOF__TIEF, Station.HARDTLINDE)

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
from vvspy.enums.stations import Station

deps = get_departures(Station.HAUPTBAHNHOF__TIEF)
for dep in deps:
    if dep.serving_line.symbol == "S4":
        print(f"Departure of S4 at {dep.real_datetime}")
```

### Get your station id

See: [#64][station_id_issue_url]

### Logging

vvspy uses the python logging module. If you want to change the log level of vvsp, use the following:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vvspy")
logger.setLevel(logging.DEBUG)
```

## ⭐️ Project assistance

If you want to say **thank you** or/and support active development of `vvspy`:

- Add a [GitHub Star][repo_url] to the project.
- Support me on [Ko-fi][kofi_url].

## 🏆 A win-win cooperation

And now, I invite you to participate in this project! Let's work **together** to
create the **most useful** tool for all PietSmiet Enjoyers.

- [Issues][repo_issues_url]: ask questions and submit your features.
- [Pull requests][repo_pull_request_url]: send your improvements to the current.
- [Mail][mail_url]: send your ideas for the project.
- [Discord][discord_url]: add me as a friend on Discord: @zaanposni

Together, we can make this project **better** every day!

## 👀 Projects using vvspy

- [vvs_direct_connect][vvs_direct_connect_url] is a dockerized REST service providing departure data by aschuma.

## 🔥 Other projects of the authors

- [discord-masz][discord_masz_url] - MASZ is a selfhostable highly sophisticated moderation bot for Discord. Includes a web dashboard and a discord bot.

## ⚠️ License

[vvspy][repo_url] is free and open-source software licensed under
the [MIT][repo_license_url].

<!-- Repository -->

[repo_url]: https://github.com/zaanposni/vvspy
[repo_issues_url]: https://github.com/zaanposni/vvspy/issues
[repo_pull_request_url]: https://github.com/zaanposni/vvspy/pulls
[repo_license_url]: https://github.com/zaanposni/vvspy/blob/master/LICENSE
[repo_license_img]: https://img.shields.io/badge/license-MIT-red?style=for-the-badge&logo=none

[python_versions_img]: https://img.shields.io/pypi/pyversions/vvspy?style=for-the-badge
[package_version_img]: https://img.shields.io/pypi/v/vvspy?style=for-the-badge

[station_id_issue_url]: https://github.com/zaanposni/vvspy/issues/64

<!-- Author -->

[kofi_url]: https://ko-fi.com/zaanposni
[discord_masz_url]: https://github.com/zaanposni/discord-masz
[mail_url]: mailto:vvspy@zaanposni.com
[discord_url]: https://discord.com

<!-- Projects -->

[vvs_direct_connect_url]: https://github.com/aschuma/vvs_direct_connect
