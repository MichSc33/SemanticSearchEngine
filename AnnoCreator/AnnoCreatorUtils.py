import os
import sys
import json
import pandas as pd
from PIL import Image

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

def _collectNestedData(path,
                       searchTypes=None):
    dataPaths, dirs, dataTypes = [], [], set()

    for file in os.listdir(path):
        if os.path.isdir(os.path.join(path, file)):
            dirs.append(os.path.join(path, file))
        else:
            if file.split(".")[-1] in ["tif", "jpg", "tiff", "jpeg", "JPG", "png", "TIF"]:
                dataPaths.append(os.path.join(path, file))
                if not file.split(".")[-1] in dataTypes:
                    dataTypes.add(file.split(".")[-1])
    for dir in dirs:
        newDataPaths, newDataTypes = _collectNestedData(dir)
        dataPaths += newDataPaths
        dataTypes = dataTypes.union(newDataTypes)
    return dataPaths, dataTypes

def _statusPrinter(start,
                   process):
    if start:
        print("Start: {} ...".format(process))
    else:
        print("End: {} ...".format(process))


def _loadMappingsFromTXT():
    return json.load(open("mappings.txt"))

def _writeMappings2TXT(dct):
    with open('mappings.txt', 'w') as f:
        f.write(json.dumps(dct))

def _getDictKeys(dct,
                id):
    newDct = {}

    for key, val in dct.items():
        try:
            newDct[key] = val[id]
        except IndexError as idxe:
            newDct[key] = None
    return newDct

def _matchPaths2Annos(annos,
                     mappings):
    if not os.path.exists("annos.txt"):
        annos["Img Path"] = None
        i, n = 0, len(mappings)
        _statusPrinter(True,
                       "Map Path to Annos")
        for key, val in mappings.items():
            _printProgress(i,
                           n,
                           "Path to Annos",
                           "Path")
            annos.loc[annos['Image File Name'] == key, "Img Path"] = val
            i += 1
        _statusPrinter(False,
                       "Map Path to Annos")
        annos.to_csv("annos.txt")
    else:
       print("Annos already created!")
       annos = pd.read_csv("annos.txt", sep=",")
       print("Annos loaded!")
    return annos

def _convertImg(imgPath):
    try:
        Image.open(imgPath)

def _convertImgs(annos):
    for anno in annos.iterrows():






