# from abc import ABC, abstractmethod
#
# class Phase(ABC):
#     @abstractmethod
#     def next_iteration(self, pressure, vessel, injector):
#         pass
#
# class Liquid(Phase):
#     def next_iteration(self, pressure, vessel, injector):
#         self.calculate_new_temp(vessel)
#         self.calculate_mass_flow(vessel, injector, pressure)
#
#         delta_outflow_mass = 0.5 * delta_time * \
#                              (3.0 * self.mass_flow - self.mass_flow.old)
#         liquid_mass_before_boil = vessel.mass_liquid - delta_outflow_mass
#         vessel.mass_total -= delta_outflow_mass
#
#         bob = liquid_mass_before_boil - vessel.mass_liquid
#         tc = delta_time / 0.15
#         self._vaporized_mass = tc * (bob - self._vaporized_mass) + self._vaporized_mass
#
#         if vessel.mass_liquid > liquid_mass_before_boil:
#             return False
#         return True
#
#
#     def calculate_new_temp(self, vessel):
#             Enth_of_vap = nox_enthV(vessel.temp)
#             Spec_heat_cap = nox_Cpl(vessel.temp)
#             deltaQ = self._vaporized_mass * Enth_of_vap
#             deltaTemp = -(deltaQ / (vessel.mass_liquid * Spec_heat_cap))
#             vessel.temp += deltaTemp
#
