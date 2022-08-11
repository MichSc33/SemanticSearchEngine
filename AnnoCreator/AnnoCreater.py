import pandas as pd
from sklearn.model_selection import train_test_split
import os
from os.path import sep

#utils

from AnnoCreatorUtils import _collectNestedData, \
                             _statusPrinter, \
                             _printProgress, \
                             _writeMappings2TXT, \
                             _loadMappingsFromTXT, \
                             _getDictKeys, \
                             _matchPaths2Annos

class AnnoCreator:
    def __init__(self,
                 imgDir=None,
                 textAnnoPath=None,
                 jLinePath=None,
                 trainTestSplit=None,
                 projectName=None,
                 outputFormat="jpeg"):

        self.OUTPUT_FORMAT = outputFormat
        self.IMG_DIR = imgDir
        self.PROJECT_NAME = projectName
        self.TEXT_ANNO_PATH = textAnnoPath
        self.TRAIN_TEST_SPLIT = trainTestSplit
        self.J_LINE_PATH = jLinePath
        assert len(self.TRAIN_TEST_SPLIT) == 2, "Train/Val/Test should be three values"
        assert (self.TRAIN_TEST_SPLIT[0] + self.TRAIN_TEST_SPLIT[1]) == 1, "Shares do not some up to 1"

    def createDataset(self):
        self._createDirs()
        annos = self._loadAnnoTxt()
        dataPaths, dataTypes = _collectNestedData(self.IMG_DIR)

        mappings = self._getImgPaths(annos["Image File Name"],
                                     dataPaths)

        annos = _matchPaths2Annos(annos,
                                  mappings)



        train, test = train_test_split(annos,
                                       train_size=self.TRAIN_TEST_SPLIT[0],
                                       test_size=self.TRAIN_TEST_SPLIT[1])


    def _processAnnos(self,
                      annos,
                      purpose):
        with open('output.jsonl', 'w') as outfile:
            for row in annos.rows():
                a = 0

    def _createDirs(self):
        if not os.path.exists(self.PROJECT_NAME):
            os.mkdir(self.PROJECT_NAME)

    def _getImgDir(self):
        return "./" + self.PROJECT_NAME

    def _writeAnnos2JsonLine(self,
                             annos):
        return 0

    def _convertImgs(self,
                     annos):
        return 0

    def _loadAnnoTxt(self):
        annosRaw = pd.read_csv(self.TEXT_ANNO_PATH,
                               header=0)
        digits = len(str(annosRaw.__len__()))
        annos = pd.concat([pd.Series([str(i).zfill(digits) for i in range(annosRaw.__len__())]),
                          annosRaw["Serial Number Painting"],
                          annosRaw["Image File Name"],
                          annosRaw["Decoration"]],
                          axis=1)
        annos.index = annosRaw["Serial Number Painting"]
        return annos

    def _writeAnnos2jLine(self,
                          file,
                          splitTag):
        return 0

    def getJLinePath(self,
                     purpose):
        return os.path.curdir + sep + "data" + sep

    def _getImgPaths(self,
                     imgNames,
                     imgPaths):


        if not os.path.exists("mappings.txt"):
            mapping = {}
            n, i = len(imgNames), 0
            _statusPrinter(True,
                           "Mapping from ids to img Paths")
            for imgName in imgNames:
                _printProgress(i,
                               n,
                               "IDs mapped to images",
                               "Images")

                mapping[imgName] = [imgPath for imgPath in imgPaths if imgName in imgPath]
                i += 1

            _statusPrinter(False,
                           "Mapping from ids to img Paths")

            _writeMappings2TXT(mapping)

        else:
            print("Mapping already created!")

            mapping = _loadMappingsFromTXT()

            print("Mapping loaded!")

        return _getDictKeys(mapping,
                            0)

