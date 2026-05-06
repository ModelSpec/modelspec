# %% NEW FILE MeetingGroupMember BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 98 "model.ump"
# line 305 "model.ump"
import os
from enum import Enum, auto

class MeetingGroupMember():
    #------------------------
    # ENUMERATIONS
    #------------------------
    class MeetingGroupMemberRole(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name
        def __str__(self):
            return str(self.value)
        Organizer = auto()
        Member = auto()

    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #MeetingGroupMember Attributes
    #MeetingGroupMember Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aRole, aMember, aMeetingGroup):
        self._meetingGroup = None
        self._member = None
        self._role = None
        self._isActive = None
        self._joinedDate = None
        self._joinedDate = None
        self._role = aRole
        if not self.setMember(aMember) :
            raise RuntimeError ("Unable to create MeetingGroupMember due to aMember. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        didAddMeetingGroup = self.setMeetingGroup(aMeetingGroup)
        if not didAddMeetingGroup :
            raise RuntimeError ("Unable to create member due to meetingGroup. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setJoinedDate(self, aJoinedDate):
        wasSet = False
        self._joinedDate = aJoinedDate
        wasSet = True
        return wasSet

    def setIsActive(self, aIsActive):
        wasSet = False
        self._isActive = aIsActive
        wasSet = True
        return wasSet

    def setRole(self, aRole):
        wasSet = False
        self._role = aRole
        wasSet = True
        return wasSet

    def getJoinedDate(self):
        return self._joinedDate

    def getIsActive(self):
        return self._isActive

    def getRole(self):
        return self._role

    # Code from template association_GetOne
    def getMember(self):
        return self._member

    # Code from template association_GetOne
    def getMeetingGroup(self):
        return self._meetingGroup

    # Code from template association_SetUnidirectionalOne
    def setMember(self, aNewMember):
        wasSet = False
        if not (aNewMember is None) :
            self._member = aNewMember
            wasSet = True
        return wasSet

    # Code from template association_SetOneToMany
    def setMeetingGroup(self, aMeetingGroup):
        wasSet = False
        if aMeetingGroup is None :
            return wasSet
        existingMeetingGroup = self._meetingGroup
        self._meetingGroup = aMeetingGroup
        if not (existingMeetingGroup is None) and not existingMeetingGroup == aMeetingGroup :
            existingMeetingGroup.removeMember(self)
        self._meetingGroup.addMember(self)
        wasSet = True
        return wasSet

    def delete(self):
        self._member = None
        placeholderMeetingGroup = self._meetingGroup
        self._meetingGroup = None
        if not (placeholderMeetingGroup is None) :
            placeholderMeetingGroup.removeMember(self)

    def __str__(self):
        return str(super().__str__()) + "[" + "]" + str(os.linesep) + "  " + "joinedDate" + "=" + str((((self.getJoinedDate().__str__().replaceAll("  ", "    ")) if not self.getJoinedDate() == self else "this") if not (self.getJoinedDate() is None) else "null")) + str(os.linesep) + "  " + "isActive" + "=" + str((((self.getIsActive().__str__().replaceAll("  ", "    ")) if not self.getIsActive() == self else "this") if not (self.getIsActive() is None) else "null")) + str(os.linesep) + "  " + "role" + "=" + str((((self.getRole().__str__().replaceAll("  ", "    ")) if not self.getRole() == self else "this") if not (self.getRole() is None) else "null")) + str(os.linesep) + "  " + "member = " + str(((format(id(self.getMember()), "x")) if not (self.getMember() is None) else "null")) + str(os.linesep) + "  " + "meetingGroup = " + ((format(id(self.getMeetingGroup()), "x")) if not (self.getMeetingGroup() is None) else "null")
