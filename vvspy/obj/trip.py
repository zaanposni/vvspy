from datetime import datetime

from .departure import Departure
from .arrival import Arrival
from .connection import Connection


class Trip:
    def __init__(self, **kwargs):
        self.connections = []
        for connection in kwargs.get("legs", []):
            self.connections.append(Connection(**connection))

        self.duration = sum([x.duration for x in self.connections])
        self.zones = kwargs.get("fare", {}).get("zones", [])[0].get("zones", [])

        # inserted raw
        self.raw = kwargs
        self.fare = kwargs.get("fare")

    def __str__(self):
        return f"Connection ({int(self.duration / 60)} minutes):\n" \
               + '\n'.join([str(x) for x in self.connections])
