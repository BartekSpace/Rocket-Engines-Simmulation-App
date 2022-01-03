import os
import sys

from rocketcea.cea_obj_w_units import CEA_Obj

delta_time = 0.01


def get_Isp(oxid_name, fuel_name, chamber_pressure, OF, eps_nozzle):
    with HiddenPrints():
        C = CEA_Obj(oxName=oxid_name, fuelName=fuel_name, pressure_units='Bar', cstar_units='m/s')
        x = C.estimate_Ambient_Isp(Pc=chamber_pressure, MR=OF, eps=eps_nozzle, Pamb=1)
        return x[0]


def get_c_star(oxid_name, fuel_name, chamber_pressure, OF):
    with HiddenPrints():
        C = CEA_Obj(oxName=oxid_name, fuelName=fuel_name, pressure_units='Bar', cstar_units='m/s')
        x = C.get_Cstar(Pc=chamber_pressure, MR=OF)
        return x


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
