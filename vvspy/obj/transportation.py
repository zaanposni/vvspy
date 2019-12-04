from .line_operator import LineOperator


class Transportation:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.disassembled_name = kwargs.get("disassembledName", "Walk")
        self.number = kwargs.get("number")
        self.description = kwargs.get("description")
        self.product = kwargs.get("product")
        self.operator = LineOperator(**kwargs.get("operator", {}))
        self.destination = kwargs.get("destination")
        self.properties = kwargs.get("properties")
