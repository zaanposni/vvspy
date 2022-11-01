from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple


class Destination:
    """Describes the destination of a `Connection`.

    * TODO: Check which fields are required

    Attributes
    -----------
    raw : Dict[str, Any]
        Raw dict received by the API.
    is_global_id : Optional[bool]
        _None_
    id : Optional[str]
        Station id of the destination station
    name : Optional[str]
        Name of the destination station
    disassembled_name : Optional[str]
        Detailed name of the destination station.
    type : Optional[str]
        Type of the destination station. (e.g. bus, track)
    point_type Optional[str]
        _None_
    coord : Tuple[int]
        Coords of the station. _By default `()`._
    niveau : Optional[int]
        _None_
    parent : Optional[Dict[str, Any]]
        _None_
    arrival_time_planned : Optional[datetime]
        Time planned of arrival.
    arrival_time_estimated : Optional[datetime]
        Time estimated with realtime info (same as `arrival_time_planned` if no realtime data is available).
    delay : Optional[int]
        Minutes of delay.
    properties : Optional[Dict[str, Any]]
        Misc info about the destination.
    """

    def __init__(self, **kwargs) -> None:
        self.raw: Dict[str, Any] = kwargs
        self.is_global_id: Optional[bool] = kwargs.get("isGlobalId")
        self.id: Optional[str] = kwargs.get("id")
        self.name: Optional[str] = kwargs.get("name")
        self.disassembled_name: Optional[str] = kwargs.get("disassembledName")
        self.type: Optional[str] = kwargs.get("type")
        self.point_type: Optional[str] = kwargs.get("pointType")
        self.coord: Tuple[int] = kwargs.get("coord", ())
        self.niveau: Optional[int] = kwargs.get("niveau")
        self.parent: Optional[Dict[str, Any]] = kwargs.get("parent")
        arrival_time_planned: Optional[str] = kwargs.get("arrivalTimePlanned")
        arrival_time_estimated: Optional[str] = kwargs.get("arrivalTimeEstimated")
        self.arrival_time_planned: Optional[datetime] = (
            datetime.strptime(arrival_time_planned[:-1], "%Y-%m-%dT%H:%M:%S") if arrival_time_planned else None
        )
        self.arrival_time_estimated: Optional[datetime] = (
            datetime.strptime(arrival_time_estimated[:-1], "%Y-%m-%dT%H:%M:%S") if arrival_time_estimated else None
        )
        if self.arrival_time_planned and self.arrival_time_estimated:
            delta: timedelta = self.arrival_time_estimated - self.arrival_time_planned
            self.delay: Optional[int] = int(delta.total_seconds() / 60)
        else:
            self.delay = None
        self.properties: Optional[Dict[str, Any]] = kwargs.get("properties")
