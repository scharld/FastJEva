import matplotlib
matplotlib.use('Agg') 

from matplotlib import pyplot as plt
import scipy
import numpy
import sys
import os

APPS = ["avrora", "batik", "pmd", "fop", "jython", "luindex",
        "lusearch", "h2", "xalan", "sunflow", "tradesoap", "tradebeans"]

autis = "_Thres1w"
def readf(path):
    alist = []
    inf = open(path, "r")
    for line in inf.readlines():
        slices = line.split(" ")
        tag = len(slices) - 2
        if (tag > 0) and (slices[tag] == "msec"):
            alist.append(slices[tag - 1])
    return alist

def plots(series, atitle):

    plt.title(atitle)
    plt.plot(series)
    plt.savefig("/home/sch/figures/" + atitle + ".jpg")
    plt.close()

def main():
    inpath = "/home/sch/result/configs"
    for app in APPS:
        if not os.path.exists(inpath + "/" + app + autis + "1"):
            continue
        print (app)
        i = 1
        while os.path.exists(inpath + "/" + app + autis + str(i)):
            atitle = app + autis + str(i)
            series = readf(inpath + "/" + app + autis + str(i))[5:]
            plots(series, atitle)
            i += 1

main()