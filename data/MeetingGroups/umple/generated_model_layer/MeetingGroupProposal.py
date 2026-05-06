# %% NEW FILE MeetingGroupProposal BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 67 "model.ump"
# line 290 "model.ump"
import os
from enum import Enum, auto

class MeetingGroupProposal():
    nextId = 1
    #------------------------
    # ENUMERATIONS
    #------------------------
    class MeetingGroupProposalStatus(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name
        def __str__(self):
            return str(self.value)
        ToVerify = auto()
        Verified = auto()
        Rejected = auto()

    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #MeetingGroupProposal Attributes
    #Autounique Attributes
    #MeetingGroupProposal Associations
    #Helper Variables
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aName, aDescription, aMeetingGroupLocation, aMember, aMeetings):
        self._canSetProposalDate = None
        self._decisions = None
        self._meetings = None
        self._member = None
        self._meetingGroupLocation = None
        self._id = None
        self._status = None
        self._proposalDate = None
        self._description = None
        self._name = None
        self._name = aName
        self._description = aDescription
        self._canSetProposalDate = True
        self._id, MeetingGroupProposal.nextId = MeetingGroupProposal.nextId, MeetingGroupProposal.nextId + 1
        if not self.setMeetingGroupLocation(aMeetingGroupLocation) :
            raise RuntimeError ("Unable to create MeetingGroupProposal due to aMeetingGroupLocation. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddMember = self.setMember(aMember)
        if not didAddMember :
            raise RuntimeError ("Unable to create meetingGroupProposal due to member. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddMeetings = self.setMeetings(aMeetings)
        if not didAddMeetings :
            raise RuntimeError ("Unable to create meetingGroupProposal due to meetings. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._decisions = []

    #------------------------
    # INTERFACE
    #------------------------
    def setName(self, aName):
        wasSet = False
        self._name = aName
        wasSet = True
        return wasSet

    def setDescription(self, aDescription):
        wasSet = False
        self._description = aDescription
        wasSet = True
        return wasSet

    # Code from template attribute_SetImmutable
    def setProposalDate(self, aProposalDate):
        wasSet = False
        if not self._canSetProposalDate :
            return False
        self._canSetProposalDate = False
        self._proposalDate = aProposalDate
        wasSet = True
        return wasSet

    def setStatus(self, aStatus):
        wasSet = False
        self._status = aStatus
        wasSet = True
        return wasSet

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

    def getProposalDate(self):
        return self._proposalDate

    def getStatus(self):
        return self._status

    def getId(self):
        return self._id

    # Code from template association_GetOne
    def getMeetingGroupLocation(self):
        return self._meetingGroupLocation

    # Code from template association_GetOne
    def getMember(self):
        return self._member

    # Code from template association_GetOne
    def getMeetings(self):
        return self._meetings

    # Code from template association_GetMany
    def getDecision(self, index):
        aDecision = self._decisions[index]
        return aDecision

    def getDecisions(self):
        newDecisions = tuple(self._decisions)
        return newDecisions

    def numberOfDecisions(self):
        number = len(self._decisions)
        return number

    def hasDecisions(self):
        has = len(self._decisions) > 0
        return has

    def indexOfDecision(self, aDecision):
        index = (-1 if not aDecision in self._decisions else self._decisions.index(aDecision))
        return index

    # Code from template association_SetUnidirectionalOne
    def setMeetingGroupLocation(self, aNewMeetingGroupLocation):
        wasSet = False
        if not (aNewMeetingGroupLocation is None) :
            self._meetingGroupLocation = aNewMeetingGroupLocation
            wasSet = True
        return wasSet

    # Code from template association_SetOneToMany
    def setMember(self, aMember):
        wasSet = False
        if aMember is None :
            return wasSet
        existingMember = self._member
        self._member = aMember
        if not (existingMember is None) and not existingMember == aMember :
            existingMember.removeMeetingGroupProposal(self)
        self._member.addMeetingGroupProposal(self)
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
            existingMeetings.removeMeetingGroupProposal(self)
        self._meetings.addMeetingGroupProposal(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfDecisions():
        return 0

    # Code from template association_AddManyToOne
    def addDecision1(self, aRejectReason, aCode, aAdministrator):
        from .MeetingGroupProposalDecision import MeetingGroupProposalDecision
        return MeetingGroupProposalDecision(aRejectReason, aCode, self, aAdministrator)

    def addDecision2(self, aDecision):
        wasAdded = False
        if (aDecision) in self._decisions :
            return False
        existingProposal = aDecision.getProposal()
        isNewProposal = not (existingProposal is None) and not self == existingProposal
        if isNewProposal :
            aDecision.setProposal(self)
        else :
            self._decisions.append(aDecision)
        wasAdded = True
        return wasAdded

    def removeDecision(self, aDecision):
        wasRemoved = False
        #Unable to remove aDecision, as it must always have a proposal
        if not self == aDecision.getProposal() :
            self._decisions.remove(aDecision)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addDecisionAt(self, aDecision, index):
        wasAdded = False
        if self.addDecision(aDecision) :
            if index < 0 :
                index = 0
            if index > self.numberOfDecisions() :
                index = self.numberOfDecisions() - 1
            self._decisions.remove(aDecision)
            self._decisions.insert(index, aDecision)
            wasAdded = True
        return wasAdded

    def addOrMoveDecisionAt(self, aDecision, index):
        wasAdded = False
        if (aDecision) in self._decisions :
            if index < 0 :
                index = 0
            if index > self.numberOfDecisions() :
                index = self.numberOfDecisions() - 1
            self._decisions.remove(aDecision)
            self._decisions.insert(index, aDecision)
            wasAdded = True
        else :
            wasAdded = self.addDecisionAt(aDecision, index)
        return wasAdded

    def delete(self):
        self._meetingGroupLocation = None
        placeholderMember = self._member
        self._member = None
        if not (placeholderMember is None) :
            placeholderMember.removeMeetingGroupProposal(self)
        placeholderMeetings = self._meetings
        self._meetings = None
        if not (placeholderMeetings is None) :
            placeholderMeetings.removeMeetingGroupProposal(self)
        i = len(self._decisions)
        while i > 0 :
            aDecision = self._decisions[i - 1]
            aDecision.delete()
            i -= 1

    def __str__(self):
        return str(super().__str__()) + "[" + "id" + ":" + str(self.getId()) + "," + "name" + ":" + str(self.getName()) + "," + "description" + ":" + str(self.getDescription()) + "]" + str(os.linesep) + "  " + "proposalDate" + "=" + str((((self.getProposalDate().__str__().replaceAll("  ", "    ")) if not self.getProposalDate() == self else "this") if not (self.getProposalDate() is None) else "null")) + str(os.linesep) + "  " + "status" + "=" + str((((self.getStatus().__str__().replaceAll("  ", "    ")) if not self.getStatus() == self else "this") if not (self.getStatus() is None) else "null")) + str(os.linesep) + "  " + "meetingGroupLocation = " + str(((format(id(self.getMeetingGroupLocation()), "x")) if not (self.getMeetingGroupLocation() is None) else "null")) + str(os.linesep) + "  " + "member = " + str(((format(id(self.getMember()), "x")) if not (self.getMember() is None) else "null")) + str(os.linesep) + "  " + "meetings = " + ((format(id(self.getMeetings()), "x")) if not (self.getMeetings() is None) else "null")

    def addDecision(self, *argv):
        from .MeetingGroupProposalDecision import MeetingGroupProposalDecision
        from .Administrator import Administrator
        if len(argv) == 3 and isinstance(argv[0], str) and isinstance(argv[1], MeetingGroupProposalDecision.MeetingGroupProposalDecisionCode) and isinstance(argv[2], Administrator) :
            return self.addDecision1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], MeetingGroupProposalDecision) :
            return self.addDecision2(argv[0])
        raise TypeError("No method matches provided parameters")
