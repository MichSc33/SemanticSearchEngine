from AnnoCreater import AnnoCreator

ac = AnnoCreator(textAnnoPath="/home/michaelschlee/ownCloud/Projekt Semantik Search Engine/List_description_clear.csv",
                 jLinePath=None,
                 trainTestSplit=[0.8, 0.2])
ac.createDatasets()