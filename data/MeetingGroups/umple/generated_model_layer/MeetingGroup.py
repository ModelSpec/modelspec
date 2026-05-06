# %% NEW FILE MeetingGroup BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 87 "model.ump"
# line 300 "model.ump"
import os

class MeetingGroup():
    meetinggroupsById = dict()
    #------------------------
    # STATIC VARIABLES
    #------------------------
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #MeetingGroup Attributes
    #MeetingGroup Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aId, aName, aDescription, aMeetingGroupLocation, aCreator, aMeetings):
        self._meetings = None
        self._members = None
        self._creator = None
        self._meetingGroupLocation = None
        self._paymentDateTo = None
        self._createDate = None
        self._description = None
        self._name = None
        self._id = None
        self._name = aName
        self._description = aDescription
        self._createDate = None
        self._paymentDateTo = None
        if not self.setId(aId) :
            raise RuntimeError ("Cannot create due to duplicate id. See https://manual.umple.org?RE003ViolationofUniqueness.html")
        if not self.setMeetingGroupLocation(aMeetingGroupLocation) :
            raise RuntimeError ("Unable to create MeetingGroup due to aMeetingGroupLocation. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddCreator = self.setCreator(aCreator)
        if not didAddCreator :
            raise RuntimeError ("Unable to create meetingGroup due to creator. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._members = []
        didAddMeetings = self.setMeetings(aMeetings)
        if not didAddMeetings :
            raise RuntimeError ("Unable to create meetingGroup due to meetings. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setId(self, aId):
        wasSet = False
        anOldId = self.getId()
        if not (anOldId is None) and anOldId == aId :
            return True
        if MeetingGroup.hasWithId(aId) :
            return wasSet
        self._id = aId
        wasSet = True
        if not (anOldId is None) :
            MeetingGroup.meetinggroupsById.pop(anOldId, None)
        MeetingGroup.meetinggroupsById[aId] = self
        return wasSet

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

    def setCreateDate(self, aCreateDate):
        wasSet = False
        self._createDate = aCreateDate
        wasSet = True
        return wasSet

    def setPaymentDateTo(self, aPaymentDateTo):
        wasSet = False
        self._paymentDateTo = aPaymentDateTo
        wasSet = True
        return wasSet

    def getId(self):
        return self._id

    # Code from template attribute_GetUnique
    @staticmethod
    def getWithId(aId):
        return MeetingGroup.meetinggroupsById.get(aId)

    # Code from template attribute_HasUnique
    @staticmethod
    def hasWithId(aId):
        return not (MeetingGroup.getWithId(aId) is None)

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

    def getCreateDate(self):
        return self._createDate

    def getPaymentDateTo(self):
        return self._paymentDateTo

    # Code from template association_GetOne
    def getMeetingGroupLocation(self):
        return self._meetingGroupLocation

    # Code from template association_GetOne
    def getCreator(self):
        return self._creator

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

    # Code from template association_GetOne
    def getMeetings(self):
        return self._meetings

    # Code from template association_SetUnidirectionalOne
    def setMeetingGroupLocation(self, aNewMeetingGroupLocation):
        wasSet = False
        if not (aNewMeetingGroupLocation is None) :
            self._meetingGroupLocation = aNewMeetingGroupLocation
            wasSet = True
        return wasSet

    # Code from template association_SetOneToMany
    def setCreator(self, aCreator):
        wasSet = False
        if aCreator is None :
            return wasSet
        existingCreator = self._creator
        self._creator = aCreator
        if not (existingCreator is None) and not existingCreator == aCreator :
            existingCreator.removeMeetingGroup(self)
        self._creator.addMeetingGroup(self)
        wasSet = True
        return wasSet

    # Code from template association_MinimumNumberOfMethod
    @staticmethod
    def minimumNumberOfMembers():
        return 0

    # Code from template association_AddManyToOne
    def addMember1(self, aRole, aMember):
        from .MeetingGroupMember import MeetingGroupMember
        return MeetingGroupMember(aRole, aMember, self)

    def addMember2(self, aMember):
        wasAdded = False
        if (aMember) in self._members :
            return False
        existingMeetingGroup = aMember.getMeetingGroup()
        isNewMeetingGroup = not (existingMeetingGroup is None) and not self == existingMeetingGroup
        if isNewMeetingGroup :
            aMember.setMeetingGroup(self)
        else :
            self._members.append(aMember)
        wasAdded = True
        return wasAdded

    def removeMember(self, aMember):
        wasRemoved = False
        #Unable to remove aMember, as it must always have a meetingGroup
        if not self == aMember.getMeetingGroup() :
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

    # Code from template association_SetOneToMany
    def setMeetings(self, aMeetings):
        wasSet = False
        if aMeetings is None :
            return wasSet
        existingMeetings = self._meetings
        self._meetings = aMeetings
        if not (existingMeetings is None) and not existingMeetings == aMeetings :
            existingMeetings.removeMeetingGroup(self)
        self._meetings.addMeetingGroup(self)
        wasSet = True
        return wasSet

    def delete(self):
        MeetingGroup.meetinggroupsById.pop(self.getId(), None)
        self._meetingGroupLocation = None
        placeholderCreator = self._creator
        self._creator = None
        if not (placeholderCreator is None) :
            placeholderCreator.removeMeetingGroup(self)
        i = len(self._members)
        while i > 0 :
            aMember = self._members[i - 1]
            aMember.delete()
            i -= 1

        placeholderMeetings = self._meetings
        self._meetings = None
        if not (placeholderMeetings is None) :
            placeholderMeetings.removeMeetingGroup(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "id" + ":" + str(self.getId()) + "," + "name" + ":" + str(self.getName()) + "," + "description" + ":" + str(self.getDescription()) + "]" + str(os.linesep) + "  " + "createDate" + "=" + str((((self.getCreateDate().__str__().replaceAll("  ", "    ")) if not self.getCreateDate() == self else "this") if not (self.getCreateDate() is None) else "null")) + str(os.linesep) + "  " + "paymentDateTo" + "=" + str((((self.getPaymentDateTo().__str__().replaceAll("  ", "    ")) if not self.getPaymentDateTo() == self else "this") if not (self.getPaymentDateTo() is None) else "null")) + str(os.linesep) + "  " + "meetingGroupLocation = " + str(((format(id(self.getMeetingGroupLocation()), "x")) if not (self.getMeetingGroupLocation() is None) else "null")) + str(os.linesep) + "  " + "creator = " + str(((format(id(self.getCreator()), "x")) if not (self.getCreator() is None) else "null")) + str(os.linesep) + "  " + "meetings = " + ((format(id(self.getMeetings()), "x")) if not (self.getMeetings() is None) else "null")

    def addMember(self, *argv):
        from .MeetingGroupMember import MeetingGroupMember
        from .Member import Member
        if len(argv) == 2 and isinstance(argv[0], MeetingGroupMember.MeetingGroupMemberRole) and isinstance(argv[1], Member) :
            return self.addMember1(argv[0], argv[1])
        if len(argv) == 1 and isinstance(argv[0], MeetingGroupMember) :
            return self.addMember2(argv[0])
        raise TypeError("No method matches provided parameters")
