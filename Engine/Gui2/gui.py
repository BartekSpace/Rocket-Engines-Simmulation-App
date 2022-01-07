import collections
import os
import shutil
from tkinter import Tk, filedialog
from typing import Any

import eel
import copy
from Engine.Injector.injector import Injector
from Engine.Propellants.fuel import Fuel
from Engine.Propellants.oxidizer import Oxidizer
from Engine.Propellants.side_classes import Ballistic, Container
from Engine.engine_simulation import Engine
from Engine.Vessel.vessel import Vessel
from Engine.Nozzle.nozzle import Nozzle
import matplotlib.pyplot as plt

# import eel.browsers
# eel.browsers.set_path('firefox', '/path/to/your/exe')
from dataPloter import Ploter



class Parser:


    def __init__(self):
        self.oxid = None
        self.fuel = None
        self.nozzle = None
        self.inj = None
        self.vessel = None
        self._time = None

    def __eq__(self, other):
        if not isinstance(other, Parser):
            return False
        a = self.oxid == other.oxid
        a &= self.fuel == other.fuel
        a &= self.nozzle == other.nozzle
        a &= self.inj == other.inj
        a &= self.vessel == other.vessel
        return a

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, val):
        if not isinstance(val, float):
            self._time = 1e20
        else:
            self._time = val
        # return self.__dict__ == other.__dict__


class Cache:
    def __init__(self):
        self._que = collections.deque(maxlen=2)
        self._que.append(Parser())
        self._data = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def que(self):
        return self._que


parser = Parser()
ploter = Ploter()
cache = Cache()



@eel.expose
def save_cache(time):
    parser.time = gently_float(time)
    # cache.append(copy.deepcopy(parser))
    cache.que.append(copy.deepcopy(parser))


def gently_float(element):
    try:
        return float(element)
    except ValueError:
        return element


@eel.expose
def injector(*args):
    args_list = [float(arg) for arg in args]
    parser.inj = Injector(*args_list)


@eel.expose
def nozzle(*args):
    args_list = [float(arg) for arg in args]
    parser.nozzle = Nozzle(*args_list)


@eel.expose
def vessel(*args):
    args_list = [float(arg) for arg in args]
    args_list[1] = args_list[1] / 1000
    parser.vessel = Vessel(*args_list)


@eel.expose
def fuel(*args):
    args_list = [gently_float(arg) for arg in args]
    b = Ballistic(*args_list[-2:])
    args_list.pop()
    args_list.pop()
    args_list.append(b)
    parser.fuel = Fuel(*args_list)


@eel.expose
def oxid(*args):
    args_list = [gently_float(arg) for arg in args]
    parser.oxid = Oxidizer(*args_list)




@eel.expose
def run(config):
    ploter.sim_plots = 0
    ploter.compare_plots = 0
    params = config[0]
    flags = config[1]


    # end = None
    engine = Engine(parser.vessel, parser.inj, parser.nozzle, parser.fuel, parser.oxid)
    shutil.rmtree('./Engine/Gui2/www/img/')
    os.mkdir('./Engine/Gui2/www/img')


    if cache.que[0] == cache.que[1] and cache.que[1].time <= cache.que[0].time:
        ploter.data = cache.data
        if cache.que[1].time < cache.que[0].time:  # if simulation should be shorter but data is the same
            # end = cache1.que[1].time
            ploter.truncate_sim(parser.time)
    else:  # if cache have changed re-run calculation
        ploter.data = engine.run(parser.time)

    cache.data = ploter.data
    ploter.truncate()
    if flags['allPressures'] and params['pressure_chamber'] and params['pressure_vessel']:
        params['pressure_chamber'] = False
        params['pressure_vessel'] = False
        params['pressure'] = True

    if flags['allMassFlows'] and params['fuel_mass_flow'] and params['oxid_mass_flow']:
        params['fuel_mass_flow'] = False
        params['oxid_mass_flow'] = False
        params['flow'] = True

    if flags['realAndSimulated']:
        for key in params:
            if params[key]:
                ploter.compare(key)
    else:
        for key in params:
            if params[key]:
                ploter.plot_real(key)
                ploter.plot_simulation(key)

    filenames = next(os.walk('./Engine/Gui2/www/img/'), (None, None, []))[2]
    paths = ['img/'+name for name in filenames]
    # paths_sim = [ 'img/sim_plot_' + key + '.png' for key in params if params[key]]
    # paths_real = [ 'img/real_plot_' + key + '.png' for key in params if params[key] and  ("pressure" in key or "thrust" in key)]
    eel.manage_images(paths)



def runApp():
    eel.init("Engine/Gui2/www")
    eel.start("view.html")


@eel.expose
def btn_ResimyoluClick():
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    # folder = filedialog.askdirectory()
    files = filedialog.askopenfiles()
    # ff = files
    ploter.read_hotflow_data(files)
    return [os.path.basename(file.name) for file in files]


@eel.expose
def earseData():
    ploter._real_data_full = []
    ploter.real_data = []



    # return  files
    # return folder


