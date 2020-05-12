'''
    this is use for collect the compiler task during each run
'''
import numpy as np

IN = "/home/sch/result/startup/"
OUT = "/home/sch/result/startup/"
APPS = ["fop","luindex","batik", "jython", "lusearch", "pmd", "avrora", "xalan", "sunflow", "tradebeans", "tradesoap", "h2"]
#APPS = ["fop"]
INPOSTFIX = "_TimeLog1"
OUTPOSTFIX = "criticals"
INTERVAL = 6

def fitting(arr0):
    '''
        calc the down trend
    '''
    x = np.arange(1, INTERVAL, 1)
    z1 = np.polyfit(x, arr0, 1)
    return z1[0]


def steady(rindex, ctasks, times):
    '''
        check steady
    '''
    threshold = 15
    stead = times[rindex: rindex + 3 * INTERVAL]
    inter = INTERVAL
    covi = np.std(stead) / np.mean(stead)
    cov1 = np.std(times[2: rindex]) / np.mean(times[2: rindex])
    print(covi, cov1)
    if ((covi < cov1 * 0.6) or (covi > cov1)) and ((covi > 0.05) or (cov1 > 0.05)):
        threshold = 5
        inter = inter * 2
    tarr3 = ctasks[rindex + 2 * inter: rindex + 3 * inter]
    tarr2 = ctasks[rindex + inter: rindex + 2 * inter]
    tarr1 = ctasks[rindex: rindex + inter]
    tarr3.remove(max(tarr3))
    tarr2.remove(max(tarr2))
    tarr1.remove(max(tarr1))
    print(tarr1, tarr2, tarr3)
    if (max(tarr1) > threshold) or (max(tarr2) > threshold) or (max(tarr3) > threshold):
        return False
   # tarr3 = times[rindex - 3 * inter: rindex - 2 * inter]
   # tarr2 = times[rindex - 2 * inter: rindex - inter]
   # tarr1 = times[rindex - inter: rindex]
   # tarr3.remove(max(tarr3))
   # tarr2.remove(max(tarr2))
   # tarr1.remove(max(tarr1))
   # print(fitting(tarr3), fitting(tarr2), fitting(tarr1))
   # if (abs(fitting(tarr3)) > 0.5)  or (abs(fitting(tarr2)) > 0.5) or (abs(fitting(tarr1)) > 0.5):
   #     return Fals
    return True


def count(fin, fout):
    '''
        calc steady 
    '''
    ctask = 0
    rindex = 0
    times = []
    ctasks = []
    isrun = False

    for line in fin.readlines():
#	print (line)
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
    #fout.write(str(np.std(times[1:]) / np.mean(times[1:])))
    for i in range(5, 200):
        if steady(i, ctasks, times):
            print (i)
            fout.write(str(i))
            return


def main():
    '''
        the main function
    '''
    fout = open(OUT + OUTPOSTFIX, "w")
    for app in APPS:
        fin = open(IN + app + INPOSTFIX, "r")
        fout.write(app + " ")
        print(app)
        count(fin, fout)
        fout.write("\n")


main()
