import re
import os
import math
import random
import time
import numpy as np
import pandas as pds
from numpy import mean, ptp, var, std, sqrt
from statsmodels.tsa.stattools import pacf, acf
from statsmodels.stats.diagnostic import lilliefors
from scipy import stats
import matplotlib.pyplot as pyplot
from Tools import *


runOneInvoc205 = "180114OneInvoc"
# runOneInvocNode21 = "180103Iter10kFromNode21"
runOneInvocNode21 = "180421SingleCombinedNode"
runMultiTierOne = "1804012TierOneMulti"
runMultiNode21 = "180110MultiInvocFromNode22"
DaCapoTmp = ["tradesoap"]
# DaCapoTmp = ["avrora", "batik", "fop", "h2", "jython", "luindex", "lusearch", "pmd", "sunflow", "tradebeans", "tradesoap", "xalan"]
startupNode21 = {"avrora": 25, "batik": 50, "fop": 129, "h2": 26, "jython": 125, "luindex": 76, "lusearch": 45, "pmd": 47, "sunflow": 19, "tradebeans": 59, "tradesoap": 29, "xalan": 38}


def NewreadMultiFromFileJXF(run, Invoc, benchmark, tail, stage, num=10):
    #dacapo time
    times = []
    filepath = DATA_PREC+run+"/"+benchmark+"_default_NewPar"
    for i in range(Invoc):
        filepathi = filepath + str(i)
        with open(filepathi, 'r') as f:
            lines = f.readlines()
            iterCount = 0
            invocData = []
            for line in lines:
                items = line.split()
                if len(items) <= 7:
                    continue
                #format like: ===== DaCapo 9.12 avrora PASSED in 74031 msec =====
                #or ===== DaCapo 9.12 tradesoap completed warmup 23 in 2981 msec =====
                if items[3] == benchmark:
                    if items[4] == "PASSED" and items[6].isdigit():
                    #inorder to calculate the means of 10 runs in each invocation
                        # invocData.append(int(items[6]))
                        # print len(invocData)
                        # times.append(mean(invocData))
                        invocData.append(int(items[6]))
                        iterCount = 0
                    if items[4] == "completed" and items[5] == "warmup" and items[8].isdigit():
                        if stage == "steady":
                            if iterCount >= num:
                                invocData.append(int(items[8]))
                                # times.append(int(items[8]))
                            else:
                                iterCount += 1
                        else:
                            times.append(int(items[8]))
            times.append(invocData)
    # print "data size: ", len(times)
    return times


def readMultiFromPureData(run, Invoc, benchmark, tail, stage, num=10):
    times = []
    # filepath = DATA_PREC+run+"/"+benchmark+"_TimeLog510"
    filepath = DATA_PREC+run+"/"+benchmark+"_"+tail
    for i in range(Invoc):
        filepathi = filepath+str(i+1)
        oneInv = []
        with open(filepathi, 'r') as f:
            lines = f.readlines()
            for line in lines:
                oneInv.append(int(line))
        if len(oneInv) != 0:
            times.append(oneInv)
    return times


## This function print data to CompareData so that R script can process it
def CLTSpeedup():
    # #2 CLT speedup node21multi vs 205multi
    spdAvg = 0
    for app in DaCapoTmp:
        for size in sizes:
            #data returned from these two functions are two dimension vector
            dataMultiNode22 = []
            if app == "tradesoap":
                dataMultiNode22 = readMultiFromFileJXF(runMultiNode21, 199, app, "default_", "steady", 0)
            else:
                dataMultiNode22 = readMultiFromPureData(runMultiNode21, 400, app, "invoc", "steady", 0)
            dataMultiTierOne = NewreadMultiFromFileJXF(runMultiTierOne, 200, app, "tail", "steady", 0)
            #last10
            sampleNode22 = []
            sample205 = []
            for d in dataMultiNode22:
                sampleNode22.append(mean(d[-10:]))
            for d in dataMultiTierOne:
                sample205.append(mean(d[-10:]))
            spd1 = CLTest(sample205, sampleNode22)
            spdAvg += spd1
            #last20-10
            i = -40
            sampleNode22 = []
            sample205 = []
            for d in dataMultiNode22:
                sampleNode22.append(mean(d[i:i+10]))
            for d in dataMultiTierOne:
                sample205.append(mean(d[-10:]))
            spd2 = CLTest(sample205, sampleNode22)
            print app, spd1, spd2
    spdAvg = spdAvg*1.0/len(DaCapoTmp)
    print spdAvg


