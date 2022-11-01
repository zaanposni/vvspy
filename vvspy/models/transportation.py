from typing import Any, Dict, Optional

from vvspy.models.line_operator import LineOperator


class Transportation:
    """Describes info about transportation of a `Connection`.

    * TODO: Check which fields are required

    Attributes
    -----------
    raw : Dict[str, Any]
        Raw dict received by the API.
    id : Optional[str]
        Id of the transportation.
    name : Optional[str]
        Name of the transportation.
    disassembled_name : str
        Detailed name of the transportation. _By default `Walk`._
    number : Optional[str]
        Line number of the transportation.
    description : Optional[str]
        Description, most of the time the string that is displayed on the bus/train itself.
    product : Optional[Dict[str, Any]]
        Describes the mean of transport (bus, train, etc.).
    operator : LineOperator
        Describes the Operator of the transport.
    destination : Optional[Dict[str, Any]]
        Destination of the transport.
    properties : Dict[str, Any]
        Misc info about the transport.
    """

    def __init__(self, **kwargs) -> None:
        self.raw: Dict[str, Any] = kwargs
        self.id: Optional[str] = kwargs.get("id")
        self.name: Optional[str] = kwargs.get("name")
        self.description: Optional[str] = kwargs.get("description")
        self.disassembled_name: str = kwargs.get("disassembledName", "Walk")
        self.number: Optional[str] = kwargs.get("number")
        self.product: Optional[Dict[str, Any]] = kwargs.get("product")
        self.operator: LineOperator = LineOperator(**kwargs.get("operator", {}))
        self.destination: Optional[Dict[str, Any]] = kwargs.get("destination")
        self.properties: Optional[Dict[str, Any]] = kwargs.get("properties")
