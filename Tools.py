import re
import os
import random
from numpy import mean, ptp, var, std, sqrt
import matplotlib.pyplot as pyplot


DaCapo09 = ["avrora", "batik", "fop", "h2", "lusearch", "luindex", "pmd", "jython", "sunflow", "tradebeans", "tradesoap", "xalan"]
#for different iteration nums
DaCapo50 = ["luindex", "lusearch", "xalan", "avrora"]
DaCapo100 = ["jython", "pmd", "sunflow"]
#, "tradebeans", "tradesoap" still running

# DaCapo09 = ["xalan"]
sizes = ["default"]
DATA_PREC = "/home/jxf/data/data/"

runNode22 = "1112MultiInvoc"
run207 = "1016SCH"


def CV(d):
    # Calculate CV
    m = mean(d)
    s = std(d)
    cv = s/m
    return cv


def readTimeFromFileJXF(run, benchmark, size, stage, iteration, num=10):
    #dacapo time
    times = []
    filepath = DATA_PREC+run+"/"+benchmark+"_"+size+"_"+iteration
    with open(filepath, 'r') as f:
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
                    invocData.append(int(items[6]))
                    # print len(invocData)
                    # times.append(mean(invocData))
                    # times.append(int(items[6]))
                    invocData = []
                    iterCount = 0
                if items[4] == "completed" and items[5] == "warmup" and items[8].isdigit():
                    if stage == "steady":
                        if iterCount >= num:
                            invocData.append(int(items[8]))
                            times.append(int(items[8]))
                        else:
                            iterCount += 1
                    else:
                        times.append(int(items[8]))
    print "data size: ", len(times)
    return times


def readTimeFromOneFileJXF(run, benchmark, tail, stage, num=10):
    #dacapo time
    times = []
    filepath = DATA_PREC+run+"/"+benchmark+"_default"+tail
    with open(filepath, 'r') as f:
        lines = f.readlines()
        iterCount = 0
        for line in lines:
            items = line.split()
            if len(items) <= 7:
                continue
            #format like: ===== DaCapo 9.12 avrora PASSED in 74031 msec =====
            #or ===== DaCapo 9.12 tradesoap completed warmup 23 in 2981 msec =====
            if items[3] == benchmark:
                if items[4] == "PASSED" and items[6].isdigit():
                    times.append(int(items[6]))
                    iterCount = 0
                if items[4] == "completed" and items[5] == "warmup" and items[8].isdigit():
                    if stage == "steady":
                        if iterCount >= num:
                            times.append(int(items[8]))
                        else:
                            iterCount += 1
                    else:
                        times.append(int(items[8]))
    return times


def readTimeFromGC(run, benchmark, tail, stage, num=10):
    #dacapo time
    tenure = []
    gctime = []
    heap = []
    filepath = DATA_PREC+run+"/"+benchmark+"_default"+tail
    with open(filepath, 'r') as f:
        lines = f.readlines()
        for line in lines:
            items = line.split()
            if len(items) <= 7:
                continue
            #format like: ===== DaCapo 9.12 avrora PASSED in 74031 msec =====
            #or ===== DaCapo 9.12 tradesoap completed warmup 23 in 2981 msec =====
            if items[0] == "[Full":
                if items[3] == "[PSYoungGen:":
                    #1020K->32056K(1373568K)
                    tmp = items[7].split("(")
                    tmp = tmp[0].split(">")
                    tmp = tmp[1].split("K")
                    tenure.append(tmp[0])
                    gctime.append(float(items[10]))
                else:
                    #1020K->32056K(1373568K)
                    tmp = items[4].split("(")
                    tmp = tmp[0].split(">")
                    tmp = tmp[1].split("K")
                    tenure.append(tmp[0])
                    gctime.append(float(items[5]))
                    #177966K->32056K(1991744K)
    return tenure, gctime


def readCTaskAndTime(run, benchmark, tail, stage, num=10):
    #dacapo time
    time = []
    ctask = []
    filepath = DATA_PREC+run+"/"+benchmark+"_info"
    with open(filepath, 'r') as f:
        lines = f.readlines()
        for line in lines:
            items = line.split()
            time.append(int(items[0]))
            ctask.append(int(items[1]))
    return time, ctask


