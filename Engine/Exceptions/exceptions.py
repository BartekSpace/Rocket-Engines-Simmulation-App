class WrongInputData(Exception):
    def __init__(self, val, message="Input data is invalid!"):
        self.val = val
        self.message = message
        super().__init__(self.message)


class LowPressureDropError(Exception):
    def __init__(self, drop, message="Too low pressure drop!"):
        self.drop = drop
        self.message = message
        super().__init__(self.message)
