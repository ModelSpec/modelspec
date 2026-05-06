# %% NEW FILE AssetType BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 77 "model.ump"
# line 246 "model.ump"
import os
from datetime import date
class AssetType():
    assettypesByName = dict()
    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #AssetType Attributes
    #AssetType Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aName, aExpectedLifeSpan, aAssetPlus):
        self._specificAssets = None
        self._assetPlus = None
        self._image = None
        self._expectedLifeSpan = None
        self._name = None
        self._expectedLifeSpan = aExpectedLifeSpan
        self._image = None
        if not self.setName(aName) :
            raise RuntimeError ("Cannot create due to duplicate name. See https://manual.umple.org?RE003ViolationofUniqueness.html")
        didAddAssetPlus = self.setAssetPlus(aAssetPlus)
        if not didAddAssetPlus :
            raise RuntimeError ("Unable to create assetType due to assetPlus. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._specificAssets = []

    #------------------------
    # INTERFACE
    #------------------------
    def setName(self, aName):
        wasSet = False
        anOldName = self.getName()
        if not (anOldName is None) and anOldName == aName :
            return True
        if AssetType.hasWithName(aName) :
            return wasSet
        self._name = aName
        wasSet = True
        if not (anOldName is None) :
            AssetType.assettypesByName.pop(anOldName, None)
        AssetType.assettypesByName[aName] = self
        return wasSet

    def setExpectedLifeSpan(self, aExpectedLifeSpan):
        wasSet = False
        self._expectedLifeSpan = aExpectedLifeSpan
        wasSet = True
        return wasSet

    def setImage(self, aImage):
        wasSet = False
        self._image = aImage
        wasSet = True
        return wasSet

    def getName(self):
        return self._name

    # Code from template attribute_GetUnique 
    @staticmethod
    def getWithName(aName):
        return AssetType.assettypesByName.get(aName)

    # Code from template attribute_HasUnique 
    @staticmethod
    def hasWithName(aName):
        return not (AssetType.getWithName(aName) is None)

    def getExpectedLifeSpan(self):
        return self._expectedLifeSpan

    def getImage(self):
        return self._image

    # Code from template association_GetOne 
    def getAssetPlus(self):
        return self._assetPlus

    # Code from template association_GetMany 
    def getSpecificAsset(self, index):
        aSpecificAsset = self._specificAssets[index]
        return aSpecificAsset

    def getSpecificAssets(self):
        newSpecificAssets = tuple(self._specificAssets)
        return newSpecificAssets

    def numberOfSpecificAssets(self):
        number = len(self._specificAssets)
        return number

    def hasSpecificAssets(self):
        has = len(self._specificAssets) > 0
        return has

    def indexOfSpecificAsset(self, aSpecificAsset):
        index = (-1 if not aSpecificAsset in self._specificAssets else self._specificAssets.index(aSpecificAsset))
        return index

    # Code from template association_SetOneToMany 
    def setAssetPlus(self, aAssetPlus):
        wasSet = False
        if aAssetPlus is None :
            return wasSet
        existingAssetPlus = self._assetPlus
        self._assetPlus = aAssetPlus
        if not (existingAssetPlus is None) and not existingAssetPlus == aAssetPlus :
            existingAssetPlus.removeAssetType(self)
        self._assetPlus.addAssetType(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfSpecificAssets():
        return 0

    # Code from template association_AddManyToOne 
    def addSpecificAsset1(self, aAssetNumber, aFloorNumber, aRoomNumber, aPurchaseDate, aAssetPlus):
        from .SpecificAsset import SpecificAsset
        return SpecificAsset(aAssetNumber, aFloorNumber, aRoomNumber, aPurchaseDate, aAssetPlus, self)

    def addSpecificAsset2(self, aSpecificAsset):
        wasAdded = False
        if (aSpecificAsset) in self._specificAssets :
            return False
        existingAssetType = aSpecificAsset.getAssetType()
        isNewAssetType = not (existingAssetType is None) and not self == existingAssetType
        if isNewAssetType :
            aSpecificAsset.setAssetType(self)
        else :
            self._specificAssets.append(aSpecificAsset)
        wasAdded = True
        return wasAdded

    def removeSpecificAsset(self, aSpecificAsset):
        wasRemoved = False
        #Unable to remove aSpecificAsset, as it must always have a assetType
        if not self == aSpecificAsset.getAssetType() :
            self._specificAssets.remove(aSpecificAsset)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addSpecificAssetAt(self, aSpecificAsset, index):
        wasAdded = False
        if self.addSpecificAsset(aSpecificAsset) :
            if index < 0 :
                index = 0
            if index > self.numberOfSpecificAssets() :
                index = self.numberOfSpecificAssets() - 1
            self._specificAssets.remove(aSpecificAsset)
            self._specificAssets.insert(index, aSpecificAsset)
            wasAdded = True
        return wasAdded

    def addOrMoveSpecificAssetAt(self, aSpecificAsset, index):
        wasAdded = False
        if (aSpecificAsset) in self._specificAssets :
            if index < 0 :
                index = 0
            if index > self.numberOfSpecificAssets() :
                index = self.numberOfSpecificAssets() - 1
            self._specificAssets.remove(aSpecificAsset)
            self._specificAssets.insert(index, aSpecificAsset)
            wasAdded = True
        else :
            wasAdded = self.addSpecificAssetAt(aSpecificAsset, index)
        return wasAdded

    def delete(self):
        AssetType.assettypesByName.pop(self.getName(), None)
        placeholderAssetPlus = self._assetPlus
        self._assetPlus = None
        if not (placeholderAssetPlus is None) :
            placeholderAssetPlus.removeAssetType(self)
        i = len(self._specificAssets)
        while i > 0 :
            aSpecificAsset = self._specificAssets[i - 1]
            aSpecificAsset.delete()
            i -= 1

    def __str__(self):
        return str(super().__str__()) + "[" + "name" + ":" + str(self.getName()) + "," + "expectedLifeSpan" + ":" + str(self.getExpectedLifeSpan()) + "," + "image" + ":" + str(self.getImage()) + "]" + str(os.linesep) + "  " + "assetPlus = " + ((format(id(self.getAssetPlus()), "x")) if not (self.getAssetPlus() is None) else "null")

    def addSpecificAsset(self, *argv):
        from .SpecificAsset import SpecificAsset
        from .AssetPlus import AssetPlus
        if len(argv) == 5 and isinstance(argv[0], int) and isinstance(argv[1], int) and isinstance(argv[2], int) and isinstance(argv[3], date) and isinstance(argv[4], AssetPlus) :
            return self.addSpecificAsset1(argv[0], argv[1], argv[2], argv[3], argv[4])
        if len(argv) == 1 and isinstance(argv[0], SpecificAsset) :
            return self.addSpecificAsset2(argv[0])
        raise TypeError("No method matches provided parameters")
