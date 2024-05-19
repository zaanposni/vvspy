from vvspy import get_departures
from vvspy.enums.stations import Station

"""
Get specific data about incoming departure
and e.g. display them on a monitor
"""

result = get_departures(Station.WEIL_DER_STADT, limit=10)

for res in result:
    symbol = res.serving_line.number
    aiming_for_station = res.serving_line.direction
    real_time_data = res.serving_line.real_time
    departure_at = str(res.real_datetime)
    platform = res.platform_name
    # do_something()
