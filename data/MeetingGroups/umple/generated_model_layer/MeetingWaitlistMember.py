# %% NEW FILE MeetingWaitlistMember BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 165 "model.ump"
# line 340 "model.ump"
import os

class MeetingWaitlistMember():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #MeetingWaitlistMember Attributes
    #MeetingWaitlistMember Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aDecisionDate, aMember, aMeeting, aMeetings):
        self._meetings = None
        self._meeting = None
        self._member = None
        self._isMovedToAttendees = None
        self._movedToAttendeesDate = None
        self._signOffDate = None
        self._signUpDate = None
        self._decisionDate = None
        self._decisionChanged = None
        self._decisionDate = aDecisionDate
        self._signUpDate = None
        self._signOffDate = None
        self._movedToAttendeesDate = None
        if not self.setMember(aMember) :
            raise RuntimeError ("Unable to create MeetingWaitlistMember due to aMember. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddMeeting = self.setMeeting(aMeeting)
        if not didAddMeeting :
            raise RuntimeError ("Unable to create meetingWaitlistMember due to meeting. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddMeetings = self.setMeetings(aMeetings)
        if not didAddMeetings :
            raise RuntimeError ("Unable to create meetingWaitlistMember due to meetings. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setDecisionChanged(self, aDecisionChanged):
        wasSet = False
        self._decisionChanged = aDecisionChanged
        wasSet = True
        return wasSet

    def setDecisionDate(self, aDecisionDate):
        wasSet = False
        self._decisionDate = aDecisionDate
        wasSet = True
        return wasSet

    def setSignUpDate(self, aSignUpDate):
        wasSet = False
        self._signUpDate = aSignUpDate
        wasSet = True
        return wasSet

    def setSignOffDate(self, aSignOffDate):
        wasSet = False
        self._signOffDate = aSignOffDate
        wasSet = True
        return wasSet

    def setMovedToAttendeesDate(self, aMovedToAttendeesDate):
        wasSet = False
        self._movedToAttendeesDate = aMovedToAttendeesDate
        wasSet = True
        return wasSet

    def setIsMovedToAttendees(self, aIsMovedToAttendees):
        wasSet = False
        self._isMovedToAttendees = aIsMovedToAttendees
        wasSet = True
        return wasSet

    def getDecisionChanged(self):
        return self._decisionChanged

    def getDecisionDate(self):
        return self._decisionDate

    def getSignUpDate(self):
        return self._signUpDate

    def getSignOffDate(self):
        return self._signOffDate

    def getMovedToAttendeesDate(self):
        return self._movedToAttendeesDate

    def getIsMovedToAttendees(self):
        return self._isMovedToAttendees

    # Code from template association_GetOne
    def getMember(self):
        return self._member

    # Code from template association_GetOne
    def getMeeting(self):
        return self._meeting

    # Code from template association_GetOne
    def getMeetings(self):
        return self._meetings

    # Code from template association_SetUnidirectionalOne
    def setMember(self, aNewMember):
        wasSet = False
        if not (aNewMember is None) :
            self._member = aNewMember
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
            existingMeeting.removeMeetingWaitlistMember(self)
        self._meeting.addMeetingWaitlistMember(self)
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
            existingMeetings.removeMeetingWaitlistMember(self)
        self._meetings.addMeetingWaitlistMember(self)
        wasSet = True
        return wasSet

    def delete(self):
        self._member = None
        placeholderMeeting = self._meeting
        self._meeting = None
        if not (placeholderMeeting is None) :
            placeholderMeeting.removeMeetingWaitlistMember(self)
        placeholderMeetings = self._meetings
        self._meetings = None
        if not (placeholderMeetings is None) :
            placeholderMeetings.removeMeetingWaitlistMember(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "]" + str(os.linesep) + "  " + "decisionChanged" + "=" + str((((self.getDecisionChanged().__str__().replaceAll("  ", "    ")) if not self.getDecisionChanged() == self else "this") if not (self.getDecisionChanged() is None) else "null")) + str(os.linesep) + "  " + "decisionDate" + "=" + str((((self.getDecisionDate().__str__().replaceAll("  ", "    ")) if not self.getDecisionDate() == self else "this") if not (self.getDecisionDate() is None) else "null")) + str(os.linesep) + "  " + "signUpDate" + "=" + str((((self.getSignUpDate().__str__().replaceAll("  ", "    ")) if not self.getSignUpDate() == self else "this") if not (self.getSignUpDate() is None) else "null")) + str(os.linesep) + "  " + "signOffDate" + "=" + str((((self.getSignOffDate().__str__().replaceAll("  ", "    ")) if not self.getSignOffDate() == self else "this") if not (self.getSignOffDate() is None) else "null")) + str(os.linesep) + "  " + "movedToAttendeesDate" + "=" + str((((self.getMovedToAttendeesDate().__str__().replaceAll("  ", "    ")) if not self.getMovedToAttendeesDate() == self else "this") if not (self.getMovedToAttendeesDate() is None) else "null")) + str(os.linesep) + "  " + "isMovedToAttendees" + "=" + str((((self.getIsMovedToAttendees().__str__().replaceAll("  ", "    ")) if not self.getIsMovedToAttendees() == self else "this") if not (self.getIsMovedToAttendees() is None) else "null")) + str(os.linesep) + "  " + "member = " + str(((format(id(self.getMember()), "x")) if not (self.getMember() is None) else "null")) + str(os.linesep) + "  " + "meeting = " + str(((format(id(self.getMeeting()), "x")) if not (self.getMeeting() is None) else "null")) + str(os.linesep) + "  " + "meetings = " + ((format(id(self.getMeetings()), "x")) if not (self.getMeetings() is None) else "null")
