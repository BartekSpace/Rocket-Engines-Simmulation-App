from Engine.Propellants.nitrous_thermodynamics import nox_vp,nox_Vrho, nox_Lrho, nox_on_press
from Engine.Propellants.constants import pCrit
from Engine.Exceptions.exceptions import WrongInputData, UnphysicalData, NonPositiveValue
from Engine.config import non_negative


@non_negative
class Vessel:
    def __init__(self, pressure, volume, mass):

        # if mass < 0:
        #     # raise ValueError("Vessel: Mass must be non negative!")
        #     raise NonPositiveValue('Mass', type(self).__name__)
        # if volume <= 0:
        #     raise NonPositiveValue('Volume',type(self).__name__)
        if pressure > pCrit:
            raise WrongInputData('Critical',type(self).__name__,"pressure reached!")
        if pressure <= 1:
            raise WrongInputData('Pressure',type(self).__name__,"must be above atmospheric")
        self._press = pressure
        self._temp = nox_on_press(pressure)
        self.dens_liq = nox_Lrho(self._temp)
        self.dens_vap = nox_Vrho(self._temp)
        self._vol = volume
        self.hasLiquid = self.__calculate_amount_of_liquid(mass) > 0
        self.mass_total = mass

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.__dict__ == other.__dict__

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
            self.mass_liquid = self.__calculate_amount_of_liquid()
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
            raise UnphysicalData()
        self._mass_vapor = value

    def __calculate_amount_of_liquid(self, mass=None):
        if mass is None:
            mass = self._mass_total
        tmp = (1.0 / self.dens_liq) - (1.0 / self.dens_vap)
        return (self.vol - (mass / self.dens_vap)) / tmp




