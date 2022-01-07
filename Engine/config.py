import inspect
import os
import sys

from rocketcea.cea_obj_w_units import CEA_Obj

from Engine.Exceptions.exceptions import NonPositiveValue
from Engine.Propellants.side_classes import Ballistic

delta_time = 0.01

# def non_negative(foo):
#     def check(self, *args):
#         for arg in args:
#             if isinstance(arg, str):
#                 continue
#             if arg < 0:
#                 raise ValueError("Should be positive value")
#         return foo(*args)
#     return check

def non_negative(foo):
    def check(*args):

        for arg, arg_name in zip(args,inspect.getfullargspec(foo).args[1:]):
            if isinstance(arg, str) or isinstance(arg, Ballistic) or 'enth' in arg_name:
                continue
            if arg <= 0:
                # raise ValueError("Should be positive value")
                raise NonPositiveValue(arg_name,foo.__name__, arg)
        return foo(*args)
    return check

def non_negative_val(fun):
    def check(self, *args):
        for arg in args:
            if isinstance(arg, str):
                continue
            if arg < 0:
                raise ValueError("Should be positive value")
        return fun(self, *args)
    return check




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
