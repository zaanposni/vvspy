from datetime import datetime


class Origin:
    def __init__(self, **kwargs):
        self.raw = kwargs
        self.is_global_id = kwargs.get("isGlobalId")
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.disassembled_name = kwargs.get("disassembledName"),
        self.type = kwargs.get("type")
        self.point_type = kwargs.get("pointType")
        self.coord = tuple(kwargs.get("coord", []))
        self.niveau = kwargs.get("niveau")
        self.parent = kwargs.get("parent")
        self.departure_time_planned = datetime.strptime(kwargs.get("departureTimePlanned", "")[:-1],
                                                        "%Y-%m-%dT%H:%M:%S")
        self.departure_time_estimated = datetime.strptime(kwargs.get("departureTimeEstimated", "")[:-1],
                                                          "%Y-%m-%dT%H:%M:%S")
        delta = self.departure_time_estimated - self.departure_time_planned
        self.delay = int(delta.total_seconds() / 60)
        self.properties = kwargs.get("properties")
