#!/usr/bin/env python
__doc__ = """{f}

Usage:
  {f} [--one=<one_cam_dir>] -f <cam_dir>...
  {f} -h | --help

Options:
  --one=<one_cam_dir>          Directory path of one camera data
  -h --help                    Show this screen and exit.
""".format(f=__file__)

from docopt import docopt
import numpy as np
import copy
import os
import glob
import sys
from matplotter import matplotter
from matplotter import dataProcess

def parse():
    args = docopt(__doc__, options_first=True)
    return args

def angleMean(_data):
    if _data is False:
        return False
    mean = np.mean(dataProcess.diff3dTime(_data)[1])
    return mean

def isValidData(_data):
    """Check if rtabmap got failure"""
    data_x = _data[:, 1]
    if data_x.size - np.count_nonzero(data_x) > 10: # If rtabmap gets failure, visual odoms set zero
        return False
    return _data

def createPlotData(angles, means, limit=None):
    means_nonzero = means.nonzero() # Remove invalid data
    if limit is not None:
        means = np.clip(means, None, limit)
    return np.array([np.array(angles)[means_nonzero].astype(np.int), means[means_nonzero]])

if __name__ == '__main__':
    args = parse()
    ylimit = 6

    filedirs = args["<cam_dir>"]
    filedirs = [os.path.abspath(_dir) for _dir in filedirs]
    filelists = [glob.glob(os.path.join(_dir, "*.path")) for _dir in filedirs]
    anglelists = [[name[name.find("shake") + len("shake"):].rsplit("_")[0] for name in flist] for flist in filelists]
    raw_datalists = [[np.loadtxt(fname) for fname in flist ] for flist in filelists]
    mean_data = [np.array([angleMean(isValidData(raw_data)) for raw_data in rdlist]) for rdlist in raw_datalists]

    data_list = [createPlotData(anglelists[i], mean_data[i], limit=ylimit) for i in range(len(mean_data))]
    # data = [data_array for data_array in data_2darray for data_2darray in data_list]
    data = [data_list[i][j] for i in range(len(data_list)) for j in range(len(data_list[i]))]

    # Plot mean data
    mean_plotter = matplotter(_data=data)
    horisontal = []
    if args["--one"] is not None:
        one_file = glob.glob(os.path.join(args["--one"], "*.path"))[0]
        one_data = np.loadtxt(one_file)
        one_mean = angleMean(isValidData(one_data))
        # For path plot #
        filelists.append([one_file])
        raw_datalists.append([one_data])
        #################
        if one_mean is not False:
            horisontal = [one_mean]

    yticks = np.arange(0, ylimit + 0.001, ylimit/6.0).tolist()
    yticks_str = copy.deepcopy(yticks)
    yticks_str[-1] = ">=" + str(yticks_str[-1])
    mean_plotter.plot(_index=[[0, 1], [2, 3]], scatter=True, ylabel=["Error mean [m]"],
                      legend=["Two", "Three", "one"], legend_loc="best", horisontal=horisontal,
                      xlim=[-5, 95], ylim=[0, ylimit + ylimit / 10.0],
                      xticks=np.arange(0, 91, 15).tolist(), yticks=yticks, yticks_str=yticks_str)

    mean_plotter.plot_show()

    print("Start path plot")
    for i in range(len(filelists)):
        for j in range(len(filelists[i])):
            path_plotter = matplotter(_data=raw_datalists[i][j] * np.array([1, 1, -1, 1, 1, 1, 1])) # Right is +y
            path_plotter.plot(_index=[[2, 1]], func=dataProcess.transpose, filename=os.path.splitext(filelists[i][j])[0],
                              xlabel="Y [m]", ylabel=["X [m]"], legend=["tmp"])

    raw_input("Press Enter to exit") # Python 2
