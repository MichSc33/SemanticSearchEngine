import pandas as pd
from sklearn.model_selection import train_test_split
import os

class AnnoCreator:
    def __init__(self,
                 textAnnoPath=None,
                 jLinePath=None,
                 trainTestSplit=None,
                 projectName=None):
        self.PROJECT_NAME = projectName
        self.TEXT_ANNO_PATH = textAnnoPath
        self.TRAIN_TEST_SPLIT = trainTestSplit
        self.J_LINE_PATH = jLinePath
        assert len(self.TRAIN_TEST_SPLIT) == 2, "Train/Val/Test should be three values"
        assert (self.TRAIN_TEST_SPLIT[0] + self.TRAIN_TEST_SPLIT[1]) == 1, "Shares do not some up to 1"

    def createDatasets(self):
        annos = self._loadAnnoTxt()
        train, test = train_test_split(annos,
                                       train_size=self.TRAIN_TEST_SPLIT[0],
                                       test_size=self.TRAIN_TEST_SPLIT[1])
        a = 0


    def _loadAnnoTxt(self):
        annosRaw = pd.read_csv(self.TEXT_ANNO_PATH, header=0)
        return pd.concat([annosRaw["Image File Name"], annosRaw["Decoration"]], axis=1)

    def _writeAnnos2jLine(self,
                          file,
                          splitTag):
        return 0

    def createJLinePath(self,
                        splitTag):
        return os.path.curdir + os.path.sep +
