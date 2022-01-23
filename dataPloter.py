import matplotlib
import numpy as np
np.seterr(all='ignore')
from sympy import pretty_print as pp, latex
from sympy.abc import a, b, n
import pandas as pd
import matplotlib.pyplot as plt
from itertools import chain
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 17}

axes = {
        'labelsize': 19,
        'titlesize': 35,
        'labelweight': 'bold'

         }

# title = {
#     'fontweight': 'bold'
# }
lines = {'linewidth' : 4}

matplotlib.rc('axes', **axes)
legend = {'loc': 'upper right',
          'fontsize': 15}
figsize = (22, 15)
figsize = [val / 2.54 for val in figsize]

# xlabel = {'fontsize': 15}

figure = {'figsize': figsize}
# matplotlib.rc('legend', loc = 'upper left')
# matplotlib.rc('title', **title)
matplotlib.rc('lines', **lines)
matplotlib.rc('legend', **legend)
matplotlib.rc('figure', **figure)
matplotlib.rc('font', **font)
# matplotlib.rc('xlabel',**xlabel )


def prepare_axis_name(name):
    if "pressure" in name:
        y = "Pressure [bar]"
    elif "flow" in name:
        y = "Mass Flow [kg/s]"
    elif "thrust" in name:
        y = "Thrust [N]"
    elif "isp" in name:
        y = "Isp [s]"
    elif "diam" in name:
        y = "Fuel Port Diameter [mm]"
    elif "of" in name:
        y = "Of"
    elif "gox" in name:
        y = r'$\frac{kg}{m^2*s}$'
        # y = "Gox [kg/(m^2*s)]"
    else:
        y = name

    return y


class Ploter():
    sim_plots = 0
    compare_plots = 0

    def __init__(self):
        self._real_data = []
        self._sim_data = None
        # self._img_names = set()
        self._real_data_full = []

    def read_hotflow_data(self, paths):
        self._real_data_full = [pd.read_csv(path, delimiter=',').rename(columns=str.lower) for path in paths]

    # @property
    # def img_names(self):
    #     return self._img_names

    @property
    def real_data(self):
        return self._real_data



    @real_data.setter
    def real_data(self, val):
        self._real_data = val

    @property
    def data(self):
        return self._sim_data

    @data.setter
    def data(self, data):
        self._sim_data = data

    def compare(self, name, path ='Engine/Gui/www/img/sim_plot' ):
        dfs = [df for df in self._real_data if name.replace('_', ' ') in ''.join(list(df.columns))]
        sim_names = [key for key in self._sim_data.keys() if name in key]
        fig, ax = plt.subplots()

        for df in dfs:
            ax.plot(df.iloc[:, 0], df.iloc[:, 1], label=list(df.columns)[1])

        for nm in sim_names:
            if "old" in nm:
                ax.plot(self._sim_data['time_old'], self._sim_data[nm], label=nm.replace('_', ' ') + " simulation")
            else:
                ax.plot(self._sim_data['time'], self._sim_data[nm], label=nm.replace('_', ' ') + " simulation")
        # ax.axis('equal')
        leg = ax.legend()
        # plt.show()
        plt.xticks(np.arange(0, max(self._sim_data['time']) + 1, 1.0))
        plt.xlabel("Time [s]", fontsize = 25)
        plt.ylabel(prepare_axis_name(name), fontsize =25)
        plt.title(name.replace('_', ' ').replace('old', '').title(), fontweight = 'bold')
        # plt.legend(sim, sim_names)
        # plt.legend(loc="upper left")
        # ax.autoscale()
        plt.grid()
        plt.tight_layout()
        plt.savefig(f"{path}_{name}.png")
        plt.close()
        # plt.show()

    def truncate(self):
        end = max(self._sim_data['time'])
        dfs = []
        for df in self._real_data_full:
            mf = df.iloc[:, 0] < end
            df = df.where(mf, None)
            dfs.append(df)

        self._real_data = dfs

    def truncate_sim(self, end):
        num_deleted = len(self._sim_data['time'])
        tmp = list(filter(lambda x: x < end, self._sim_data['time']))
        num_deleted -= len(tmp)
        self._sim_data = {key: val[:-num_deleted] for (key, val) in self._sim_data.items()}
        self._sim_data['time'] = tmp


    def plot_real(self, name, path = 'Engine/Gui/www/img/real_plot'):
        dfs = [df for df in self._real_data if name.replace('_', ' ') in ''.join(list(df.columns))]
        if len(dfs) == 0:
            return
        fig, ax = plt.subplots()

        for df in dfs:
            ax.plot(df.iloc[:, 0], df.iloc[:, 1], label=list(df.columns)[1])

        leg = ax.legend()
        # plt.show()
        plt.xticks(np.arange(0, max(self._sim_data['time']) + 1, 1.0))
        plt.xlabel("Time [s]", fontsize = 25)
        plt.ylabel(prepare_axis_name(name), fontsize = 25)
        # plt.legend(sim, sim_names)
        # plt.legend(loc="upper left")
        # ax.autoscale()
        plt.grid()
        plt.title(name.replace('_', ' ').title(), fontweight = 'bold')
        plt.tight_layout()
        plt.savefig(f"{path}_{name}.png")
        plt.close()
        # plt.show()

    def plot_simulation(self, name, path='Engine/Gui/www/img/sim_plot', end= None):
        sim_names = [key for key in self._sim_data.keys() if name in key]
        num = 1
        if end:
            num = len(self._sim_data['time'])
            tmp = list(filter(lambda x: x < end, self._sim_data['time']))
            num -= len(tmp)

        fig, ax = plt.subplots()
        if name == "pressure" or name == "flow":
            dict_name = list(self._sim_data.keys())
            names = [x for x in dict_name if name in x]
            for name in names:
                if "old" in name:
                    ax.plot(self._sim_data['time_old'][:-num], self._sim_data[name][:-num],
                            label=name.replace('_', ' ') + " simulation")
                else:
                    ax.plot(self._sim_data['time'][:-num], self._sim_data[name][:-num],
                        label=name.replace('_', ' ') + " simulation")

            # ax.plot(self._sim_data['time'][:-num], self._sim_data[names[1]][:-num], 'b', label=names[1].replace('_', ' ')+" simulation")
        #
        # elif name == "flow":
        #     dict_name = list(self._sim_data.keys())
        #     names = [x for x in dict_name if "flow" in x]
        #     ax.plot(self._sim_data['time'][:-num], self._sim_data[names[0]][:-num], 'r', label=names[0].replace('_', ' ')+" simulation")
        #     ax.plot(self._sim_data['time'][:-num], self._sim_data[names[1]][:-num], 'b', label=names[1].replace('_', ' ')+" simulation")
        else:
            for name in sim_names:
                if "old" in name:
                    ax.plot(self._sim_data['time_old'][:-num], self._sim_data[name][:-num],
                            label=name.replace('_', ' ') + " simulation")
                else:
                    ax.plot(self._sim_data['time'][:-num], self._sim_data[name][:-num], label=name.replace('_', ' ')+" simulation")
        ax.grid()
        ax.legend()
        plt.xlabel("Time [s]", fontsize = 25)
        plt.ylabel(prepare_axis_name(name), fontsize = 25)
        plt.title(name.replace('_', ' ').replace('old', '').title(), fontweight='bold')

        plt.tight_layout()
        plt.savefig(f"{path}_{name}.png")
        plt.close()

        # self._img_names.append(f"{path}_{self.sim_plots}.png")
        # self._img_names.add(f"{path}_{self.sim_plots}.png")
        # self.sim_plots += 1
