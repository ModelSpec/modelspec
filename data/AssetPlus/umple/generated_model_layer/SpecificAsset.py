# %% NEW FILE SpecificAsset BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 69 "model.ump"
# line 241 "model.ump"
import os
from datetime import date
class SpecificAsset():
    specificassetsByAssetNumber = dict()
    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #SpecificAsset Attributes
    #SpecificAsset Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aAssetNumber, aFloorNumber, aRoomNumber, aPurchaseDate, aAssetPlus, aAssetType):
        self._assetType = None
        self._maintenanceTickets = None
        self._assetPlus = None
        self._purchaseDate = None
        self._roomNumber = None
        self._floorNumber = None
        self._assetNumber = None
        self._floorNumber = aFloorNumber
        self._roomNumber = aRoomNumber
        self._purchaseDate = aPurchaseDate
        if not self.setAssetNumber(aAssetNumber) :
            raise RuntimeError ("Cannot create due to duplicate assetNumber. See https://manual.umple.org?RE003ViolationofUniqueness.html")
        didAddAssetPlus = self.setAssetPlus(aAssetPlus)
        if not didAddAssetPlus :
            raise RuntimeError ("Unable to create specificAsset due to assetPlus. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._maintenanceTickets = []
        didAddAssetType = self.setAssetType(aAssetType)
        if not didAddAssetType :
            raise RuntimeError ("Unable to create specificAsset due to assetType. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setAssetNumber(self, aAssetNumber):
        wasSet = False
        anOldAssetNumber = self.getAssetNumber()
        if not (anOldAssetNumber is None) and anOldAssetNumber == aAssetNumber :
            return True
        if SpecificAsset.hasWithAssetNumber(aAssetNumber) :
            return wasSet
        self._assetNumber = aAssetNumber
        wasSet = True
        if not (anOldAssetNumber is None) :
            SpecificAsset.specificassetsByAssetNumber.pop(anOldAssetNumber, None)
        SpecificAsset.specificassetsByAssetNumber[aAssetNumber] = self
        return wasSet

    def setFloorNumber(self, aFloorNumber):
        wasSet = False
        self._floorNumber = aFloorNumber
        wasSet = True
        return wasSet

    def setRoomNumber(self, aRoomNumber):
        wasSet = False
        self._roomNumber = aRoomNumber
        wasSet = True
        return wasSet

    def setPurchaseDate(self, aPurchaseDate):
        wasSet = False
        self._purchaseDate = aPurchaseDate
        wasSet = True
        return wasSet

    def getAssetNumber(self):
        return self._assetNumber

    # Code from template attribute_GetUnique 
    @staticmethod
    def getWithAssetNumber(aAssetNumber):
        return SpecificAsset.specificassetsByAssetNumber.get(aAssetNumber)

    # Code from template attribute_HasUnique 
    @staticmethod
    def hasWithAssetNumber(aAssetNumber):
        return not (SpecificAsset.getWithAssetNumber(aAssetNumber) is None)

    def getFloorNumber(self):
        return self._floorNumber

    def getRoomNumber(self):
        return self._roomNumber

    def getPurchaseDate(self):
        return self._purchaseDate

    # Code from template association_GetOne 
    def getAssetPlus(self):
        return self._assetPlus

    # Code from template association_GetMany 
    def getMaintenanceTicket(self, index):
        aMaintenanceTicket = self._maintenanceTickets[index]
        return aMaintenanceTicket

    def getMaintenanceTickets(self):
        newMaintenanceTickets = tuple(self._maintenanceTickets)
        return newMaintenanceTickets

    def numberOfMaintenanceTickets(self):
        number = len(self._maintenanceTickets)
        return number

    def hasMaintenanceTickets(self):
        has = len(self._maintenanceTickets) > 0
        return has

    def indexOfMaintenanceTicket(self, aMaintenanceTicket):
        index = (-1 if not aMaintenanceTicket in self._maintenanceTickets else self._maintenanceTickets.index(aMaintenanceTicket))
        return index

    # Code from template association_GetOne 
    def getAssetType(self):
        return self._assetType

    # Code from template association_SetOneToMany 
    def setAssetPlus(self, aAssetPlus):
        wasSet = False
        if aAssetPlus is None :
            return wasSet
        existingAssetPlus = self._assetPlus
        self._assetPlus = aAssetPlus
        if not (existingAssetPlus is None) and not existingAssetPlus == aAssetPlus :
            existingAssetPlus.removeSpecificAsset(self)
        self._assetPlus.addSpecificAsset(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfMaintenanceTickets():
        return 0

    # Code from template association_AddManyToOptionalOne 
    def addMaintenanceTicket(self, aMaintenanceTicket):
        wasAdded = False
        if (aMaintenanceTicket) in self._maintenanceTickets :
            return False
        existingAsset = aMaintenanceTicket.getAsset()
        if existingAsset is None :
            aMaintenanceTicket.setAsset(self)
        elif not self == existingAsset :
            existingAsset.removeMaintenanceTicket(aMaintenanceTicket)
            self.addMaintenanceTicket(aMaintenanceTicket)
        else :
            self._maintenanceTickets.append(aMaintenanceTicket)
        wasAdded = True
        return wasAdded

    def removeMaintenanceTicket(self, aMaintenanceTicket):
        wasRemoved = False
        if (aMaintenanceTicket) in self._maintenanceTickets :
            self._maintenanceTickets.remove(aMaintenanceTicket)
            aMaintenanceTicket.setAsset(None)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addMaintenanceTicketAt(self, aMaintenanceTicket, index):
        wasAdded = False
        if self.addMaintenanceTicket(aMaintenanceTicket) :
            if index < 0 :
                index = 0
            if index > self.numberOfMaintenanceTickets() :
                index = self.numberOfMaintenanceTickets() - 1
            self._maintenanceTickets.remove(aMaintenanceTicket)
            self._maintenanceTickets.insert(index, aMaintenanceTicket)
            wasAdded = True
        return wasAdded

    def addOrMoveMaintenanceTicketAt(self, aMaintenanceTicket, index):
        wasAdded = False
        if (aMaintenanceTicket) in self._maintenanceTickets :
            if index < 0 :
                index = 0
            if index > self.numberOfMaintenanceTickets() :
                index = self.numberOfMaintenanceTickets() - 1
            self._maintenanceTickets.remove(aMaintenanceTicket)
            self._maintenanceTickets.insert(index, aMaintenanceTicket)
            wasAdded = True
        else :
            wasAdded = self.addMaintenanceTicketAt(aMaintenanceTicket, index)
        return wasAdded

    # Code from template association_SetOneToMany 
    def setAssetType(self, aAssetType):
        wasSet = False
        if aAssetType is None :
            return wasSet
        existingAssetType = self._assetType
        self._assetType = aAssetType
        if not (existingAssetType is None) and not existingAssetType == aAssetType :
            existingAssetType.removeSpecificAsset(self)
        self._assetType.addSpecificAsset(self)
        wasSet = True
        return wasSet

    def delete(self):
        SpecificAsset.specificassetsByAssetNumber.pop(self.getAssetNumber(), None)
        placeholderAssetPlus = self._assetPlus
        self._assetPlus = None
        if not (placeholderAssetPlus is None) :
            placeholderAssetPlus.removeSpecificAsset(self)

        while self._maintenanceTickets:
            aMaintenanceTicket = self._maintenanceTickets[0]
            aMaintenanceTicket.delete()

        placeholderAssetType = self._assetType
        self._assetType = None
        if not (placeholderAssetType is None) :
            placeholderAssetType.removeSpecificAsset(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "assetNumber" + ":" + str(self.getAssetNumber()) + "," + "floorNumber" + ":" + str(self.getFloorNumber()) + "," + "roomNumber" + ":" + str(self.getRoomNumber()) + "]" + str(os.linesep) + "  " + "purchaseDate" + "=" + str((((self.getPurchaseDate().__str__().replaceAll("  ", "    ")) if not self.getPurchaseDate() == self else "this") if not (self.getPurchaseDate() is None) else "null")) + str(os.linesep) + "  " + "assetPlus = " + str(((format(id(self.getAssetPlus()), "x")) if not (self.getAssetPlus() is None) else "null")) + str(os.linesep) + "  " + "assetType = " + ((format(id(self.getAssetType()), "x")) if not (self.getAssetType() is None) else "null")
