# %% NEW FILE Basement BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8183.32a6408a9 modeling language!
# line 7 "model.ump"
# line 81 "model.ump"
from abc import ABC, abstractmethod
import os

class Basement(ABC):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Basement Attributes
    #Basement Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aSize, aName, aHouse):
        self._house = None
        self._Name = None
        self._Size = None
        self._Size = aSize
        self._Name = aName
        didAddHouse = self.setHouse(aHouse)
        if not didAddHouse :
            raise RuntimeError ("Unable to create basement due to house. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setSize(self, aSize):
        wasSet = False
        self._Size = aSize
        wasSet = True
        return wasSet

    def setName(self, aName):
        wasSet = False
        self._Name = aName
        wasSet = True
        return wasSet

    def getSize(self):
        return self._Size

    def getName(self):
        return self._Name

    # Code from template association_GetOne 
    def getHouse(self):
        return self._house

    # Code from template association_SetOneToOptionalOne 
    def setHouse(self, aNewHouse):
        wasSet = False
        if aNewHouse is None :
            #Unable to setHouse to null, as basement must always be associated to a house
            return wasSet
        existingBasement = aNewHouse.getBasement()
        if not (existingBasement is None) and not self == existingBasement :
            #Unable to setHouse, the current house already has a basement, which would be orphaned if it were re-assigned
            return wasSet
        anOldHouse = self._house
        self._house = aNewHouse
        self._house.setBasement(self)
        if not (anOldHouse is None) :
            anOldHouse.setBasement(None)
        wasSet = True
        return wasSet

    def delete(self):
        existingHouse = self._house
        self._house = None
        if not (existingHouse is None) :
            existingHouse.setBasement(None)

    def __str__(self):
        return str(super().__str__()) + "[" + "Size" + ":" + str(self.getSize()) + "," + "Name" + ":" + str(self.getName()) + "]" + str(os.linesep) + "  " + "house = " + ((format(id(self.getHouse()), "x")) if not (self.getHouse() is None) else "null")
