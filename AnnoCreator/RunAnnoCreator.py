from AnnoCreater import AnnoCreator

ac = AnnoCreator(imgDir="/media/michaelschlee/1694342894340D2D",
                 textAnnoPath="/home/michaelschlee/ownCloud/Projekt Semantik Search Engine/List_description_clear.csv",
                 projectName="GreekVases",
                 jLinePath=None,
                 trainTestSplit=[0.8, 0.2])
ac.createDataset()