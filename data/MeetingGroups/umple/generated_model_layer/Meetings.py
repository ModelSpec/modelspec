# %% NEW FILE Meetings BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 11 "model.ump"
# line 255 "model.ump"
from datetime import date

class Meetings():
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Meetings Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self):
        self._meetingWaitlistMembers = None
        self._meetingNotAttendees = None
        self._meetingAttendees = None
        self._meetingLocations = None
        self._meetings = None
        self._meetingGroups = None
        self._meetingGroupProposals = None
        self._members = None
        self._members = []
        self._meetingGroupProposals = []
        self._meetingGroups = []
        self._meetings = []
        self._meetingLocations = []
        self._meetingAttendees = []
        self._meetingNotAttendees = []
        self._meetingWaitlistMembers = []

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetMany
    def getMember(self, index):
        aMember = self._members[index]
        return aMember

    def getMembers(self):
        newMembers = tuple(self._members)
        return newMembers

    def numberOfMembers(self):
        number = len(self._members)
        return number

    def hasMembers(self):
        has = len(self._members) > 0
        return has

    def indexOfMember(self, aMember):
        index = (-1 if not aMember in self._members else self._members.index(aMember))
        return index

    # Code from template association_GetMany
    def getMeetingGroupProposal(self, index):
        aMeetingGroupProposal = self._meetingGroupProposals[index]
        return aMeetingGroupProposal

    def getMeetingGroupProposals(self):
        newMeetingGroupProposals = tuple(self._meetingGroupProposals)
        return newMeetingGroupProposals

    def numberOfMeetingGroupProposals(self):
        number = len(self._meetingGroupProposals)
        return number

    def hasMeetingGroupProposals(self):
        has = len(self._meetingGroupProposals) > 0
        return has

    def indexOfMeetingGroupProposal(self, aMeetingGroupProposal):
        index = (-1 if not aMeetingGroupProposal in self._meetingGroupProposals else self._meetingGroupProposals.index(aMeetingGroupProposal))
        return index

    # Code from template association_GetMany
    def getMeetingGroup(self, index):
        aMeetingGroup = self._meetingGroups[index]
        return aMeetingGroup

    def getMeetingGroups(self):
        newMeetingGroups = tuple(self._meetingGroups)
        return newMeetingGroups

    def numberOfMeetingGroups(self):
        number = len(self._meetingGroups)
        return number

    def hasMeetingGroups(self):
        has = len(self._meetingGroups) > 0
        return has

    def indexOfMeetingGroup(self, aMeetingGroup):
        index = (-1 if not aMeetingGroup in self._meetingGroups else self._meetingGroups.index(aMeetingGroup))
        return index

    # Code from template association_GetMany
    def getMeeting(self, index):
        aMeeting = self._meetings[index]
        return aMeeting

    def getMeetings(self):
        newMeetings = tuple(self._meetings)
        return newMeetings

    def numberOfMeetings(self):
        number = len(self._meetings)
        return number

    def hasMeetings(self):
        has = len(self._meetings) > 0
        return has

    def indexOfMeeting(self, aMeeting):
        index = (-1 if not aMeeting in self._meetings else self._meetings.index(aMeeting))
        return index

    # Code from template association_GetMany
    def getMeetingLocation(self, index):
        aMeetingLocation = self._meetingLocations[index]
        return aMeetingLocation

    def getMeetingLocations(self):
        newMeetingLocations = tuple(self._meetingLocations)
        return newMeetingLocations

    def numberOfMeetingLocations(self):
        number = len(self._meetingLocations)
        return number

    def hasMeetingLocations(self):
        has = len(self._meetingLocations) > 0
        return has

    def indexOfMeetingLocation(self, aMeetingLocation):
        index = (-1 if not aMeetingLocation in self._meetingLocations else self._meetingLocations.index(aMeetingLocation))
        return index

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

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfMembers():
        return 0

    # Code from template association_AddManyToOne
    def addMember1(self, aId, aLogin, aEmail, aFirstName, aLastName, aName, aUserAccess):
        from .Member import Member
        return Member(aId, aLogin, aEmail, aFirstName, aLastName, aName, aUserAccess, self)

    def addMember2(self, aMember):
        wasAdded = False
        if (aMember) in self._members :
            return False
        existingMeetings = aMember.getMeetings()
        isNewMeetings = not (existingMeetings is None) and not self == existingMeetings
        if isNewMeetings :
            aMember.setMeetings(self)
        else :
            self._members.append(aMember)
        wasAdded = True
        return wasAdded

    def removeMember(self, aMember):
        wasRemoved = False
        #Unable to remove aMember, as it must always have a meetings
        if not self == aMember.getMeetings() :
            self._members.remove(aMember)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addMemberAt(self, aMember, index):
        wasAdded = False
        if self.addMember(aMember) :
            if index < 0 :
                index = 0
            if index > self.numberOfMembers() :
                index = self.numberOfMembers() - 1
            self._members.remove(aMember)
            self._members.insert(index, aMember)
            wasAdded = True
        return wasAdded

    def addOrMoveMemberAt(self, aMember, index):
        wasAdded = False
        if (aMember) in self._members :
            if index < 0 :
                index = 0
            if index > self.numberOfMembers() :
                index = self.numberOfMembers() - 1
            self._members.remove(aMember)
            self._members.insert(index, aMember)
            wasAdded = True
        else :
            wasAdded = self.addMemberAt(aMember, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfMeetingGroupProposals():
        return 0

    # Code from template association_AddManyToOne
    def addMeetingGroupProposal1(self, aName, aDescription, aMeetingGroupLocation, aMember):
        from .MeetingGroupProposal import MeetingGroupProposal
        return MeetingGroupProposal(aName, aDescription, aMeetingGroupLocation, aMember, self)

    def addMeetingGroupProposal2(self, aMeetingGroupProposal):
        wasAdded = False
        if (aMeetingGroupProposal) in self._meetingGroupProposals :
            return False
        existingMeetings = aMeetingGroupProposal.getMeetings()
        isNewMeetings = not (existingMeetings is None) and not self == existingMeetings
        if isNewMeetings :
            aMeetingGroupProposal.setMeetings(self)
        else :
            self._meetingGroupProposals.append(aMeetingGroupProposal)
        wasAdded = True
        return wasAdded

    def removeMeetingGroupProposal(self, aMeetingGroupProposal):
        wasRemoved = False
        #Unable to remove aMeetingGroupProposal, as it must always have a meetings
        if not self == aMeetingGroupProposal.getMeetings() :
            self._meetingGroupProposals.remove(aMeetingGroupProposal)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addMeetingGroupProposalAt(self, aMeetingGroupProposal, index):
        wasAdded = False
        if self.addMeetingGroupProposal(aMeetingGroupProposal) :
            if index < 0 :
                index = 0
            if index > self.numberOfMeetingGroupProposals() :
                index = self.numberOfMeetingGroupProposals() - 1
            self._meetingGroupProposals.remove(aMeetingGroupProposal)
            self._meetingGroupProposals.insert(index, aMeetingGroupProposal)
            wasAdded = True
        return wasAdded

    def addOrMoveMeetingGroupProposalAt(self, aMeetingGroupProposal, index):
        wasAdded = False
        if (aMeetingGroupProposal) in self._meetingGroupProposals :
            if index < 0 :
                index = 0
            if index > self.numberOfMeetingGroupProposals() :
                index = self.numberOfMeetingGroupProposals() - 1
            self._meetingGroupProposals.remove(aMeetingGroupProposal)
            self._meetingGroupProposals.insert(index, aMeetingGroupProposal)
            wasAdded = True
        else :
            wasAdded = self.addMeetingGroupProposalAt(aMeetingGroupProposal, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfMeetingGroups():
        return 0

    # Code from template association_AddManyToOne
    def addMeetingGroup1(self, aId, aName, aDescription, aMeetingGroupLocation, aCreator):
        from .MeetingGroup import MeetingGroup
        return MeetingGroup(aId, aName, aDescription, aMeetingGroupLocation, aCreator, self)

    def addMeetingGroup2(self, aMeetingGroup):
        wasAdded = False
        if (aMeetingGroup) in self._meetingGroups :
            return False
        existingMeetings = aMeetingGroup.getMeetings()
        isNewMeetings = not (existingMeetings is None) and not self == existingMeetings
        if isNewMeetings :
            aMeetingGroup.setMeetings(self)
        else :
            self._meetingGroups.append(aMeetingGroup)
        wasAdded = True
        return wasAdded

    def removeMeetingGroup(self, aMeetingGroup):
        wasRemoved = False
        #Unable to remove aMeetingGroup, as it must always have a meetings
        if not self == aMeetingGroup.getMeetings() :
            self._meetingGroups.remove(aMeetingGroup)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addMeetingGroupAt(self, aMeetingGroup, index):
        wasAdded = False
        if self.addMeetingGroup(aMeetingGroup) :
            if index < 0 :
                index = 0
            if index > self.numberOfMeetingGroups() :
                index = self.numberOfMeetingGroups() - 1
            self._meetingGroups.remove(aMeetingGroup)
            self._meetingGroups.insert(index, aMeetingGroup)
            wasAdded = True
        return wasAdded

    def addOrMoveMeetingGroupAt(self, aMeetingGroup, index):
        wasAdded = False
        if (aMeetingGroup) in self._meetingGroups :
            if index < 0 :
                index = 0
            if index > self.numberOfMeetingGroups() :
                index = self.numberOfMeetingGroups() - 1
            self._meetingGroups.remove(aMeetingGroup)
            self._meetingGroups.insert(index, aMeetingGroup)
            wasAdded = True
        else :
            wasAdded = self.addMeetingGroupAt(aMeetingGroup, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfMeetings():
        return 0

    # Code from template association_AddManyToOne
    def addMeeting1(self, aTitle, aDescription, aTerm, aLocation, aMeetingLimit, aRsvpTerm, aCreator):
        from .Meeting import Meeting
        return Meeting(aTitle, aDescription, aTerm, aLocation, aMeetingLimit, aRsvpTerm, aCreator, self)

    def addMeeting2(self, aMeeting):
        wasAdded = False
        if (aMeeting) in self._meetings :
            return False
        existingMeetings = aMeeting.getMeetings()
        isNewMeetings = not (existingMeetings is None) and not self == existingMeetings
        if isNewMeetings :
            aMeeting.setMeetings(self)
        else :
            self._meetings.append(aMeeting)
        wasAdded = True
        return wasAdded

    def removeMeeting(self, aMeeting):
        wasRemoved = False
        #Unable to remove aMeeting, as it must always have a meetings
        if not self == aMeeting.getMeetings() :
            self._meetings.remove(aMeeting)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addMeetingAt(self, aMeeting, index):
        wasAdded = False
        if self.addMeeting(aMeeting) :
            if index < 0 :
                index = 0
            if index > self.numberOfMeetings() :
                index = self.numberOfMeetings() - 1
            self._meetings.remove(aMeeting)
            self._meetings.insert(index, aMeeting)
            wasAdded = True
        return wasAdded

    def addOrMoveMeetingAt(self, aMeeting, index):
        wasAdded = False
        if (aMeeting) in self._meetings :
            if index < 0 :
                index = 0
            if index > self.numberOfMeetings() :
                index = self.numberOfMeetings() - 1
            self._meetings.remove(aMeeting)
            self._meetings.insert(index, aMeeting)
            wasAdded = True
        else :
            wasAdded = self.addMeetingAt(aMeeting, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfMeetingLocations():
        return 0

    # Code from template association_AddManyToOne
    def addMeetingLocation1(self, aName, aAddress, aCity, aCountryCode):
        from .MeetingLocation import MeetingLocation
        return MeetingLocation(aName, aAddress, aCity, aCountryCode, self)

    def addMeetingLocation2(self, aMeetingLocation):
        wasAdded = False
        if (aMeetingLocation) in self._meetingLocations :
            return False
        existingMeetings = aMeetingLocation.getMeetings()
        isNewMeetings = not (existingMeetings is None) and not self == existingMeetings
        if isNewMeetings :
            aMeetingLocation.setMeetings(self)
        else :
            self._meetingLocations.append(aMeetingLocation)
        wasAdded = True
        return wasAdded

    def removeMeetingLocation(self, aMeetingLocation):
        wasRemoved = False
        #Unable to remove aMeetingLocation, as it must always have a meetings
        if not self == aMeetingLocation.getMeetings() :
            self._meetingLocations.remove(aMeetingLocation)
            wasRemoved = True
        return wasRemoved

    # Code from template association_AddIndexControlFunctions
    def addMeetingLocationAt(self, aMeetingLocation, index):
        wasAdded = False
        if self.addMeetingLocation(aMeetingLocation) :
            if index < 0 :
                index = 0
            if index > self.numberOfMeetingLocations() :
                index = self.numberOfMeetingLocations() - 1
            self._meetingLocations.remove(aMeetingLocation)
            self._meetingLocations.insert(index, aMeetingLocation)
            wasAdded = True
        return wasAdded

    def addOrMoveMeetingLocationAt(self, aMeetingLocation, index):
        wasAdded = False
        if (aMeetingLocation) in self._meetingLocations :
            if index < 0 :
                index = 0
            if index > self.numberOfMeetingLocations() :
                index = self.numberOfMeetingLocations() - 1
            self._meetingLocations.remove(aMeetingLocation)
            self._meetingLocations.insert(index, aMeetingLocation)
            wasAdded = True
        else :
            wasAdded = self.addMeetingLocationAt(aMeetingLocation, index)
        return wasAdded

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfMeetingAttendees():
        return 0

    # Code from template association_AddManyToOne
    def addMeetingAttendee1(self, aGuestNumber, aDecisionDate, aRole, aAttendee, aMeeting):
        from .MeetingAttendee import MeetingAttendee
        return MeetingAttendee(aGuestNumber, aDecisionDate, aRole, aAttendee, aMeeting, self)

    def addMeetingAttendee2(self, aMeetingAttendee):
        wasAdded = False
        if (aMeetingAttendee) in self._meetingAttendees :
            return False
        existingMeetings = aMeetingAttendee.getMeetings()
        isNewMeetings = not (existingMeetings is None) and not self == existingMeetings
        if isNewMeetings :
            aMeetingAttendee.setMeetings(self)
        else :
            self._meetingAttendees.append(aMeetingAttendee)
        wasAdded = True
        return wasAdded

    def removeMeetingAttendee(self, aMeetingAttendee):
        wasRemoved = False
        #Unable to remove aMeetingAttendee, as it must always have a meetings
        if not self == aMeetingAttendee.getMeetings() :
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
    def addMeetingNotAttendee1(self, aDecisionDate, aMember, aMeeting):
        from .MeetingNotAttendee import MeetingNotAttendee
        return MeetingNotAttendee(aDecisionDate, aMember, aMeeting, self)

    def addMeetingNotAttendee2(self, aMeetingNotAttendee):
        wasAdded = False
        if (aMeetingNotAttendee) in self._meetingNotAttendees :
            return False
        existingMeetings = aMeetingNotAttendee.getMeetings()
        isNewMeetings = not (existingMeetings is None) and not self == existingMeetings
        if isNewMeetings :
            aMeetingNotAttendee.setMeetings(self)
        else :
            self._meetingNotAttendees.append(aMeetingNotAttendee)
        wasAdded = True
        return wasAdded

    def removeMeetingNotAttendee(self, aMeetingNotAttendee):
        wasRemoved = False
        #Unable to remove aMeetingNotAttendee, as it must always have a meetings
        if not self == aMeetingNotAttendee.getMeetings() :
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
    def addMeetingWaitlistMember1(self, aDecisionDate, aMember, aMeeting):
        from .MeetingWaitlistMember import MeetingWaitlistMember
        return MeetingWaitlistMember(aDecisionDate, aMember, aMeeting, self)

    def addMeetingWaitlistMember2(self, aMeetingWaitlistMember):
        wasAdded = False
        if (aMeetingWaitlistMember) in self._meetingWaitlistMembers :
            return False
        existingMeetings = aMeetingWaitlistMember.getMeetings()
        isNewMeetings = not (existingMeetings is None) and not self == existingMeetings
        if isNewMeetings :
            aMeetingWaitlistMember.setMeetings(self)
        else :
            self._meetingWaitlistMembers.append(aMeetingWaitlistMember)
        wasAdded = True
        return wasAdded

    def removeMeetingWaitlistMember(self, aMeetingWaitlistMember):
        wasRemoved = False
        #Unable to remove aMeetingWaitlistMember, as it must always have a meetings
        if not self == aMeetingWaitlistMember.getMeetings() :
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

    def delete(self):

        while len(self._members) > 0 :
            aMember = self._members[len(self._members) - 1]
            aMember.delete()
            self._members.remove(aMember)

        while len(self._meetingGroupProposals) > 0 :
            aMeetingGroupProposal = self._meetingGroupProposals[len(self._meetingGroupProposals) - 1]
            aMeetingGroupProposal.delete()
            self._meetingGroupProposals.remove(aMeetingGroupProposal)

        while len(self._meetingGroups) > 0 :
            aMeetingGroup = self._meetingGroups[len(self._meetingGroups) - 1]
            aMeetingGroup.delete()
            self._meetingGroups.remove(aMeetingGroup)

        while len(self._meetings) > 0 :
            aMeeting = self._meetings[len(self._meetings) - 1]
            aMeeting.delete()
            self._meetings.remove(aMeeting)

        while len(self._meetingLocations) > 0 :
            aMeetingLocation = self._meetingLocations[len(self._meetingLocations) - 1]
            aMeetingLocation.delete()
            self._meetingLocations.remove(aMeetingLocation)

        while len(self._meetingAttendees) > 0 :
            aMeetingAttendee = self._meetingAttendees[len(self._meetingAttendees) - 1]
            aMeetingAttendee.delete()
            self._meetingAttendees.remove(aMeetingAttendee)

        while len(self._meetingNotAttendees) > 0 :
            aMeetingNotAttendee = self._meetingNotAttendees[len(self._meetingNotAttendees) - 1]
            aMeetingNotAttendee.delete()
            self._meetingNotAttendees.remove(aMeetingNotAttendee)

        while len(self._meetingWaitlistMembers) > 0 :
            aMeetingWaitlistMember = self._meetingWaitlistMembers[len(self._meetingWaitlistMembers) - 1]
            aMeetingWaitlistMember.delete()
            self._meetingWaitlistMembers.remove(aMeetingWaitlistMember)

    def addMember(self, *argv):
        from .Member import Member
        from .UserAccess import UserAccess
        if len(argv) == 7 and isinstance(argv[0], int) and isinstance(argv[1], str) and isinstance(argv[2], str) and isinstance(argv[3], str) and isinstance(argv[4], str) and isinstance(argv[5], str) and isinstance(argv[6], UserAccess) :
            return self.addMember1(argv[0], argv[1], argv[2], argv[3], argv[4], argv[5], argv[6])
        if len(argv) == 1 and isinstance(argv[0], Member) :
            return self.addMember2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addMeetingGroupProposal(self, *argv):
        from .MeetingGroupProposal import MeetingGroupProposal
        from .Member import Member
        from .MeetingGroupLocation import MeetingGroupLocation
        if len(argv) == 4 and isinstance(argv[0], str) and isinstance(argv[1], str) and isinstance(argv[2], MeetingGroupLocation) and isinstance(argv[3], Member) :
            return self.addMeetingGroupProposal1(argv[0], argv[1], argv[2], argv[3])
        if len(argv) == 1 and isinstance(argv[0], MeetingGroupProposal) :
            return self.addMeetingGroupProposal2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addMeetingGroup(self, *argv):
        from .MeetingGroup import MeetingGroup
        from .Member import Member
        from .MeetingGroupLocation import MeetingGroupLocation
        if len(argv) == 5 and isinstance(argv[0], int) and isinstance(argv[1], str) and isinstance(argv[2], str) and isinstance(argv[3], MeetingGroupLocation) and isinstance(argv[4], Member) :
            return self.addMeetingGroup1(argv[0], argv[1], argv[2], argv[3], argv[4])
        if len(argv) == 1 and isinstance(argv[0], MeetingGroup) :
            return self.addMeetingGroup2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addMeeting(self, *argv):
        from .MeetingLocation import MeetingLocation
        from .Meeting import Meeting
        from .Member import Member
        from .MeetingTerm import MeetingTerm
        from .MeetingLimit import MeetingLimit
        from .Term import Term
        if len(argv) == 7 and isinstance(argv[0], str) and isinstance(argv[1], str) and isinstance(argv[2], MeetingTerm) and isinstance(argv[3], MeetingLocation) and isinstance(argv[4], MeetingLimit) and isinstance(argv[5], Term) and isinstance(argv[6], Member) :
            return self.addMeeting1(argv[0], argv[1], argv[2], argv[3], argv[4], argv[5], argv[6])
        if len(argv) == 1 and isinstance(argv[0], Meeting) :
            return self.addMeeting2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addMeetingLocation(self, *argv):
        from .MeetingLocation import MeetingLocation
        if len(argv) == 4 and isinstance(argv[0], str) and isinstance(argv[1], str) and isinstance(argv[2], str) and isinstance(argv[3], str) :
            return self.addMeetingLocation1(argv[0], argv[1], argv[2], argv[3])
        if len(argv) == 1 and isinstance(argv[0], MeetingLocation) :
            return self.addMeetingLocation2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addMeetingAttendee(self, *argv):
        from .MeetingAttendee import MeetingAttendee
        from .Meeting import Meeting
        from .Member import Member
        if len(argv) == 5 and isinstance(argv[0], int) and isinstance(argv[1], date) and isinstance(argv[2], MeetingAttendee.MeetingAttendeeRole) and isinstance(argv[3], Member) and isinstance(argv[4], Meeting) :
            return self.addMeetingAttendee1(argv[0], argv[1], argv[2], argv[3], argv[4])
        if len(argv) == 1 and isinstance(argv[0], MeetingAttendee) :
            return self.addMeetingAttendee2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addMeetingNotAttendee(self, *argv):
        from .MeetingNotAttendee import MeetingNotAttendee
        from .Meeting import Meeting
        from .Member import Member
        if len(argv) == 3 and isinstance(argv[0], date) and isinstance(argv[1], Member) and isinstance(argv[2], Meeting) :
            return self.addMeetingNotAttendee1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], MeetingNotAttendee) :
            return self.addMeetingNotAttendee2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addMeetingWaitlistMember(self, *argv):
        from .MeetingWaitlistMember import MeetingWaitlistMember
        from .Meeting import Meeting
        from .Member import Member
        if len(argv) == 3 and isinstance(argv[0], date) and isinstance(argv[1], Member) and isinstance(argv[2], Meeting) :
            return self.addMeetingWaitlistMember1(argv[0], argv[1], argv[2])
        if len(argv) == 1 and isinstance(argv[0], MeetingWaitlistMember) :
            return self.addMeetingWaitlistMember2(argv[0])
        raise TypeError("No method matches provided parameters")
