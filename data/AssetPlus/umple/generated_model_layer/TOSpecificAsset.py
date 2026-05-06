# %% NEW FILE TOSpecificAsset BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 160 "model.ump"
# line 286 "model.ump"
import os
from datetime import date
class TOSpecificAsset():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #TOSpecificAsset Attributes
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aAssetNumber, aFloorNumber, aRoomNumber, aPurchaseDate, aAssetType):
        self._assetType = None
        self._purchaseDate = None
        self._roomNumber = None
        self._floorNumber = None
        self._assetNumber = None
        self._assetNumber = aAssetNumber
        self._floorNumber = aFloorNumber
        self._roomNumber = aRoomNumber
        self._purchaseDate = aPurchaseDate
        self._assetType = aAssetType

    #------------------------
    # INTERFACE
    #------------------------
    def getAssetNumber(self):
        return self._assetNumber

    def getFloorNumber(self):
        return self._floorNumber

    def getRoomNumber(self):
        return self._roomNumber

    def getPurchaseDate(self):
        return self._purchaseDate

    def getAssetType(self):
        return self._assetType

    def delete(self):
        pass

    def __str__(self):
        return str(super().__str__()) + "[" + "assetNumber" + ":" + str(self.getAssetNumber()) + "," + "floorNumber" + ":" + str(self.getFloorNumber()) + "," + "roomNumber" + ":" + str(self.getRoomNumber()) + "]" + str(os.linesep) + "  " + "purchaseDate" + "=" + str((((self.getPurchaseDate().__str__().replaceAll("  ", "    ")) if not self.getPurchaseDate() == self else "this") if not (self.getPurchaseDate() is None) else "null")) + str(os.linesep) + "  " + "assetType" + "=" + (((self.getAssetType().__str__().replaceAll("  ", "    ")) if not self.getAssetType() == self else "this") if not (self.getAssetType() is None) else "null")
