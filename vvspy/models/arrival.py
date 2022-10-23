from datetime import datetime
from typing import Any, Dict, Optional

from loguru import logger

from vvspy.models.line_operator import LineOperator
from vvspy.models.serving_line import ServingLine


class Arrival:
    """Arrival object from a arrival request of one station.

    * TODO: Check `datetime` and `real_datetime`
    * TODO: Check typing for `ServingLine` and `LineOperator`

    Attributes
    -----------
    raw : Dict[str, Any]
        Raw dict received by the API.
    stop_id : str
        Station_id of the arrival. _By default `""`._
    platform : str
        Platform / track of the arrival. _By default `""`._
    platform_name : str
        Name of the platform. _By default `""`._
    stop_name : str
        Name of the station. _By default `""`._
    name_wo : str
        Name of the station. _By default `""`._
    area : str
        The area of the station (unsure atm). _By default `""`._
    x : str
        Coordinates of the station. _By default `""`._
    y : str
        Coordinates of the station. _By default `""`._
    map_name : str
        Map name the API works on. _By default `""`._
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
        Planned arrival datetime. _By default `None`._
    real_datetime : Optional[datetime]
        Estimated arrival datetime (equal to `self.datetime` if no realtime data is available). _By default `None`._
    delay : int
        Delay of arrival in minutes. _By default `-1`._
    """

    def __init__(self, **kwargs):
        self.raw: Dict[str, Any] = kwargs
        self.stop_id: str = kwargs.get("stopID", "")
        self.platform: str = kwargs.get("platform", "")
        self.platform_name: str = kwargs.get("platformName", "")
        self.stop_name: str = kwargs.get("stopName", "")
        self.name_wo: str = kwargs.get("nameWO", "")
        self.area: str = kwargs.get("area", "")
        self.x: str = kwargs.get("x", "")
        self.y: str = kwargs.get("y", "")
        self.map_name: str = kwargs.get("mapName", "")
        self.serving_line: ServingLine = ServingLine(**kwargs.get("servingLine", {}))
        self.operator = LineOperator(**kwargs.get("operator", {}))
        self.stop_infos: Optional[Dict[str, Any]] = kwargs.get("stopInfos")
        self.line_infos: Optional[Dict[str, Any]] = kwargs.get("lineInfos")
        self.point_type: Optional[str] = kwargs.get("pointType")

        self.countdown: int = int(kwargs.get("countdown", -1))
        # TODO: Correct default value and type
        self.datetime: Optional[datetime] = None
        self.real_datetime = self.datetime
        dt = kwargs.get("dateTime", None)
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
                logger.debug("Could not parse datetime")
                self.datetime = None
        r_dt = kwargs.get("realDateTime", None)
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
                logger.debug("Could not parse real datetime")
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

        logger.debug("No real datetime available")
        return f"{pre}[N/A] {self.serving_line}"
