from .departure import Departure
from .arrival import Arrival


class Trip:
    def __init__(self, arrival: Arrival, departure: Departure):
        self.arrival = arrival
        self.departure = departure
        # self.specialstuff for this trip
        # TODO: multiple arrival departure (list?) for connections with multiple stops
