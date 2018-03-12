#!/usr/bin/env python
import matplotlib as mpl
import matplotlib.pyplot as plt
import signal
import roslib
import numpy as np
from os import path
import sys
import types

def popList(_list):
    if not isinstance(_list, types.ListType):
        raise TypeError('You must pass list')
    if not _list: # Empty
        return ""
    return _list.pop()

class dataProcess:
    def __init__(self):
        pass

    @staticmethod
    def transpose(_data):
        return _data.transpose()

    @staticmethod
    # time, vx, vy, vz, -y, x, z
    def diff3dTime(_data):
        visual_path = _data[:, 1:4]
        ref_path = np.array([_data[:, 5], -_data[:, 4], _data[:, 6]]).transpose()
        return np.array([_data[:, 0], np.linalg.norm(visual_path - ref_path, axis=1)])

class matplotter:
    def __init__(self, _filename=None, _data=None):
        if _filename is not None:
            self.data = np.loadtxt(_filename)
        else:
            self.data = _data

        # Matplotlib settings
        plt.rcParams['font.size'] = 10
        mpl.rcParams['axes.labelsize'] = 10
        mpl.rcParams['xtick.labelsize'] = 10
        mpl.rcParams['ytick.labelsize'] = 10
        mpl.rcParams['legend.fontsize'] = 10
        mpl.rcParams['text.usetex'] = False
        mpl.rcParams['svg.fonttype'] = 'none'
        plt.rcParams['font.family'] = 'Times New Roman'

    def plot(self, func=lambda x: x, _index=[[0, 1]], filename="image", scatter=False, _width=90.8, _height=40,
             horisontal=[], vertical=[], title="", xlabel="Time [s]", ylabel=[""], legend=[""], legend_loc="best",
             xlim=[None, None], ylim=[None, None], xticks=[], xticks_str=[], yticks=[], yticks_str=[]):
        # if len(_index) < 2 or len(_index) > 3: # This condition is for multiple ylabel
        #     raise IndexError('index length must be 2 or 3')

        width = _width / 25.4     # mm -> inch
        height = _height / 25.4   # mm -> inch
        plt.figure(figsize=(width, height))
        legend = legend[::-1]
        color_list = ["#9400D3", "#009E73", "#56B4E9", "#E69F00"][::-1] # gnuplot5 default

        data = func(self.data)

        # For multiple ylabel
        # for i in range(1, len(index)): # [0, 1, 2] => [1, 2]
        #     if isinstance(index[i], types.ListType):
        #         for j in range(len(index[i])):
        #             plt.plot(data[:, index[0]], data[:, index[i][j]], label=popList(legend), color=popList(color_list))
        #     else if len(index) == 2:
        #         plt.plot(data[:, index[0]], data[:, index[i]], label=popList(legend), color=popList(color_list))
        #     else:
        #         # TODO: Multiple ylabel plot
        #         pass

        if(scatter):
            for i in range(len(_index)):
                plt.scatter(data[_index[i][0]], data[_index[i][1]], s=10, label=popList(legend), color=popList(color_list))
        else:
            for i in range(len(_index)):
                plt.plot(data[_index[i][0]], data[_index[i][1]], linewidth=2, label=popList(legend), color=popList(color_list))

        if horisontal:
            for _y in horisontal:
                plt.axhline(y = _y, linewidth=2, label=popList(legend), color=popList(color_list))
        if vertical:
            for _x in vertical:
                plt.axvline(x = _x, linewidth=2, label=popList(legend), color=popList(color_list))
        plt.title(title)
        plt.xlabel(xlabel, fontsize=10)
        plt.ylabel(ylabel[0], fontsize=10)
        plt.legend(loc=legend_loc, scatterpoints=1)# .get_frame().set_alpha(0.0)

        plt.xlim(xlim[0], xlim[1])
        plt.ylim(ylim[0], ylim[1])
        if isinstance(xticks, types.ListType) and xticks:
            if isinstance(xticks_str, types.ListType) and xticks_str:
                plt.xticks(xticks, xticks_str)
            else:
                plt.xticks(xticks)
        if isinstance(yticks, types.ListType) and yticks:
            if isinstance(yticks_str, types.ListType) and yticks_str:
                print(yticks_str)
                plt.yticks(yticks, yticks_str)
            else:
                plt.yticks(yticks)

        plt.grid()
        plt.savefig(filename + '.svg', bbox_inches='tight')

    def plot_show(self):
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        plt.show(block=False)

if __name__ == '__main__':
    filename = sys.argv[1]
    plotter = matplotter(filename)
    plotter.plot(func=dataProcess.diff3dTime)
    plotter.plot_show()
