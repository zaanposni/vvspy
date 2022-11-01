from typing import Any, Dict, Optional


class LineOperator:
    """Describes the operator of a Connection class

    * TODO: Check which fields are required

    Attributes
    -----------
    raw : Dict[str, Any]
        Raw dict received by the API.
    id : Optional[str]
        Id of the operator.
    name : Optional[str]
        Display name of the operator.
    public_code : Optional[str]
        Public_code of the operator.
    """

    def __init__(self, **kwargs) -> None:
        self.raw: Dict[str, Any] = kwargs
        self.id: Optional[str] = kwargs.get("code", kwargs.get("id"))
        self.name: Optional[str] = kwargs.get("name")
        self.public_code: Optional[str] = kwargs.get("publicCode")

    def __str__(self) -> str:
        return f"{self.name} ({self.id})"
