from .line_operator import LineOperator


class Transportation:
    r"""

        Describes info about transportation of a :class:`Connection`.

        Attributes
        -----------

        raw :class:`dict`
            Raw dict received by the API.
        id :class:`str`
            id of the transportation.
        name :class:`str`
            name of the transportation.
        disassembled_name :class:`str`
            detailed name of the transportation.
        number :class:`str`
            line number of the transportation.
        description :class:`str`
            description, most of the time the string that is displayed on the bus/train itself.
        product :class:`dict`
            describes the mean of transport (bus, train, etc.)
        operator :class:`LineOperator`
            describes the Operator of the transport.
        destination :class:`dict`
            destination of the transport.
        properties :class:`dict`
            misc info about the transport.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.disassembled_name = kwargs.get("disassembledName", "Walk")
        self.number = kwargs.get("number")
        self.description = kwargs.get("description")
        self.product = kwargs.get("product")
        self.operator = LineOperator(**kwargs.get("operator", {}))
        self.destination = kwargs.get("destination")

        # inserted raw
        self.raw = kwargs
        self.properties = kwargs.get("properties")
