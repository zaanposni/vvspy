from datetime import datetime

from .departure import Departure
from .arrival import Arrival
from .connection import Connection


class Trip:
    r"""

        Result object from a trip request from one station to another including interchanges

        Attributes
        -----------

        raw :class:`dict`
            Raw dict received by the API.
        connections List[:class:`Connection`]
            List of connections the trip consists of.
        duration :class:`int`
            seconds the trip takes overall.
        zones Optional[List[:class:`str`]]
            List of zones this trip goes through.
        fare Optional[:class:`dict`]
            misc info about this trip, ticket prices, etc.
    """

    def __init__(self, **kwargs):
        self.connections = []
        for connection in kwargs.get("legs", []):
            self.connections.append(Connection(**connection))

        self.duration = sum([x.duration for x in self.connections if x.duration])

        try:
            self.zones = kwargs.get("fare", {}).get("zones", [])[0].get("zones", [])
        except IndexError:
            self.zones = []
        # inserted raw
        self.raw = kwargs
        self.fare = kwargs.get("fare")

    def __str__(self):
        return f"Connection ({int(self.duration / 60)} minutes):\n" \
               + '\n'.join([str(x) for x in self.connections])
