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
runMulti205 = "180109MultiInvoc"
runMultiNode21 = "180110MultiInvocFromNode22"
DaCapoTmp = ["jython"]
# DaCapoTmp = ["avrora", "batik", "fop", "h2", "jython", "luindex", "lusearch", "pmd", "sunflow", "tradebeans", "tradesoap", "xalan"]
startupNode21 = {"avrora": 25, "batik": 50, "fop": 129, "h2": 26, "jython": 125, "luindex": 76, "lusearch": 45, "pmd": 47, "sunflow": 19, "tradebeans": 59, "tradesoap": 29, "xalan": 38}


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


def CLTSpeedup():
    ##2 CLT speedup node21multi vs 205multi
    spdAvg = 0
    for app in DaCapoTmp:
        for size in sizes:
            #data returned from these two functions are two dimension vector
            # dataMultiNode22 = readMultiFromPureData(runMultiNode21, 400, app, "invoc", "steady", 0)
            ## special for tradesoap
            dataMultiNode22 = []
            if app == "tradesoap":
                dataMultiNode22 = readMultiFromFileJXF(runMultiNode21, 199, app, "default_", "steady", 0)
            dataMulti205 = readMultiFromFileJXF(runMulti205, 200, app, "tail", "steady", 0)
            #last10
            sampleNode22 = []
            sample205 = []
            for d in range(-50, -1):
                sampleNode22.append(mean(dataMultiNode22[d][-10:]))
            for d in dataMulti205:
                sample205.append(mean(d[-10:]))
            ## CLT test
            spd1 = CLTest(sample205, sampleNode22)
            spdAvg += spd1
            ## Different position
            ## last20-10
            i = -40
            sampleNode22 = []
            sample205 = []
            for d in dataMultiNode22:
                sampleNode22.append(mean(d[i:i+10]))
            for d in dataMulti205:
                sample205.append(mean(d[-10:]))
            ## CLT Test
            spd2 = CLTest(sample205, sampleNode22)
            print app, spd1, spd2
    spdAvg = spdAvg*1.0/12
    print spdAvg


def HypothesisTest(dataSingleNode21, sample1, sample2, app, ratio, size):
    find = True
    while find:
        for i in range(size):
            sample2[i] = dataSingleNode21[startupNode21[app]+i]*ratio
        pvalue = SBBTest(sample1, sample2, app, ratio)
        if pvalue < 0.95:
            find = False
        else:
            ratio += 0.01
    return ratio


def SBBSpeedup():
    #SBB test && sensitive (multipos multi invocation)
    print "Benchmark", "Origin", "Iteration", "Invocation"
    for app in DaCapoTmp:
        for size in sizes:
            #multi position
            # dataMultiNode22 = readMultiFromPureData(runOneInvocNode21, 400, app, "invoc", "steady", 0)
            # dataMulti205 = readMultiFromFileJXF(runMulti205, 200, app, "tail", "steady", 0)
            dataSingle205 = readTimeFromOneFileJXF(runOneInvoc205, app, "", "steady", 0)
            tail = "all"+str(1)
            dataSingleNode21 = readTimeFromPureData(runOneInvocNode21, app, tail, "steady", 0)
            ## ratio is the start value for testing, can be changed for each app to accelerate the process
            ratio = 2
            if app == "avrora":
                ratio = 11
            if app == "tradebeans":
                ratio = 1
            if app == "xalan":
                ratio = 7
            # sample1 = dataSingle205[-40:]
            # sample2 = dataSingleNode21[startupNode21[app]:startupNode21[app]+40]
            #                 # print pvalue, ratio
            # ratioOrigin = HypothesisTest(dataSingleNode21, sample1, sample2, app, ratio)

            # sample2 = dataSingleNode21[startupNode21[app]+40:startupNode21[app]+80]
            # ratio = ratio - 1
            # ratioIter = HypothesisTest(dataSingleNode21, sample1, sample2, app, ratio)

            # tail = "all"+str(2)
            # dataSingleNode21 = readTimeFromPureData(runOneInvocNode21, app, tail, "steady", 0)
            # sample2 = dataSingleNode21[startupNode21[app]:startupNode21[app]+40]
            # ratio = ratio - 1
            # ratioInvoc = HypothesisTest(dataSingleNode21, sample1, sample2, app, ratio)
            # print app, ratioOrigin, ratioIter, ratioInvoc, mean(sample1)/mean(sample2)

            ## Test difference size of samples
            # sample1 = dataSingle205[-30:]
            sample1 = dataSingle205[startupNode21[app]:startupNode21[app]+30]
            sample2 = dataSingleNode21[startupNode21[app]:startupNode21[app]+30]
            ratio30 = HypothesisTest(dataSingleNode21, sample1, sample2, app, ratio, 30)

            # sample1 = dataSingle205[-50:]
            sample1 = dataSingle205[startupNode21[app]:startupNode21[app]+50]
            sample2 = dataSingleNode21[startupNode21[app]:startupNode21[app]+50]
            ratio = ratio30 - 0.5
            ratio50 = HypothesisTest(dataSingleNode21, sample1, sample2, app, ratio, 50)
            #sample1 = dataSingle205[-100:]
            sample1 = dataSingle205[startupNode21[app]:startupNode21[app]+100]
            sample2 = dataSingleNode21[startupNode21[app]:startupNode21[app]+100]
            ratio = ratio50 - 0.5
            ratio100 = HypothesisTest(dataSingleNode21, sample1, sample2, app, ratio, 100)
            print app, ratio30, ratio50, ratio100, mean(sample1)/mean(sample2)

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


##Speedup in CLT
CLTSpeedup()
##Speedup in SBB
SBBSpeedup()
