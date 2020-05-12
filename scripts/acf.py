import re
import os
import numpy as np
import random

#ROOT = "/public/sch/javav/data/1112MultiInvoc/"
ROOT = "/home/sch/result/multitest/dropcache/"
DI = "/home/sch/result/multitest/"
APPS = ["batik", "jython", "luindex", "lusearch", "pmd",
         "avrora", "tradebeans", "xalan", "sunflow", "fop", "h2","tradesoap"]
#APPS=[ "xalan", "fop"]

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


def readf(app, i):
    alist = []
    inf = open(ROOT + app+"_TimeLog" + str(i), "r")
    fout = open(ROOT + app + "_value" + str(i), "w")
    for line in inf.readlines():
        slices = line.split(" ")
        tag = len(slices) - 2
        if (tag > 0) and (slices[tag] == "msec"):
            alist.append(int(slices[tag - 1]))
            if len(alist) > 200:
                fout.write(slices[tag - 1] + "\n")
    return np.array(alist[200:])

def acf(series, lag):
    '''
        autocorrection
    '''
    tmean = np.mean(series)
    tvar = np.var(series)
    xat = []
    for i in range(lag, len(series)):
        xat.append((series[i - lag] - tmean)*(series[i] - tmean))
    #print(xat, xah)
    nat = np.array(xat)
    #print(tmean, str(np.mean(nat)), str(np.mean(nah)), tvar)
    rst = float(np.mean(nat) / tvar)
    return rst

def main():
    '''
        main process
    '''
    if not os.path.exists(DI):
        os.makedirs(DI)
    for i in range(1,4):
        outfile = open(DI + "acf_drop" + str(i), "w")
        for app in APPS:
            print (app)
            if not os.path.exists(ROOT + app + "_TimeLog" + str(i)):
                continue
            outfile.write(app)
            series = readf(app, i)
            for lag in range(1, 100):
                rst = acf(series, lag)
                outfile.write(" " + str(rst))
            outfile.write("\n")
    return

main()
