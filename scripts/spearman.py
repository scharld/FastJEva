import re
import os
import numpy as np
import random
from scipy.stats import rankdata as rank 

#ROOT = "/public/sch/javav/data/1112MultiInvoc/"
ROOT = "/home/sch/time10000/"
DI = "/home/sch/result/spearman/"
APPS = ["batik", "jython", "luindex", "lusearch", "pmd",
         "avrora", "tradebeans", "xalan", "sunflow", "fop", "h2","tradesoap"]
#APPS=["jython", "xalan", "h2", "fop"]

def readInovc(app):
    alist = []
    inf = open(ROOT + app + "_default", "r")
    #fout = open(ROOT + app + "_invoc", "w")
    last = 0
    for line in inf.readlines():
        slices = line.split(" ")
        tag = len(slices) - 2
        if (len(slices) == 1):
            alist.append(last)
        if (tag > 0) and (slices[tag] == "msec"):
            last = int(slices[tag - 1])
    return np.array(alist)

def readRandom(app):
    alist = []
    inf = open(ROOT + app+"_TimeLog", "r")
    for line in inf.readlines():
        slices = line.split(" ")
        tag = len(slices) - 2
        if (tag > 0) and (slices[tag] == "msec"):
            alist.append(int(slices[tag - 1]))
    alist  = alist[200:]
    random.shuffle(alist)
    return np.array(alist)


def readf(app):
    alist = []
    inf = open(ROOT + app+"_TimeLog", "r")
    fout = open(ROOT + app + "_value", "w")
    for line in inf.readlines():
        slices = line.split(" ")
        tag = len(slices) - 2
        if (tag > 0) and (slices[tag] == "msec"):
            alist.append(int(slices[tag - 1]))
            if len(alist) > 200:
                fout.write(slices[tag - 1] + "\n")
    return np.array(alist[200:])

def spearman(series, lag):
    '''
        autocorrection
    '''
    seriesx = rank(series[:len(series) - lag], method="dense")
    seriesy = rank(series[lag:], method="dense")
    rxy = 0
    stdx = np.std(seriesx)
    stdy = np.std(seriesy)
    covxy = np.mean(list(map(lambda x: x[0]*x[1], zip(seriesx, seriesy)))) - np.mean(seriesx)* np.mean(seriesy)
    rxy = covxy / (stdx * stdy)
    #print (seriesx, seriesy)

    return rxy

def main():
    '''
        main process
    '''
    if not os.path.exists(DI):
        os.makedirs(DI)
    outfile = open(DI + "spearman_resut", "w")
    for app in APPS:
    #for app in "batik":
        outfile.write(app)
        print (app)
        series = readf(app)
        for lag in range(1, 31):
            rst = spearman(series, lag)
            outfile.write(" " + str(rst))
            print ("%.10f " %(rst))
        #print("\n")
        outfile.write("\n")
    return

main()
