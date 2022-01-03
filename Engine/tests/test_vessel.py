from Engine.Exceptions.exceptions import WrongInputData
from Engine.Vessel.vessel import Vessel
import pytest


def test_wrong_input_data():
    with pytest.raises(ValueError):
        ves = Vessel(-1, 0.015, 30)
    with pytest.raises(ValueError):
        ves = Vessel(55, -3, 30)
    with pytest.raises(ValueError):
        ves = Vessel(55, 0.015, -4)


def test_check_no_liquid_scenario():
    ves = Vessel(60, 0.015, 1)
    assert not ves.hasLiquid


def test_check_liquid_scenario():
    ves = Vessel(60, 0.015, 10)
    assert ves.hasLiquid


def test_check_too_much_mass():
    with pytest.raises(WrongInputData):
        ves = Vessel(60, 0.015, 30)


def test_check_critical_conditions():
    with pytest.raises(ValueError):
        ves = Vessel(80, 0.015, 10)
