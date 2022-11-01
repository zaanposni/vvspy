from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple


class Origin:
    """Describes the origin of a `Connection`.

    * TODO: Check which fields are required

    Attributes
    -----------
    raw : Dict[str, Any]
        Raw dict received by the API.
    is_global_id : Optional[bool]
        _None_
    id : Optional[str]
        Station id of the origin station
    name : Optional[str]
        Name of the origin station
    disassembled_name : Optional[str]
        Detailed name of the origin station.
    type : Optional[str]
        Type of the origin station. (e.g. bus, track)
    point_type Optional[str]
        _None_
    coord : Tuple[int]
        Coords of the station. _By default `()`._
    niveau : Optional[int]
        _None_
    parent : Optional[Dict[str, Any]]
        _None_
    departure_time_planned : Optional[datetime]
        Time planned of arrival.
    departure_time_estimated : Optional[datetime]
        Time estimated with realtime info (same as `departure_time_planned` if no realtime data is available).
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
        departure_time_planned = kwargs.get("departureTimePlanned")
        departure_time_estimated = kwargs.get("departureTimeEstimated")
        self.departure_time_planned = (
            datetime.strptime(departure_time_planned[:-1], "%Y-%m-%dT%H:%M:%S") if departure_time_planned else None
        )
        self.departure_time_estimated = (
            datetime.strptime(departure_time_estimated[:-1], "%Y-%m-%dT%H:%M:%S") if departure_time_estimated else None
        )
        if self.departure_time_planned and self.departure_time_estimated:
            delta: timedelta = self.departure_time_estimated - self.departure_time_planned
            self.delay: Optional[int] = int(delta.total_seconds() / 60)
        else:
            self.delay = None
        self.properties = kwargs.get("properties")
