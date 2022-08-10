import pandas as pd
from sklearn.model_selection import train_test_split
import os


#utils

from AnnoCreatorUtils import _collectNestedData, \
                             _statusPrinter, \
                             _printProgress

class AnnoCreator:
    def __init__(self,
                 imgDir=None,
                 textAnnoPath=None,
                 jLinePath=None,
                 trainTestSplit=None,
                 projectName=None):

        self.IMG_DIR = imgDir
        self.PROJECT_NAME = projectName
        self.TEXT_ANNO_PATH = textAnnoPath
        self.TRAIN_TEST_SPLIT = trainTestSplit
        self.J_LINE_PATH = jLinePath
        assert len(self.TRAIN_TEST_SPLIT) == 2, "Train/Val/Test should be three values"
        assert (self.TRAIN_TEST_SPLIT[0] + self.TRAIN_TEST_SPLIT[1]) == 1, "Shares do not some up to 1"

    def createDataset(self):
        annos = self._loadAnnoTxt()
        dataPaths, dataTypes = _collectNestedData(self.IMG_DIR)

        mappings = self._getImgPaths(annos["Image File Name"],
                                     dataPaths)

        annos["Img Path"] = mappings.values()

        train, test = train_test_split(annos,
                                       train_size=self.TRAIN_TEST_SPLIT[0],
                                       test_size=self.TRAIN_TEST_SPLIT[1])


    def _processAnnos(self,
                      annos):
        return 0

    def _writeAnnos2JsonLine(self,
                             annos):
        return 0

    def _convertImgs(self,
                     annos):


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

    def createJLinePath(self,
                        splitTag):
        return os.path.curdir + os.path.sep + "0"

    def _getImgPaths(self,
                     ids,
                     imgPaths):
        mapping = {}
        n, i = len(imgPaths), 0

        _statusPrinter(True,
                       "Mapping from ids to img Paths")

        for id in ids:
            _printProgress(i,
                           n,
                           "IDs mapped to images",
                           "Images")
            mapping[id] = []
            mapping[id].append([match for match in imgPaths if id in match])
            i += 1

        _statusPrinter(False,
                       "Mapping from ids to img Paths")

        return mapping
