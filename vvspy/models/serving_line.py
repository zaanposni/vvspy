from typing import Any, Dict, Optional


class ServingLine:
    """Describes the line, departing or arriving in a Departure/Arrival result.

    * TODO: Check which fields are required

    Attributes
    -----------
    raw : Dict[str, Any]
        Raw dict received by the API.
    key : Optional[str]
        Key (most likely an ID) of the line.
    code : Optional[str]
        Code (most likely type) of the line.
    number : Optional[str]
        Number of line (e.g. U12).
    symbol : Optional[str]
        Symbol displayed on the transport itself (e.g. U12).
    mot_type : Optional[str]
        _None_
    mt_sub_code : Optional[str]
        _None_
    real_time : bool
        Whether or not the transport supports realtime tracking. _By default `False`._
    direction : Optional[str]
        Last station the transport is heading to.
    direction : Optional[str]
        Last station the transport is heading to.
    direction_from : Optional[str]
        Starting station of the transport.
    name : Optional[str]
        Name of the line type (e.g. Stadtbahn).
    train_num : Optional[str]
        Last station the transport is heading to.
    delay : Optional[str]
        Minutes of delay.
    li_erg_ri_proj : Optional[Dict[str, Any]]
        Detailed line information (e.g. network)
    dest_id : Optional[str]
        Station id of the destination
    stateless : Optional[str]
        _None_
    """

    def __init__(self, **kwargs) -> None:
        self.raw: Dict[str, Any] = kwargs
        self.key: Optional[str] = kwargs.get("key")
        self.code: Optional[str] = kwargs.get("code")
        self.number: Optional[str] = kwargs.get("number")
        self.symbol: Optional[str] = kwargs.get("symbol")
        self.mot_type: Optional[str] = kwargs.get("motType")
        self.mt_sub_code: Optional[str] = kwargs.get("mtSubCode")
        self.real_time: bool = True if kwargs.get("realtime") == "True" else False
        self.direction: Optional[str] = kwargs.get("direction")
        self.direction_from: Optional[str] = kwargs.get("directionFrom")
        self.name: Optional[str] = kwargs.get("trainName", kwargs.get("name"))
        self.delay: Optional[str] = kwargs.get("delay")
        self.li_erg_ri_proj: Optional[Dict[str, Any]] = kwargs.get("liErgRiProj")
        self.dest_id: Optional[str] = kwargs.get("destID")
        self.stateless: Optional[str] = kwargs.get("stateless")

    def __str__(self) -> str:
        return f"[{self.symbol}]: {self.direction_from} - {self.direction}"
