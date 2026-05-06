# %% NEW FILE TOAssetType BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 153 "model.ump"
# line 281 "model.ump"

class TOAssetType():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #TOAssetType Attributes
    #Helper Variables
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aName, aExpectedLifeSpan):
        self._canSetImageURL = None
        self._imageURL = None
        self._expectedLifeSpan = None
        self._name = None
        self._name = aName
        self._expectedLifeSpan = aExpectedLifeSpan
        self._canSetImageURL = True

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template attribute_SetImmutable 
    def setImageURL(self, aImageURL):
        wasSet = False
        if not self._canSetImageURL :
            return False
        self._canSetImageURL = False
        self._imageURL = aImageURL
        wasSet = True
        return wasSet

    def getName(self):
        return self._name

    def getExpectedLifeSpan(self):
        return self._expectedLifeSpan

    def getImageURL(self):
        return self._imageURL

    def delete(self):
        pass

    def __str__(self):
        return str(super().__str__()) + "[" + "name" + ":" + str(self.getName()) + "," + "expectedLifeSpan" + ":" + str(self.getExpectedLifeSpan()) + "," + "imageURL" + ":" + str(self.getImageURL()) + "]"
