from .constants import pCrit, ZCrit
import numpy as np


class Ballistic:
    def __init__(self, a, n):
        self._a = a
        self._n = n

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @property
    def a(self):
        return self._a

    @property
    def n(self):
        return self._n




class InitialVapour():
    def __init__(self, temp, mass, press, dens):
        self.temp = temp
        self.mass = mass
        self.press = press
        self.dens = dens
        self.Z = np.interp(press, (0, pCrit), (1, ZCrit))
    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Container:
    def __init__(self, val, initial_old_val=0):
        self._val = val
        self._old = initial_old_val

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, value):
        self._old = self._val
        self._val = value

    @property
    def old(self):
        return self._old

    @old.setter
    def old(self, val):
        self._old = val

    def __add__(self, other):
        return self._val + other

    def __sub__(self, other):
        return self._val - other

    def __mul__(self, other):
        return self._val * other

    def __floordiv__(self, other):
        return self._val // other

    def __truediv__(self, other):
        return self._val / other

    def __radd__(self, other):
        return self._val + other

    def __rsub__(self, other):
        return other - self._val

    def __rmul__(self, other):
        return self._val * other

    def __rtruediv__(self, other):
        return other / self._val

    def __rfloordiv__(self, other):
        return other // self._val

    def __iadd__(self, other):
        self._old = self._val
        self._val += other
        return self

    def __isub__(self, other):
        self._old = self._val
        self._val -= other
        return self

    def __imul__(self, other):
        self._old = self._val
        self._val *= other
        return self

    def __itruediv__(self, other):
        self._old = self._val
        self._val /= other
        return self
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

