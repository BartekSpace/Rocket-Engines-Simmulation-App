from Engine.config import non_negative


@non_negative
class Injector:
    def __init__(self, num_orifices, diameter_orifices, k_loss):
        self._num_orifices = num_orifices
        self._diam_orifice = diameter_orifices
        self.D_loss = k_loss / (num_orifices * 3.14 * (diameter_orifices / 1000) ** 2 / 4) ** 2

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.__dict__ == other.__dict__


    @property
    def num_orifices(self):
        return self._num_orifices

    @property
    def diam_orifice(self):
        return self._diam_orifice

    # @num_orifices.setter
    # def num_orifices(self, value):
    #     self._num_orifices = value


