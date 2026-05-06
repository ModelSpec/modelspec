# %% NEW FILE Garage BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8183.32a6408a9 modeling language!
# line 56 "model.ump"
# line 126 "model.ump"
import os

class Garage():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Garage Attributes
    #Garage Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    @classmethod
    def alternateConstructor(cls, aAutomatic, aSemiDetachedWithGarage):
        self = cls.__new__(cls)
        self._semiDetachedWithGarage = None
        self._Automatic = None
        self._Automatic = aAutomatic
        if aSemiDetachedWithGarage is None or not (aSemiDetachedWithGarage.getGarage() is None) :
            raise RuntimeError ("Unable to create Garage due to aSemiDetachedWithGarage. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._semiDetachedWithGarage = aSemiDetachedWithGarage
        return self

    def __init__(self, aAutomatic, aAddressForSemiDetachedWithGarage, aBuildingMaterialForSemiDetachedWithGarage, aGardenForSemiDetachedWithGarage, aWindowsForSemiDetachedWithGarage):
        from .SemiDetachedWithGarage import SemiDetachedWithGarage
        self._semiDetachedWithGarage = None
        self._Automatic = None
        self._Automatic = aAutomatic
        self._semiDetachedWithGarage = SemiDetachedWithGarage.alternateConstructor(aAddressForSemiDetachedWithGarage, aBuildingMaterialForSemiDetachedWithGarage, aGardenForSemiDetachedWithGarage, aWindowsForSemiDetachedWithGarage, self)

    #------------------------
    # INTERFACE
    #------------------------
    def setAutomatic(self, aAutomatic):
        wasSet = False
        self._Automatic = aAutomatic
        wasSet = True
        return wasSet

    def getAutomatic(self):
        return self._Automatic

    # Code from template attribute_IsBoolean 
    def isAutomatic(self):
        return self._Automatic

    # Code from template association_GetOne 
    def getSemiDetachedWithGarage(self):
        return self._semiDetachedWithGarage

    def delete(self):
        existingSemiDetachedWithGarage = self._semiDetachedWithGarage
        self._semiDetachedWithGarage = None
        if not (existingSemiDetachedWithGarage is None) :
            existingSemiDetachedWithGarage.delete()

    def __str__(self):
        return str(super().__str__()) + "[" + "Automatic" + ":" + str(self.getAutomatic()) + "]" + str(os.linesep) + "  " + "semiDetachedWithGarage = " + ((format(id(self.getSemiDetachedWithGarage()), "x")) if not (self.getSemiDetachedWithGarage() is None) else "null")