def readGCNum(run, benchmark, tail, stage, num=10):
    #dacapo time
    tenure = []
    gctime = []
    heap = []
    filepath = DATA_PREC+run+"/"+benchmark+"_default"+tail
    with open(filepath, 'r') as f:
        lines = f.readlines()
        localGCCount = 0
        for line in lines:
            items = line.split()
            if len(items) <= 7:
                continue
            #format like: ===== DaCapo 9.12 avrora PASSED in 74031 msec =====
            #or ===== DaCapo 9.12 tradesoap completed warmup 23 in 2981 msec =====
            if items[0] == "[GC":
                localGCCount = localGCCount+1
            if items[4] == "PASSED" or items[4] == "completed":
                gctime.append(localGCCount)
                localGCCount = 0
    return gctime


def readMultiFromFileJXF(run, Invoc, benchmark, tail, stage, num=10):
    #dacapo time
    times = []
    filepath = DATA_PREC+run+"/"+benchmark+"_default"
    for i in range(Invoc):
        filepathi = filepath + "_" + str(i+1)
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


def readTimeFromSPECFileJXF(run, benchmark, stage, num=10):
    #dacapo time
    times = []
    filepath = DATA_PREC+run+"/"+benchmark+"_"+stage
    with open(filepath, 'r') as f:
        lines = f.readlines()
        iterCount = 0
        for line in lines:
            items = line.split()
            if len(items) <= 1:
                continue
            #format like:compiler.compiler iteration 1  null   17304   48.00   166.44
            if items[0] == benchmark and items[1] == "iteration":
                if iterCount >= num:
                    times.append(int(items[4]))
                iterCount = iterCount+1
            if iterCount == 30:
                iterCount = 0
    return times


def readTimeFromFileSCH(run, benchmark, stage, num=10):
    #dacapo time
    times = []
    for i in range(1, 501):
        filepath = DATA_PREC+run+"/"+benchmark+"/TimeLog"+str(i)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                lines = f.readlines()
                iterCount = 0
                for line in lines:
                    items = line.split()
                    if len(items) <= 7:
                        continue
                    #format like: ===== DaCapo 9.12 avrora PASSED in 74031 msec =====
                    #or ===== DaCapo 9.12 tradesoap completed warmup 23 in 2981 msec =====
                    if items[3] == benchmark:
                        # if items[4] == "PASSED" and items[6].isdigit():
                        #     times.append(int(items[6]))
                        #     iterCount = 0
                        if items[4] == "completed" and items[5] == "warmup" and items[8].isdigit():
                            if stage == "steady":
                                if iterCount == num:
                                    times.append(int(items[8]))
                                    iterCount += 1
                                else:
                                    iterCount += 1
                            else:
                                times.append(int(items[8]))
    return times


def readTimeFromOneFileSCH(run, benchmark, stage, num=10):
    #dacapo time
    times = []
    # filepath = DATA_PREC+run+"/"+benchmark+"_TimeLog510"
    filepath = DATA_PREC+run+"/"+benchmark+"_TimeLog"
    with open(filepath, 'r') as f:
        lines = f.readlines()
        iterCount = 0
        for line in lines:
            items = line.split()
            if len(items) <= 7:
                continue
            #format like: ===== DaCapo 9.12 avrora PASSED in 74031 msec =====
            #or ===== DaCapo 9.12 tradesoap completed warmup 23 in 2981 msec =====
            if items[3] == benchmark:
                if items[4] == "PASSED" and items[6].isdigit():
                    times.append(int(items[6]))
                    iterCount = 0
                if items[4] == "completed" and items[5] == "warmup" and items[8].isdigit():
                    if stage == "steady":
                        if iterCount >= num:
                            times.append(int(items[8]))
                        else:
                            iterCount += 1
                    else:
                        times.append(int(items[8]))
    print len(times)
    return times


def readTimeFromPureData(run, benchmark, tail, stage, num=10):
    #dacapo time
    times = []
    # filepath = DATA_PREC+run+"/"+benchmark+"_TimeLog510"
    filepath = DATA_PREC+run+"/"+benchmark+"_"+tail
    with open(filepath, 'r') as f:
        lines = f.readlines()
        for line in lines:
            times.append(int(line))
    # print len(times)
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


