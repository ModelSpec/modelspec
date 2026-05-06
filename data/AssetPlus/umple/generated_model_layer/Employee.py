# %% NEW FILE Employee BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 32 "model.ump"
# line 216 "model.ump"
from .HotelStaff import HotelStaff

class Employee(HotelStaff):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Employee Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aEmail, aName, aPassword, aPhoneNumber, aAssetPlus):
        self._assetPlus = None
        super().__init__(aEmail, aName, aPassword, aPhoneNumber)
        didAddAssetPlus = self.setAssetPlus(aAssetPlus)
        if not didAddAssetPlus :
            raise RuntimeError ("Unable to create employee due to assetPlus. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetOne 
    def getAssetPlus(self):
        return self._assetPlus

    # Code from template association_SetOneToMany 
    def setAssetPlus(self, aAssetPlus):
        wasSet = False
        if aAssetPlus is None :
            return wasSet
        existingAssetPlus = self._assetPlus
        self._assetPlus = aAssetPlus
        if not (existingAssetPlus is None) and not existingAssetPlus == aAssetPlus :
            existingAssetPlus.removeEmployee(self)
        self._assetPlus.addEmployee(self)
        wasSet = True
        return wasSet

    def delete(self):
        placeholderAssetPlus = self._assetPlus
        self._assetPlus = None
        if not (placeholderAssetPlus is None) :
            placeholderAssetPlus.removeEmployee(self)
        super().delete()
