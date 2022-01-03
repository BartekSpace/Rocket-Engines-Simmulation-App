import pytest

from Engine.Exceptions.exceptions import LowPressureDropError
from Engine.Injector.injector import Injector
from Engine.Propellants.oxidizer import Oxidizer
from Engine.Vessel.vessel import Vessel


def test_check():
    ves = Vessel(60, 0.015, 10)
    inj = Injector(36, 1.5, 4.2)
    ox = Oxidizer(300,75,"name","N 2 O 1")
    with pytest.raises(LowPressureDropError):
        ox.calculate_mass_flow(ves, inj, 60)