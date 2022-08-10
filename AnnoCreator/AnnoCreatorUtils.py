import os
import sys

def _printProgress(i,
                  n,
                  process,
                  fileType):

    if i == 0:
        print("\n" + process + " " + fileType + ":")
    sys.stdout.write('\r{} of {} '.format(i, n) + " " + process + ": " + '{:2.2%} completed'.format((i / n)))
    sys.stdout.flush()
    if i + 1 == n:
        print("\n" + process + " " + "finished!")

def _collectNestedData(self,
                       path,
                       searchTypes=None):
    dataPaths, dirs, dataTypes = [], [], []

    for file in os.listdir(path):
        if os.path.isdir(os.path.join(path, file)):
            dirs.append(os.path.join(path, file))
        else:
            dataPaths.append(os.path.join(path, file))
            if not file.split(".")[-1] in dataTypes:
                dataTypes.append(file.split(".")[-1])
    for dir in dirs:
        newDataPaths, newDataTypes = self._collectNestedData(dir)
        dataPaths += newDataPaths
        dataTypes += newDataTypes
    return dataPaths, dataTypes

def _statusPrinter(start,
                   process):
    if start:
        print("Start: {} ...".format(process))
    else:
        print("End: {} ...".format(process))



