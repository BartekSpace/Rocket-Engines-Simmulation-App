
import copy

from Engine.Injector.injector import Injector
from Engine.Nozzle.nozzle import Nozzle
from Engine.Propellants.fuel import Fuel
from Engine.Propellants.oxidizer import Oxidizer
from Engine.Propellants.side_classes import Ballistic
from Engine.Vessel.vessel import Vessel
from Engine.engine_simulation import Engine


def test_check_values_liquid():
    ves = Vessel(60, 0.015, 10)
    inj = Injector(36, 1.5, 4.2)
    nozzle = Nozzle(72, 33)

    b = Ballistic(0.00772597539149796, 0.777265794840152)
    fuel = Fuel(300, 67.69, 'Nylon', 'C 6.0   H 11.0   O 1.0  N 1.0', 61, 1000, 1130, b)
    oxid = Oxidizer(300, 75.24, 'N2O1', 'N 2.0 O 1.0')

    t0 = Engine(ves, inj, nozzle, fuel, oxid)
    t1 = copy.deepcopy(t0)
    t1.next_iteration()

    assert t0._vessel.press > t1._vessel.press
    assert t0._vessel.temp  > t1._vessel.temp
    assert t0._vessel.dens_liq < t1._vessel.dens_liq
    assert t0._vessel.dens_vap > t1._vessel.dens_vap
    assert t0._vessel.vol == t1._vessel.vol
    assert t0._vessel.mass_total > t1._vessel.mass_total
    assert t0._vessel.mass_liquid > t1._vessel.mass_liquid
    assert t0._vessel.mass_vapor < t1._vessel.mass_vapor


def test_check_values_gas():
    ves = Vessel(60, 0.015, 2)
    inj = Injector(36, 1.5, 4.2)
    nozzle = Nozzle(72, 33)
    b = Ballistic(0.00772597539149796, 0.777265794840152)
    fuel = Fuel(300, 67.69, 'Nylon', 'C 6.0   H 11.0   O 1.0  N 1.0', 61, 1000, 1130, b)
    oxid = Oxidizer(300, 75.24, 'N2O1', 'N 2.0 O 1.0')

    t0 = Engine(ves, inj, nozzle, fuel, oxid)
    # t0 = Engine(1, ves, inj)
    t1 = copy.deepcopy(t0)
    t1.next_iteration()

    assert t0._vessel.press > t1._vessel.press
    assert t0._vessel.temp  > t1._vessel.temp
    assert t0._vessel.dens_vap > t1._vessel.dens_vap
    assert t0._vessel.vol == t1._vessel.vol
    assert t0._vessel.mass_total > t1._vessel.mass_total
    assert t0._vessel.mass_vapor > t1._vessel.mass_vapor