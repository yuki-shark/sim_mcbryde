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

def createPlotData(angles, means):
    means_nonzero = means.nonzero()
    return np.array([np.array(angles)[means_nonzero].astype(np.int), means[means_nonzero]])

if __name__ == '__main__':
    args = parse()

    filedirs = args["<cam_dir>"]
    filedirs = [os.path.abspath(_dir) for _dir in filedirs]
    filelists = [glob.glob(os.path.join(_dir, "*.path")) for _dir in filedirs]
    anglelists = [[name[name.find("shake") + len("shake"):].rsplit("_")[0] for name in flist] for flist in filelists]
    mean_data = [np.array([angleMean(isValidData(np.loadtxt(fname))) for fname in flist]) for flist in filelists]

    data_list = [createPlotData(anglelists[i], mean_data[i]) for i in range(len(mean_data))]
    # data = [data_array for data_array in data_2darray for data_2darray in data_list]
    data = [data_list[i][j] for i in range(len(data_list)) for j in range(len(data_list[i]))]

    plotter = matplotter(_data=data)

    horisontal = []
    if args["--one"] is not None:
        one_file = glob.glob(os.path.join(args["--one"], "*.path"))[0]
        one_mean = angleMean(isValidData(np.loadtxt(one_file)))
        if one_mean is not False:
            horisontal = [one_mean]
    plotter.plot(_index=[[0, 1], [2, 3]], scatter=True, legend=["Two", "Three", "one"], horisontal=horisontal)
    plotter.plot_show()
