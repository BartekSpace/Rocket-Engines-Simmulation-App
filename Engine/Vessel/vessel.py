from Engine.Propellants.nitrous_thermodynamics import nox_vp,nox_Vrho, nox_Lrho, nox_on_press
from Engine.Propellants.constants import pCrit
from Engine.Exceptions.exceptions import WrongInputData

def non_negative(foo):
    def check(*args):
        for arg in args:
            if arg < 0:
                raise ValueError("Should be positive value")
        return foo(*args)
    return check


@non_negative
class Vessel:
    def __init__(self, pressure, volume, mass):
        if pressure > pCrit:
            raise ValueError("Critical pressure reached!")
        self._press = pressure
        self._temp = nox_on_press(pressure)
        self.dens_liq = nox_Lrho(self._temp)
        self.dens_vap = nox_Vrho(self._temp)
        self._vol = volume
        self.hasLiquid = self.calculate_amount_of_liquid(mass) > 0
        self.mass_total = mass

    @property
    def vol(self):
        return self._vol

    @property
    def temp(self):
        return self._temp

    # @non_negative
    @temp.setter
    def temp(self, value):
        self._temp = value
        if self.hasLiquid:
            self._press = nox_vp(self._temp)
            self.dens_liq = nox_Lrho(self._temp)
            self.dens_vap = nox_Vrho(self._temp)


    @property
    def press(self):
        return self._press

    @press.setter
    def press(self, value):
        self._press = value

    @property
    def mass_total(self):
        return self._mass_total

    @mass_total.setter
    def mass_total(self, value):
        self._mass_total = value
        if self.hasLiquid:
            # tmp = (1.0 / self.dens_liq) - (1.0 / self.dens_vap)
            # self.mass_liquid = (self.vol - (value / self.dens_vap)) / tmp
            self.mass_liquid = self.calculate_amount_of_liquid()
            if self.mass_liquid <= 0:
                self.mass_liquid = 0
                self.hasLiquid = False
            self.mass_vapor = value - self.mass_liquid
        else:
            self.mass_vapor = value

    @property
    def mass_vapor(self):
        return self._mass_vapor

    @mass_vapor.setter
    def mass_vapor(self, value):
        if value < 0:
            raise WrongInputData(value)
        self._mass_vapor = value

    def calculate_amount_of_liquid(self, mass=None):
        if mass is None:
            mass = self._mass_total
        tmp = (1.0 / self.dens_liq) - (1.0 / self.dens_vap)
        return (self.vol - (mass / self.dens_vap)) / tmp



