# %% NEW FILE MaintenanceTicket BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 42 "model.ump"
# line 226 "model.ump"
import os
from enum import Enum, auto
from datetime import date
class MaintenanceTicket():
    maintenanceticketsById = dict()
    #------------------------
    # ENUMERATIONS
    #------------------------
    class TimeEstimate(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name
        def __str__(self):
            return str(self.value)
        LessThanADay = auto()
        OneToThreeDays = auto()
        ThreeToSevenDays = auto()
        OneToThreeWeeks = auto()
        ThreeOrMoreWeeks = auto()

    class PriorityLevel(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name
        def __str__(self):
            return str(self.value)
        Urgent = auto()
        Normal = auto()
        Low = auto()

    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #MaintenanceTicket Attributes
    #MaintenanceTicket Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aId, aRaisedOnDate, aDescription, aAssetPlus, aTicketRaiser):
        self._fixApprover = None
        self._asset = None
        self._ticketFixer = None
        self._ticketRaiser = None
        self._assetPlus = None
        self._ticketImages = None
        self._ticketNotes = None
        self._priority = None
        self._timeToResolve = None
        self._description = None
        self._raisedOnDate = None
        self._id = None
        self._raisedOnDate = aRaisedOnDate
        self._description = aDescription
        if not self.setId(aId) :
            raise RuntimeError ("Cannot create due to duplicate id. See https://manual.umple.org?RE003ViolationofUniqueness.html")
        self._ticketNotes = []
        self._ticketImages = []
        didAddAssetPlus = self.setAssetPlus(aAssetPlus)
        if not didAddAssetPlus :
            raise RuntimeError ("Unable to create maintenanceTicket due to assetPlus. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddTicketRaiser = self.setTicketRaiser(aTicketRaiser)
        if not didAddTicketRaiser :
            raise RuntimeError ("Unable to create raisedTicket due to ticketRaiser. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setId(self, aId):
        wasSet = False
        anOldId = self.getId()
        if not (anOldId is None) and anOldId == aId :
            return True
        if MaintenanceTicket.hasWithId(aId) :
            return wasSet
        self._id = aId
        wasSet = True
        if not (anOldId is None) :
            MaintenanceTicket.maintenanceticketsById.pop(anOldId, None)
        MaintenanceTicket.maintenanceticketsById[aId] = self
        return wasSet

    def setRaisedOnDate(self, aRaisedOnDate):
        wasSet = False
        self._raisedOnDate = aRaisedOnDate
        wasSet = True
        return wasSet

    def setDescription(self, aDescription):
        wasSet = False
        self._description = aDescription
        wasSet = True
        return wasSet

    def setTimeToResolve(self, aTimeToResolve):
        wasSet = False
        self._timeToResolve = aTimeToResolve
        wasSet = True
        return wasSet

    def setPriority(self, aPriority):
        wasSet = False
        self._priority = aPriority
        wasSet = True
        return wasSet

    def getId(self):
        return self._id

    # Code from template attribute_GetUnique 
    @staticmethod
    def getWithId(aId):
        return MaintenanceTicket.maintenanceticketsById.get(aId)

    # Code from template attribute_HasUnique 
    @staticmethod
    def hasWithId(aId):
        return not (MaintenanceTicket.getWithId(aId) is None)

    def getRaisedOnDate(self):
        return self._raisedOnDate

    def getDescription(self):
        return self._description

    def getTimeToResolve(self):
        return self._timeToResolve

    def getPriority(self):
        return self._priority

    # Code from template association_GetMany 
    def getTicketNote(self, index):
        aTicketNote = self._ticketNotes[index]
        return aTicketNote

    def getTicketNotes(self):
        newTicketNotes = tuple(self._ticketNotes)
        return newTicketNotes

    def numberOfTicketNotes(self):
        number = len(self._ticketNotes)
        return number

    def hasTicketNotes(self):
        has = len(self._ticketNotes) > 0
        return has

    def indexOfTicketNote(self, aTicketNote):
        index = (-1 if not aTicketNote in self._ticketNotes else self._ticketNotes.index(aTicketNote))
        return index

    # Code from template association_GetMany 
    def getTicketImage(self, index):
        aTicketImage = self._ticketImages[index]
        return aTicketImage

    def getTicketImages(self):
        newTicketImages = tuple(self._ticketImages)
        return newTicketImages

    def numberOfTicketImages(self):
        number = len(self._ticketImages)
        return number

    def hasTicketImages(self):
        has = len(self._ticketImages) > 0
        return has

    def indexOfTicketImage(self, aTicketImage):
        index = (-1 if not aTicketImage in self._ticketImages else self._ticketImages.index(aTicketImage))
        return index

    # Code from template association_GetOne 
    def getAssetPlus(self):
        return self._assetPlus

    # Code from template association_GetOne 
    def getTicketRaiser(self):
        return self._ticketRaiser

    # Code from template association_GetOne 
    def getTicketFixer(self):
        return self._ticketFixer

    def hasTicketFixer(self):
        has = not (self._ticketFixer is None)
        return has

    # Code from template association_GetOne 
    def getAsset(self):
        return self._asset

    def hasAsset(self):
        has = not (self._asset is None)
        return has

    # Code from template association_GetOne 
    def getFixApprover(self):
        return self._fixApprover

    def hasFixApprover(self):
        has = not (self._fixApprover is None)
        return has

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfTicketNotes():
        return 0

    # Code from template association_AddManyToOne 
    def addTicketNote1(self, aDate, aDescription, aNoteTaker):
        from .MaintenanceNote import MaintenanceNote
        return MaintenanceNote(aDate, aDescription, self, aNoteTaker)

    def addTicketNote2(self, aTicketNote):
        wasAdded = False
        if (aTicketNote) in self._ticketNotes :
            return False
        existingTicket = aTicketNote.getTicket()
        isNewTicket = not (existingTicket is None) and not self == existingTicket
        if isNewTicket :
            aTicketNote.setTicket(self)
        else :
            self._ticketNotes.append(aTicketNote)
        wasAdded = True
        return wasAdded

    def removeTicketNote(self, aTicketNote):
        wasRemoved = False
        #Unable to remove aTicketNote, as it must always have a ticket
        if not self == aTicketNote.getTicket() :
            self._ticketNotes.remove(aTicketNote)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addTicketNoteAt(self, aTicketNote, index):
        wasAdded = False
        if self.addTicketNote(aTicketNote) :
            if index < 0 :
                index = 0
            if index > self.numberOfTicketNotes() :
                index = self.numberOfTicketNotes() - 1
            self._ticketNotes.remove(aTicketNote)
            self._ticketNotes.insert(index, aTicketNote)
            wasAdded = True
        return wasAdded

    def addOrMoveTicketNoteAt(self, aTicketNote, index):
        wasAdded = False
        if (aTicketNote) in self._ticketNotes :
            if index < 0 :
                index = 0
            if index > self.numberOfTicketNotes() :
                index = self.numberOfTicketNotes() - 1
            self._ticketNotes.remove(aTicketNote)
            self._ticketNotes.insert(index, aTicketNote)
            wasAdded = True
        else :
            wasAdded = self.addTicketNoteAt(aTicketNote, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod 
    @staticmethod
    def minimumNumberOfTicketImages():
        return 0

    # Code from template association_AddManyToOne 
    def addTicketImage1(self, aImageURL):
        from .TicketImage import TicketImage
        return TicketImage(aImageURL, self)

    def addTicketImage2(self, aTicketImage):
        wasAdded = False
        if (aTicketImage) in self._ticketImages :
            return False
        existingTicket = aTicketImage.getTicket()
        isNewTicket = not (existingTicket is None) and not self == existingTicket
        if isNewTicket :
            aTicketImage.setTicket(self)
        else :
            self._ticketImages.append(aTicketImage)
        wasAdded = True
        return wasAdded

    def removeTicketImage(self, aTicketImage):
        wasRemoved = False
        #Unable to remove aTicketImage, as it must always have a ticket
        if not self == aTicketImage.getTicket() :
            self._ticketImages.remove(aTicketImage)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions 
    def addTicketImageAt(self, aTicketImage, index):
        wasAdded = False
        if self.addTicketImage(aTicketImage) :
            if index < 0 :
                index = 0
            if index > self.numberOfTicketImages() :
                index = self.numberOfTicketImages() - 1
            self._ticketImages.remove(aTicketImage)
            self._ticketImages.insert(index, aTicketImage)
            wasAdded = True
        return wasAdded

    def addOrMoveTicketImageAt(self, aTicketImage, index):
        wasAdded = False
        if (aTicketImage) in self._ticketImages :
            if index < 0 :
                index = 0
            if index > self.numberOfTicketImages() :
                index = self.numberOfTicketImages() - 1
            self._ticketImages.remove(aTicketImage)
            self._ticketImages.insert(index, aTicketImage)
            wasAdded = True
        else :
            wasAdded = self.addTicketImageAt(aTicketImage, index)
        return wasAdded

    # Code from template association_SetOneToMany 
    def setAssetPlus(self, aAssetPlus):
        wasSet = False
        if aAssetPlus is None :
            return wasSet
        existingAssetPlus = self._assetPlus
        self._assetPlus = aAssetPlus
        if not (existingAssetPlus is None) and not existingAssetPlus == aAssetPlus :
            existingAssetPlus.removeMaintenanceTicket(self)
        self._assetPlus.addMaintenanceTicket(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToMany 
    def setTicketRaiser(self, aTicketRaiser):
        wasSet = False
        if aTicketRaiser is None :
            return wasSet
        existingTicketRaiser = self._ticketRaiser
        self._ticketRaiser = aTicketRaiser
        if not (existingTicketRaiser is None) and not existingTicketRaiser == aTicketRaiser :
            existingTicketRaiser.removeRaisedTicket(self)
        self._ticketRaiser.addRaisedTicket(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOptionalOneToMany 
    def setTicketFixer(self, aTicketFixer):
        wasSet = False
        existingTicketFixer = self._ticketFixer
        self._ticketFixer = aTicketFixer
        if not (existingTicketFixer is None) and not existingTicketFixer == aTicketFixer :
            existingTicketFixer.removeMaintenanceTask(self)
        if not (aTicketFixer is None) :
            aTicketFixer.addMaintenanceTask(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOptionalOneToMany 
    def setAsset(self, aAsset):
        wasSet = False
        existingAsset = self._asset
        self._asset = aAsset
        if not (existingAsset is None) and not existingAsset == aAsset :
            existingAsset.removeMaintenanceTicket(self)
        if not (aAsset is None) :
            aAsset.addMaintenanceTicket(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOptionalOneToMany 
    def setFixApprover(self, aFixApprover):
        wasSet = False
        existingFixApprover = self._fixApprover
        self._fixApprover = aFixApprover
        if not (existingFixApprover is None) and not existingFixApprover == aFixApprover :
            existingFixApprover.removeTicketsForApproval(self)
        if not (aFixApprover is None) :
            aFixApprover.addTicketsForApproval(self)
        wasSet = True
        return wasSet

    def delete(self):
        MaintenanceTicket.maintenanceticketsById.pop(self.getId(), None)

        while len(self._ticketNotes) > 0 :
            aTicketNote = self._ticketNotes[len(self._ticketNotes) - 1]
            aTicketNote.delete()
            self._ticketNotes.remove(aTicketNote)

        while len(self._ticketImages) > 0 :
            aTicketImage = self._ticketImages[len(self._ticketImages) - 1]
            aTicketImage.delete()
            self._ticketImages.remove(aTicketImage)

        placeholderAssetPlus = self._assetPlus
        self._assetPlus = None
        if not (placeholderAssetPlus is None) :
            placeholderAssetPlus.removeMaintenanceTicket(self)
        placeholderTicketRaiser = self._ticketRaiser
        self._ticketRaiser = None
        if not (placeholderTicketRaiser is None) :
            placeholderTicketRaiser.removeRaisedTicket(self)
        if not (self._ticketFixer is None) :
            placeholderTicketFixer = self._ticketFixer
            self._ticketFixer = None
            placeholderTicketFixer.removeMaintenanceTask(self)
        if not (self._asset is None) :
            placeholderAsset = self._asset
            self._asset = None
            placeholderAsset.removeMaintenanceTicket(self)
        if not (self._fixApprover is None) :
            placeholderFixApprover = self._fixApprover
            self._fixApprover = None
            placeholderFixApprover.removeTicketsForApproval(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "id" + ":" + str(self.getId()) + "," + "description" + ":" + str(self.getDescription()) + "]" + str(os.linesep) + "  " + "raisedOnDate" + "=" + str((((self.getRaisedOnDate().__str__().replaceAll("  ", "    ")) if not self.getRaisedOnDate() == self else "this") if not (self.getRaisedOnDate() is None) else "null")) + str(os.linesep) + "  " + "timeToResolve" + "=" + str((((self.getTimeToResolve().__str__().replaceAll("  ", "    ")) if not self.getTimeToResolve() == self else "this") if not (self.getTimeToResolve() is None) else "null")) + str(os.linesep) + "  " + "priority" + "=" + str((((self.getPriority().__str__().replaceAll("  ", "    ")) if not self.getPriority() == self else "this") if not (self.getPriority() is None) else "null")) + str(os.linesep) + "  " + "assetPlus = " + str(((format(id(self.getAssetPlus()), "x")) if not (self.getAssetPlus() is None) else "null")) + str(os.linesep) + "  " + "ticketRaiser = " + str(((format(id(self.getTicketRaiser()), "x")) if not (self.getTicketRaiser() is None) else "null")) + str(os.linesep) + "  " + "ticketFixer = " + str(((format(id(self.getTicketFixer()), "x")) if not (self.getTicketFixer() is None) else "null")) + str(os.linesep) + "  " + "asset = " + str(((format(id(self.getAsset()), "x")) if not (self.getAsset() is None) else "null")) + str(os.linesep) + "  " + "fixApprover = " + ((format(id(self.getFixApprover()), "x")) if not (self.getFixApprover() is None) else "null")

    def addTicketNote(self, *argv):
        from .HotelStaff import HotelStaff
        from .MaintenanceNote import MaintenanceNote
        if len(argv) == 3 and isinstance(argv[0], date) and isinstance(argv[1], str) and isinstance(argv[2], HotelStaff) :
            return self.addTicketNote1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], MaintenanceNote) :
            return self.addTicketNote2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addTicketImage(self, *argv):
        from .TicketImage import TicketImage
        if len(argv) == 1 and isinstance(argv[0], str) :
            return self.addTicketImage1(argv[0])
        if len(argv) == 1 and isinstance(argv[0], TicketImage) :
            return self.addTicketImage2(argv[0])
        raise TypeError("No method matches provided parameters")