def readTimeWithHPCFromOneFile(run, benchmark, tail, stage, num=10):
    #dacapo time
    times = []
    hpc = []
    filepath = DATA_PREC+run+"/"+benchmark+"_default"+tail
    with open(filepath, 'r') as f:
        lines = f.readlines()
        iterCount = 0
        dataCount = 0
        i = 0
        while i < len(lines):
            line = lines[i]
            i += 1
            items = line.split()
            if len(items) == 0:
                continue
            if items[0] == "HPC_output":
                dataCount += 1
                metrics = []
                for events in range(16):
                    line = lines[i]
                    i += 1
                    metrics.append(int(line))
                hpc.append(metrics)
                continue
            if len(items) <= 7:
                continue
            #format like: ===== DaCapo 9.12 avrora PASSED in 74031 msec =====
            #or ===== DaCapo 9.12 tradesoap completed warmup 23 in 2981 msec =====
            if items[3] == benchmark:
                if items[4] == "PASSED" and items[6].isdigit():
                    times.append(int(items[6]))
                    iterCount = 0
                if items[4] == "completed" and items[5] == "warmup" and items[8].isdigit():
                    if stage == "steady":
                        if iterCount >= num:
                            times.append(int(items[8]))
                        else:
                            iterCount += 1
                    else:
                        times.append(int(items[8]))
    return times, hpc, dataCount


def calculateCI(sample):
    means = mean(sample)
    # print means, var, i
    z = 1.96
    v = z * std(sample)/sqrt(len(sample))
    down = means - v
    up = means + v
    return down, up



# for app in DaCapo50:
#     for size in sizes:
#         data = readTimeFromFileJXF(runNode22, app, size, "steady", "50", 49)
#         print app
#         # for i in range(5, 51):
#         #     z = 1.96
#         #     sample = data[0:(i+1)]
#         #     means = mean(sample)
#         #     # print means, var, i
#         #     var = z * std(sample)/sqrt(len(sample))
#         #     down = means - var
#         #     up = means + var
#         #     if up/(means*1.0) < 1.01:
#         #         print i
#         #         break
#         for sample_size in [10, 30, 50, 70, 100, 120, 150, 200, 250]:
#             onesample = []
#             for i in range(500):
#                 onesample.append(mean(random.sample(data, sample_size)))
#             pyplot.hist(onesample, bins=50)
#             pyplot.xlabel('Time(ms)')
#             pyplot.ylabel('Frequency')
#             benchmark = app.replace('.', '_')
#             name = benchmark+" "+str(sample_size)
#             print "Title: ", name
#             pyplot.title(name)
#             filepath = DATA_PREC+runNode22+"/figure/"+benchmark+"_"+str(sample_size)
#             # pyplot.show()
#             pyplot.savefig(filepath)
#             pyplot.close()

# for app in DaCapo09:
    # for size in sizes:
        # printDistribution(run, app, size, "startup")
    # data1 = readTimeFromOneFileJXF(runNode22, app, "_1", "steady", 200)
    # data2 = readTimeFromOneFileJXF(runNode22, app, "_2", "steady", 200)
    # data2 = readTimeFromOneFileSCH(run207, app, "steady", 1000)
    # data3 = readTimeFromFileSCH(run207, app, "steady", 21)

    # data2 = data2[301:401]
    # mean2 = mean(data2)
    # mean3 = mean(data3)
    # z = 1.96
    # down2 = mean2 - z * std(data2)/sqrt(len(data2))
    # up2 = mean2 + z * std(data2)/sqrt(len(data2))
    # down3 = mean3 - z * std(data3)/sqrt(len(data3))
    # up3 = mean3 + z * std(data3)/sqrt(len(data3))
    # print mean2, down2, up2
    # print mean3, down3, up3

    # print app
    # print max(data1), max(data2)
    # print min(data1), min(data2)
    # print max(data1)*1.0/min(data1), max(data2)*1.0/min(data2)
    # output = DATA_PREC+"CompareData/1109_"+app
    # with open(output, 'w') as f:
    #     f.write("run1\t")
    #     for i in data1:
    #         f.write(str(i)+"\t")
    #     f.write("\n")
    #     f.write("run2\t")
    #     for i in data2:
    #         f.write(str(i)+"\t")
    #     f.write("\n")
