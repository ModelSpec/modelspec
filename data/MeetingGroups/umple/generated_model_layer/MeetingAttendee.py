# %% NEW FILE MeetingAttendee BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 140 "model.ump"
# line 330 "model.ump"
import os
from enum import Enum, auto

class MeetingAttendee():
    #------------------------
    # ENUMERATIONS
    #------------------------
    class MeetingAttendeeRole(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name
        def __str__(self):
            return str(self.value)
        Host = auto()
        Attendee = auto()

    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #MeetingAttendee Attributes
    #MeetingAttendee Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aGuestNumber, aDecisionDate, aRole, aAttendee, aMeeting, aMeetings):
        self._meetings = None
        self._meeting = None
        self._removingMember = None
        self._fee = None
        self._attendee = None
        self._role = None
        self._removedDate = None
        self._decisionChangeDate = None
        self._decisionDate = None
        self._removingReason = None
        self._isRemoved = None
        self._isFeePaid = None
        self._decisionChanged = None
        self._guestNumber = None
        self._guestNumber = aGuestNumber
        self._removingReason = None
        self._decisionDate = aDecisionDate
        self._decisionChangeDate = None
        self._removedDate = None
        self._role = aRole
        if not self.setAttendee(aAttendee) :
            raise RuntimeError ("Unable to create MeetingAttendee due to aAttendee. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddMeeting = self.setMeeting(aMeeting)
        if not didAddMeeting :
            raise RuntimeError ("Unable to create meetingAttendee due to meeting. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddMeetings = self.setMeetings(aMeetings)
        if not didAddMeetings :
            raise RuntimeError ("Unable to create meetingAttendee due to meetings. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setGuestNumber(self, aGuestNumber):
        wasSet = False
        self._guestNumber = aGuestNumber
        wasSet = True
        return wasSet

    def setDecisionChanged(self, aDecisionChanged):
        wasSet = False
        self._decisionChanged = aDecisionChanged
        wasSet = True
        return wasSet

    def setIsFeePaid(self, aIsFeePaid):
        wasSet = False
        self._isFeePaid = aIsFeePaid
        wasSet = True
        return wasSet

    def setIsRemoved(self, aIsRemoved):
        wasSet = False
        self._isRemoved = aIsRemoved
        wasSet = True
        return wasSet

    def setRemovingReason(self, aRemovingReason):
        wasSet = False
        self._removingReason = aRemovingReason
        wasSet = True
        return wasSet

    def setDecisionDate(self, aDecisionDate):
        wasSet = False
        self._decisionDate = aDecisionDate
        wasSet = True
        return wasSet

    def setDecisionChangeDate(self, aDecisionChangeDate):
        wasSet = False
        self._decisionChangeDate = aDecisionChangeDate
        wasSet = True
        return wasSet

    def setRemovedDate(self, aRemovedDate):
        wasSet = False
        self._removedDate = aRemovedDate
        wasSet = True
        return wasSet

    def setRole(self, aRole):
        wasSet = False
        self._role = aRole
        wasSet = True
        return wasSet

    def getGuestNumber(self):
        return self._guestNumber

    def getDecisionChanged(self):
        return self._decisionChanged

    def getIsFeePaid(self):
        return self._isFeePaid

    def getIsRemoved(self):
        return self._isRemoved

    def getRemovingReason(self):
        return self._removingReason

    def getDecisionDate(self):
        return self._decisionDate

    def getDecisionChangeDate(self):
        return self._decisionChangeDate

    def getRemovedDate(self):
        return self._removedDate

    def getRole(self):
        return self._role

    # Code from template association_GetOne
    def getAttendee(self):
        return self._attendee

    # Code from template association_GetOne
    def getFee(self):
        return self._fee

    def hasFee(self):
        has = not (self._fee is None)
        return has

    # Code from template association_GetOne
    def getRemovingMember(self):
        return self._removingMember

    def hasRemovingMember(self):
        has = not (self._removingMember is None)
        return has

    # Code from template association_GetOne
    def getMeeting(self):
        return self._meeting

    # Code from template association_GetOne
    def getMeetings(self):
        return self._meetings

    # Code from template association_SetUnidirectionalOne
    def setAttendee(self, aNewAttendee):
        wasSet = False
        if not (aNewAttendee is None) :
            self._attendee = aNewAttendee
            wasSet = True
        return wasSet

    # Code from template association_SetUnidirectionalOptionalOne
    def setFee(self, aNewFee):
        wasSet = False
        self._fee = aNewFee
        wasSet = True
        return wasSet

    # Code from template association_SetUnidirectionalOptionalOne
    def setRemovingMember(self, aNewRemovingMember):
        wasSet = False
        self._removingMember = aNewRemovingMember
        wasSet = True
        return wasSet

    # Code from template association_SetOneToMany
    def setMeeting(self, aMeeting):
        wasSet = False
        if aMeeting is None :
            return wasSet
        existingMeeting = self._meeting
        self._meeting = aMeeting
        if not (existingMeeting is None) and not existingMeeting == aMeeting :
            existingMeeting.removeMeetingAttendee(self)
        self._meeting.addMeetingAttendee(self)
        wasSet = True
        return wasSet

    # Code from template association_SetOneToMany
    def setMeetings(self, aMeetings):
        wasSet = False
        if aMeetings is None :
            return wasSet
        existingMeetings = self._meetings
        self._meetings = aMeetings
        if not (existingMeetings is None) and not existingMeetings == aMeetings :
            existingMeetings.removeMeetingAttendee(self)
        self._meetings.addMeetingAttendee(self)
        wasSet = True
        return wasSet

    def delete(self):
        self._attendee = None
        self._fee = None
        self._removingMember = None
        placeholderMeeting = self._meeting
        self._meeting = None
        if not (placeholderMeeting is None) :
            placeholderMeeting.removeMeetingAttendee(self)
        placeholderMeetings = self._meetings
        self._meetings = None
        if not (placeholderMeetings is None) :
            placeholderMeetings.removeMeetingAttendee(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "guestNumber" + ":" + str(self.getGuestNumber()) + "," + "removingReason" + ":" + str(self.getRemovingReason()) + "]" + str(os.linesep) + "  " + "decisionChanged" + "=" + str((((self.getDecisionChanged().__str__().replaceAll("  ", "    ")) if not self.getDecisionChanged() == self else "this") if not (self.getDecisionChanged() is None) else "null")) + str(os.linesep) + "  " + "isFeePaid" + "=" + str((((self.getIsFeePaid().__str__().replaceAll("  ", "    ")) if not self.getIsFeePaid() == self else "this") if not (self.getIsFeePaid() is None) else "null")) + str(os.linesep) + "  " + "isRemoved" + "=" + str((((self.getIsRemoved().__str__().replaceAll("  ", "    ")) if not self.getIsRemoved() == self else "this") if not (self.getIsRemoved() is None) else "null")) + str(os.linesep) + "  " + "decisionDate" + "=" + str((((self.getDecisionDate().__str__().replaceAll("  ", "    ")) if not self.getDecisionDate() == self else "this") if not (self.getDecisionDate() is None) else "null")) + str(os.linesep) + "  " + "decisionChangeDate" + "=" + str((((self.getDecisionChangeDate().__str__().replaceAll("  ", "    ")) if not self.getDecisionChangeDate() == self else "this") if not (self.getDecisionChangeDate() is None) else "null")) + str(os.linesep) + "  " + "removedDate" + "=" + str((((self.getRemovedDate().__str__().replaceAll("  ", "    ")) if not self.getRemovedDate() == self else "this") if not (self.getRemovedDate() is None) else "null")) + str(os.linesep) + "  " + "role" + "=" + str((((self.getRole().__str__().replaceAll("  ", "    ")) if not self.getRole() == self else "this") if not (self.getRole() is None) else "null")) + str(os.linesep) + "  " + "attendee = " + str(((format(id(self.getAttendee()), "x")) if not (self.getAttendee() is None) else "null")) + str(os.linesep) + "  " + "fee = " + str(((format(id(self.getFee()), "x")) if not (self.getFee() is None) else "null")) + str(os.linesep) + "  " + "removingMember = " + str(((format(id(self.getRemovingMember()), "x")) if not (self.getRemovingMember() is None) else "null")) + str(os.linesep) + "  " + "meeting = " + str(((format(id(self.getMeeting()), "x")) if not (self.getMeeting() is None) else "null")) + str(os.linesep) + "  " + "meetings = " + ((format(id(self.getMeetings()), "x")) if not (self.getMeetings() is None) else "null")