def SBBSpeedup():
    #SBB test && sensitive (multipos multi invocation)
    print "Benchmark", "Origin", "Iteration", "Invocation"
    for app in DaCapoTmp:
        for size in sizes:
            #multi position
            # dataMultiNode22 = readMultiFromPureData(runOneInvocNode21, 400, app, "invoc", "steady", 0)
            # dataMulti205 = readMultiFromFileJXF(runMulti205, 200, app, "tail", "steady", 0)
            # dataSingle205 = readTimeFromOneFileJXF(runOneInvoc205, app, "", "steady", 0)
            dataTierOne = NewreadMultiFromFileJXF(runMultiTierOne, 200, app, "tail", "steady", 0)
            dataSingleTierOne = dataTierOne[0]
            tail = "all"+str(1)
            dataSingleNode21 = readTimeFromPureData(runOneInvocNode21, app, tail, "steady", 0)
            ratio = 0.8
            sample1 = dataSingleTierOne[-40:]
            sample2 = dataSingleNode21[startupNode21[app]:startupNode21[app]+40]
            find = True
            while find:
                for i in range(40):
                    sample2[i] = dataSingleNode21[startupNode21[app]+i]*ratio
                pvalue = SBBTest(sample1, sample2, app, ratio)
                if pvalue < 0.95:
                    find = False
                else:
                    ratio += 0.01
                # print pvalue, ratio
            ratioOrigin = ratio

            sample2 = dataSingleNode21[startupNode21[app]+40:startupNode21[app]+80]
            find = True
            ratio = ratio - 1
            while find:
                for i in range(40):
                    sample2[i] = dataSingleNode21[startupNode21[app]+40+i]*ratio
                pvalue = SBBTest(sample1, sample2, app, ratio)
                if pvalue < 0.95:
                    find = False
                else:
                    ratio += 0.01
                # print pvalue, ratio
            ratioIter = ratio

            # tail = "all"+str(2)
            # dataSingleNode21 = readTimeFromPureData(runOneInvocNode21, app, tail, "steady", 0)
            # sample2 = dataSingleNode21[startupNode21[app]:startupNode21[app]+40]
            # find = True
            # ratio = ratio - 1
            # while find:
            #     for i in range(40):
            #         sample2[i] = dataSingleNode21[startupNode21[app]+i]*ratio
            #     pvalue = SBBTest(sample1, sample2, app, ratio)
            #     if pvalue < 0.95:
            #         find = False
            #     else:
            #         ratio += 0.01
            #     # print pvalue, ratio
            ratioInvoc = ratio
            print app, ratioOrigin, ratioIter, ratioInvoc, mean(sample1)/mean(sample2)
            #last10


def SBBTest(data1, data2, app, ratio):
    t_obs = mean(data1) - mean(data2)
    data = data1+data2
    SampleTime = 5000
    length = len(data1)
    # print length
    means = []
    # probability p
    p = math.log(length, 2)
    p = math.log(p, 2)
    p = 1.0/p*100
    tcount = 0
    for i in range(SampleTime):
        BlockSample = []
        samplelen = 1
        start = np.random.randint(length*10)
        start = start/10
        BlockSample.append(data1[start])
        current = start
        while samplelen < length:
            prob = np.random.randint(100)
            if prob < p:
                current = np.random.randint(length*10)
                current = current/10
            else:
                current = (current+1) % length
            BlockSample.append(data1[current])
            samplelen += 1
        # print BlockSample
        # print mean(BlockSample)
        x1 = mean(BlockSample)

        BlockSample = []
        samplelen = 1
        start = np.random.randint(length*10)
        start = start/10
        BlockSample.append(data2[start])
        current = start
        while samplelen < length:
            prob = np.random.randint(100)
            if prob < p:
                current = np.random.randint(length*10)
                current = current/10
            else:
                current = (current+1) % length
            BlockSample.append(data2[current])
            samplelen += 1
        # print BlockSample
        # print mean(BlockSample)
        x2 = mean(BlockSample)
        t1 = x1-x2
        if t1 > 0:
            tcount += 1
    pvalue = tcount*1.0/SampleTime
    return pvalue


def CLTest(data1, data2):
    z = 1.96
    mean1 = mean(data1)
    down1 = mean1 - z * std(data1)/sqrt(len(data1))
    up1 = mean1 + z * std(data1)/sqrt(len(data1))
    mean2 = mean(data2)
    down2 = mean2 - z * std(data2)/sqrt(len(data2))
    up2 = mean2 + z * std(data2)/sqrt(len(data2))
    spd = down1 / up2
    return spd


CLTSpeedup()
SBBSpeedup()
