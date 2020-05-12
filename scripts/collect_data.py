'''

Using for collect run time for invocations and iterations

'''
import sys
import os

APPS = ["avrora", "batik", "pmd", "fop", "jython", "luindex",
        "lusearch", "h2", "xalan", "sunflow", "tradesoap", "tradebeans"]


def readf(path):
    alist = []
    inf = open(path, "r")
    for line in inf.readlines():
        slices = line.split(" ")
        tag = len(slices) - 2
        if (tag > 0) and (slices[tag] == "msec"):
            alist.append(slices[tag - 1])
    return alist


def collect_inter(args): 
    inpath = "./"
    outpath = "./"
    if args:
        inpath = args[0]
    if len(args) > 1:
        outpath = args[1]
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    for app in APPS:
        if not os.path.exists(inpath + "/" + app + "_TimeLog1"):
            continue
        print (app)
        i = 1
        while os.path.exists(inpath + "/" + app + "_TimeLog" + str(i)):
            series = readf(inpath + "/" + app + "_TimeLog" + str(i))
            fout = open(outpath + "/" + app + "_invoc" + str(i), 'w')
            for time in series:
                fout.write(time + "\n")
            i += 1


def collect_invoc(args):
    inpath = "./"
    outpath = "./"
    if args:
        inpath = args[0]
    if len(args) > 1:
        outpath = args[1]
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    for app in APPS:
        if not os.path.exists(inpath + "/" + app + "_TimeLog1"):
            continue
        fout = open(outpath + "/" + app + "_multiinvoc", 'w')
        print (app)
        i = 1
        while os.path.exists(inpath + "/" + app + "_TimeLog" + str(i)):
            series = readf(inpath + "/" + app + "_TimeLog" + str(i))
            for time in series:
                fout.write(time + " ")
            fout.write("\n")
            i += 1

def none(args):
    print("Error!")

SWITHCER = {
    'invoc': collect_invoc,
    'inter': collect_inter
}

def main(kind, args):
    func = SWITHCER.get(kind, none)
    return func(args)

main(sys.argv[1], sys.argv[2:])
