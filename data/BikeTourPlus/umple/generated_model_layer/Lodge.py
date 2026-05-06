# %% NEW FILE Lodge BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8091.03bcab5b3 modeling language!
# line 77 "model.ump"
# line 151 "model.ump"
import os
from enum import Enum, auto

class Lodge():
    lodgesByName = dict()
    #------------------------
    # ENUMERATIONS
    #------------------------
    class LodgeRating(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name
        def __str__(self):
            return str(self.value)
        OneStar = auto()
        TwoStars = auto()
        ThreeStars = auto()
        FourStars = auto()
        FiveStars = auto()

    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Lodge Attributes
    #Lodge Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aName, aAddress, aRating, aBikeTourPlus):
        self._bikeTours = None
        self._bikeTourPlus = None
        self._rating = None
        self._address = None
        self._name = None
        self._address = aAddress
        self._rating = aRating
        if not self.setName(aName) :
            raise RuntimeError ("Cannot create due to duplicate name. See https://manual.umple.org?RE003ViolationofUniqueness.html")
        didAddBikeTourPlus = self.setBikeTourPlus(aBikeTourPlus)
        if not didAddBikeTourPlus :
            raise RuntimeError ("Unable to create lodge due to bikeTourPlus. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._bikeTours = []

    #------------------------
    # INTERFACE
    #------------------------
    def setName(self, aName):
        wasSet = False
        anOldName = self.getName()
        if not (anOldName is None) and anOldName == aName :
            return True
        if Lodge.hasWithName(aName) :
            return wasSet
        self._name = aName
        wasSet = True
        if not (anOldName is None) :
            Lodge.lodgesByName.pop(anOldName, None)
        Lodge.lodgesByName[aName] = self
        return wasSet

    def setAddress(self, aAddress):
        wasSet = False
        self._address = aAddress
        wasSet = True
        return wasSet

    def setRating(self, aRating):
        wasSet = False
        self._rating = aRating
        wasSet = True
        return wasSet

    def getName(self):
        return self._name

    # Code from template attribute_GetUnique
    @staticmethod
    def getWithName(aName):
        return Lodge.lodgesByName.get(aName)

    # Code from template attribute_HasUnique
    @staticmethod
    def hasWithName(aName):
        return not (Lodge.getWithName(aName) is None)

    def getAddress(self):
        return self._address

    def getRating(self):
        return self._rating

    # Code from template association_GetOne
    def getBikeTourPlus(self):
        return self._bikeTourPlus

    # Code from template association_GetMany
    def getBikeTour(self, index):
        aBikeTour = self._bikeTours[index]
        return aBikeTour

    def getBikeTours(self):
        newBikeTours = tuple(self._bikeTours)
        return newBikeTours

    def numberOfBikeTours(self):
        number = len(self._bikeTours)
        return number

    def hasBikeTours(self):
        has = len(self._bikeTours) > 0
        return has

    def indexOfBikeTour(self, aBikeTour):
        index = (-1 if not aBikeTour in self._bikeTours else self._bikeTours.index(aBikeTour))
        return index

    # Code from template association_SetOneToMany
    def setBikeTourPlus(self, aBikeTourPlus):
        wasSet = False
        if aBikeTourPlus is None :
            return wasSet
        existingBikeTourPlus = self._bikeTourPlus
        self._bikeTourPlus = aBikeTourPlus
        if not (existingBikeTourPlus is None) and not existingBikeTourPlus == aBikeTourPlus :
            existingBikeTourPlus.removeLodge(self)
        self._bikeTourPlus.addLodge(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfBikeTours():
        return 0

    # Code from template association_AddManyToOptionalOne
    def addBikeTour(self, aBikeTour):
        wasAdded = False
        if (aBikeTour) in self._bikeTours :
            return False
        existingLodge = aBikeTour.getLodge()
        if existingLodge is None :
            aBikeTour.setLodge(self)
        elif not self == existingLodge :
            existingLodge.removeBikeTour(aBikeTour)
            self.addBikeTour(aBikeTour)
        else :
            self._bikeTours.append(aBikeTour)
        wasAdded = True
        return wasAdded

    def removeBikeTour(self, aBikeTour):
        wasRemoved = False
        if (aBikeTour) in self._bikeTours :
            self._bikeTours.remove(aBikeTour)
            aBikeTour.setLodge(None)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addBikeTourAt(self, aBikeTour, index):
        wasAdded = False
        if self.addBikeTour(aBikeTour) :
            if index < 0 :
                index = 0
            if index > self.numberOfBikeTours() :
                index = self.numberOfBikeTours() - 1
            self._bikeTours.remove(aBikeTour)
            self._bikeTours.insert(index, aBikeTour)
            wasAdded = True
        return wasAdded

    def addOrMoveBikeTourAt(self, aBikeTour, index):
        wasAdded = False
        if (aBikeTour) in self._bikeTours :
            if index < 0 :
                index = 0
            if index > self.numberOfBikeTours() :
                index = self.numberOfBikeTours() - 1
            self._bikeTours.remove(aBikeTour)
            self._bikeTours.insert(index, aBikeTour)
            wasAdded = True
        else :
            wasAdded = self.addBikeTourAt(aBikeTour, index)
        return wasAdded

    def delete(self):
        Lodge.lodgesByName.pop(self.getName(), None)
        placeholderBikeTourPlus = self._bikeTourPlus
        self._bikeTourPlus = None
        if not (placeholderBikeTourPlus is None) :
            placeholderBikeTourPlus.removeLodge(self)

        while not self._bikeTours.isEmpty() :
            self._bikeTours[0].setLodge(None)

    def __str__(self):
        return str(super().__str__()) + "[" + "name" + ":" + str(self.getName()) + "," + "address" + ":" + str(self.getAddress()) + "]" + str(os.linesep) + "  " + "rating" + "=" + str((((self.getRating().__str__().replaceAll("  ", "    ")) if not self.getRating() == self else "this") if not (self.getRating() is None) else "null")) + str(os.linesep) + "  " + "bikeTourPlus = " + ((format(id(self.getBikeTourPlus()), "x")) if not (self.getBikeTourPlus() is None) else "null")