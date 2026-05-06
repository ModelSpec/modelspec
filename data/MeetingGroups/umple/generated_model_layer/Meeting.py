# %% NEW FILE Meeting BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 123 "model.ump"
# line 325 "model.ump"
import os
from datetime import date

class Meeting():
    nextId = 1
    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Meeting Attributes
    #Autounique Attributes
    #Meeting Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aTitle, aDescription, aTerm, aLocation, aMeetingLimit, aRsvpTerm, aCreator, aMeetings):
        self._meetingFees = None
        self._meetingWaitlistMembers = None
        self._meetingNotAttendees = None
        self._meetingAttendees = None
        self._meetings = None
        self._cancelMember = None
        self._changeMember = None
        self._creator = None
        self._rsvpTerm = None
        self._meetingLimit = None
        self._location = None
        self._term = None
        self._id = None
        self._isCanceled = None
        self._cancelDate = None
        self._changeDate = None
        self._createDate = None
        self._description = None
        self._title = None
        self._title = aTitle
        self._description = aDescription
        self._createDate = None
        self._changeDate = None
        self._cancelDate = None
        self._id, Meeting.nextId = Meeting.nextId, Meeting.nextId + 1
        if not self.setTerm(aTerm) :
            raise RuntimeError ("Unable to create Meeting due to aTerm. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        if not self.setLocation(aLocation) :
            raise RuntimeError ("Unable to create Meeting due to aLocation. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        if not self.setMeetingLimit(aMeetingLimit) :
            raise RuntimeError ("Unable to create Meeting due to aMeetingLimit. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        if not self.setRsvpTerm(aRsvpTerm) :
            raise RuntimeError ("Unable to create Meeting due to aRsvpTerm. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        if not self.setCreator(aCreator) :
            raise RuntimeError ("Unable to create Meeting due to aCreator. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddMeetings = self.setMeetings(aMeetings)
        if not didAddMeetings :
            raise RuntimeError ("Unable to create meeting due to meetings. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._meetingAttendees = []
        self._meetingNotAttendees = []
        self._meetingWaitlistMembers = []
        self._meetingFees = []

    #------------------------
    # INTERFACE
    #------------------------
    def setTitle(self, aTitle):
        wasSet = False
        self._title = aTitle
        wasSet = True
        return wasSet

    def setDescription(self, aDescription):
        wasSet = False
        self._description = aDescription
        wasSet = True
        return wasSet

    def setCreateDate(self, aCreateDate):
        wasSet = False
        self._createDate = aCreateDate
        wasSet = True
        return wasSet

    def setChangeDate(self, aChangeDate):
        wasSet = False
        self._changeDate = aChangeDate
        wasSet = True
        return wasSet

    def setCancelDate(self, aCancelDate):
        wasSet = False
        self._cancelDate = aCancelDate
        wasSet = True
        return wasSet

    def setIsCanceled(self, aIsCanceled):
        wasSet = False
        self._isCanceled = aIsCanceled
        wasSet = True
        return wasSet

    def getTitle(self):
        return self._title

    def getDescription(self):
        return self._description

    def getCreateDate(self):
        return self._createDate

    def getChangeDate(self):
        return self._changeDate

    def getCancelDate(self):
        return self._cancelDate

    def getIsCanceled(self):
        return self._isCanceled

    def getId(self):
        return self._id

    # Code from template association_GetOne
    def getTerm(self):
        return self._term

    # Code from template association_GetOne
    def getLocation(self):
        return self._location

    # Code from template association_GetOne
    def getMeetingLimit(self):
        return self._meetingLimit

    # Code from template association_GetOne
    def getRsvpTerm(self):
        return self._rsvpTerm

    # Code from template association_GetOne
    def getCreator(self):
        return self._creator

    # Code from template association_GetOne
    def getChangeMember(self):
        return self._changeMember

    def hasChangeMember(self):
        has = not (self._changeMember is None)
        return has

    # Code from template association_GetOne
    def getCancelMember(self):
        return self._cancelMember

    def hasCancelMember(self):
        has = not (self._cancelMember is None)
        return has

    # Code from template association_GetOne
    def getMeetings(self):
        return self._meetings

    # Code from template association_GetMany
    def getMeetingAttendee(self, index):
        aMeetingAttendee = self._meetingAttendees[index]
        return aMeetingAttendee

    def getMeetingAttendees(self):
        newMeetingAttendees = tuple(self._meetingAttendees)
        return newMeetingAttendees

    def numberOfMeetingAttendees(self):
        number = len(self._meetingAttendees)
        return number

    def hasMeetingAttendees(self):
        has = len(self._meetingAttendees) > 0
        return has

    def indexOfMeetingAttendee(self, aMeetingAttendee):
        index = (-1 if not aMeetingAttendee in self._meetingAttendees else self._meetingAttendees.index(aMeetingAttendee))
        return index

    # Code from template association_GetMany
    def getMeetingNotAttendee(self, index):
        aMeetingNotAttendee = self._meetingNotAttendees[index]
        return aMeetingNotAttendee

    def getMeetingNotAttendees(self):
        newMeetingNotAttendees = tuple(self._meetingNotAttendees)
        return newMeetingNotAttendees

    def numberOfMeetingNotAttendees(self):
        number = len(self._meetingNotAttendees)
        return number

    def hasMeetingNotAttendees(self):
        has = len(self._meetingNotAttendees) > 0
        return has

    def indexOfMeetingNotAttendee(self, aMeetingNotAttendee):
        index = (-1 if not aMeetingNotAttendee in self._meetingNotAttendees else self._meetingNotAttendees.index(aMeetingNotAttendee))
        return index

    # Code from template association_GetMany
    def getMeetingWaitlistMember(self, index):
        aMeetingWaitlistMember = self._meetingWaitlistMembers[index]
        return aMeetingWaitlistMember

    def getMeetingWaitlistMembers(self):
        newMeetingWaitlistMembers = tuple(self._meetingWaitlistMembers)
        return newMeetingWaitlistMembers

    def numberOfMeetingWaitlistMembers(self):
        number = len(self._meetingWaitlistMembers)
        return number

    def hasMeetingWaitlistMembers(self):
        has = len(self._meetingWaitlistMembers) > 0
        return has

    def indexOfMeetingWaitlistMember(self, aMeetingWaitlistMember):
        index = (-1 if not aMeetingWaitlistMember in self._meetingWaitlistMembers else self._meetingWaitlistMembers.index(aMeetingWaitlistMember))
        return index

    # Code from template association_GetMany
    def getMeetingFee(self, index):
        aMeetingFee = self._meetingFees[index]
        return aMeetingFee

    def getMeetingFees(self):
        newMeetingFees = tuple(self._meetingFees)
        return newMeetingFees

    def numberOfMeetingFees(self):
        number = len(self._meetingFees)
        return number

    def hasMeetingFees(self):
        has = len(self._meetingFees) > 0
        return has

    def indexOfMeetingFee(self, aMeetingFee):
        index = (-1 if not aMeetingFee in self._meetingFees else self._meetingFees.index(aMeetingFee))
        return index

    # Code from template association_SetUnidirectionalOne
    def setTerm(self, aNewTerm):
        wasSet = False
        if not (aNewTerm is None) :
            self._term = aNewTerm
            wasSet = True
        return wasSet

    # Code from template association_SetUnidirectionalOne
    def setLocation(self, aNewLocation):
        wasSet = False
        if not (aNewLocation is None) :
            self._location = aNewLocation
            wasSet = True
        return wasSet

    # Code from template association_SetUnidirectionalOne
    def setMeetingLimit(self, aNewMeetingLimit):
        wasSet = False
        if not (aNewMeetingLimit is None) :
            self._meetingLimit = aNewMeetingLimit
            wasSet = True
        return wasSet

    # Code from template association_SetUnidirectionalOne
    def setRsvpTerm(self, aNewRsvpTerm):
        wasSet = False
        if not (aNewRsvpTerm is None) :
            self._rsvpTerm = aNewRsvpTerm
            wasSet = True
        return wasSet

    # Code from template association_SetUnidirectionalOne
    def setCreator(self, aNewCreator):
        wasSet = False
        if not (aNewCreator is None) :
            self._creator = aNewCreator
            wasSet = True
        return wasSet

    # Code from template association_SetUnidirectionalOptionalOne
    def setChangeMember(self, aNewChangeMember):
        wasSet = False
        self._changeMember = aNewChangeMember
        wasSet = True
        return wasSet

    # Code from template association_SetUnidirectionalOptionalOne
    def setCancelMember(self, aNewCancelMember):
        wasSet = False
        self._cancelMember = aNewCancelMember
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
            existingMeetings.removeMeeting(self)
        self._meetings.addMeeting(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfMeetingAttendees():
        return 0

    # Code from template association_AddManyToOne
    def addMeetingAttendee1(self, aGuestNumber, aDecisionDate, aRole, aAttendee, aMeetings):
        from .MeetingAttendee import MeetingAttendee
        return MeetingAttendee(aGuestNumber, aDecisionDate, aRole, aAttendee, self, aMeetings)

    def addMeetingAttendee2(self, aMeetingAttendee):
        wasAdded = False
        if (aMeetingAttendee) in self._meetingAttendees :
            return False
        existingMeeting = aMeetingAttendee.getMeeting()
        isNewMeeting = not (existingMeeting is None) and not self == existingMeeting
        if isNewMeeting :
            aMeetingAttendee.setMeeting(self)
        else :
            self._meetingAttendees.append(aMeetingAttendee)
        wasAdded = True
        return wasAdded

    def removeMeetingAttendee(self, aMeetingAttendee):
        wasRemoved = False
        #Unable to remove aMeetingAttendee, as it must always have a meeting
        if not self == aMeetingAttendee.getMeeting() :
            self._meetingAttendees.remove(aMeetingAttendee)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addMeetingAttendeeAt(self, aMeetingAttendee, index):
        wasAdded = False
        if self.addMeetingAttendee(aMeetingAttendee) :
            if index < 0 :
                index = 0
            if index > self.numberOfMeetingAttendees() :
                index = self.numberOfMeetingAttendees() - 1
            self._meetingAttendees.remove(aMeetingAttendee)
            self._meetingAttendees.insert(index, aMeetingAttendee)
            wasAdded = True
        return wasAdded

    def addOrMoveMeetingAttendeeAt(self, aMeetingAttendee, index):
        wasAdded = False
        if (aMeetingAttendee) in self._meetingAttendees :
            if index < 0 :
                index = 0
            if index > self.numberOfMeetingAttendees() :
                index = self.numberOfMeetingAttendees() - 1
            self._meetingAttendees.remove(aMeetingAttendee)
            self._meetingAttendees.insert(index, aMeetingAttendee)
            wasAdded = True
        else :
            wasAdded = self.addMeetingAttendeeAt(aMeetingAttendee, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfMeetingNotAttendees():
        return 0

    # Code from template association_AddManyToOne
    def addMeetingNotAttendee1(self, aDecisionDate, aMember, aMeetings):
        from .MeetingNotAttendee import MeetingNotAttendee
        return MeetingNotAttendee(aDecisionDate, aMember, self, aMeetings)

    def addMeetingNotAttendee2(self, aMeetingNotAttendee):
        wasAdded = False
        if (aMeetingNotAttendee) in self._meetingNotAttendees :
            return False
        existingMeeting = aMeetingNotAttendee.getMeeting()
        isNewMeeting = not (existingMeeting is None) and not self == existingMeeting
        if isNewMeeting :
            aMeetingNotAttendee.setMeeting(self)
        else :
            self._meetingNotAttendees.append(aMeetingNotAttendee)
        wasAdded = True
        return wasAdded

    def removeMeetingNotAttendee(self, aMeetingNotAttendee):
        wasRemoved = False
        #Unable to remove aMeetingNotAttendee, as it must always have a meeting
        if not self == aMeetingNotAttendee.getMeeting() :
            self._meetingNotAttendees.remove(aMeetingNotAttendee)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addMeetingNotAttendeeAt(self, aMeetingNotAttendee, index):
        wasAdded = False
        if self.addMeetingNotAttendee(aMeetingNotAttendee) :
            if index < 0 :
                index = 0
            if index > self.numberOfMeetingNotAttendees() :
                index = self.numberOfMeetingNotAttendees() - 1
            self._meetingNotAttendees.remove(aMeetingNotAttendee)
            self._meetingNotAttendees.insert(index, aMeetingNotAttendee)
            wasAdded = True
        return wasAdded

    def addOrMoveMeetingNotAttendeeAt(self, aMeetingNotAttendee, index):
        wasAdded = False
        if (aMeetingNotAttendee) in self._meetingNotAttendees :
            if index < 0 :
                index = 0
            if index > self.numberOfMeetingNotAttendees() :
                index = self.numberOfMeetingNotAttendees() - 1
            self._meetingNotAttendees.remove(aMeetingNotAttendee)
            self._meetingNotAttendees.insert(index, aMeetingNotAttendee)
            wasAdded = True
        else :
            wasAdded = self.addMeetingNotAttendeeAt(aMeetingNotAttendee, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfMeetingWaitlistMembers():
        return 0

    # Code from template association_AddManyToOne
    def addMeetingWaitlistMember1(self, aDecisionDate, aMember, aMeetings):
        from .MeetingWaitlistMember import MeetingWaitlistMember
        return MeetingWaitlistMember(aDecisionDate, aMember, self, aMeetings)

    def addMeetingWaitlistMember2(self, aMeetingWaitlistMember):
        wasAdded = False
        if (aMeetingWaitlistMember) in self._meetingWaitlistMembers :
            return False
        existingMeeting = aMeetingWaitlistMember.getMeeting()
        isNewMeeting = not (existingMeeting is None) and not self == existingMeeting
        if isNewMeeting :
            aMeetingWaitlistMember.setMeeting(self)
        else :
            self._meetingWaitlistMembers.append(aMeetingWaitlistMember)
        wasAdded = True
        return wasAdded

    def removeMeetingWaitlistMember(self, aMeetingWaitlistMember):
        wasRemoved = False
        #Unable to remove aMeetingWaitlistMember, as it must always have a meeting
        if not self == aMeetingWaitlistMember.getMeeting() :
            self._meetingWaitlistMembers.remove(aMeetingWaitlistMember)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addMeetingWaitlistMemberAt(self, aMeetingWaitlistMember, index):
        wasAdded = False
        if self.addMeetingWaitlistMember(aMeetingWaitlistMember) :
            if index < 0 :
                index = 0
            if index > self.numberOfMeetingWaitlistMembers() :
                index = self.numberOfMeetingWaitlistMembers() - 1
            self._meetingWaitlistMembers.remove(aMeetingWaitlistMember)
            self._meetingWaitlistMembers.insert(index, aMeetingWaitlistMember)
            wasAdded = True
        return wasAdded

    def addOrMoveMeetingWaitlistMemberAt(self, aMeetingWaitlistMember, index):
        wasAdded = False
        if (aMeetingWaitlistMember) in self._meetingWaitlistMembers :
            if index < 0 :
                index = 0
            if index > self.numberOfMeetingWaitlistMembers() :
                index = self.numberOfMeetingWaitlistMembers() - 1
            self._meetingWaitlistMembers.remove(aMeetingWaitlistMember)
            self._meetingWaitlistMembers.insert(index, aMeetingWaitlistMember)
            wasAdded = True
        else :
            wasAdded = self.addMeetingWaitlistMemberAt(aMeetingWaitlistMember, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfMeetingFees():
        return 0

    # Code from template association_AddManyToOne
    def addMeetingFee1(self, aPayer, aValue, aPayments):
        from .MeetingFee import MeetingFee
        return MeetingFee(aPayer, self, aValue, aPayments)

    def addMeetingFee2(self, aMeetingFee):
        wasAdded = False
        if (aMeetingFee) in self._meetingFees :
            return False
        existingMeeting = aMeetingFee.getMeeting()
        isNewMeeting = not (existingMeeting is None) and not self == existingMeeting
        if isNewMeeting :
            aMeetingFee.setMeeting(self)
        else :
            self._meetingFees.append(aMeetingFee)
        wasAdded = True
        return wasAdded

    def removeMeetingFee(self, aMeetingFee):
        wasRemoved = False
        #Unable to remove aMeetingFee, as it must always have a meeting
        if not self == aMeetingFee.getMeeting() :
            self._meetingFees.remove(aMeetingFee)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addMeetingFeeAt(self, aMeetingFee, index):
        wasAdded = False
        if self.addMeetingFee(aMeetingFee) :
            if index < 0 :
                index = 0
            if index > self.numberOfMeetingFees() :
                index = self.numberOfMeetingFees() - 1
            self._meetingFees.remove(aMeetingFee)
            self._meetingFees.insert(index, aMeetingFee)
            wasAdded = True
        return wasAdded

    def addOrMoveMeetingFeeAt(self, aMeetingFee, index):
        wasAdded = False
        if (aMeetingFee) in self._meetingFees :
            if index < 0 :
                index = 0
            if index > self.numberOfMeetingFees() :
                index = self.numberOfMeetingFees() - 1
            self._meetingFees.remove(aMeetingFee)
            self._meetingFees.insert(index, aMeetingFee)
            wasAdded = True
        else :
            wasAdded = self.addMeetingFeeAt(aMeetingFee, index)
        return wasAdded

    def delete(self):
        self._term = None
        self._location = None
        self._meetingLimit = None
        self._rsvpTerm = None
        self._creator = None
        self._changeMember = None
        self._cancelMember = None
        placeholderMeetings = self._meetings
        self._meetings = None
        if not (placeholderMeetings is None) :
            placeholderMeetings.removeMeeting(self)
        i = len(self._meetingAttendees)
        while i > 0 :
            aMeetingAttendee = self._meetingAttendees[i - 1]
            aMeetingAttendee.delete()
            i -= 1

        i = len(self._meetingNotAttendees)
        while i > 0 :
            aMeetingNotAttendee = self._meetingNotAttendees[i - 1]
            aMeetingNotAttendee.delete()
            i -= 1

        i = len(self._meetingWaitlistMembers)
        while i > 0 :
            aMeetingWaitlistMember = self._meetingWaitlistMembers[i - 1]
            aMeetingWaitlistMember.delete()
            i -= 1

        i = len(self._meetingFees)
        while i > 0 :
            aMeetingFee = self._meetingFees[i - 1]
            aMeetingFee.delete()
            i -= 1

    def __str__(self):
        return str(super().__str__()) + "[" + "id" + ":" + str(self.getId()) + "," + "title" + ":" + str(self.getTitle()) + "," + "description" + ":" + str(self.getDescription()) + "]" + str(os.linesep) + "  " + "createDate" + "=" + str((((self.getCreateDate().__str__().replaceAll("  ", "    ")) if not self.getCreateDate() == self else "this") if not (self.getCreateDate() is None) else "null")) + str(os.linesep) + "  " + "changeDate" + "=" + str((((self.getChangeDate().__str__().replaceAll("  ", "    ")) if not self.getChangeDate() == self else "this") if not (self.getChangeDate() is None) else "null")) + str(os.linesep) + "  " + "cancelDate" + "=" + str((((self.getCancelDate().__str__().replaceAll("  ", "    ")) if not self.getCancelDate() == self else "this") if not (self.getCancelDate() is None) else "null")) + str(os.linesep) + "  " + "isCanceled" + "=" + str((((self.getIsCanceled().__str__().replaceAll("  ", "    ")) if not self.getIsCanceled() == self else "this") if not (self.getIsCanceled() is None) else "null")) + str(os.linesep) + "  " + "term = " + str(((format(id(self.getTerm()), "x")) if not (self.getTerm() is None) else "null")) + str(os.linesep) + "  " + "location = " + str(((format(id(self.getLocation()), "x")) if not (self.getLocation() is None) else "null")) + str(os.linesep) + "  " + "meetingLimit = " + str(((format(id(self.getMeetingLimit()), "x")) if not (self.getMeetingLimit() is None) else "null")) + str(os.linesep) + "  " + "rsvpTerm = " + str(((format(id(self.getRsvpTerm()), "x")) if not (self.getRsvpTerm() is None) else "null")) + str(os.linesep) + "  " + "creator = " + str(((format(id(self.getCreator()), "x")) if not (self.getCreator() is None) else "null")) + str(os.linesep) + "  " + "changeMember = " + str(((format(id(self.getChangeMember()), "x")) if not (self.getChangeMember() is None) else "null")) + str(os.linesep) + "  " + "cancelMember = " + str(((format(id(self.getCancelMember()), "x")) if not (self.getCancelMember() is None) else "null")) + str(os.linesep) + "  " + "meetings = " + ((format(id(self.getMeetings()), "x")) if not (self.getMeetings() is None) else "null")

    def addMeetingAttendee(self, *argv):
        from .MeetingAttendee import MeetingAttendee
        from .Meetings import Meetings
        from .Member import Member
        if len(argv) == 5 and isinstance(argv[0], int) and isinstance(argv[1], date) and isinstance(argv[2], MeetingAttendee.MeetingAttendeeRole) and isinstance(argv[3], Member) and isinstance(argv[4], Meetings) :
            return self.addMeetingAttendee1(argv[0], argv[1], argv[2], argv[3], argv[4])
        if len(argv) == 1 and isinstance(argv[0], MeetingAttendee) :
            return self.addMeetingAttendee2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addMeetingNotAttendee(self, *argv):
        from .MeetingNotAttendee import MeetingNotAttendee
        from .Meetings import Meetings
        from .Member import Member
        if len(argv) == 3 and isinstance(argv[0], date) and isinstance(argv[1], Member) and isinstance(argv[2], Meetings) :
            return self.addMeetingNotAttendee1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], MeetingNotAttendee) :
            return self.addMeetingNotAttendee2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addMeetingWaitlistMember(self, *argv):
        from .MeetingWaitlistMember import MeetingWaitlistMember
        from .Meetings import Meetings
        from .Member import Member
        if len(argv) == 3 and isinstance(argv[0], date) and isinstance(argv[1], Member) and isinstance(argv[2], Meetings) :
            return self.addMeetingWaitlistMember1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], MeetingWaitlistMember) :
            return self.addMeetingWaitlistMember2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addMeetingFee(self, *argv):
        from .MeetingFee import MeetingFee
        from .Member import Member
        from .MoneyValue import MoneyValue
        from .Payments import Payments
        if len(argv) == 3 and isinstance(argv[0], Member) and isinstance(argv[1], MoneyValue) and isinstance(argv[2], Payments) :
            return self.addMeetingFee1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], MeetingFee) :
            return self.addMeetingFee2(argv[0])
        raise TypeError("No method matches provided parameters")
