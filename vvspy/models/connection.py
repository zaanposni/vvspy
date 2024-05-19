from datetime import datetime

from .origin import Origin
from .destination import Destination
from .transportation import Transportation


class Connection:
    r"""

        Several connections describe one :class:`Trip`.


        Attributes
        -----------

        raw :class:`dict`
            Raw dict received by the API.
        duration :class:`int`
            seconds this connection takes
        is_realtime_controlled :class:`bool`
            whether or not this connection has realtime tracking
        origin :class:`Origin`
            Origin, where this connection starts
        destination :class:`Destination`
            Where this connection is heading to
        transportation :class:`Transportation`
            Transportation info of this connection
        stop_sequence Optional[List[:class:`dict`]]
            stop sequence of this connection
        foot_path_info Optional[]
            Info if you really want to walk ?
        infos Optional[List[]]
            ~
        coords Optional[List[List[:class:`int`]]]
            coords of this connection
        path_description Optional[]
            ~
        interchange Optional[]
            ~
        properties Optional[:class:`dict`]
            misc info about this connection
    """

    def __init__(self, **kwargs):
        self.duration = kwargs.get("duration")
        self.is_realtime_controlled = kwargs.get("isRealtimeControlled", False)
        self.origin = Origin(**kwargs.get("origin"))
        self.destination = Destination(**kwargs.get("destination"))
        self.transportation = Transportation(**kwargs.get("transportation"))

        # inserted raw
        self.raw = kwargs
        self.stop_sequence = kwargs.get("stopSequence")
        self.foot_path_info = kwargs.get("footPathInfo")
        self.infos = kwargs.get("infos")
        self.coords = kwargs.get("coords")
        self.path_description = kwargs.get("pathDescription")
        self.interchange = kwargs.get("interchange")
        self.properties = kwargs.get("properties")

    def __str__(self):
        dep_pre = "[Delayed] " if self.origin.delay else ""
        arr_pre = "[Delayed] " if self.destination.delay else ""
        if self.origin.departure_time_estimated.date() == datetime.now().date():
            return f"[{self.transportation.disassembled_name}]: " \
                f"{dep_pre}[{self.origin.departure_time_estimated.strftime('%H:%M')}] @ {self.origin.name} - " \
                f"{arr_pre}[{self.destination.arrival_time_estimated.strftime('%H:%M')}] @ {self.destination.name}"
        return f"[{self.transportation.disassembled_name}]: " \
            f"{dep_pre}[{self.origin.departure_time_estimated}] @ {self.origin.name} - " \
            f"{arr_pre}[{self.destination.arrival_time_estimated}] @ {self.destination.name}"
