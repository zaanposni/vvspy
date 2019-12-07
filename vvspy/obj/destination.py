from datetime import datetime


class Destination:
    r"""

        Describes the destination of a :class:`Connection`.

        Attributes
        -----------

        raw :class:`dict`
            Raw dict received by the API.
        is_global_id :class:`bool`
            ~
        id :class:`str`
            station id of the destination station
        name :class:`str`
            name of the destination station
        disassembled_name Optional[:class:`str`]
            detailed name of the destination station.
        type :class:`str`
            type of the destination station. (e.g. bus, track)
        point_type Optional[:class:`str`]
            ~
        coord List[:class:`int`]
            coords of the station
        niveau :class:`int`
            ~
        parent :class:`dict`
            ~
        arrival_time_planned :class:`datetime.datetime`
            Time planned of arrival.
        arrival_time_estimated :class:`datetime.datetime`
            Time estimated with realtime info (same as `arrival_time_planned` if no realtime data is available).
        delay :class:`int`
            Minutes of delay.
        properties :class:`dict`
            misc info about the destination.
    """
    def __init__(self, **kwargs):
        self.is_global_id = kwargs.get("isGlobalId")
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.disassembled_name = kwargs.get("disassembledName"),
        self.type = kwargs.get("type")
        self.point_type = kwargs.get("pointType")
        self.coord = tuple(kwargs.get("coord", []))
        self.niveau = kwargs.get("niveau")
        self.parent = kwargs.get("parent")
        self.arrival_time_planned = datetime.strptime(kwargs.get("arrivalTimePlanned", "")[:-1], "%Y-%m-%dT%H:%M:%S")
        self.arrival_time_estimated = datetime.strptime(kwargs.get("arrivalTimeEstimated", "")[:-1],
                                                        "%Y-%m-%dT%H:%M:%S")
        delta = self.arrival_time_estimated - self.arrival_time_planned
        self.delay = int(delta.total_seconds() / 60)

        # inserted raw
        self.raw = kwargs
        self.properties = kwargs.get("properties")
