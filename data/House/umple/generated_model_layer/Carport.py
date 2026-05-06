# %% NEW FILE Carport BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8183.32a6408a9 modeling language!
# line 51 "model.ump"
# line 121 "model.ump"
import os

class Carport():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Carport Attributes
    #Carport Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aDoublePort, aFlatRoof, aSemiDetachedWithCarport):
        self._semiDetachedWithCarport = None
        self._flatRoof = None
        self._DoublePort = None
        self._DoublePort = aDoublePort
        self._flatRoof = aFlatRoof
        didAddSemiDetachedWithCarport = self.setSemiDetachedWithCarport(aSemiDetachedWithCarport)
        if not didAddSemiDetachedWithCarport :
            raise RuntimeError ("Unable to create carport due to semiDetachedWithCarport. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setDoublePort(self, aDoublePort):
        wasSet = False
        self._DoublePort = aDoublePort
        wasSet = True
        return wasSet

    def setFlatRoof(self, aFlatRoof):
        wasSet = False
        self._flatRoof = aFlatRoof
        wasSet = True
        return wasSet

    def getDoublePort(self):
        return self._DoublePort

    def getFlatRoof(self):
        return self._flatRoof

    # Code from template attribute_IsBoolean 
    def isDoublePort(self):
        return self._DoublePort

    # Code from template attribute_IsBoolean 
    def isFlatRoof(self):
        return self._flatRoof

    # Code from template association_GetOne 
    def getSemiDetachedWithCarport(self):
        return self._semiDetachedWithCarport

    # Code from template association_SetOneToAtMostN 
    def setSemiDetachedWithCarport(self, aSemiDetachedWithCarport):
        from .SemiDetachedWithCarport import SemiDetachedWithCarport
        wasSet = False
        #Must provide semiDetachedWithCarport to carport
        if aSemiDetachedWithCarport is None :
            return wasSet
        #semiDetachedWithCarport already at maximum (2)
        if aSemiDetachedWithCarport.numberOfCarports() >= SemiDetachedWithCarport.maximumNumberOfCarports() :
            return wasSet
        existingSemiDetachedWithCarport = self._semiDetachedWithCarport
        self._semiDetachedWithCarport = aSemiDetachedWithCarport
        if not (existingSemiDetachedWithCarport is None) and not existingSemiDetachedWithCarport == aSemiDetachedWithCarport :
            didRemove = existingSemiDetachedWithCarport.removeCarport(self)
            if not didRemove :
                self._semiDetachedWithCarport = existingSemiDetachedWithCarport
                return wasSet
        self._semiDetachedWithCarport.addCarport(self)
        wasSet = True
        return wasSet

    def delete(self):
        placeholderSemiDetachedWithCarport = self._semiDetachedWithCarport
        self._semiDetachedWithCarport = None
        if not (placeholderSemiDetachedWithCarport is None) :
            placeholderSemiDetachedWithCarport.removeCarport(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "DoublePort" + ":" + str(self.getDoublePort()) + "," + "flatRoof" + ":" + str(self.getFlatRoof()) + "]" + str(os.linesep) + "  " + "semiDetachedWithCarport = " + ((format(id(self.getSemiDetachedWithCarport()), "x")) if not (self.getSemiDetachedWithCarport() is None) else "null")
