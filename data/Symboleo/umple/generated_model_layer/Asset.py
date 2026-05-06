# %% NEW FILE Asset BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 27 "model.ump"
import os

class Asset():
    assetsById = dict()
    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Asset Attributes
    #Asset Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aId, aContract):
        self._contract = None
        self._legalPositions = None
        self._owners = None
        self._id = None
        if not self.setId(aId) :
            raise RuntimeError ("Cannot create due to duplicate id. See https://manual.umple.org?RE003ViolationofUniqueness.html")
        self._owners = []
        self._legalPositions = []
        didAddContract = self.setContract(aContract)
        if not didAddContract :
            raise RuntimeError ("Unable to create asset due to contract. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setId(self, aId):
        wasSet = False
        anOldId = self.getId()
        if not (anOldId is None) and anOldId == aId :
            return True
        if Asset.hasWithId(aId) :
            return wasSet
        self._id = aId
        wasSet = True
        if not (anOldId is None) :
            Asset.assetsById.pop(anOldId, None)
        Asset.assetsById[aId] = self
        return wasSet

    def getId(self):
        return self._id

    # Code from template attribute_GetUnique
    @staticmethod
    def getWithId(aId):
        return Asset.assetsById.get(aId)

    # Code from template attribute_HasUnique
    @staticmethod
    def hasWithId(aId):
        return not (Asset.getWithId(aId) is None)

    # Code from template association_GetMany
    def getOwner(self, index):
        aOwner = self._owners[index]
        return aOwner

    def getOwners(self):
        newOwners = tuple(self._owners)
        return newOwners

    def numberOfOwners(self):
        number = len(self._owners)
        return number

    def hasOwners(self):
        has = len(self._owners) > 0
        return has

    def indexOfOwner(self, aOwner):
        index = (-1 if not aOwner in self._owners else self._owners.index(aOwner))
        return index

    # Code from template association_GetMany
    def getLegalPosition(self, index):
        aLegalPosition = self._legalPositions[index]
        return aLegalPosition

    def getLegalPositions(self):
        newLegalPositions = tuple(self._legalPositions)
        return newLegalPositions

    def numberOfLegalPositions(self):
        number = len(self._legalPositions)
        return number

    def hasLegalPositions(self):
        has = len(self._legalPositions) > 0
        return has

    def indexOfLegalPosition(self, aLegalPosition):
        index = (-1 if not aLegalPosition in self._legalPositions else self._legalPositions.index(aLegalPosition))
        return index

    # Code from template association_GetOne
    def getContract(self):
        return self._contract

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfOwners():
        return 0

    # Code from template association_AddManyToManyMethod
    def addOwner(self, aOwner):
        wasAdded = False
        if (aOwner) in self._owners :
            return False
        self._owners.append(aOwner)
        if aOwner.indexOfAsset(self) != -1 :
            wasAdded = True
        else :
            wasAdded = aOwner.addAsset(self)
            if not wasAdded :
                self._owners.remove(aOwner)
        return wasAdded

    # Code from template association_RemoveMany
    def removeOwner(self, aOwner):
        wasRemoved = False
        if not (aOwner) in self._owners :
            return wasRemoved
        oldIndex = (-1 if not aOwner in self._owners else self._owners.index(aOwner))
        self._owners.remove(oldIndex)
        if aOwner.indexOfAsset(self) == -1 :
            wasRemoved = True
        else :
            wasRemoved = aOwner.removeAsset(self)
            if not wasRemoved :
                self._owners.insert(oldIndex, aOwner)
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addOwnerAt(self, aOwner, index):
        wasAdded = False
        if self.addOwner(aOwner) :
            if index < 0 :
                index = 0
            if index > self.numberOfOwners() :
                index = self.numberOfOwners() - 1
            self._owners.remove(aOwner)
            self._owners.insert(index, aOwner)
            wasAdded = True
        return wasAdded

    def addOrMoveOwnerAt(self, aOwner, index):
        wasAdded = False
        if (aOwner) in self._owners :
            if index < 0 :
                index = 0
            if index > self.numberOfOwners() :
                index = self.numberOfOwners() - 1
            self._owners.remove(aOwner)
            self._owners.insert(index, aOwner)
            wasAdded = True
        else :
            wasAdded = self.addOwnerAt(aOwner, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfLegalPositions():
        return 0

    # Code from template association_AddManyToOptionalOne
    def addLegalPosition(self, aLegalPosition):
        wasAdded = False
        if (aLegalPosition) in self._legalPositions :
            return False
        existingAsset = aLegalPosition.getAsset()
        if existingAsset is None :
            aLegalPosition.setAsset(self)
        elif not self == existingAsset :
            existingAsset.removeLegalPosition(aLegalPosition)
            self.addLegalPosition(aLegalPosition)
        else :
            self._legalPositions.append(aLegalPosition)
        wasAdded = True
        return wasAdded

    def removeLegalPosition(self, aLegalPosition):
        wasRemoved = False
        if (aLegalPosition) in self._legalPositions :
            self._legalPositions.remove(aLegalPosition)
            aLegalPosition.setAsset(None)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addLegalPositionAt(self, aLegalPosition, index):
        wasAdded = False
        if self.addLegalPosition(aLegalPosition) :
            if index < 0 :
                index = 0
            if index > self.numberOfLegalPositions() :
                index = self.numberOfLegalPositions() - 1
            self._legalPositions.remove(aLegalPosition)
            self._legalPositions.insert(index, aLegalPosition)
            wasAdded = True
        return wasAdded

    def addOrMoveLegalPositionAt(self, aLegalPosition, index):
        wasAdded = False
        if (aLegalPosition) in self._legalPositions :
            if index < 0 :
                index = 0
            if index > self.numberOfLegalPositions() :
                index = self.numberOfLegalPositions() - 1
            self._legalPositions.remove(aLegalPosition)
            self._legalPositions.insert(index, aLegalPosition)
            wasAdded = True
        else :
            wasAdded = self.addLegalPositionAt(aLegalPosition, index)
        return wasAdded

    # Code from template association_SetOneToMany
    def setContract(self, aContract):
        wasSet = False
        if aContract is None :
            return wasSet
        existingContract = self._contract
        self._contract = aContract
        if not (existingContract is None) and not existingContract == aContract :
            existingContract.removeAsset(self)
        self._contract.addAsset(self)
        wasSet = True
        return wasSet

    def delete(self):
        Asset.assetsById.pop(self.getId(), None)
        copyOfOwners = self._owners.copy()
        self._owners.clear()
        for aOwner in copyOfOwners:
            aOwner.removeAsset(self)

        while not self._legalPositions.isEmpty() :
            self._legalPositions[0].setAsset(None)

        placeholderContract = self._contract
        self._contract = None
        if not (placeholderContract is None) :
            placeholderContract.removeAsset(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "id" + ":" + str(self.getId()) + "]" + str(os.linesep) + "  " + "contract = " + ((format(id(self.getContract()), "x")) if not (self.getContract() is None) else "null")
