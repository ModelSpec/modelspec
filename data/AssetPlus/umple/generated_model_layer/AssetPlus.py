# %% NEW FILE AssetPlus BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 2 "model.ump"
# line 196 "model.ump"
from datetime import date
class AssetPlus():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #AssetPlus Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self):
        self._specificAssets = None
        self._assetTypes = None
        self._maintenanceTickets = None
        self._manager = None
        self._guests = None
        self._employees = None
        self._employees = []
        self._guests = []
        self._maintenanceTickets = []
        self._assetTypes = []
        self._specificAssets = []

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetMany 
    def getEmployee(self, index):
        aEmployee = self._employees[index]
        return aEmployee

    def getEmployees(self):
        newEmployees = tuple(self._employees)
        return newEmployees

    def numberOfEmployees(self):
        number = len(self._employees)
        return number

    def hasEmployees(self):
        has = len(self._employees) > 0
        return has

    def indexOfEmployee(self, aEmployee):
        index = (-1 if not aEmployee in self._employees else self._employees.index(aEmployee))
        return index

    # Code from template association_GetMany 
    def getGuest(self, index):
        aGuest = self._guests[index]
        return aGuest

    def getGuests(self):
        newGuests = tuple(self._guests)
        return newGuests

    def numberOfGuests(self):
        number = len(self._guests)
        return number

    def hasGuests(self):
        has = len(self._guests) > 0
        return has

    def indexOfGuest(self, aGuest):
        index = (-1 if not aGuest in self._guests else self._guests.index(aGuest))
        return index

    # Code from template association_GetOne 
    def getManager(self):
        return self._manager

    def hasManager(self):
        has = not (self._manager is None)
        return has

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

    # Code from template association_GetMany 
    def getAssetType(self, index):
        aAssetType = self._assetTypes[index]
        return aAssetType

    def getAssetTypes(self):
        newAssetTypes = tuple(self._assetTypes)
        return newAssetTypes

    def numberOfAssetTypes(self):
        number = len(self._assetTypes)
        return number

    def hasAssetTypes(self):
        has = len(self._assetTypes) > 0
        return has

    def indexOfAssetType(self, aAssetType):
        index = (-1 if not aAssetType in self._assetTypes else self._assetTypes.index(aAssetType))
        return index

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

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfEmployees():
        return 0

    # Code from template association_AddManyToOne 
    def addEmployee1(self, aEmail, aName, aPassword, aPhoneNumber):
        from .Employee import Employee
        return Employee(aEmail, aName, aPassword, aPhoneNumber, self)

    def addEmployee2(self, aEmployee):
        wasAdded = False
        if (aEmployee) in self._employees :
            return False
        existingAssetPlus = aEmployee.getAssetPlus()
        isNewAssetPlus = not (existingAssetPlus is None) and not self == existingAssetPlus
        if isNewAssetPlus :
            aEmployee.setAssetPlus(self)
        else :
            self._employees.append(aEmployee)
        wasAdded = True
        return wasAdded

    def removeEmployee(self, aEmployee):
        wasRemoved = False
        #Unable to remove aEmployee, as it must always have a assetPlus
        if not self == aEmployee.getAssetPlus() :
            self._employees.remove(aEmployee)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addEmployeeAt(self, aEmployee, index):
        wasAdded = False
        if self.addEmployee(aEmployee) :
            if index < 0 :
                index = 0
            if index > self.numberOfEmployees() :
                index = self.numberOfEmployees() - 1
            self._employees.remove(aEmployee)
            self._employees.insert(index, aEmployee)
            wasAdded = True
        return wasAdded

    def addOrMoveEmployeeAt(self, aEmployee, index):
        wasAdded = False
        if (aEmployee) in self._employees :
            if index < 0 :
                index = 0
            if index > self.numberOfEmployees() :
                index = self.numberOfEmployees() - 1
            self._employees.remove(aEmployee)
            self._employees.insert(index, aEmployee)
            wasAdded = True
        else :
            wasAdded = self.addEmployeeAt(aEmployee, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfGuests():
        return 0

    # Code from template association_AddManyToOne 
    def addGuest1(self, aEmail, aName, aPassword, aPhoneNumber):
        from .Guest import Guest
        return Guest(aEmail, aName, aPassword, aPhoneNumber, self)

    def addGuest2(self, aGuest):
        wasAdded = False
        if (aGuest) in self._guests :
            return False
        existingAssetPlus = aGuest.getAssetPlus()
        isNewAssetPlus = not (existingAssetPlus is None) and not self == existingAssetPlus
        if isNewAssetPlus :
            aGuest.setAssetPlus(self)
        else :
            self._guests.append(aGuest)
        wasAdded = True
        return wasAdded

    def removeGuest(self, aGuest):
        wasRemoved = False
        #Unable to remove aGuest, as it must always have a assetPlus
        if not self == aGuest.getAssetPlus() :
            self._guests.remove(aGuest)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addGuestAt(self, aGuest, index):
        wasAdded = False
        if self.addGuest(aGuest) :
            if index < 0 :
                index = 0
            if index > self.numberOfGuests() :
                index = self.numberOfGuests() - 1
            self._guests.remove(aGuest)
            self._guests.insert(index, aGuest)
            wasAdded = True
        return wasAdded

    def addOrMoveGuestAt(self, aGuest, index):
        wasAdded = False
        if (aGuest) in self._guests :
            if index < 0 :
                index = 0
            if index > self.numberOfGuests() :
                index = self.numberOfGuests() - 1
            self._guests.remove(aGuest)
            self._guests.insert(index, aGuest)
            wasAdded = True
        else :
            wasAdded = self.addGuestAt(aGuest, index)
        return wasAdded

    # Code from template association_SetOptionalOneToOne 
    def setManager(self, aNewManager):
        wasSet = False
        if not (self._manager is None) and not self._manager == aNewManager and self == self._manager.getAssetPlus() :
            #Unable to setManager, as existing manager would become an orphan
            return wasSet
        self._manager = aNewManager
        anOldAssetPlus = (aNewManager.getAssetPlus()) if not (aNewManager is None) else None
        if not self == anOldAssetPlus :
            if not (anOldAssetPlus is None) :
                anOldAssetPlus.manager = None
            if not (self._manager is None) :
                self._manager.setAssetPlus(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfMaintenanceTickets():
        return 0

    # Code from template association_AddManyToOne 
    def addMaintenanceTicket1(self, aId, aRaisedOnDate, aDescription, aTicketRaiser):
        from .MaintenanceTicket import MaintenanceTicket
        return MaintenanceTicket(aId, aRaisedOnDate, aDescription, self, aTicketRaiser)

    def addMaintenanceTicket2(self, aMaintenanceTicket):
        wasAdded = False
        if (aMaintenanceTicket) in self._maintenanceTickets :
            return False
        existingAssetPlus = aMaintenanceTicket.getAssetPlus()
        isNewAssetPlus = not (existingAssetPlus is None) and not self == existingAssetPlus
        if isNewAssetPlus :
            aMaintenanceTicket.setAssetPlus(self)
        else :
            self._maintenanceTickets.append(aMaintenanceTicket)
        wasAdded = True
        return wasAdded

    def removeMaintenanceTicket(self, aMaintenanceTicket):
        wasRemoved = False
        #Unable to remove aMaintenanceTicket, as it must always have a assetPlus
        if not self == aMaintenanceTicket.getAssetPlus() :
            self._maintenanceTickets.remove(aMaintenanceTicket)
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

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfAssetTypes():
        return 0

    # Code from template association_AddManyToOne 
    def addAssetType1(self, aName, aExpectedLifeSpan):
        from .AssetType import AssetType
        return AssetType(aName, aExpectedLifeSpan, self)

    def addAssetType2(self, aAssetType):
        wasAdded = False
        if (aAssetType) in self._assetTypes :
            return False
        existingAssetPlus = aAssetType.getAssetPlus()
        isNewAssetPlus = not (existingAssetPlus is None) and not self == existingAssetPlus
        if isNewAssetPlus :
            aAssetType.setAssetPlus(self)
        else :
            self._assetTypes.append(aAssetType)
        wasAdded = True
        return wasAdded

    def removeAssetType(self, aAssetType):
        wasRemoved = False
        #Unable to remove aAssetType, as it must always have a assetPlus
        if not self == aAssetType.getAssetPlus() :
            self._assetTypes.remove(aAssetType)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addAssetTypeAt(self, aAssetType, index):
        wasAdded = False
        if self.addAssetType(aAssetType) :
            if index < 0 :
                index = 0
            if index > self.numberOfAssetTypes() :
                index = self.numberOfAssetTypes() - 1
            self._assetTypes.remove(aAssetType)
            self._assetTypes.insert(index, aAssetType)
            wasAdded = True
        return wasAdded

    def addOrMoveAssetTypeAt(self, aAssetType, index):
        wasAdded = False
        if (aAssetType) in self._assetTypes :
            if index < 0 :
                index = 0
            if index > self.numberOfAssetTypes() :
                index = self.numberOfAssetTypes() - 1
            self._assetTypes.remove(aAssetType)
            self._assetTypes.insert(index, aAssetType)
            wasAdded = True
        else :
            wasAdded = self.addAssetTypeAt(aAssetType, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfSpecificAssets():
        return 0

    # Code from template association_AddManyToOne 
    def addSpecificAsset1(self, aAssetNumber, aFloorNumber, aRoomNumber, aPurchaseDate, aAssetType):
        from .SpecificAsset import SpecificAsset
        return SpecificAsset(aAssetNumber, aFloorNumber, aRoomNumber, aPurchaseDate, self, aAssetType)

    def addSpecificAsset2(self, aSpecificAsset):
        wasAdded = False
        if (aSpecificAsset) in self._specificAssets :
            return False
        existingAssetPlus = aSpecificAsset.getAssetPlus()
        isNewAssetPlus = not (existingAssetPlus is None) and not self == existingAssetPlus
        if isNewAssetPlus :
            aSpecificAsset.setAssetPlus(self)
        else :
            self._specificAssets.append(aSpecificAsset)
        wasAdded = True
        return wasAdded

    def removeSpecificAsset(self, aSpecificAsset):
        wasRemoved = False
        #Unable to remove aSpecificAsset, as it must always have a assetPlus
        if not self == aSpecificAsset.getAssetPlus() :
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

        while len(self._employees) > 0 :
            aEmployee = self._employees[len(self._employees) - 1]
            aEmployee.delete()
            self._employees.remove(aEmployee)

        while len(self._guests) > 0 :
            aGuest = self._guests[len(self._guests) - 1]
            aGuest.delete()
            self._guests.remove(aGuest)

        existingManager = self._manager
        self._manager = None
        if not (existingManager is None) :
            existingManager.delete()
            existingManager.setAssetPlus(None)

        while len(self._maintenanceTickets) > 0 :
            aMaintenanceTicket = self._maintenanceTickets[len(self._maintenanceTickets) - 1]
            aMaintenanceTicket.delete()
            self._maintenanceTickets.remove(aMaintenanceTicket)

        while len(self._assetTypes) > 0 :
            aAssetType = self._assetTypes[len(self._assetTypes) - 1]
            aAssetType.delete()
            self._assetTypes.remove(aAssetType)

        while len(self._specificAssets) > 0 :
            aSpecificAsset = self._specificAssets[len(self._specificAssets) - 1]
            aSpecificAsset.delete()
            self._specificAssets.remove(aSpecificAsset)

    def addEmployee(self, *argv):
        from .Employee import Employee
        if len(argv) == 4 and isinstance(argv[0], str) and isinstance(argv[1], str) and isinstance(argv[2], str) and isinstance(argv[3], str) :
            return self.addEmployee1(argv[0], argv[1], argv[2], argv[3])
        if len(argv) == 1 and isinstance(argv[0], Employee) :
            return self.addEmployee2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addGuest(self, *argv):
        from .Guest import Guest
        if len(argv) == 4 and isinstance(argv[0], str) and isinstance(argv[1], str) and isinstance(argv[2], str) and isinstance(argv[3], str) :
            return self.addGuest1(argv[0], argv[1], argv[2], argv[3])
        if len(argv) == 1 and isinstance(argv[0], Guest) :
            return self.addGuest2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addMaintenanceTicket(self, *argv):
        from .MaintenanceTicket import MaintenanceTicket
        from .User import User
        if len(argv) == 4 and isinstance(argv[0], int) and isinstance(argv[1], date) and isinstance(argv[2], str) and isinstance(argv[3], User) :
            return self.addMaintenanceTicket1(argv[0], argv[1], argv[2], argv[3])
        if len(argv) == 1 and isinstance(argv[0], MaintenanceTicket) :
            return self.addMaintenanceTicket2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addAssetType(self, *argv):
        from .AssetType import AssetType
        if len(argv) == 2 and isinstance(argv[0], str) and isinstance(argv[1], int) :
            return self.addAssetType1(argv[0], argv[1])
        if len(argv) == 1 and isinstance(argv[0], AssetType) :
            return self.addAssetType2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addSpecificAsset(self, *argv):
        from .SpecificAsset import SpecificAsset
        from .AssetType import AssetType
        if len(argv) == 5 and isinstance(argv[0], int) and isinstance(argv[1], int) and isinstance(argv[2], int) and isinstance(argv[3], date) and isinstance(argv[4], AssetType) :
            return self.addSpecificAsset1(argv[0], argv[1], argv[2], argv[3], argv[4])
        if len(argv) == 1 and isinstance(argv[0], SpecificAsset) :
            return self.addSpecificAsset2(argv[0])
        raise TypeError("No method matches provided parameters")
