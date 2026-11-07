class Stop:
    r"""

        Describes a stop found by :func:`vvspy.get_stops`.

        Attributes
        -----------

        raw :class:`dict`
            Raw dict received by the API.
        stop_id Optional[:class:`str`]
            station id of the stop (e.g. 5006118).
        global_id Optional[:class:`str`]
            global station id of the stop, same format as :class:`vvspy.enums.Station` (e.g. de:08111:6118).
        name :class:`str`
            name of the stop
        disassembled_name Optional[:class:`str`]
            name of the stop without locality.
        type :class:`str`
            type of the location (always "stop").
        coord Tuple[:class:`float`]
            coords of the stop
        parent :class:`dict`
            locality the stop belongs to.
        locality Optional[:class:`str`]
            name of the locality the stop belongs to.
        match_quality :class:`int`
            how well the stop matches the search term, higher is better.
        is_best :class:`bool`
            whether or not this is the best match for the search term.
        product_classes List[:class:`int`]
            means of transport serving the stop.
        assigned_stops List[:class:`Stop`]
            stops belonging to this stop (e.g. platforms of a station).
        properties :class:`dict`
            misc info about the stop.
    """
    def __init__(self, **kwargs):
        self.properties = kwargs.get("properties", {})
        self.stop_id = self.properties.get("stopId")
        self.global_id = kwargs.get("id") if kwargs.get("isGlobalId") else None
        self.name = kwargs.get("name")
        self.disassembled_name = kwargs.get("disassembledName")
        self.type = kwargs.get("type")
        self.coord = tuple(kwargs.get("coord", []))
        self.parent = kwargs.get("parent", {})
        self.locality = self.parent.get("name")
        self.match_quality = kwargs.get("matchQuality")
        self.is_best = kwargs.get("isBest", False)
        self.product_classes = kwargs.get("productClasses", [])
        self.assigned_stops = [Stop(**x) for x in kwargs.get("assignedStops", [])]

        # inserted raw
        self.raw = kwargs

    def __str__(self):
        return f"{self.name} ({self.global_id or self.stop_id})"
