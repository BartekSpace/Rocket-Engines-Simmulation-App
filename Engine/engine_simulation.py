


# import Execptions.LowPressureDropError
# delta_time = 0.01
import sys

from Engine.Exceptions.exceptions import LowPressureDropError
from Engine.Propellants.side_classes import Container
from Engine.config import delta_time, get_c_star, get_Isp, get_thrust_cF, get_combustion_temp


class Engine:

    def __init__(self, vessel, injector, nozzle, fuel, oxid):  # , nozzle, fuel): #, nozzle):
        self._oxid = oxid
        # self._pressure = pressure
        self._vessel = vessel
        self._injector = injector

        self._nozzle = nozzle
        self._fuel = fuel


        self.c_star = 1000  # nonzero value

        self.evaluate_chamber_pressure()

        self._names = ["time", "pressure_chamber", "fuel_mass_flow", "oxid_mass_flow", "pressure_vessel",
                       "thrust", "isp", "c_star", "of", "diam_port", "gox", "temperature"]
        self._data = dict.fromkeys(self._names, [])
        for key in self._data.keys():
            self._data[key] = []

    def __eq__(self, other):
        if not isinstance(other, Engine):
            return False
        a = self.oxid == other.oxid
        a &= self.fuel == other.fuel
        a &= self.nozzle == other.nozzle
        a &= self.injector == other.injector
        a &= self.vessel == other.vessel
        return a

        # self._data['time'] = []
        # self._data['pressure_combustion'] = []
        # self._data['fuel_mass_flow'] = []
        # self._data['oxid_mass_flow'] = []
        # self._data['pressure_vessel'] = []
        # self._data['thrust'] = []
        # self._data['isp'] = []
        # self._data['c_star'] = []
        # self._data['of'] = []
        # self._data['diam_port'] = []

    @property
    def pressure(self):
        return self._pressure

    @pressure.setter
    def pressure(self, val):
        self._pressure = val

    @property
    def oxid(self):
        return self._oxid

    @property
    def fuel(self):
        return self._fuel

    @property
    def nozzle(self):
        return self._nozzle

    @property
    def vessel(self):
        return self._vessel

    @property
    def injector(self):
        return self._injector

    @property
    def data(self):
        return self._data

    # def next_iteration(self):
    #     self.pressure = self.nozzle.calculate_chamber_pressure(self.c_star,
    #                                                            self.oxid._mass_flow.val + self.fuel_flow)
    #     self.fuel_flow = self.fuel.calculate_fuel_flow(self.oxid._mass_flow.val)
    #     return self.oxid.next_iteration(self.vessel, self.injector, self.pressure)

    def next_iteration(self):
        self.pressure = self.nozzle.calculate_chamber_pressure(self.c_star,
                                                                self.oxid.mass_flow + self.fuel.mass_flow)

        # self.evaluate_chamber_pressure()
        self.fuel.calculate_mass_flow(self.oxid.mass_flow)




        return self.oxid.next_iteration(self.vessel, self.injector, self.pressure)

    # def evaluate_chamber_pressure(self):
    #
    #     press = Container(10, 1)
    #     while press / press.old > 1.000001 or press.old / press > 1.000001:
    #         self.fuel_flow = self.fuel.calculate_fuel_flow(self.oxid._mass_flow.val, change_diam_port=False)
    #         press.val = self.nozzle.calculate_chamber_pressure(self.c_star,
    #                                                            self.oxid._mass_flow.val + self.fuel_flow)
    #         self.oxid.calculate_oxid_mass_flow(self.vessel, self.injector, press)
    #         self.c_star = get_c_star(self.oxid.name, self.fuel.name, press,
    #                                  self.oxid._mass_flow.val / self.fuel_flow)
    #     self.pressure = press.val

    def evaluate_chamber_pressure(self):


        press = Container(10, 1)


        while press / press.old > 1.000001 or press.old / press > 1.000001:


            self.fuel.calculate_mass_flow(self.oxid.mass_flow, change_diam_port=False)
            press.val = self.nozzle.calculate_chamber_pressure(self.c_star,
                                                               self.oxid.mass_flow + self.fuel.mass_flow)
            self.oxid.calculate_mass_flow(self.vessel, self.injector, press)
            self.c_star = get_c_star(self.oxid.name, self.fuel.name, press,
                                     self.oxid.mass_flow / self.fuel.mass_flow)
        self.pressure = press.val

    def run(self, end_time=999999):

        time = 0
        # val = []
        # t = []
        while time < end_time:

            try:
                if not self.next_iteration():
                    self.evaluate_chamber_pressure()
                self.c_star = get_c_star(self.oxid.name, self.fuel.name, self.pressure,
                                         self.oxid.mass_flow / self.fuel.mass_flow) ## todo check if it should be here
                # t.append(time)
                # val.append(self.fuel_flow)
                # val.append(self.pressure)
                self.collect_data()
                time += delta_time
            except LowPressureDropError:
                return self._data


            if self.pressure <= 1:
                    return self._data

            # except:
            #     return t, val

            # if self.pressure <= 3:
            #     return t, val
        # [self._data[key].pop() for key in self._data]
        return self._data

    def collect_data(self):
        self._data['time'].append(len(self._data['time']) * delta_time)
        self._data['pressure_chamber'].append(self.pressure)
        self._data['fuel_mass_flow'].append(self.fuel.mass_flow)
        self._data['oxid_mass_flow'].append(self.oxid.mass_flow.val)
        self._data['pressure_vessel'].append(self.vessel.press)
        self._data['of'].append(self.oxid.mass_flow / self.fuel.mass_flow)
        isp = get_Isp(self.oxid.name, self.fuel.name, self.pressure, self.oxid.mass_flow / self.fuel.mass_flow,
                      self.nozzle.esp)*self.nozzle.efficiency
        self._data['isp'].append(isp)
        self._data['thrust'].append(isp * 9.81 * (self.oxid.mass_flow + self.fuel.mass_flow))

        # CF = get_thrust_cF(self.oxid.name,self.fuel.name,self.pressure,self.oxid.mass_flow / self.fuel.mass_flow,self.nozzle.esp)
        # CF = CF[0]
        # self._data['thrust'].append(CF*self.pressure*self.nozzle.area_th*100000*self.nozzle.efficiency)
        self._data['c_star'].append(self.c_star)
        self._data['diam_port'].append(self.fuel.diam_port)
        self._data['gox'].append(self.oxid.mass_flow/self.fuel.port_area)
        self._data['temperature'] .append(get_combustion_temp(self.oxid.name, self.fuel.name,self.pressure,self.oxid.mass_flow + self.fuel.mass_flow))
