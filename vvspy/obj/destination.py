from datetime import datetime


class Destination:
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
        self.arrival_time_planned = datetime.strptime(kwargs.get("arrivalTimePlanned", "")[:-1], "%Y-%m-%dT%H:%M:%S")
        self.arrival_time_estimated = datetime.strptime(kwargs.get("arrivalTimeEstimated", "")[:-1],
                                                        "%Y-%m-%dT%H:%M:%S")
        delta = self.arrival_time_estimated - self.arrival_time_planned
        self.delay = int(delta.total_seconds() / 60)
        self.properties = kwargs.get("properties")
