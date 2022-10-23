from typing import Any, Dict


class LineOperator:
    """Describes the operator of a Connection class

    Attributes
    -----------
    raw : Dict[str, Any]
        Raw dict received by the API.
    id : str
        Id of the operator. _By default `""`._
    name : str
        Display name of the operator. _By default `""`._
    public_code : str
        Public_code of the operator. _By default `""`._
    """

    def __init__(self, **kwargs):
        self.raw: Dict[str, Any] = kwargs
        self.id: str = kwargs.get("code", kwargs.get("id", ""))
        self.name: str = kwargs.get("name", "")
        self.public_code: str = kwargs.get("publicCode", "")

    def __str__(self):
        return f"{self.name} ({self.id})"
