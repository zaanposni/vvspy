class ServingLine:
    r"""

        Describes the line, departing or arriving in a Departure/Arrival result.

        Attributes
        -----------

        raw :class:`dict`
            Raw dict received by the API.
        key :class:`str`
            key (most likely an ID) of the line.
        code :class:`str`
            code (most likely type) of the line.
        number :class:`str`
            number of line (e.g. U12).
        symbol :class:`str`
            symbol displayed on the transport itself (e.g. U12).
        mot_type :class:`str`
            ~
        mt_sub_code :class:`str`
            ~
        real_time :class:`bool`
            whether or not the transport supports realtime tracking.
        direction :class:`str`
            Last station the transport is heading to.
        direction :class:`str`
            Last station the transport is heading to.
        direction_from :class:`str`
            Starting station of the transport.
        name :class:`str`
            name of the line type (e.g. Stadtbahn).
        train_num :class:`str`
            Last station the transport is heading to.
        delay Optional[:class:`str`]
            Minutes of delay.
        li_erg_ri_proj :class:`dict`
            Detailed line information (e.g. network)
        dest_id :class:`str`
            station id of the destination
        stateless :class:`str`
            ~
    """
    def __init__(self, **kwargs):
        self.raw = kwargs
        self.key = kwargs.get("key")
        self.code = kwargs.get("code")
        self.number = kwargs.get("number")
        self.symbol = kwargs.get("symbol")
        self.mot_type = kwargs.get("motType")
        self.mt_sub_code = kwargs.get("mtSubCode")
        try:
            self.real_time = bool(int(kwargs.get("realtime", "0")))
        except ValueError:
            self.real_time = False
        self.direction = kwargs.get("direction")
        self.direction_from = kwargs.get("directionFrom")
        self.name = kwargs.get("trainName", kwargs.get("name"))
        self.delay = kwargs.get("delay")
        self.li_erg_ri_proj = kwargs.get("liErgRiProj")
        self.dest_id = kwargs.get("destID")
        self.stateless = kwargs.get("stateless")

    def __str__(self):
        return f"[{self.symbol}]: {self.direction_from} - {self.direction}"
