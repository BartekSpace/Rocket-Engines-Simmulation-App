from Engine.Injector.injector import Injector
from Engine.Propellants.fuel import Fuel
from Engine.Propellants.oxidizer import Oxidizer
from Engine.Propellants.side_classes import Ballistic
from Engine.engine_simulation import Engine
from Engine.Vessel.vessel import Vessel
from Engine.Nozzle.nozzle import Nozzle

import matplotlib.pyplot as plt
import time


def run():
    ves = Vessel(53, 0.0155, 11.5)
    nozzle = Nozzle(70, 34.5)
    inj = Injector(36, 1.5, 3.4)
    b = Ballistic(0.00772597539149796, 0.777265794840152)
    fuel = Fuel(300, 67.69, 'nyl', 'C 6.0   H 11.0   O 1.0  N 1.0', 63, 1000, 1130, b)
    oxid = Oxidizer(300, 75.24, 'nitrous', 'N 2 O 1')
    engine = Engine(ves, inj, nozzle, fuel, oxid)
    start_time = time.time()
    data = engine.run()
    # print("--- %s seconds ---" % (time.time() - start_time))
    # plt.plot(data['time'], data['pressure_combustion'])
    # plt.show()

    import csv
    with open('../Chamber.txt') as f:
        reader = csv.DictReader(f)
        t = []
        val = []
        for row in reader:
            t.append(float(row['Timestamp']))
            val.append(float(row['Value']))
            if float(row['Timestamp']) > 14:
                break
            # print(row['Timestamp'], row['Value'])
        # data['thrust'] = [val* 0.85 for val in data['thrust']]

        plt.plot(data['time'], data['pressure_combustion'], t, val)
        # plt.plot(data['time'], data['isp'])#, t, val)
        plt.show()
