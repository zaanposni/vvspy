class ServingLine:
    def __init__(self, **kwargs):
        self.key = kwargs.get("key")
        self.code = kwargs.get("code")
        self.number = kwargs.get("number")
        self.symbol = kwargs.get("symbol")
        self.mot_type = kwargs.get("motType")
        self.mt_sub_code = kwargs.get("mtSubCode")
        self.real_time = kwargs.get("realtime")
        self.direction = kwargs.get("direction")
        self.direction_from = kwargs.get("directionFrom")
        self.train_name = kwargs.get("trainName")
        self.train_num = kwargs.get("trainNum")
        self.name = kwargs.get("name")
        self.li_erg_ri_proj = kwargs.get("liErgRiProj")
        self.dest_id = kwargs.get("destID")
        self.stateless = kwargs.get("stateless")

    def __str__(self):
        return f"[{self.symbol}]: {self.direction_from} - {self.direction}"
