import eel

from Engine.Injector.injector import Injector
from Engine.Propellants.fuel import Fuel
from Engine.Propellants.oxidizer import Oxidizer
from Engine.Propellants.side_classes import Ballistic
from Engine.engine_simulation import Engine
from Engine.Vessel.vessel import Vessel
from Engine.Nozzle.nozzle import Nozzle
import matplotlib.pyplot as plt


# import eel.browsers
# eel.browsers.set_path('firefox', '/path/to/your/exe')
class Parser:
    pass


parser = Parser()


# @eel.expose
# def injector(num_orifices, diam_orifices, k_loss):
#
#     parser.inj = Injector(float(num_orifices),float(diam_orifices), float(k_loss) )

@eel.expose
def injector(*args):
    b = [float(arg) for arg in args]
    parser.inj = Injector(*b)


@eel.expose
def run():
    ves = Vessel(60, 0.015, 10)
    nozzle = Nozzle(72, 33)
    # inj = Injector(36, 1.5, 4.2)

    b = Ballistic(0.00772597539149796, 0.777265794840152)
    fuel = Fuel(300, 67.69, 'nyl', 'C 6.0   H 11.0   O 1.0  N 1.0', 61, 1000, 1130, b)
    oxid = Oxidizer(300, 75.24, 'nitrous', 'N 2 O 1')
    engine = Engine(ves, parser.inj, nozzle, fuel, oxid)
    # start_time = time.time()
    data = engine.run()
    # print("--- %s seconds ---" % (time.time() - start_time))
    plt.plot(data['time'], data['pressure_combustion'])
    plt.show()

    eel.sendData(data)


eel.init("www")
eel.start("index.html")
#
# def run(injector):
