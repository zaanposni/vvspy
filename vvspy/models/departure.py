from datetime import datetime

from .serving_line import ServingLine
from .line_operator import LineOperator


class Departure:
    r"""

     Departure object from a departure request of one station.

    Attributes
    -----------

    raw :class:`dict`
        Raw dict received by the API.
    stop_id :class:`str`
        Station_id of the departure.
    x :class:`str`
        Coordinates of the station.
    y :class:`str`
        Coordinates of the station.
    map_name :class:`str`
        Map name the API works on.
    area :class:`str`
        The area of the station (unsure atm)
    platform :class:`str`
        Platform / track of the departure.
    platform_name :class:`str`
        name of the platform.
    stop_name :class:`str`
        name of the station.
    name_wo :class:`str`
        name of the station.
    countdown :class:`int`
        minutes until departure.
    datetime :class:`datetime.datetime`
        Planned departure datetime.
    real_datetime :class:`datetime.datetime`
        Estimated departure datetime (equal to ``self.datetime`` if no realtime data is available).
    delay :class:`int`
        Delay of departure in minutes.
    serving_line :class:`ServingLine`
        line of the incoming departure.
    operator :class:`LineOperator`
        Operator of the incoming departure.
    stop_infos: Optional[:class:`dict`]
        All related info to the station (e.g. maintenance work).
    line_infos Optional[:class:`dict`]
        All related info to the station (e.g. maintenance work).
    """

    def __init__(self, **kwargs):
        self.stop_id = kwargs.get("stopID")
        self.x = kwargs.get("x")
        self.y = kwargs.get("y")
        self.map_name = kwargs.get("mapName")
        self.area = kwargs.get("area")
        self.platform = kwargs.get("platform")
        self.platform_name = kwargs.get("platformName")
        self.stop_name = kwargs.get("stopName")
        self.name_wo = kwargs.get("nameWO")
        self.point_type = kwargs.get("pointType")
        self.countdown = int(kwargs.get("countdown", "0"))
        dt = kwargs.get("dateTime")
        if dt:
            try:
                self.datetime = datetime(
                    year=int(dt.get("year", datetime.now().year)),
                    month=int(dt.get("month", datetime.now().month)),
                    day=int(dt.get("day", datetime.now().day)),
                    hour=int(dt.get("hour", datetime.now().hour)),
                    minute=int(dt.get("minute", datetime.now().minute))
                )
            except ValueError:
                pass
        else:
            self.datetime = None
        r_dt = kwargs.get("realDateTime")
        if r_dt:
            try:
                self.real_datetime = datetime(
                    year=int(r_dt.get("year", datetime.now().year)),
                    month=int(r_dt.get("month", datetime.now().month)),
                    day=int(r_dt.get("day", datetime.now().day)),
                    hour=int(r_dt.get("hour", datetime.now().hour)),
                    minute=int(r_dt.get("minute", datetime.now().minute))
                )
            except ValueError:
                pass
        else:
            self.real_datetime = self.datetime

        self.delay = int((self.real_datetime - self.datetime).total_seconds() / 60)
        self.serving_line = ServingLine(**kwargs.get("servingLine", {}))
        self.operator = LineOperator(**kwargs.get("operator", {}))

        # inserted raw
        self.raw = kwargs
        self.stop_infos = kwargs.get("stopInfos")
        self.line_infos = kwargs.get("lineInfos")

    def __str__(self):
        pre = "[Delayed] " if self.delay else ""
        if self.real_datetime.date() == datetime.now().date():
            return f"{pre}[{str(self.real_datetime.strftime('%H:%M'))}] {self.serving_line}"
        return f"{pre}[{str(self.real_datetime)}] {self.serving_line}"
