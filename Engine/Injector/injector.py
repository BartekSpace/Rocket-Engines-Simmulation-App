def non_negative(foo):
    def check(*args):
        for arg in args:
            if arg < 0:
                raise ValueError("Should be positive value")
        return foo(*args)

    return check


@non_negative
class Injector:
    def __init__(self, num_orifices, diameter_orifices, k_loss):
        self._num_orifices = num_orifices
        self._diam_orifice = diameter_orifices
        self.D_loss = k_loss / (num_orifices * 3.14 * (diameter_orifices / 1000) ** 2 / 4) ** 2

    @property
    def num_orifices(self):
        return self._num_orifices

    @property
    def diam_orifice(self):
        return self._diam_orifice

    # @num_orifices.setter
    # def num_orifices(self, value):
    #     self._num_orifices = value


