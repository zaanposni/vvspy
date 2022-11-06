import logging
from typing import Any, Dict, List, Optional

from vvspy.models.connection import Connection


class Trip:
    """Result object from a trip request from one station to another including interchanges.

    * TODO: Check which fields are required

    Attributes
    -----------
    raw : Dict[str, Any]
        Raw dict received by the API.
    connections : List[Connection]
        List of connections the trip consists of.
    duration : int
        Seconds the trip takes overall.
    zones : Optional[List[str]]
        List of zones this trip goes through.
    fare : Optional[Dict[str, Any]]
        Misc info about this trip, ticket prices, etc.
    """

    def __init__(self, **kwargs) -> None:
        self.raw: Dict[str, Any] = kwargs
        self.connections: List[Connection] = [Connection(**connection) for connection in kwargs.get("legs", [])]
        self.duration: int = sum(x.duration for x in self.connections if x.duration)
        try:
            self.zones: Optional[List[str]] = kwargs.get("fare", {}).get("zones", [])[0].get("zones", [])
        except (IndexError, KeyError):
            logging.warning("No zones provided.")
            self.zones = []
        self.fare: Optional[Dict[str, Any]] = kwargs.get("fare")

    def __str__(self) -> str:
        return f"Connection ({int(self.duration / 60)} minutes):\n" + "\n".join([str(x) for x in self.connections])
