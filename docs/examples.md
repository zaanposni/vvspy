# Examples

<!-- TODO: add introduction -->

## Departures

```python
from vvspy import get_departures

"""
Get specific data about incoming departure
and e.g. display them on a monitor
"""

station = 5001303  # Weil der Stadt

result = get_departures(station, limit=10)

for res in result:
    symbol = res.serving_line.number
    aiming_for_station = res.serving_line.direction
    real_time_data = res.serving_line.real_time
    departure_at = res.real_datetime.strftime()
    platform = res.platform_name
    # do_something()
```

## Trips

```python
from vvspy import get_trips

"""
Check connections between two stations and alarm on delay.

Note that there are destination.delay and origin.delay.
origin.delay => departure delay on first station
destination.delay => arrival delay on the final station
"""

station_1 = 5006118  # Stuttgart main station
station_2 = 5001303  # Weil der Stadt

result = get_trips(station_1, station_2)

for res in result:
    if res.connections[0].destination.delay > 0:
        print(
            f"{res.connections[0].transportation.number} is too late!"
            f" Now arriving {res.connections[0].destination.arrival_time_estimated}"
        )
```
