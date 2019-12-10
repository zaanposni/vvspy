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
        print(f"{res.connections[0].transportation.number} is too late!"
              f" Now arriving {res.connections[0].destination.arrival_time_estimated}")
