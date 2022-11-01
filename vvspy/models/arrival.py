import logging
from datetime import datetime
from typing import Any, Dict, Optional

from vvspy.models.line_operator import LineOperator
from vvspy.models.serving_line import ServingLine


class Arrival:
    """Arrival object from a arrival request of one station.

    * TODO: Check `datetime` and `real_datetime`
    * TODO: Check typing for `ServingLine` and `LineOperator`
    * TODO: Check which fields are required

    Attributes
    -----------
    raw : Dict[str, Any]
        Raw dict received by the API.
    stop_id : Optional[str]
        Station_id of the arrival.
    platform : Optional[str]
        Platform / track of the arrival.
    platform_name : Optional[str]
        Name of the platform.
    stop_name : Optional[str]
        Name of the station.
    name_wo : Optional[str]
        Name of the station.
    area : Optional[str]
        The area of the station (unsure atm).
    x : Optional[str]
        Coordinates of the station.
    y : Optional[str]
        Coordinates of the station.
    map_name : Optional[str]
        Map name the API works on.
    serving_line : ServingLine
        Line of the incoming arrival. _By default `ServingLine({})`._
    operator : LineOperator
        Operator of the incoming arrival. _By default `LineOperator({})`._
    stop_infos : Optional[Dict[str, Any]]
        All related info to the station (e.g. maintenance work).
    line_infos : Optional[Dict[str, Any]]
        All related info to the station (e.g. maintenance work).
    point_type : Optional[str]
        _None_
    countdown : int
        Minutes until arrival. _By default `-1`._
    datetime : Optional[datetime]
        Planned arrival datetime.
    real_datetime : Optional[datetime]
        Estimated arrival datetime (equal to `self.datetime` if no realtime data is available).
    delay : int
        Delay of arrival in minutes. _By default `-1`._
    """

    def __init__(self, **kwargs):
        self.raw: Dict[str, Any] = kwargs
        self.stop_id: Optional[str] = kwargs.get("stopID")
        self.platform: Optional[str] = kwargs.get("platform")
        self.platform_name: Optional[str] = kwargs.get("platformName")
        self.stop_name: Optional[str] = kwargs.get("stopName")
        self.name_wo: Optional[str] = kwargs.get("nameWO")
        self.area: Optional[str] = kwargs.get("area")
        self.x: Optional[str] = kwargs.get("x")
        self.y: Optional[str] = kwargs.get("y")
        self.map_name: Optional[str] = kwargs.get("mapName")
        self.serving_line: ServingLine = ServingLine(**kwargs.get("servingLine", {}))
        self.operator = LineOperator(**kwargs.get("operator", {}))
        self.stop_infos: Optional[Dict[str, Any]] = kwargs.get("stopInfos")
        self.line_infos: Optional[Dict[str, Any]] = kwargs.get("lineInfos")
        self.point_type: Optional[str] = kwargs.get("pointType")

        self.countdown: int = int(kwargs.get("countdown", -1))
        # TODO: Correct default value and type
        self.datetime: Optional[datetime] = None
        self.real_datetime = self.datetime
        dt = kwargs.get("dateTime")
        if dt:
            try:
                self.datetime = datetime(
                    year=int(dt.get("year", datetime.now().year)),
                    month=int(dt.get("month", datetime.now().month)),
                    day=int(dt.get("day", datetime.now().day)),
                    hour=int(dt.get("hour", datetime.now().hour)),
                    minute=int(dt.get("minute", datetime.now().minute)),
                )
            except ValueError:
                logging.debug("Could not parse datetime")
                self.datetime = None
        r_dt = kwargs.get("realDateTime")
        if r_dt:
            try:
                self.real_datetime = datetime(
                    year=int(r_dt.get("year", datetime.now().year)),
                    month=int(r_dt.get("month", datetime.now().month)),
                    day=int(r_dt.get("day", datetime.now().day)),
                    hour=int(r_dt.get("hour", datetime.now().hour)),
                    minute=int(r_dt.get("minute", datetime.now().minute)),
                )
            except ValueError:
                logging.debug("Could not parse real datetime")
                self.real_datetime = self.datetime

        self.delay: int = -1
        if self.datetime and self.real_datetime:
            self.delay = int((self.real_datetime - self.datetime).total_seconds() / 60)

    def __str__(self) -> str:
        """Prints the arrival in a readable format

        Returns
        -------
        str
            Readable format of the arrival
        """
        pre = "[Delayed] " if self.delay > 0 else ""

        if self.real_datetime:
            if self.real_datetime.date() == datetime.now().date():
                return f"{pre}[{str(self.real_datetime.strftime('%H:%M'))}] {self.serving_line}"
            return f"{pre}[{str(self.real_datetime)}] {self.serving_line}"

        logging.debug("No real datetime available")
        return f"{pre}[N/A] {self.serving_line}"
