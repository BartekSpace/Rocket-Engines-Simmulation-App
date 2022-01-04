import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import chain


class Ploter():
    def __init__(self, data):
        self._real_data = None
        self._sim_data = data
        # self._real_data_1 = None
        # self._real_data_2 = None

    # def read_hotflow_data(self, path1, path2=None):
    #     self._real_data_1 = pd.read_csv(path1, delimiter=',')
    #     if path2:
    #         self._real_data_2 = pd.read_csv(path2, delimiter=',')
    def read_hotflow_data(self, *paths):
        self._real_data = [pd.read_csv(path, delimiter=',').rename(columns=str.lower) for path in paths]

    def compare(self, name):
        # dfs = [df for df in self._real_data if name.replace('_',' ') in list(df.columns)]
        dfs = [df for df in self._real_data if name.replace('_', ' ') in ''.join(list(df.columns))]
        # real_names = [list(df.columns)[1] for df in dfs]
        # a =  [[df.iloc[:,0], df.iloc[:,1]] for df in dfs]
        # a = list(chain.from_iterable(a))
        #
        sim_names = [key for key in self._sim_data.keys() if name in key]
        #
        #
        # sim = [[self._sim_data['time'],self._sim_data[nm]] for nm in sim_names]
        # sim = list(chain.from_iterable(sim))
        # pl = sim + a
        # names = real_names + sim_names
        # plt.plot(*pl)

        fig, ax = plt.subplots()

        for df in dfs:
            ax.plot(df.iloc[:, 0], df.iloc[:, 1], label=list(df.columns)[1])

        for nm in sim_names:
            ax.plot(self._sim_data['time'], self._sim_data[nm], label=nm + " simulation")
        # ax.axis('equal')
        leg = ax.legend()
        # plt.show()
        plt.xticks(np.arange(0, max(self._sim_data['time']) + 1, 1.0))
        # plt.legend(sim, sim_names)
        # plt.legend(loc="upper left")
        # ax.autoscale()
        plt.grid()
        plt.show()

    # def compare(self, name=None):
    #     if name is None:
    #         dict_name = self._sim_data.keys()
    #         cols_name = [key.lower() for key in self._real_data_1.columns]
    #         name = next((x for x in dict_name if cols_name[1] in x), None)
    #         # name = list(set(cols_name) & set(dict_name))[0]
    #
    #     if "pressure" in name:
    #         dict_name = list(self._sim_data.keys())
    #         dict_name.remove(name)
    #         second = next((x for x in dict_name if "pressure" in x), None)
    #         if self._real_data_2 is not None:
    #             plt.plot(self._sim_data['time'], self._sim_data[name],
    #                      self._sim_data['time'], self._sim_data[second],
    #                      self._real_data_1.iloc[:, 0], self._real_data_1.iloc[:, 1],
    #                      self._real_data_2.iloc[:, 0], self._real_data_2.iloc[:, 1])
    #
    #         else:
    #             plt.plot(self._sim_data['time'], self._sim_data[name],
    #                      self._sim_data['time'], self._sim_data[second],
    #                      self._real_data_1.iloc[:, 0], self._real_data_1.iloc[:, 1])
    #
    #     else:
    #         plt.plot(self._sim_data['time'], self._sim_data[name], self._real_data_1.iloc[:, 0],
    #                  self._real_data_1.iloc[:, 1])
    #     plt.grid()
    #     plt.show()

    # def truncate(self):
    #     end = min(max(self._sim_data['time']), max(self._real_data_1.iloc[:, 0]))
    #     mf = self._real_data_1.iloc[:, 0] < end
    #     self._real_data_1 = self._real_data_1.where(mf, None)
    #     if self._real_data_2 is not None:
    #         mf = self._real_data_2.iloc[:, 0] < end
    #         self._real_data_2 = self._real_data_2.where(mf, None)

    def truncate(self):

        end = max(self._sim_data['time'])
        dfs = []
        for df in self._real_data:
            mf = df.iloc[:, 0] < end
            df = df.where(mf, None)
            dfs.append(df)
        self._real_data = dfs

        # mf = self._real_data_1.iloc[:, 0] < end
        # self._real_data_1 = self._real_data_1.where(mf, None)
        # if self._real_data_2 is not None:
        #     mf = self._real_data_2.iloc[:, 0] < end
        #     self._real_data_2 = self._real_data_2.where(mf, None)

    def plot_simulation(self, name):

        fig, ax = plt.subplots()
        if name == "pressure":
            dict_name = list(self._sim_data.keys())
            names = [x for x in dict_name if "pressure" in x]
            ax.plot(self._sim_data['time'], self._sim_data[names[0]], 'r', label=names[0])
            ax.plot(self._sim_data['time'], self._sim_data[names[1]], 'b', label=names[1])

        elif name == "flow":
            dict_name = list(self._sim_data.keys())
            names = [x for x in dict_name if "flow" in x]
            ax.plot(self._sim_data['time'], self._sim_data[names[0]], 'r', label=names[0])
            ax.plot(self._sim_data['time'], self._sim_data[names[1]], 'b', label=names[1])
        else:
            ax.plot(self._sim_data['time'], self._sim_data[name], label = name)
        ax.grid()
        ax.legend()
        plt.show()

    # with open(path) as f:
    #     reader = csv.DictReader(f)
    #     t = []
    #     val = []
    #     for row in reader:
    #         t.append(float(row['Timestamp']))
    #         val.append(float(row['Value']))
    #         if float(row['Timestamp']) > 14:
    #             break
    #         # print(row['Timestamp'], row['Value'])
    #     data['isp'] = [val * 0.80 for val in data['isp']]
    #
    #     # plt.plot(data['time'], data['thrust'], t, val)
    #     plt.plot(data['time'], data['isp'])  # , t, val)
    #     plt.show()
