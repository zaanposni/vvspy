class LineOperator:
    r"""

       Describes the operator of a :class:`Connection`.

       Attributes
       -----------

       raw :class:`dict`
           Raw dict received by the API.
       id :class:`str`
           id of the operator.
       name :class:`str`
           display name of the operator.
       public_code :class:`str`
           public_code of the operator.
    """
    def __init__(self, **kwargs):
        self.raw = kwargs
        self.id = kwargs.get("code", kwargs.get("id"))
        self.name = kwargs.get("name")
        self.public_code = kwargs.get("publicCode")

    def __str__(self):
        return f"{self.name} ({self.id})"
