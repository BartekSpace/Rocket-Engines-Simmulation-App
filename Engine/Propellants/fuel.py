import numpy as np

from Engine.Propellants.propellant import Propellant
from Engine.config import delta_time, non_negative, non_negative_val
from rocketcea.cea_obj import add_new_fuel


class Fuel(Propellant):


    def __init__(self, temp, enth, name, formula, diam_port, length, dens, ballistic):
        super().__init__(temp, enth, name, formula)
        self._diam_port = diam_port
        self._ballistic = ballistic
        self._length = length
        self._dens = dens
        self._port_area = np.pi * (self.diam_port / 1000) ** 2 / 4
        # self._mass_flow = 0.00001  # nonzero value
        # add_fuel(name, formula, temp, enth)
        self.add_propellant()
        # self._flow = 0
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.__dict__ == other.__dict__


    @property
    def port_area(self):
        return self._port_area

    @property
    def initial_temperature(self):
        return self._initial_temperature

    @property
    def enthalpy_formation(self):
        return self._enthalpy_formation

    @property
    def length(self):
        return self._length

    @property
    def dens(self):
        return self._dens

    @property
    def ballistic(self):
        return self._ballistic

    @property
    def diam_port(self):
        return self._diam_port


    @diam_port.setter
    def diam_port(self, val):
        self._diam_port = val
        self._port_area = np.pi * (val / 1000) ** 2 / 4

    @property
    def mass_flow(self):
        return self._mass_flow

    @mass_flow.setter
    def mass_flow(self, val):
        self._mass_flow = val

    # @property
    # def flow(self):
    #     return self._flow
    #
    # @flow.setter
    # def flow(self, val):
    #     self._flow = val

    def calculate_mass_flow(self, oxid_flow, change_diam_port=True):
        # port_area = np.pi * (self.diam_port / 1000) ** 2 / 4
        gox = oxid_flow / self.port_area
        reg = self.ballistic.a * gox ** self.ballistic.n / 1000
        if change_diam_port:
            self.diam_port += 2 * 1000 * reg * delta_time
        # return np.pi*self.diam_port/1000 * self.length/1000 * self.dens * reg
        self.mass_flow = np.pi * self.diam_port / 1000 * self.length / 1000 * self.dens * reg

        # 2 * 3.14 * radius * length / 1000 * dens * reg

    def add_propellant(self):
        string = """
        fuel {} {} wt%=100.00
        h,kJ/mol={}     t(k)={}""".format(self.name, self.formula, self.enthalpy_formation, self.initial_temperature)
        add_new_fuel(self.name, string)
