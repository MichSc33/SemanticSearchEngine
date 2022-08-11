from AnnoCreater import AnnoCreator

ac = AnnoCreator(imgDir="/media/michaelschlee/5fda827c-18ca-4f1d-8a7e-2bfff9daa623/Epoisen",
                 textAnnoPath="/home/michaelschlee/ownCloud/Projekt Semantik Search Engine/List_description_clear.csv",
                 projectName="GreekVases",
                 jLinePath=None,
                 trainTestSplit=[0.8, 0.2])
ac.createDataset()