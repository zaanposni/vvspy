from vvspy import get_trips
from vvspy.enums.stations import Station

"""
Check connections between two stations and alarm on delay.

Note that there are destination.delay and origin.delay.
origin.delay => departure delay on first station
destination.delay => arrival delay on the final station
"""

result = get_trips(Station.HAUPTBAHNHOF__TIEF, Station.WEIL_DER_STADT)

for res in result:
    if res.connections[0].destination.delay > 0:
        print(f"{res.connections[0].transportation.number} is too late!"
              f" Now arriving {res.connections[0].destination.arrival_time_estimated}")
