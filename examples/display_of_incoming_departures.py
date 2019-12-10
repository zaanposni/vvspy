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
