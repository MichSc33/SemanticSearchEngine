import os
import sys
import json
import pandas as pd
import numpy as np
import math
from PIL import Image
from PIL import Image, UnidentifiedImageError
from rembg.bg import remove
import numpy as np
import io
from PIL import Image, ImageFile

def _cropAlpha(imgArr):
    return

def _removeBackground(imgArr):
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    result = remove(imgArr)
    return Image.open(io.BytesIO(result)).convert("RGBA")

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
                if file[0:2] != "._":
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
        print("Start: {}...".format(process))
    else:
        print("End: {}...".format(process))


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
def _checkMappings(mappings):
    with open("missings.csv", "w") as f:
        for key, val in mappings.items():
            if len(val) == 0:
                f.write(key + "\n")
        f.close()

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
            annos.loc[annos['Image File Name'] == key, "Img Path"] = "|".join(val)
            i += 1
        _statusPrinter(False,
                       "Map Path to Annos")
        annos.to_csv("annos.txt")
    else:
       print("Annos already created!")
       annos = pd.read_csv("annos.txt", sep=",annos")
       digits = len(str(len(annos)))
       annos["0"] = [str(i).zfill(digits) for i in range(len(annos))]
       print("Annos loaded!")
    return annos













