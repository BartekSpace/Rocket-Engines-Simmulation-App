from abc import ABC, abstractmethod


class Propellant(ABC):

    def __init__(self, temp, enth, name, formula):
        self._initial_temperature = temp
        self._enthalpy_formation = enth
        self.name = name
        self.formula = formula
        self._mass_flow = 0.00001

    @property
    @abstractmethod
    def initial_temperature(self):
        pass

    @property
    @abstractmethod
    def enthalpy_formation(self):
        pass

    @property
    @abstractmethod
    def mass_flow(self):
        pass

    @mass_flow.setter
    @abstractmethod
    def mass_flow(self, val):
        pass
