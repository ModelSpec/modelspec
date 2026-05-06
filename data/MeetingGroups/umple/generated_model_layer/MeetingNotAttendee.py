# %% NEW FILE MeetingNotAttendee BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 157 "model.ump"
# line 335 "model.ump"
import os

class MeetingNotAttendee():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #MeetingNotAttendee Attributes
    #MeetingNotAttendee Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aDecisionDate, aMember, aMeeting, aMeetings):
        self._meetings = None
        self._meeting = None
        self._member = None
        self._decisionChangeDate = None
        self._decisionDate = None
        self._decisionChanged = None
        self._decisionDate = aDecisionDate
        self._decisionChangeDate = None
        if not self.setMember(aMember) :
            raise RuntimeError ("Unable to create MeetingNotAttendee due to aMember. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddMeeting = self.setMeeting(aMeeting)
        if not didAddMeeting :
            raise RuntimeError ("Unable to create meetingNotAttendee due to meeting. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddMeetings = self.setMeetings(aMeetings)
        if not didAddMeetings :
            raise RuntimeError ("Unable to create meetingNotAttendee due to meetings. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

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

    def setDecisionChangeDate(self, aDecisionChangeDate):
        wasSet = False
        self._decisionChangeDate = aDecisionChangeDate
        wasSet = True
        return wasSet

    def getDecisionChanged(self):
        return self._decisionChanged

    def getDecisionDate(self):
        return self._decisionDate

    def getDecisionChangeDate(self):
        return self._decisionChangeDate

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
            existingMeeting.removeMeetingNotAttendee(self)
        self._meeting.addMeetingNotAttendee(self)
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
            existingMeetings.removeMeetingNotAttendee(self)
        self._meetings.addMeetingNotAttendee(self)
        wasSet = True
        return wasSet

    def delete(self):
        self._member = None
        placeholderMeeting = self._meeting
        self._meeting = None
        if not (placeholderMeeting is None) :
            placeholderMeeting.removeMeetingNotAttendee(self)
        placeholderMeetings = self._meetings
        self._meetings = None
        if not (placeholderMeetings is None) :
            placeholderMeetings.removeMeetingNotAttendee(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "]" + str(os.linesep) + "  " + "decisionChanged" + "=" + str((((self.getDecisionChanged().__str__().replaceAll("  ", "    ")) if not self.getDecisionChanged() == self else "this") if not (self.getDecisionChanged() is None) else "null")) + str(os.linesep) + "  " + "decisionDate" + "=" + str((((self.getDecisionDate().__str__().replaceAll("  ", "    ")) if not self.getDecisionDate() == self else "this") if not (self.getDecisionDate() is None) else "null")) + str(os.linesep) + "  " + "decisionChangeDate" + "=" + str((((self.getDecisionChangeDate().__str__().replaceAll("  ", "    ")) if not self.getDecisionChangeDate() == self else "this") if not (self.getDecisionChangeDate() is None) else "null")) + str(os.linesep) + "  " + "member = " + str(((format(id(self.getMember()), "x")) if not (self.getMember() is None) else "null")) + str(os.linesep) + "  " + "meeting = " + str(((format(id(self.getMeeting()), "x")) if not (self.getMeeting() is None) else "null")) + str(os.linesep) + "  " + "meetings = " + ((format(id(self.getMeetings()), "x")) if not (self.getMeetings() is None) else "null")
