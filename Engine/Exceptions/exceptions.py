class WrongInputData(Exception):
    def __init__(self ,param="", source="", message="Input data is invalid!", val = ""):
        # self.val = str(val)
        # self.message = f"{source}: {param} {message}"
        self.value = val
        self.param = param
        self.source = source
        self.message = message
        super().__init__(self.message)


class NonPositiveValue(WrongInputData):
    def __init__(self, param, source, val =""):
        super().__init__(param, source, "Must be positive value!", val)


class LowPressureDropError(Exception):
    def __init__(self, drop, message="Too low pressure drop!"):
        self.drop = drop
        self.message = message
        super().__init__(self.message)


class UnphysicalData(WrongInputData):
    def __init__(self, message="correlation between vessel volume, pressure, or oxid mass is unphysical!"):
        self.message = message
        super().__init__( message= self.message)
