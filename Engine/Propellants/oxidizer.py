import numpy as np
# from rocketcea.cea_obj import add_new_oxidizer

from Engine.Propellants.constants import pCrit, ZCrit, Gamma
from Engine.Propellants.nitrous_thermodynamics import nox_enthV, nox_Cpl
from Engine.config import delta_time
from .propellant import Propellant

from .side_classes import Container, InitialVapour
from ..Exceptions.exceptions import LowPressureDropError
from rocketcea.cea_obj_w_units import CEA_Obj
from rocketcea.cea_obj import add_new_oxidizer
class Oxidizer(Propellant):
    def __init__(self, temp, enth, name, formula):
        super().__init__(temp, enth, name, formula)
        self.add_oxid()
        self._mass_flow = Container(0.00001)  ## nonzero value
        self._vaporized_mass = 0.00001
        self.init = None

    @property
    def initial_temperature(self):
        return self._initial_temperature

    @property
    def enthalpy_formation(self):
        return self._enthalpy_formation

    @property
    def mass_flow(self):
        return self._mass_flow

    @mass_flow.setter
    def mass_flow(self, val):
        self._mass_flow.val = val

    # @property
    # def vaporized_mass(self):
    #     return self._vaporized_mass
    #

    def calculate_mass_flow(self, vessel, injector, pressure):
        drop = vessel.press - pressure
        if drop < 0.00001:
            drop = 0.00001
        if drop / pressure < 0.2:
            # pass# safety reason, prevent backflow and instabilities
            raise LowPressureDropError(drop)
        # if type(self) is LiquidPhase:
        if vessel.hasLiquid:
            dens = vessel.dens_liq
        else:
            dens = vessel.dens_vap

        mass_flow = (2 * dens * drop * 100000 / injector.D_loss) ** 0.5
        self.mass_flow.val = mass_flow

    def calculate_new_temp_liquid(self, vessel):
        Enth_of_vap = nox_enthV(vessel.temp)
        Spec_heat_cap = nox_Cpl(vessel.temp)
        deltaQ = self._vaporized_mass * Enth_of_vap
        deltaTemp = -(deltaQ / (vessel.mass_liquid * Spec_heat_cap))
        vessel.temp += deltaTemp

    def next_iteration_liquid(self, pressure, vessel, injector):
        self.calculate_new_temp_liquid(vessel)
        self.calculate_mass_flow(vessel, injector, pressure)

        delta_outflow_mass = 0.5 * delta_time * \
                             (3.0 * self.mass_flow - self.mass_flow.old)
        liquid_mass_before_boil = vessel.mass_liquid - delta_outflow_mass
        vessel.mass_total -= delta_outflow_mass

        bob = liquid_mass_before_boil - vessel.mass_liquid
        tc = delta_time / 0.15
        self._vaporized_mass = tc * (bob - self._vaporized_mass) + self._vaporized_mass

        if vessel.mass_liquid > liquid_mass_before_boil:
            return False
        return True

    def update_press_and_temp_gas(self, vessel):
        current_z_guess = np.interp(vessel.press, (0, pCrit), (1, ZCrit))
        step = 1 / 0.9
        Aim = 0
        current_z = -1
        while current_z_guess / current_z > 1.000001 or current_z_guess / current_z < (1 / 1.000001):
            exp = Gamma - 1
            temp = self.init.temp * (vessel.mass_total * current_z_guess / self.init.mass / self.init.Z) ** exp

            exp = Gamma / (Gamma - 1)
            press = self.init.press * (temp / self.init.temp) ** exp

            current_z = np.interp(press, (0, pCrit), (1, ZCrit))
            OldAim = Aim

            if current_z_guess < current_z:
                current_z_guess *= step
                Aim = 1
            else:
                current_z_guess /= step
                Aim = -1

            if Aim == -OldAim:
                step = step ** 0.5

            # if not (current_z_guess / current_z > 1.000001 or current_z_guess / current_z < (1 / 1.000001)):
            #     break
        return press, temp

    def next_iteration_gas(self, vessel, injector, pressure):
        self.calculate_mass_flow(vessel, injector, pressure)
        delta_outflow_mass = 0.5 * delta_time * \
                             (3.0 * self._mass_flow - self._mass_flow.old)
        vessel.mass_total -= delta_outflow_mass

        vessel.press, vessel.temp = self.update_press_and_temp_gas(vessel)

        exp = 1 / (Gamma - 1)
        vessel.dens_vap = self.init.dens * (vessel.temp / self.init.temp) ** exp

    def next_iteration(self, vessel, injector, pressure):
        if vessel.hasLiquid:
            has_liquid = self.next_iteration_liquid(pressure, vessel, injector)
            if not has_liquid:
                self.init = InitialVapour(vessel.temp, vessel.mass_total, vessel.press,
                                          vessel.dens_vap)
                vessel.hasLiquid = False
                return False
            return True
        else:
            if self.init is None:
                self.init = InitialVapour(vessel.temp, vessel.mass_total, vessel.press,
                                          vessel.dens_vap)
            self.next_iteration_gas(vessel, injector, pressure)
            return True

    def add_oxid(self):
        # string = """
        # oxid """ + name + """ """ + formula + """  wt%=100.00
        # h,kJ/mol="""+enthalpy+"""   t(k)=""" + temperature
        string = """
           oxid {} {} wt%=100.00
           h,kJ/mol={}     t(k)={}""".format(self.name, self.formula, self.enthalpy_formation, self.initial_temperature)
        add_new_oxidizer(self.name, string)
