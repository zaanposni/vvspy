class LineOperator:
    def __init__(self, **kwargs):
        self.code = kwargs.get("code")
        self.name = kwargs.get("name")
        self.public_code = kwargs.get("publicCode")

    def __str__(self):
        return f"{self.name} ({self.code})"
