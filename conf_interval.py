#!/usr/bin/python
import numpy as np
import scipy as sp
import scipy.stats
import sys
import os
import pandas as pd

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    print m, h
    return str(m) + " " + str(h)

# TODO: import data from files and output to final file; power means output to folders respectively

f=open("conf_interval_results", "a")
numlist = len(sys.argv) - 1
for i in np.arange(numlist):
    listpath = sys.argv[i + 1]
    if not os.path.isdir(listpath):
        dataArray = pd.read_csv(listpath, header=None)
        print >> f, listpath + " " + mean_confidence_interval(dataArray[0])
    else:
        path_precision = listpath + "/precision"
        print >> f, path_precision
        os.chdir(path_precision)
        resultsList = os.listdir(".")
        for result in resultsList:
            dataArray = pd.read_csv(result, header=None)
            print >> f, result + " " + mean_confidence_interval(dataArray[0])
        os.chdir("../recall")
        print >> f, "recall"
        resultsList = os.listdir(".")
        for result in resultsList:
            dataArray = pd.read_csv(result, header=None)
            print >> f, result + " " + mean_confidence_interval(dataArray[0])
        os.chdir("../../")
f.close()