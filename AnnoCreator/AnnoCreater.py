import jsonlines
import pandas as pd
from sklearn.model_selection import train_test_split
import os
from os.path import sep
from PIL import Image, UnidentifiedImageError

#utils

from AnnoCreatorUtils import _collectNestedData, \
                             _statusPrinter, \
                             _printProgress, \
                             _writeMappings2TXT, \
                             _loadMappingsFromTXT, \
                             _getDictKeys, \
                             _matchPaths2Annos, \
                             _checkMappings

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
        self.IMG_CONVERSION_EXCPS = set()
        assert len(self.TRAIN_TEST_SPLIT) == 2, "Train/Val/Test should be three values"
        assert (self.TRAIN_TEST_SPLIT[0] + self.TRAIN_TEST_SPLIT[1]) == 1, "Shares do not some up to 1"

    def createDataset(self):
        self._createDirs()
        annos = self._loadAnnoTxt()
        dataPaths, dataTypes = _collectNestedData(self.IMG_DIR)
        mappings = self._getImgPaths(annos["Image File Name"],
                                     dataPaths)

        _checkMappings(mappings)

        annos = _matchPaths2Annos(annos,
                                  mappings)

        self._convertImgs(annos)

        train, test = train_test_split(annos,
                                       train_size=self.TRAIN_TEST_SPLIT[0],
                                       test_size=self.TRAIN_TEST_SPLIT[1])
        self._createJsonLine(train,
                             "train")

        self._createJsonLine(test,
                             "test")

    def _removeBackground(self,
                          imgArr):
        import matplotlib
        from rembg.bg import remove
        import numpy as np
        import io
        from PIL import Image

            ImageFile.LOAD_TRUNCATED_IMAGES = True

            f = np.fromfile(input_path)
            result = remove(f)
            img = Image.open(io.BytesIO(result)).convert("RGBA")
            img.save(output_path)

        # Press the green button in the gutter to run the script.
        if __name__ == '__main__':
            print_hi('PyCharm')

        # See PyCharm help at https://www.jetbrains.com/help/pycharm/

    def _createJsonLine(self,
                        annos,
                        name):
        with jsonlines.open(name + ".jsonl", "w") as fw:
            items = [{"filename": idx + "." + self.OUTPUT_FORMAT,
                      "captions": [anno["Decoration"]]} for idx, anno in annos.iterrows()]
            fw.write_all(items)
            fw.close()

    def _createDirs(self):
        if not os.path.exists(self.PROJECT_NAME):
            os.mkdir(self.PROJECT_NAME)

    def _getImgDir(self):
        return "./" + self.PROJECT_NAME

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


        return mapping


    def _convertImg(self,
                    anno,
                    f):
        try:
            img = Image.open(anno[1]["Img Path"].split("|")[0]).convert("RGB")
            self._getImgName(anno)
            img.save(self._getImgPath(anno))
        except AttributeError as ae:
            f.write(ae.args[0] + ":" + anno[1]["Image File Name"] + "\n")
        except IndexError as idxe:
            f.write(idxe.args[0] + ":" + anno[1]["Image File Name"] + "\n")
        except Exception as e:
            f.write(e.args[0] + ":" + anno[1]["Image File Name"] + "\n")




    def _getImgPath(self,
                    anno):
        return os.path.join(self.PROJECT_NAME,
                            self._getImgName(anno))
    def _getImgName(self,
                    anno):
        return anno[1]["0"] + "." + self.OUTPUT_FORMAT

    def _convertImgs(self,
                     annos):
        i, n = 0, len(annos)
        _statusPrinter(True,
                       "Convert Imgs")
        with open("failures.txt", "w") as f:
            for anno in annos.iterrows():
                _printProgress(i,
                               n,
                               "Convert",
                               "Imgs")
                self._convertImg(anno,
                                 f)
                i += 1
            _statusPrinter(False,
                           "Convert Imgs")
            f.close()
