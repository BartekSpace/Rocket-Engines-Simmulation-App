# from Engine.Injector.injector import Injector
# from Engine.Propellants.fuel import Fuel
# from Engine.Propellants.oxidizer import Oxidizer
# from Engine.Propellants.side_classes import Ballistic
# from Engine.engine_simulation import Engine
# from Engine.Vessel.vessel import Vessel
# from Engine.Nozzle.nozzle import Nozzle
#
# import matplotlib.pyplot as plt
# import time
#
# from dataPloter import Ploter
#
#
# def run():
#     ves = Vessel(53, 0.0155, 11.5)
#
#     nozzle = Nozzle(70, 34.5)
#     inj = Injector(36, 1.5, 3.4)
#     b = Ballistic(0.00772597539149796, 0.777265794840152)
#     fuel = Fuel(300, 67.69, 'nyl', 'C 6.0   H 11.0   O 1.0  N 1.0', 63, 1000, 1130, b)
#
#     oxid = Oxidizer(300, 75.24, 'nitrous', 'N 2 O 1')
#     engine = Engine(ves, inj, nozzle, fuel, oxid)
#     start_time = time.time()
#     data = engine.run()
#     # print("--- %s seconds ---" % (time.time() - start_time))
#     # plt.plot(data['time'], data['pressure_combustion'])
#     # plt.show()
#
#     ploter = Ploter(data)
#     ploter.read_hotflow_data('../Injector.txt', '../Chamber.txt', '../Thrust.txt')
#     ploter.truncate()
#     ploter.compare('pressure')
#     # ploter.plot_simulation("thrust")
#
#     # import csv
#     # with open('../Thrust.txt') as f:
#     #     reader = csv.DictReader(f)
#     #     t = []
#     #     val = []
#     #     for row in reader:
#     #         t.append(float(row['Timestamp']))
#     #         val.append(float(row['Thrust']))
#     #         if float(row['Timestamp']) > 14:
#     #             break
#     #         # print(row['Timestamp'], row['Value'])
#     #     data['isp'] = [val* 0.80 for val in data['isp']]
#     #
#     #     # plt.plot(data['time'], data['thrust'], t, val)
#     #     fig, ax = plt.subplots()
#     #     fig.subplots_adjust(right=0.75)
#     #
#     #     twin1 = ax.twinx()
#     #     # twin2 = ax.twinx()
#     #     p1, = ax.plot(data['time'],data['pressure_combustion'], "b-", label="Pressure Chamber")
#     #     p2, = twin1.plot(data['time'], data['thrust'], "r-", label="Thrust")
#     #     # p3, = twin2.plot([0, 1, 2], [50, 30, 15], "g-", label="Velocity")
#     #
#     #     # plt.plot(data['time'], data['isp'])#, t, val)
#     #     plt.show()
