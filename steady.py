'''
    this is use for collect the compiler task during each run
'''
import numpy as np
from scipy import optimize as opt
import math

IN = "/home/sch/pkg/data/result/startup/"
OUT = "/public/sch/"
APPS = ["batik", "jython", "luindex", "lusearch", "pmd", "avrora", "tradebeans","xalan", "sunflow", "fop", "h2", "tradesoap"]
#APPS = ["fop", "batik"]
INPOSTFIXS = ["_TimeLog1"]
#INPOSTFIXS=["_default_Serial", "_default_Par", "_default_NewPar", "_default_CMS"]
OUTPOSTFIX = "criticalv4"
INTERVAL = 11

def func(x, A, B):
    #return A * (B**x) + C
    return A*x+B

def curvefit(sample):
    x1 = []
    for i in range(len(sample)):
        x1.append(i)
    return opt.curve_fit(func, x1, sample)[0]

def homogeneity(times):

    interval1 = times[: INTERVAL]
    interval2 = times[INTERVAL: 2*INTERVAL]
    interval3 = times[2*INTERVAL: 3*INTERVAL]
    size = INTERVAL
    k = 3
    # coefficient of variation cv = std/mean
    cv = [np.std(interval1) / np.mean(interval1), np.std(interval2) / np.mean(interval2), np.std(interval3) / np.mean(interval3)]
    print(cv)
    #pooled CV, calculated by sum((n-1)*cv))/(n*k-k)
    pcv = 0
    #cvk = sum((n-1)*cv^2)
    cvk = 0
    for i in range(k):
        pcv += (size - 1) * cv[i]
        cvk += (size - 1) * cv[i]**2
    pcv = pcv / (k*size - k)
    #x2=(cvk-(nk-k)*pcv^2)/((pcv^2)(pcv^2+0.5))
    x2 = (cvk - (k*size - k) * pcv**2)/(pcv**2 * (pcv**2 + 0.5))
    #or ((cv[0] < 0.01) a:nd (cv[1] < 0.01) and (cv[2] < 0.01))
    if (x2 < 5.99) or ((cv[0] < 0.01) and (cv[1] < 0.01) and (cv[2] < 0.01)):
        return True
    return False

def compiler(ctasks):

# compiler test
    cts1 = ctasks[: INTERVAL]
    cts1.remove(max(cts1))
    cts2 = ctasks[INTERVAL: 2*INTERVAL]
    cts2.remove(max(cts2))
    cts3 = ctasks[2*INTERVAL: 3*INTERVAL]
    cts3.remove(max(cts3))
    fitsamples = cts1 + cts2 + cts3 
    A, B = curvefit(fitsamples)
    print (A, B)
    if (abs(A) <0.1) and (abs(B) < 5):
        return True
    return False

def count(fin, fout, app):
    '''
        calc steady 
    '''
    ctask = 0
    rindex = 0
    times = []
    ctasks = []
    isrun = False

# read files
    for line in fin.readlines():
        if (line.find(" msec ") > 0):
                #fout.write( " " + str(compcount))
            slices = line.split(" ")
            times.append(int(slices[slices.index("msec") - 1]))
            rindex += 1
            ctasks.append(ctask)
           # fout.write(str(times[-1]) + " ")
            ctask = 0
            isrun = not isrun
        if line.find(" starting "):
            isrun = not isrun
        if (line.find("::") > 0) and (isrun):
            ctask += 1

#test print ctasks and times
    ftest = open("/public/sch/" + app + "_info", "w")
    for i in range(0, len(times)):
        ftest.write(str(times[i]) + " " + str(ctasks[i]) + "\n")
        
# calc steady
#    for i in range(0, len(times) - 33):
#        if homogeneity(times[i:i+3*INTERVAL]) and compiler(ctasks[i:i+3*INTERVAL]):
#            print (i)
#            fout.write(str(i))
#            return


def main():
    '''
        the main function
    '''
    fout = open(OUT + OUTPOSTFIX, "w")
    for inpostfix in INPOSTFIXS:
        for app in APPS:
            fin = open(IN + app + inpostfix, "r")
            fout.write(app + inpostfix + " ")
            print(app)
            count(fin, fout, app)
            fout.write("\n")
        fout.write("\n")


main()
