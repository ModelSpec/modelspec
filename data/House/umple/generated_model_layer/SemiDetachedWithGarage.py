# %% NEW FILE SemiDetachedWithGarage BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8183.32a6408a9 modeling language!
# line 42 "model.ump"
# line 111 "model.ump"
from .SemiDetached import SemiDetached

class SemiDetachedWithGarage(SemiDetached):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #SemiDetachedWithGarage Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    @classmethod
    def alternateConstructor(cls, aAddress, aBuildingMaterial, aGarden, aWindows, aGarage):
        self = cls.__new__(cls)
        self._garage = None
        super().__init__(aAddress, aBuildingMaterial, aGarden, aWindows)
        if aGarage is None or not (aGarage.getSemiDetachedWithGarage() is None) :
            raise RuntimeError ("Unable to create SemiDetachedWithGarage due to aGarage. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._garage = aGarage
        return self

    def __init__(self, aAddress, aBuildingMaterial, aGarden, aWindows, aAutomaticForGarage):
        from .Garage import Garage
        self._garage = None
        super().__init__(aAddress, aBuildingMaterial, aGarden, aWindows)
        self._garage = Garage.alternateConstructor(aAutomaticForGarage, self)

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetOne 
    def getGarage(self):
        return self._garage

    def delete(self):
        existingGarage = self._garage
        self._garage = None
        if not (existingGarage is None) :
            existingGarage.delete()
        super().delete()
