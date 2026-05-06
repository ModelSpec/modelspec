# %% NEW FILE Participant BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8091.03bcab5b3 modeling language!
# line 38 "model.ump"
# line 121 "model.ump"
from .NamedUser import NamedUser
import os
from enum import Enum, auto

class Participant(NamedUser):
    #------------------------
    # ENUMERATIONS
    #------------------------
    class Status(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name
        def __str__(self):
            return str(self.value)
        NotAssigned = auto()
        Assigned = auto()
        Paid = auto()
        Started = auto()
        Finished = auto()
        Cancelled = auto()
        Banned = auto()

    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Participant Attributes
    #Participant Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aEmail, aPassword, aName, aEmergencyContact, aNrWeeks, aWeekAvailableFrom, aWeekAvailableUntil, aLodgeRequired, aAuthorizationCode, aRefundedPercentageAmount, aBikeTourPlus):
        self._bookedItems = None
        self._bikeTour = None
        self._bikeTourPlus = None
        self._status = None
        self._refundedPercentageAmount = None
        self._authorizationCode = None
        self._lodgeRequired = None
        self._weekAvailableUntil = None
        self._weekAvailableFrom = None
        self._nrWeeks = None
        super().__init__(aEmail, aPassword, aName, aEmergencyContact)
        self._nrWeeks = aNrWeeks
        self._weekAvailableFrom = aWeekAvailableFrom
        self._weekAvailableUntil = aWeekAvailableUntil
        self._lodgeRequired = aLodgeRequired
        self._authorizationCode = aAuthorizationCode
        self._refundedPercentageAmount = aRefundedPercentageAmount
        self._status = Participant.Status.NotAssigned
        didAddBikeTourPlus = self.setBikeTourPlus(aBikeTourPlus)
        if not didAddBikeTourPlus :
            raise RuntimeError ("Unable to create participant due to bikeTourPlus. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._bookedItems = []

    #------------------------
    # INTERFACE
    #------------------------
    def setNrWeeks(self, aNrWeeks):
        wasSet = False
        self._nrWeeks = aNrWeeks
        wasSet = True
        return wasSet

    def setWeekAvailableFrom(self, aWeekAvailableFrom):
        wasSet = False
        self._weekAvailableFrom = aWeekAvailableFrom
        wasSet = True
        return wasSet

    def setWeekAvailableUntil(self, aWeekAvailableUntil):
        wasSet = False
        self._weekAvailableUntil = aWeekAvailableUntil
        wasSet = True
        return wasSet

    def setLodgeRequired(self, aLodgeRequired):
        wasSet = False
        self._lodgeRequired = aLodgeRequired
        wasSet = True
        return wasSet

    def setAuthorizationCode(self, aAuthorizationCode):
        wasSet = False
        self._authorizationCode = aAuthorizationCode
        wasSet = True
        return wasSet

    def setRefundedPercentageAmount(self, aRefundedPercentageAmount):
        wasSet = False
        self._refundedPercentageAmount = aRefundedPercentageAmount
        wasSet = True
        return wasSet

    def setStatus(self, aStatus):
        wasSet = False
        self._status = aStatus
        wasSet = True
        return wasSet

    def getNrWeeks(self):
        return self._nrWeeks

    def getWeekAvailableFrom(self):
        return self._weekAvailableFrom

    def getWeekAvailableUntil(self):
        return self._weekAvailableUntil

    def getLodgeRequired(self):
        return self._lodgeRequired

    def getAuthorizationCode(self):
        return self._authorizationCode

    def getRefundedPercentageAmount(self):
        return self._refundedPercentageAmount

    def getStatus(self):
        return self._status

    # Code from template attribute_IsBoolean
    def isLodgeRequired(self):
        return self._lodgeRequired

    # Code from template association_GetOne
    def getBikeTourPlus(self):
        return self._bikeTourPlus

    # Code from template association_GetOne
    def getBikeTour(self):
        return self._bikeTour

    def hasBikeTour(self):
        has = not (self._bikeTour is None)
        return has

    # Code from template association_GetMany
    def getBookedItem(self, index):
        aBookedItem = self._bookedItems[index]
        return aBookedItem

    def getBookedItems(self):
        newBookedItems = tuple(self._bookedItems)
        return newBookedItems

    def numberOfBookedItems(self):
        number = len(self._bookedItems)
        return number

    def hasBookedItems(self):
        has = len(self._bookedItems) > 0
        return has

    def indexOfBookedItem(self, aBookedItem):
        index = (-1 if not aBookedItem in self._bookedItems else self._bookedItems.index(aBookedItem))
        return index

    # Code from template association_SetOneToMany
    def setBikeTourPlus(self, aBikeTourPlus):
        wasSet = False
        if aBikeTourPlus is None :
            return wasSet
        existingBikeTourPlus = self._bikeTourPlus
        self._bikeTourPlus = aBikeTourPlus
        if not (existingBikeTourPlus is None) and not existingBikeTourPlus == aBikeTourPlus :
            existingBikeTourPlus.removeParticipant(self)
        self._bikeTourPlus.addParticipant(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOptionalOneToMany
    def setBikeTour(self, aBikeTour):
        wasSet = False
        existingBikeTour = self._bikeTour
        self._bikeTour = aBikeTour
        if not (existingBikeTour is None) and not existingBikeTour == aBikeTour :
            existingBikeTour.removeParticipant(self)
        if not (aBikeTour is None) :
            aBikeTour.addParticipant(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfBookedItems():
        return 0

    # Code from template association_AddManyToOne
    def addBookedItem1(self, aQuantity, aBikeTourPlus, aItem):
        from .BookedItem import BookedItem
        return BookedItem(aQuantity, aBikeTourPlus, self, aItem)

    def addBookedItem2(self, aBookedItem):
        wasAdded = False
        if (aBookedItem) in self._bookedItems :
            return False
        existingParticipant = aBookedItem.getParticipant()
        isNewParticipant = not (existingParticipant is None) and not self == existingParticipant
        if isNewParticipant :
            aBookedItem.setParticipant(self)
        else :
            self._bookedItems.append(aBookedItem)
        wasAdded = True
        return wasAdded

    def removeBookedItem(self, aBookedItem):
        wasRemoved = False
        #Unable to remove aBookedItem, as it must always have a participant
        if not self == aBookedItem.getParticipant() :
            self._bookedItems.remove(aBookedItem)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addBookedItemAt(self, aBookedItem, index):
        wasAdded = False
        if self.addBookedItem(aBookedItem) :
            if index < 0 :
                index = 0
            if index > self.numberOfBookedItems() :
                index = self.numberOfBookedItems() - 1
            self._bookedItems.remove(aBookedItem)
            self._bookedItems.insert(index, aBookedItem)
            wasAdded = True
        return wasAdded

    def addOrMoveBookedItemAt(self, aBookedItem, index):
        wasAdded = False
        if (aBookedItem) in self._bookedItems :
            if index < 0 :
                index = 0
            if index > self.numberOfBookedItems() :
                index = self.numberOfBookedItems() - 1
            self._bookedItems.remove(aBookedItem)
            self._bookedItems.insert(index, aBookedItem)
            wasAdded = True
        else :
            wasAdded = self.addBookedItemAt(aBookedItem, index)
        return wasAdded

    def delete(self):
        placeholderBikeTourPlus = self._bikeTourPlus
        self._bikeTourPlus = None
        if not (placeholderBikeTourPlus is None) :
            placeholderBikeTourPlus.removeParticipant(self)
        if not (self._bikeTour is None) :
            placeholderBikeTour = self._bikeTour
            self._bikeTour = None
            placeholderBikeTour.removeParticipant(self)
        i = len(self._bookedItems)
        while i > 0 :
            aBookedItem = self._bookedItems[i - 1]
            aBookedItem.delete()
            i -= 1

        super().delete()

    def __str__(self):
        return str(super().__str__()) + "[" + "nrWeeks" + ":" + str(self.getNrWeeks()) + "," + "weekAvailableFrom" + ":" + str(self.getWeekAvailableFrom()) + "," + "weekAvailableUntil" + ":" + str(self.getWeekAvailableUntil()) + "," + "lodgeRequired" + ":" + str(self.getLodgeRequired()) + "," + "authorizationCode" + ":" + str(self.getAuthorizationCode()) + "," + "refundedPercentageAmount" + ":" + str(self.getRefundedPercentageAmount()) + "]" + str(os.linesep) + "  " + "status" + "=" + str((((self.getStatus().__str__().replaceAll("  ", "    ")) if not self.getStatus() == self else "this") if not (self.getStatus() is None) else "null")) + str(os.linesep) + "  " + "bikeTourPlus = " + str(((format(id(self.getBikeTourPlus()), "x")) if not (self.getBikeTourPlus() is None) else "null")) + str(os.linesep) + "  " + "bikeTour = " + ((format(id(self.getBikeTour()), "x")) if not (self.getBikeTour() is None) else "null")

    def addBookedItem(self, *argv):
        from .BookedItem import BookedItem
        from .BikeTourPlus import BikeTourPlus
        from .BookableItem import BookableItem
        if len(argv) == 3 and isinstance(argv[0], int) and isinstance(argv[1], BikeTourPlus) and isinstance(argv[2], BookableItem) :
            return self.addBookedItem1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], BookedItem) :
            return self.addBookedItem2(argv[0])
        raise TypeError("No method matches provided parameters")
