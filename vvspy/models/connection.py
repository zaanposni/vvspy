from datetime import datetime
from typing import Any, Dict, List, Optional

from vvspy.models.destination import Destination
from vvspy.models.origin import Origin
from vvspy.models.transportation import Transportation


class Connection:
    """Function to initialize a Connection object

    * TODO: Check typing for Origin, Destination, and Transportation
    * TODO: Check which fields are required

    Attributes
    -----------
    raw : Dict[str, Any]
        Raw dict received by the API.
    origin : Origin
        Origin, where this connection starts. _By default `Origin({})`._
    destination : Destination
        Where this connection is heading to. _By default `Destination({})`._
    transportation : Transportation
        Transportation info of this connection (e.g. line number, type, etc.). _By default `Transportation({})`._
    duration : int
        Seconds this connection takes. _By default `-1`._
    is_realtime_controlled : bool
        Whether or not this connection has realtime tracking. _By default `False`._
    stop_sequence : List[Dict[str, Any]]
        Stop sequence of this connection. _By default `[]`._
    foot_path_info : Optional[List[Any]]
        Info if you really want to walk.
    coords : Optional[List[List[int]]]
        Coords of this connection.
    properties : Optional[Dict[str, Any]]
        Misc info about this connection.
    infos : Optional[List[Any]]
        _None_
    path_description : Optional[List[Any]]
        _None_
    interchange : Optional[List[Any]]
        _None_
    """

    def __init__(self, **kwargs):
        self.raw: Dict[str, Any] = kwargs
        self.origin: Origin = Origin(**kwargs.get("origin", {}))
        self.destination: Destination = Destination(**kwargs.get("destination", {}))
        self.transportation: Transportation = Transportation(**kwargs.get("transportation", {}))
        self.duration: int = kwargs.get("duration", -1)
        self.is_realtime_controlled: bool = kwargs.get("isRealtimeControlled", False)
        self.stop_sequence: List[Dict[str, Any]] = kwargs.get("stopSequence", [])
        self.foot_path_info: Optional[List[Any]] = kwargs.get("footPathInfo")
        self.coords: Optional[List[List[int]]] = kwargs.get("coords")
        self.properties: Optional[Dict[str, Any]] = kwargs.get("properties")
        self.infos: Optional[List[Any]] = kwargs.get("infos")
        self.path_description: Optional[List[Any]] = kwargs.get("pathDescription")
        self.interchange: Optional[List[Any]] = kwargs.get("interchange")

    def __str__(self) -> str:
        """Prints a string representation of this object

        Returns
        -------
        str
            A string representation of this object
        """
        dep_pre = "[Delayed] " if self.origin.delay else ""
        arr_pre = "[Delayed] " if self.destination.delay else ""

        if (
            self.origin.departure_time_estimated
            and self.destination.arrival_time_estimated
            and self.origin.departure_time_estimated.date() == datetime.now().date()
        ):
            return f"[{self.transportation.disassembled_name}]: {dep_pre}[{self.origin.departure_time_estimated.strftime('%H:%M')}] @ {self.origin.name} - {arr_pre}[{self.destination.arrival_time_estimated.strftime('%H:%M')}] @ {self.destination.name}"

        return f"[{self.transportation.disassembled_name}]: {dep_pre}[{self.origin.departure_time_estimated}] @ {self.origin.name} - {arr_pre}[{self.destination.arrival_time_estimated}] @ {self.destination.name}"
