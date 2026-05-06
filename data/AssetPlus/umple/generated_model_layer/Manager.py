# %% NEW FILE Manager BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 37 "model.ump"
# line 221 "model.ump"
from .HotelStaff import HotelStaff

class Manager(HotelStaff):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Manager Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aEmail, aName, aPassword, aPhoneNumber, aAssetPlus):
        self._ticketsForApproval = None
        self._assetPlus = None
        super().__init__(aEmail, aName, aPassword, aPhoneNumber)
        didAddAssetPlus = self.setAssetPlus(aAssetPlus)
        if not didAddAssetPlus :
            raise RuntimeError ("Unable to create manager due to assetPlus. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._ticketsForApproval = []

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetOne 
    def getAssetPlus(self):
        return self._assetPlus

    # Code from template association_GetMany 
    def getTicketsForApproval1(self, index):
        aTicketsForApproval = self._ticketsForApproval[index]
        return aTicketsForApproval

    def getTicketsForApproval2(self):
        newTicketsForApproval = tuple(self._ticketsForApproval)
        return newTicketsForApproval

    def numberOfTicketsForApproval(self):
        number = len(self._ticketsForApproval)
        return number

    def hasTicketsForApproval(self):
        has = len(self._ticketsForApproval) > 0
        return has

    def indexOfTicketsForApproval(self, aTicketsForApproval):
        index = (-1 if not aTicketsForApproval in self._ticketsForApproval else self._ticketsForApproval.index(aTicketsForApproval))
        return index

    # Code from template association_SetOneToOptionalOne 
    def setAssetPlus(self, aNewAssetPlus):
        wasSet = False
        if aNewAssetPlus is None :
            #Unable to setAssetPlus to null, as manager must always be associated to a assetPlus
            return wasSet
        existingManager = aNewAssetPlus.getManager()
        if not (existingManager is None) and not self == existingManager :
            #Unable to setAssetPlus, the current assetPlus already has a manager, which would be orphaned if it were re-assigned
            return wasSet
        anOldAssetPlus = self._assetPlus
        self._assetPlus = aNewAssetPlus
        self._assetPlus.setManager(self)
        if not (anOldAssetPlus is None) :
            anOldAssetPlus.setManager(None)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfTicketsForApproval():
        return 0

    # Code from template association_AddManyToOptionalOne 
    def addTicketsForApproval(self, aTicketsForApproval):
        wasAdded = False
        if (aTicketsForApproval) in self._ticketsForApproval :
            return False
        existingFixApprover = aTicketsForApproval.getFixApprover()
        if existingFixApprover is None :
            aTicketsForApproval.setFixApprover(self)
        elif not self == existingFixApprover :
            existingFixApprover.removeTicketsForApproval(aTicketsForApproval)
            self.addTicketsForApproval(aTicketsForApproval)
        else :
            self._ticketsForApproval.append(aTicketsForApproval)
        wasAdded = True
        return wasAdded

    def removeTicketsForApproval(self, aTicketsForApproval):
        wasRemoved = False
        if (aTicketsForApproval) in self._ticketsForApproval :
            self._ticketsForApproval.remove(aTicketsForApproval)
            aTicketsForApproval.setFixApprover(None)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addTicketsForApprovalAt(self, aTicketsForApproval, index):
        wasAdded = False
        if self.addTicketsForApproval(aTicketsForApproval) :
            if index < 0 :
                index = 0
            if index > self.numberOfTicketsForApproval() :
                index = self.numberOfTicketsForApproval() - 1
            self._ticketsForApproval.remove(aTicketsForApproval)
            self._ticketsForApproval.insert(index, aTicketsForApproval)
            wasAdded = True
        return wasAdded

    def addOrMoveTicketsForApprovalAt(self, aTicketsForApproval, index):
        wasAdded = False
        if (aTicketsForApproval) in self._ticketsForApproval :
            if index < 0 :
                index = 0
            if index > self.numberOfTicketsForApproval() :
                index = self.numberOfTicketsForApproval() - 1
            self._ticketsForApproval.remove(aTicketsForApproval)
            self._ticketsForApproval.insert(index, aTicketsForApproval)
            wasAdded = True
        else :
            wasAdded = self.addTicketsForApprovalAt(aTicketsForApproval, index)
        return wasAdded

    def delete(self):
        existingAssetPlus = self._assetPlus
        self._assetPlus = None
        if not (existingAssetPlus is None) :
            existingAssetPlus.setManager(None)

        while not self._ticketsForApproval.isEmpty() :
            self._ticketsForApproval[0].setFixApprover(None)

        super().delete()

    def getTicketsForApproval(self, *argv):
        if len(argv) == 1 and isinstance(argv[0], int) :
            return self.getTicketsForApproval1(argv[0])
        if len(argv) == 0 :
            return self.getTicketsForApproval2()
        raise TypeError("No method matches provided parameters")
