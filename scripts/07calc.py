import re
import os
import numpy as np

ROOT = "/home/sch/result/startup/"
DI = "/home/sch/"
APPS = ["batik", "jython", "luindex", "lusearch", "pmd",
        "avrora", "tradebeans", "xalan", "sunflow", "fop", "h2", "tradesoap"]
#APPS=["batik"]
WARMUP = 10

def readfile(filepath):
    '''
        read file
    '''
    alist = []
    inf = open(filepath, "r")
    warmup = 0
    for line in inf.readlines():
        slices = line.split(" ")
        tag = len(slices) - 2
        if (tag > 0) and (slices[tag] == "msec"):
            if warmup == 0:
                alist.append(int(slices[tag - 1]))
            else:
                warmup -= 1
    return np.array(alist)

def calc(arr0):
    '''
    calc cov
    '''
    return float(np.std(arr0) / np.mean(arr0))

def run(arr0):
    '''
    calc steady
    '''
    last = 0
    for i in range(len(arr0) - 10):
#	print arr1
#	print calc(arr1)
        ret = calc(arr0[i:i+10])
       # print arr0[i:i+5]
#	print ret
        # if (abs(ret-last) < 0.02):
        if (ret < 0.06):
            return str(i+1)
        else: 
	        last = ret
    return str(0)

def draw(arr0):
    ret = ""
    for i in range(0, 651):
        ret += str(calc(arr0[i : i + 5])) + " "
    return ret


def main():
    '''
        the main func
    '''
    if not os.path.exists(DI):
        os.makedirs(DI)
    outfile = open(DI + "covdraw", "w")
    for app in APPS:
        print app
        nms = readfile(ROOT + app + "_TimeLog1")
#        if app == "jython":
#            nms = nms[20:]
        outfile.write(app + " " + run(nms) + "\n")
#	outfile.write(app + " " + draw(nms) + "\n")
#	outfile.write(app + " ")
#	for i in range(len(nms)):
#	    outfile.write(str(nms[i]) + " ")
#	outfile.write("\n")

main()
