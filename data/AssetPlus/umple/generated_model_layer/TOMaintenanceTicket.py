# %% NEW FILE TOMaintenanceTicket BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 169 "model.ump"
# line 291 "model.ump"
import os
from datetime import date
class TOMaintenanceTicket():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #TOMaintenanceTicket Attributes
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aId, aRaisedOnDate, aDescription, aRaisedByEmail, aStatus, aFixedByEmail, aTimeToResolve, aPriority, aApprovalRequired, aAssetName, aExpectedLifeSpanInDays, aPurchaseDate, aFloorNumber, aRoomNumber):
        self._noteTakerEmails = None
        self._noteDescriptions = None
        self._noteDates = None
        self._imageURLs = None
        self._roomNumber = None
        self._floorNumber = None
        self._purchaseDate = None
        self._expectedLifeSpanInDays = None
        self._assetName = None
        self._approvalRequired = None
        self._priority = None
        self._timeToResolve = None
        self._fixedByEmail = None
        self._status = None
        self._raisedByEmail = None
        self._description = None
        self._raisedOnDate = None
        self._id = None
        self._id = aId
        self._raisedOnDate = aRaisedOnDate
        self._description = aDescription
        self._raisedByEmail = aRaisedByEmail
        self._status = aStatus
        self._fixedByEmail = aFixedByEmail
        self._timeToResolve = aTimeToResolve
        self._priority = aPriority
        self._approvalRequired = aApprovalRequired
        self._assetName = aAssetName
        self._expectedLifeSpanInDays = aExpectedLifeSpanInDays
        self._purchaseDate = aPurchaseDate
        self._floorNumber = aFloorNumber
        self._roomNumber = aRoomNumber
        self._imageURLs = []
        self._noteDates = []
        self._noteDescriptions = []
        self._noteTakerEmails = []

    #------------------------
    # INTERFACE
    #------------------------
    def getId(self):
        return self._id

    def getRaisedOnDate(self):
        return self._raisedOnDate

    def getDescription(self):
        return self._description

    def getRaisedByEmail(self):
        return self._raisedByEmail

    def getStatus(self):
        return self._status

    def getFixedByEmail(self):
        return self._fixedByEmail

    def getTimeToResolve(self):
        return self._timeToResolve

    def getPriority(self):
        return self._priority

    def getApprovalRequired(self):
        return self._approvalRequired

    def getAssetName(self):
        return self._assetName

    def getExpectedLifeSpanInDays(self):
        return self._expectedLifeSpanInDays

    def getPurchaseDate(self):
        return self._purchaseDate

    def getFloorNumber(self):
        return self._floorNumber

    def getRoomNumber(self):
        return self._roomNumber

    # Code from template attribute_GetMany 
    def getImageURL(self, index):
        aImageURL = self._imageURLs[index]
        return aImageURL

    def getImageURLs(self):
        newImageURLs = self._imageURLs.copy()
        return newImageURLs

    def numberOfImageURLs(self):
        number = len(self._imageURLs)
        return number

    def hasImageURLs(self):
        has = len(self._imageURLs) > 0
        return has

    def indexOfImageURL(self, aImageURL):
        index = (-1 if not aImageURL in self._imageURLs else self._imageURLs.index(aImageURL))
        return index

    # Code from template attribute_GetMany 
    def getNoteDate(self, index):
        aNoteDate = self._noteDates[index]
        return aNoteDate

    def getNoteDates(self):
        newNoteDates = self._noteDates.copy()
        return newNoteDates

    def numberOfNoteDates(self):
        number = len(self._noteDates)
        return number

    def hasNoteDates(self):
        has = len(self._noteDates) > 0
        return has

    def indexOfNoteDate(self, aNoteDate):
        index = (-1 if not aNoteDate in self._noteDates else self._noteDates.index(aNoteDate))
        return index

    # Code from template attribute_GetMany 
    def getNoteDescription(self, index):
        aNoteDescription = self._noteDescriptions[index]
        return aNoteDescription

    def getNoteDescriptions(self):
        newNoteDescriptions = self._noteDescriptions.copy()
        return newNoteDescriptions

    def numberOfNoteDescriptions(self):
        number = len(self._noteDescriptions)
        return number

    def hasNoteDescriptions(self):
        has = len(self._noteDescriptions) > 0
        return has

    def indexOfNoteDescription(self, aNoteDescription):
        index = (-1 if not aNoteDescription in self._noteDescriptions else self._noteDescriptions.index(aNoteDescription))
        return index

    # Code from template attribute_GetMany 
    def getNoteTakerEmail(self, index):
        aNoteTakerEmail = self._noteTakerEmails[index]
        return aNoteTakerEmail

    def getNoteTakerEmails(self):
        newNoteTakerEmails = self._noteTakerEmails.copy()
        return newNoteTakerEmails

    def numberOfNoteTakerEmails(self):
        number = len(self._noteTakerEmails)
        return number

    def hasNoteTakerEmails(self):
        has = len(self._noteTakerEmails) > 0
        return has

    def indexOfNoteTakerEmail(self, aNoteTakerEmail):
        index = (-1 if not aNoteTakerEmail in self._noteTakerEmails else self._noteTakerEmails.index(aNoteTakerEmail))
        return index

    # Code from template attribute_IsBoolean 
    def isApprovalRequired(self):
        return self._approvalRequired

    def delete(self):
        pass

    def __str__(self):
        return str(super().__str__()) + "[" + "id" + ":" + str(self.getId()) + "," + "description" + ":" + str(self.getDescription()) + "," + "raisedByEmail" + ":" + str(self.getRaisedByEmail()) + "," + "status" + ":" + str(self.getStatus()) + "," + "fixedByEmail" + ":" + str(self.getFixedByEmail()) + "," + "timeToResolve" + ":" + str(self.getTimeToResolve()) + "," + "priority" + ":" + str(self.getPriority()) + "," + "approvalRequired" + ":" + str(self.getApprovalRequired()) + "," + "assetName" + ":" + str(self.getAssetName()) + "," + "expectedLifeSpanInDays" + ":" + str(self.getExpectedLifeSpanInDays()) + "," + "floorNumber" + ":" + str(self.getFloorNumber()) + "," + "roomNumber" + ":" + str(self.getRoomNumber()) + "]" + str(os.linesep) + "  " + "raisedOnDate" + "=" + str((((self.getRaisedOnDate().__str__().replaceAll("  ", "    ")) if not self.getRaisedOnDate() == self else "this") if not (self.getRaisedOnDate() is None) else "null")) + str(os.linesep) + "  " + "purchaseDate" + "=" + (((self.getPurchaseDate().__str__().replaceAll("  ", "    ")) if not self.getPurchaseDate() == self else "this") if not (self.getPurchaseDate() is None) else "null")
