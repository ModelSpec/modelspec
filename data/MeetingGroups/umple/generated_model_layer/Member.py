# %% NEW FILE Member BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 58 "model.ump"
# line 280 "model.ump"
from .User import User

class Member(User):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #Member Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aId, aLogin, aEmail, aFirstName, aLastName, aName, aUserAccess, aMeetings):
        self._meetingGroups = None
        self._meetingGroupProposals = None
        self._meetings = None
        super().__init__(aId, aLogin, aEmail, aFirstName, aLastName, aName, aUserAccess)
        didAddMeetings = self.setMeetings(aMeetings)
        if not didAddMeetings :
            raise RuntimeError ("Unable to create member due to meetings. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._meetingGroupProposals = []
        self._meetingGroups = []

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetOne
    def getMeetings(self):
        return self._meetings

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

    # Code from template association_SetOneToMany
    def setMeetings(self, aMeetings):
        wasSet = False
        if aMeetings is None :
            return wasSet
        existingMeetings = self._meetings
        self._meetings = aMeetings
        if not (existingMeetings is None) and not existingMeetings == aMeetings :
            existingMeetings.removeMember(self)
        self._meetings.addMember(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfMeetingGroupProposals():
        return 0

    # Code from template association_AddManyToOne
    def addMeetingGroupProposal1(self, aName, aDescription, aMeetingGroupLocation, aMeetings):
        from .MeetingGroupProposal import MeetingGroupProposal
        return MeetingGroupProposal(aName, aDescription, aMeetingGroupLocation, self, aMeetings)

    def addMeetingGroupProposal2(self, aMeetingGroupProposal):
        wasAdded = False
        if (aMeetingGroupProposal) in self._meetingGroupProposals :
            return False
        existingMember = aMeetingGroupProposal.getMember()
        isNewMember = not (existingMember is None) and not self == existingMember
        if isNewMember :
            aMeetingGroupProposal.setMember(self)
        else :
            self._meetingGroupProposals.append(aMeetingGroupProposal)
        wasAdded = True
        return wasAdded

    def removeMeetingGroupProposal(self, aMeetingGroupProposal):
        wasRemoved = False
        #Unable to remove aMeetingGroupProposal, as it must always have a member
        if not self == aMeetingGroupProposal.getMember() :
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
    def addMeetingGroup1(self, aId, aName, aDescription, aMeetingGroupLocation, aMeetings):
        from .MeetingGroup import MeetingGroup
        return MeetingGroup(aId, aName, aDescription, aMeetingGroupLocation, self, aMeetings)

    def addMeetingGroup2(self, aMeetingGroup):
        wasAdded = False
        if (aMeetingGroup) in self._meetingGroups :
            return False
        existingCreator = aMeetingGroup.getCreator()
        isNewCreator = not (existingCreator is None) and not self == existingCreator
        if isNewCreator :
            aMeetingGroup.setCreator(self)
        else :
            self._meetingGroups.append(aMeetingGroup)
        wasAdded = True
        return wasAdded

    def removeMeetingGroup(self, aMeetingGroup):
        wasRemoved = False
        #Unable to remove aMeetingGroup, as it must always have a creator
        if not self == aMeetingGroup.getCreator() :
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

    def delete(self):
        placeholderMeetings = self._meetings
        self._meetings = None
        if not (placeholderMeetings is None) :
            placeholderMeetings.removeMember(self)
        i = len(self._meetingGroupProposals)
        while i > 0 :
            aMeetingGroupProposal = self._meetingGroupProposals[i - 1]
            aMeetingGroupProposal.delete()
            i -= 1

        i = len(self._meetingGroups)
        while i > 0 :
            aMeetingGroup = self._meetingGroups[i - 1]
            aMeetingGroup.delete()
            i -= 1

        super().delete()

    def addMeetingGroupProposal(self, *argv):
        from .MeetingGroupProposal import MeetingGroupProposal
        from .Meetings import Meetings
        from .MeetingGroupLocation import MeetingGroupLocation
        if len(argv) == 4 and isinstance(argv[0], str) and isinstance(argv[1], str) and isinstance(argv[2], MeetingGroupLocation) and isinstance(argv[3], Meetings) :
            return self.addMeetingGroupProposal1(argv[0], argv[1], argv[2], argv[3])
        if len(argv) == 1 and isinstance(argv[0], MeetingGroupProposal) :
            return self.addMeetingGroupProposal2(argv[0])
        raise TypeError("No method matches provided parameters")

    def addMeetingGroup(self, *argv):
        from .MeetingGroup import MeetingGroup
        from .Meetings import Meetings
        from .MeetingGroupLocation import MeetingGroupLocation
        if len(argv) == 5 and isinstance(argv[0], int) and isinstance(argv[1], str) and isinstance(argv[2], str) and isinstance(argv[3], MeetingGroupLocation) and isinstance(argv[4], Meetings) :
            return self.addMeetingGroup1(argv[0], argv[1], argv[2], argv[3], argv[4])
        if len(argv) == 1 and isinstance(argv[0], MeetingGroup) :
            return self.addMeetingGroup2(argv[0])
        raise TypeError("No method matches provided parameters")
