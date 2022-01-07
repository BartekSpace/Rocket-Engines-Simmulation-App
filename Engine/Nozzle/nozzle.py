import numpy as np
np.seterr(all='ignore')

from Engine.config import non_negative


@non_negative
class Nozzle:
    def __init__(self, diameter_exit, diameter_throat, efficiency):#, fuel):
        self._diam_exit = diameter_exit
        self._area_th = np.pi*(diameter_throat/1000)**2/4
        self._efficiency = efficiency
        # self._fuel = fuel
        # self._c_star = 0
        # self._isp = 0
        self._esp = (diameter_exit / diameter_throat)**2

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.__dict__ == other.__dict__


    @property
    def diam_exit(self):
        return self._diam_exit

    @property
    def efficiency(self):
        return self._efficiency

    @property
    def area_th(self):
        return self._area_th

    @property
    def esp(self):
        return self._esp

    # @property
    # def fuel(self):
    #     return self._fuel

    def calculate_c_star(self, press, flow_rate):
        return press*100000*self.area_th/flow_rate

    def calculate_chamber_pressure(self, c_star, flow_rate):
        return c_star*flow_rate/self.area_th/100000








    # @property
    # def c_star(self):




